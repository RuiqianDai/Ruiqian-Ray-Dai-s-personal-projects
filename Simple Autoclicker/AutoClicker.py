from tkinter import *
from tkinter import messagebox
from time import *
import threading
import pynput.mouse as mouse
import pynput.keyboard as keyboard

### core of program

# program state indicators
autoclicker_running = False
rebind_left_click = False
rebind_right_click = False
rebind_left_press = False
rebind_right_press = False
rebind_exit = False

# delay between clicks for both mouse buttons
left_mouse_delay = 0.001
right_mouse_delay = 0.001

# declare both mouse buttons
button1 = mouse.Button.left
button2 = mouse.Button.right

# default keybinds of autoclicker
# start or stop spamming left click (default c)
left_click = keyboard.KeyCode(char='c') 
# start or stop spamming right click (default v)
right_click = keyboard.KeyCode(char='v')
# hold down or release left click (default b)
left_press = keyboard.KeyCode(char='b')
# hold down or release right click (default n)
right_press = keyboard.KeyCode(char='n')
# terminate autoclicker (default p)
exit_key = keyboard.KeyCode(char='p')

# object for mouse clicks
class ClickMouse(threading.Thread):
    # init
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        # delay is the amount of delay between clicks
        self.delay = delay
        # each ClickMouse would be either left or right button
        self.button = button
        # boolean for running the click loop
        self.running = False
        # boolean value for holding button
        self.hold = False
        # boolean value for checking if button is held
        self.pressed = False
        # boolean for running the autoclicker loop
        self.autoclick_running = True
    
    # start click loop when called
    def start_clicking(self):
        self.running = True
    
    # stop click loop when called
    def stop_clicking(self):
        self.running = False
    
    # signal to start holding down button
    def start_holding(self):
        self.hold = True
    
    # signal to stop holding down button
    def stop_holding(self):
        self.hold = False
    
    # actually press the button
    def do_press(self):
        mouse.press(self.button)
        self.pressed = True
    
    # actually release the button
    def do_release(self):
        mouse.release(self.button)
        self.pressed = False

    # stop autoclicker loop when called
    def exit(self):
        self.stop_clicking()
        self.stop_holding()
        self.do_release()
        self.autoclick_running = False
    
    # click loop
    def run(self):
        # when autoclicker runs,
        while self.autoclick_running:
            # hold down button when key was not pressed and needs to be
            if(self.hold and not self.pressed):
                self.do_press()
            # release button when key is pressed but should not be
            elif(not self.hold and self.pressed):
                self.do_release()
            # keep clicking if click loop is on
            while self.running:
                mouse.click(self.button) 
                sleep(self.delay)
            # note to self: delay below is load-bearing and allows computer to react to key
            # do not remove or bad things happen
            sleep(0.1)

#declare mouse controller and threads
mouse = mouse.Controller()
click_thread_left = ClickMouse(left_mouse_delay, button1)
click_thread_right = ClickMouse(right_mouse_delay, button2)

# input detection
def on_press(key):
    global autoclicker_running
    global rebind_left_click
    global rebind_right_click
    global rebind_left_press
    global rebind_right_press
    global left_click
    global right_click
    global left_press
    global right_press
    global exit_key

    # input detection for running autoclicker
    if autoclicker_running:

        # if the left click loop key is pressed, turn it on or off depending on its state
        # also release the key from pressing first if applicable
        if key == left_click:
            if click_thread_left.running:
                click_thread_left.stop_clicking()
            else:
                click_thread_left.stop_holding()
                click_thread_left.start_clicking()
        
        # same for right click loop
        elif key == right_click:
            if click_thread_right.running:
                click_thread_right.stop_clicking()
            else:
                click_thread_right.stop_holding()
                click_thread_right.start_clicking()
        
        # if left mouse hold key is pressed, press or release it, and also disable clicking if applicable
        elif key == left_press:
            # disable clicking first
            if click_thread_left.running:
                click_thread_left.stop_clicking()
            # then start or stop holding
            if click_thread_left.hold:
                click_thread_left.stop_holding()
            else:
                click_thread_left.start_holding()
        
        # same for right press
        elif key == right_press:
            # disable clicking first
            if click_thread_right.running:
                click_thread_right.stop_clicking()
            # then start or stop holding
            if click_thread_right.hold:
                click_thread_right.stop_holding()
            else:
                click_thread_right.start_holding()
        
        # when exit key is pressed, terminate autoclicker
        elif key == exit_key:
            # reactivate settings
            activate_functions()
            # turn off everything else
            autoclicker_running = False
            click_thread_left.exit()
            click_thread_right.exit()
            listener.stop()
    
    # input detection for rebinding left mouse click key
    elif rebind_left_click:
        # rebind key and then stop listener
        left_click = key
        # also update text
        left_click_key_label.config(text=fetch_key_name(left_click))
        # reactivate settings
        activate_functions()
        # exit
        rebind_left_click = False
        listener.stop()
    
    # input detection for rebinding right mouse click key
    elif rebind_right_click:
        # rebind key and then stop listener
        right_click = key
        # also update text
        right_click_key_label.config(text=fetch_key_name(right_click))
        # reactivate settings
        activate_functions()
        # exit
        rebind_right_click = False
        listener.stop()
    
    # input detection for rebinding left mouse press key
    elif rebind_left_press:
        # rebind key then stop listener
        left_press = key
        # also update text
        left_press_key_label.config(text=fetch_key_name(left_press))
        # reactivate settings
        activate_functions()
        # exit
        rebind_left_press = False
        listener.stop()
    
    # input detection for rebinding right mouse press key
    elif rebind_right_press:
        # rebind key then stop listener
        right_press = key
        # also update text
        right_press_key_label.config(text=fetch_key_name(right_press))
        # reactivate settings
        activate_functions()
        # exit
        rebind_right_press = False
        listener.stop()
    
    # input detection for rebinding exit key
    elif rebind_exit:
        # rebind key then stop listener
        exit_key = key
        # also update text
        exit_key_label.config(text=fetch_key_name(exit_key))
        # reactivate settings
        activate_functions()
        # exit
        rebind_right_press = False
        listener.stop()

# declare keyboard listener
listener = keyboard.Listener(on_press=on_press)

# function to start autoclicker
def start_autoclick():
    # initialize
    global autoclicker_running
    global click_thread_left
    global click_thread_right
    global listener
    global left_mouse_delay
    global right_mouse_delay
    
    valid_input = False
    
    try:
        # try fetching delay values from input box
        left_mouse_delay = float(left_click_delay_input.get())
        right_mouse_delay = float(right_click_delay_input.get())
        valid_input = True
    # report error and refuse to start program if input is invalid
    except:
        valid_input = False
        messagebox.showerror("Invalid input", "Please input numeric delay values")
        
    # only start if input is valid
    if valid_input:
        # suspend settings
        suspend_functions()
        # turn on program
        autoclicker_running = True
        # set click threads
        click_thread_left = ClickMouse(left_mouse_delay, button1)
        click_thread_right = ClickMouse(right_mouse_delay, button2)
        # start both mouse button threads and keyboard listener thread and let them sort themselves out
        click_thread_left.start()
        click_thread_right.start()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

# function to rebind key that starts/stops left click
def change_left_click():
    global rebind_left_click
    global listener
    # suspend settings
    suspend_functions()
    # start
    rebind_left_click = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# function to rebind key that starts/stops left click
def change_right_click():
    global rebind_right_click
    global listener
    # suspend settings
    suspend_functions()
    # start
    rebind_right_click = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# function to rebind key that starts/stops left press
def change_left_press():
    global rebind_left_press
    global listener
    # suspend settings
    suspend_functions()
    # start
    rebind_left_press = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# function to rebind key that starts/stops left press
def change_right_press():
    global rebind_right_press
    global listener
    # suspend settings
    suspend_functions()
    # start
    rebind_right_press = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# function to rebind exit key
def change_exit_key():
    global rebind_exit
    global listener
    # suspend settings
    suspend_functions()
    # start
    rebind_exit = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

# suspend all buttons/entries when changing keybind or running clicker
def suspend_functions():
    start_button["state"]=DISABLED
    left_click_keybind_button["state"]=DISABLED
    right_click_keybind_button["state"]=DISABLED
    left_press_keybind_button["state"]=DISABLED
    right_press_keybind_button["state"]=DISABLED
    exit_keybind_button["state"]=DISABLED
    left_click_delay_input["state"]=DISABLED
    right_click_delay_input["state"]=DISABLED

# reactivate all buttons/entries after changing keybind or running clicker
def activate_functions():
    start_button["state"]=NORMAL
    left_click_keybind_button["state"]=NORMAL
    right_click_keybind_button["state"]=NORMAL
    left_press_keybind_button["state"]=NORMAL
    right_press_keybind_button["state"]=NORMAL
    exit_keybind_button["state"]=NORMAL
    left_click_delay_input["state"]=NORMAL
    right_click_delay_input["state"]=NORMAL

# function for fetching the name of the key to show current keybind
def fetch_key_name(key):
    # return the character if key is alphanumeric
    try:
        return key.char
    except:
        return key_names.get(key, "???")    

def help_popup():
    messagebox.showinfo("instructions",
    """- Click "start autoclicker" to run program.

- When program is running, press designated keys to start each function, and press again to stop.

- Press the exit key to stop the program and return to settings.

- "left click" and "right click" clicks the left and right mouse button with the designated delay between each click.

- "left press" and "right press" holds down the left and right mouse button.

- multiple functions can be used at the same time.

- To change key binds, click "change" and then the new key.
""")

# list of names of special keys in string form
key_names = {
    keyboard.Key.alt: "alt",
    keyboard.Key.alt_gr: "alt gr",
    keyboard.Key.alt_l: "left alt",
    keyboard.Key.alt_r: "right alt",
    keyboard.Key.backspace: "backspace",
    keyboard.Key.caps_lock: "caps lock",
    keyboard.Key.cmd: "cmd",
    keyboard.Key.cmd_l: "left cmd",
    keyboard.Key.cmd_r: "right cmd",
    keyboard.Key.ctrl: "ctrl",
    keyboard.Key.ctrl_l: "left ctrl",
    keyboard.Key.ctrl_r: "right ctrl",
    keyboard.Key.delete: "delete",
    keyboard.Key.down: "down arrow",
    keyboard.Key.end: "end",
    keyboard.Key.enter: "enter",
    keyboard.Key.esc: "esc",
    keyboard.Key.f1: "f1",
    keyboard.Key.f2: "f2",
    keyboard.Key.f3: "f3",
    keyboard.Key.f4: "f4",
    keyboard.Key.f5: "f5",
    keyboard.Key.f6: "f6",
    keyboard.Key.f7: "f7",
    keyboard.Key.f8: "f8",
    keyboard.Key.f9: "f9",
    keyboard.Key.f10: "f10",
    keyboard.Key.f11: "f11",
    keyboard.Key.f12: "f12",
    keyboard.Key.f13: "f13",
    keyboard.Key.f14: "f14",
    keyboard.Key.f15: "f15",
    keyboard.Key.f16: "f16",
    keyboard.Key.f17: "f17",
    keyboard.Key.f18: "f18",
    keyboard.Key.f19: "f19",
    keyboard.Key.f20: "f20",
    keyboard.Key.home: "home",
    keyboard.Key.insert: "insert",
    keyboard.Key.left: "left arrow",
    keyboard.Key.media_next: "next track",
    keyboard.Key.media_play_pause: "play/pause",
    keyboard.Key.media_previous: "prev track",
    keyboard.Key.media_volume_down: "volume down",
    keyboard.Key.media_volume_mute: "mute",
    keyboard.Key.media_volume_up: "volume up",
    keyboard.Key.menu: "menu",
    keyboard.Key.num_lock: "numlock",
    keyboard.Key.page_down: "page down",
    keyboard.Key.page_up: "page up",
    keyboard.Key.pause: "pause",
    keyboard.Key.print_screen: "printscreen",
    keyboard.Key.right: "right arrow",
    keyboard.Key.scroll_lock: "scroll lock",
    keyboard.Key.shift: "shift",
    keyboard.Key.shift_l: "left shift",
    keyboard.Key.shift_r: "right shift",
    keyboard.Key.space: "space",
    keyboard.Key.tab: "tab",
    keyboard.Key.up: "up arrow",
}

### GUI of program

# create window for program
screen = Tk()
screen.title("Simple Autoclicker")
screen.resizable(False, False)

filler_0 = Label(screen, text=" ", width=5, height=1)
filler_0.grid(row=0, column=0)

# start button
start_button = Button(screen, text="start autoclicker", command=start_autoclick)
start_button.grid(row=1, column=1)

# mouse left click key bind label and button
left_click_keybind_title = Label(screen, text="left click: ")
left_click_keybind_title.grid(row=2, column=1)

left_click_key_label = Label(screen, text=fetch_key_name(left_click), width=10)
left_click_key_label.grid(row=2, column=2)

left_click_keybind_button = Button(screen, text="change", command=change_left_click)
left_click_keybind_button.grid(row=2, column=3)

filler_1 = Label(screen, text=" ", width=5)
filler_1.grid(row=2, column=4)

# mouse left click delay input label and text box
left_click_delay_label = Label(screen, text="left click delay: ")
left_click_delay_label.grid(row=2, column=5)

left_click_delay_input = Entry(screen, width=20)
left_click_delay_input.insert(0, "0.001")
left_click_delay_input.grid(row=2, column=6)

# filler on right
fill_right = Label(screen, text=" ", width=5)
fill_right.grid(row=2, column=7)

# mouse right click key bind button
right_click_keybind_title = Label(screen, text="right click: ")
right_click_keybind_title.grid(row=3, column=1)

right_click_key_label = Label(screen, text=fetch_key_name(right_click), width=10)
right_click_key_label.grid(row=3, column=2)

right_click_keybind_button = Button(screen, text="change", command=change_right_click)
right_click_keybind_button.grid(row=3, column=3)

filler_2 = Label(screen, text=" ", width=5)
filler_2.grid(row=3, column=4)

# mouse left click delay input label and text box
right_click_delay_title = Label(screen, text="right click delay: ", width=20)
right_click_delay_title.grid(row=3, column=5)

right_click_delay_input = Entry(screen, width=20)
right_click_delay_input.insert(0, "0.001")
right_click_delay_input.grid(row=3, column=6)

# mouse left press key bind button
left_press_keybind_label = Label(screen, text="left press: ")
left_press_keybind_label.grid(row=4, column=1)

left_press_key_label = Label(screen, text=fetch_key_name(left_press), width=10)
left_press_key_label.grid(row=4, column=2)

left_press_keybind_button = Button(screen, text="change", command=change_left_press)
left_press_keybind_button.grid(row=4, column=3)

# mouse right press key bind button
right_press_keybind_title = Label(screen, text="right press: ")
right_press_keybind_title.grid(row=5, column=1)

right_press_key_label = Label(screen, text=fetch_key_name(right_press), width=10)
right_press_key_label.grid(row=5, column=2)

right_press_keybind_button = Button(screen, text="change", command=change_right_press)
right_press_keybind_button.grid(row=5, column=3)

# exit key bind button
exit_keybind_title = Label(screen, text="exit button: ")
exit_keybind_title.grid(row=6, column=1)

exit_key_label = Label(screen, text=fetch_key_name(exit_key), width=10)
exit_key_label.grid(row=6, column=2)

exit_keybind_button = Button(screen, text="change", command=change_exit_key)
exit_keybind_button.grid(row=6, column=3)

filler_3 = Label(screen, text=" ")
filler_3.grid(row=6, column=4)
filler_4 = Label(screen, text=" ")
filler_4.grid(row=6, column=5)

# help button
help_button = Button(screen, text="help",command=help_popup)
help_button.grid(row=5, column=6)

# first column fillers
fill_r1 = Label(screen, text=" ")
fill_r1.grid(row=1, column=0)
fill_r2 = Label(screen, text=" ")
fill_r2.grid(row=2, column=0)
fill_r3 = Label(screen, text=" ")
fill_r3.grid(row=3, column=0)
fill_r4 = Label(screen, text=" ")
fill_r4.grid(row=4, column=0)
fill_r5 = Label(screen, text=" ")
fill_r5.grid(row=5, column=0)
fill_r6 = Label(screen, text=" ")
fill_r6.grid(row=6, column=0)

# last row filler
fill_r7 = Label(screen, text=" ", height=1)
fill_r7.grid(row=7, column=0)

# start screen
screen.mainloop()