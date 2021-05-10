let FONTSIZE = 30;
// these two constants can be changed to alter the difficulty and how chaotic the game is
let BOUNCE_COEFFICIENT = -1.01;
let GRAVITATIONAL_CONSTANT = 5;

// game state variables
let gameNotStarted = true;
let gameRunning = false;
let gameOver = false;
let victory = false;

// ball variable
let bouncy;

// ball physics variables
let xCord = 0;
let yCord = 0;

let nextXCord;
let nextYCord;
let tempXCord;
let tempYCord;

let xVelocity = 0;
let yVelocity = 0;

// gravity variables
let gravityX;
let gravityY;

// borders
let leftBorder;
let rightBorder;
let topBorder;
let bottomBorder;

function preload(){
  // load the ball sprite and sound effect
  bouncy = loadImage("assets/bouncy_ball.png");
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  
  // define the borders of the ball's movement
  leftBorder = 0;
  rightBorder = windowWidth - bouncy.width;
  topBorder = 0;
  bottomBorder = windowHeight - bouncy.height;
  
  // place the ball at the center
  xCord = windowWidth/2 - bouncy.width/2;
  yCord = windowHeight/2 - bouncy.height/2;

  xVelocity = 0;
  yVelocity = 0;

  textAlign(CENTER, CENTER);
  textSize(FONTSIZE);
}


function draw() {
  // game starts when g is pressed
  if(keyIsPressed && key === "g"){
    startGame();
  }

  // game pauses when p is pressed
  if(keyIsPressed && key === "p"){
    pauseGame();
  }
  
  // main menu that displays before game starts
  if(gameNotStarted){
    mainMenu();
  }
  //run game
  if(gameRunning){
    runGame();
  }
  if(victory){
    victoryScreen();
  }
  if(gameOver){
    deathScreen();
  }

}


// main function
function runGame(){
  background(220);
  // game runs when ball doesn't breach the speed limit
  if(Math.abs(xVelocity) <= 200 && Math.abs(yVelocity) <= 200){
    // chaotic gravity
    gravityX = random(-1*GRAVITATIONAL_CONSTANT,GRAVITATIONAL_CONSTANT);
    gravityY = random(-1*GRAVITATIONAL_CONSTANT,GRAVITATIONAL_CONSTANT);
    // move and print ball onto screen
    moveBall();
    image(bouncy, xCord, yCord);
    // player dies when mouse touches ball
    if(mouseX >= xCord && mouseX <= xCord + bouncy.width && mouseY >= yCord && mouseY <= yCord + bouncy.height){
      gameOver = true;
      gameRunning = false;
      gameReset();
    }
  }
  // player wins if ball goes too fast and breaks out of screen
  else{
    victory = true;
    gameRunning = false;
    gameReset();
  }
}





// ball movement physics
function moveBall() {
  // gravity accelerates ball
  xVelocity += gravityX;
  yVelocity += gravityY;
  
  // map out the location of the ball after moving
  nextXCord = xCord + xVelocity;
  nextYCord = yCord + yVelocity;
  
  // ball not running into a wall
  if(nextXCord > leftBorder && nextXCord < rightBorder && nextYCord > topBorder && nextYCord < bottomBorder){
    xCord += xVelocity;
    yCord += yVelocity;
  }

  // ball running into left wall
  if (nextXCord < leftBorder){
    tempYCord = yCord + yVelocity / xVelocity * (leftBorder - xCord);
    if(tempYCord > topBorder && tempYCord < bottomBorder){
      xCord = leftBorder;
      yCord = tempYCord;
      xVelocity = xVelocity * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into right wall
  if(nextXCord > rightBorder){
    tempYCord = yCord + yVelocity / xVelocity * (rightBorder - xCord);
    if(tempYCord > topBorder && tempYCord < bottomBorder){
      xCord = rightBorder;
      yCord = tempYCord;
      xVelocity = xVelocity * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into ceiling (top wall)
  if(nextYCord <= topBorder){
    tempXCord = xCord + xVelocity / yVelocity * (topBorder - yCord);
    if(tempXCord > leftBorder && tempXCord < rightBorder){
      xCord = tempXCord;
      yCord = topBorder;
      yVelocity = yVelocity * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into floor (bottom wall)
  if(nextYCord >= bottomBorder){
    tempXCord = xCord + xVelocity / yVelocity * (bottomBorder - yCord);
    if(tempXCord > leftBorder && tempXCord < rightBorder){
      xCord = tempXCord;
      yCord = bottomBorder;
      yVelocity = yVelocity * BOUNCE_COEFFICIENT;
    }
  }
}






// resizes window when the window size is changed
function windowResized(){
  createCanvas(windowWidth, windowHeight);
  leftBorder = 0;
  rightBorder = windowWidth - bouncy.width;
  topBorder = 0;
  bottomBorder = windowHeight - bouncy.height;
  textAlign(CENTER, CENTER);
  textSize(FONTSIZE);
}

// displays main menu
function mainMenu(){
  background(220);
  text("This game is about dodging the ball. Except the ball gains energy and momentum when it bounces.", windowWidth/2, windowHeight/2 - FONTSIZE);
  text("Oh and the room has a chaotic gravity that changes force and direction every second.", windowWidth/2, windowHeight/2);
  text("Press G to start. Press P to pause the game at any time.", windowWidth/2, windowHeight/2 + FONTSIZE);
}

//starts the game
function startGame(){
  gameNotStarted = false;
  gameRunning = true;
  victory = false;
  gameOver = false;
}

function pauseGame(){
  gameRunning = false;
  text("Game Paused", windowWidth/2, FONTSIZE);
  text("Press G to continue", windowWidth/2, FONTSIZE*2);
}

// displays death screen
function deathScreen(){
  background(220);
  text("You were hit by the ball and died. Press G to play again.", windowWidth/2, windowHeight/2);
}

// displays when player wins
function victoryScreen(){
  background(220);
  text("The ball gained so much momentum that it broke out of the screen.", windowWidth/2, windowHeight/2);
  text("Congratulations, you survived. Press G to Play again.", windowWidth/2, windowHeight/2 + FONTSIZE);
}

// reset game after it ends
function gameReset(){
  xVelocity = 0;
  yVelocity = 0;
  xCord = windowWidth/2 - bouncy.width/2;
  yCord = windowHeight/2 - bouncy.height/2;
}