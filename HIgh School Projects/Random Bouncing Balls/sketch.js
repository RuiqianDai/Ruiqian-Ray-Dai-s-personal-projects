let FONTSIZE = 30;
// these two constants can be changed to alter the difficulty and how chaotic the game is
let BOUNCE_COEFFICIENT = -0.7;
let GRAVITATIONAL_CONSTANT = 0.3;

// game state variables
let gameNotStarted = true;
let gameRunning = false;
let gameOver = false;

// array that stores balls data
let ballArray = [];

// physics variables
let nextXCord;
let nextYCord;
let tempXCord;
let tempYCord;

// player score that's equal to how many balls they dodged
let score = 0;


// borders
let leftBorder;
let rightBorder;
let topBorder;
let bottomBorder;


function setup() {
  createCanvas(windowWidth, windowHeight);

  // define the borders of the ball's movement
  leftBorder = 25;
  rightBorder = windowWidth - 25;
  topBorder = 25;
  bottomBorder = windowHeight - 25;

  // initialize circle drawing modes
  ellipseMode(CENTER);
  noStroke();
  
  // get ready to display starting screen
  textAlign(CENTER, CENTER);
  textSize(FONTSIZE);

  window.setInterval(addBall, 400);
}


function draw() {
  // main menu that displays before game starts
  if(gameNotStarted){
    mainMenu();
  }
  // run game
  if(gameRunning){
    runGame();
  }
  
  if(gameOver){
    deathScreen();
    gameReset();
  }
}

// keyboard interaction
function keyPressed(){
  // if g is pressed, start/resume game
  if(key === "g"){
    if(gameNotStarted || gameOver){
      startGame();
    }
    else{ // this is when game is paused
      gameRunning = true;
    }
  }
  // if p is pressed while game is running, pause game
  if(key === "p" && gameRunning){
    pauseGame();
  }
  if(key === "m" && gameRunning){
    for(let i = 0; i < 5; i++){
      addBall();
    }
  }
}

// main function
function runGame(){
  background(220);
  // move each ball
  for(let i = 0; i < ballArray.length; i++){
    fill(ballArray[i].color);
    moveBall(ballArray[i]);
    ellipse(ballArray[i].x, ballArray[i].y, ballArray[i].radius, ballArray[i].radius);
    // player dies when mouse touches ball
    if(dist(mouseX, mouseY, ballArray[i].x, ballArray[i].y) <= ballArray[i].radius){
      gameOver = true;
      gameRunning = false;
    }
  }
  fill(0);
  text("Score: " + score, windowWidth/2, windowHeight - FONTSIZE + 10);
}

// watch out, this ball is coming to get you
// a random horizontal velocity is first assigned to the ball, then it aims for the mouse in a parabolic trajectory by calculating the required vertical velocity based on that horizontal velocity and the locations of the ball and mouse
// this isn't really an AI but it's close, it does the job of chasing the player.
// some balls spawn too far away from the mouse with too little horizontal velocity and just can't reach the ball; the other ones will definitely go for the kill if you don't move.
// assuming Mr. Guest has taught me well and I didn't mess up my physics calculation, that is.
function addBall(){
  let thisBall = {
    x: random(25, width - 25),
    y: random(25, height - 25),
    dx: random(1, 10),
    dy: 0,
    radius: 25,
    color: color(random(255), random(255), random(255)),
  };
  if(thisBall.x > mouseX){
    thisBall.dx = thisBall.dx * (-1);
  }
  thisBall.dy = (mouseY - thisBall.y)/(mouseX - thisBall.x)*thisBall.dx + GRAVITATIONAL_CONSTANT * (mouseX - thisBall.x)/thisBall.dx/2;
  ballArray.push(thisBall);
  if(gameRunning){
    score += 1;
  }
}


// ball movement physics
function moveBall(theBall) {
  // apply effect of gravity
  theBall.dy += GRAVITATIONAL_CONSTANT;
  
  // map out the location of the ball after moving
  nextXCord = theBall.x + theBall.dx;
  nextYCord = theBall.y + theBall.dy;

  // ball not running into a wall
  if(nextXCord > leftBorder && nextXCord < rightBorder && nextYCord > topBorder && nextYCord < bottomBorder){
    theBall.x += theBall.dx;
    theBall.y += theBall.dy;
  }

  // ball running into left wall
  if (nextXCord < leftBorder){
    tempYCord = theBall.y + theBall.dy / theBall.dx * (leftBorder - theBall.x);
    if(tempYCord > topBorder && tempYCord < bottomBorder){
      theBall.x = leftBorder;
      theBall.y = tempYCord;
      theBall.dx = theBall.dx * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into right wall
  if(nextXCord > rightBorder){
    tempYCord = theBall.y + theBall.dy / theBall.dx * (rightBorder - theBall.x);
    if(tempYCord > topBorder && tempYCord < bottomBorder){
      theBall.x = rightBorder;
      theBall.y = tempYCord;
      theBall.dx = theBall.dx * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into ceiling (top wall)
  if(nextYCord <= topBorder){
    tempXCord = theBall.x + theBall.dx / theBall.dy * (topBorder - theBall.y);
    if(tempXCord > leftBorder && tempXCord < rightBorder){
      theBall.x = tempXCord;
      theBall.y = topBorder;
      theBall.dy = theBall.dy * BOUNCE_COEFFICIENT;
    }
  }

  // ball running into floor (bottom wall)
  if(nextYCord >= bottomBorder){
    tempXCord = theBall.x + theBall.dx / theBall.dy * (bottomBorder - theBall.y);
    if(tempXCord > leftBorder && tempXCord < rightBorder){
      theBall.x = tempXCord;
      theBall.y = bottomBorder;
      theBall.dy = theBall.dy * BOUNCE_COEFFICIENT;
    }
  }
}




// resizes window when the window size is changed
function windowResized(){
  createCanvas(windowWidth, windowHeight);
  leftBorder = 25;
  rightBorder = windowWidth - 25;
  topBorder = 25;
  bottomBorder = windowHeight - 25;
  textAlign(CENTER, CENTER);
  textSize(FONTSIZE);
}

// displays main menu
function mainMenu(){
  background(220);
  text("Welcome to the ball dodging game v2.0, where you try dodging the balls with your mouse for as long as you can.", windowWidth/2, windowHeight/2 - FONTSIZE);
  text("This time balls bounce following the laws of physics, but there's more than one, and they are coming for you.", windowWidth/2, windowHeight/2);
  text("Press G to start. Press P to pause the game at any time. Press M to add more balls, if you insist.", windowWidth/2, windowHeight/2 + FONTSIZE);
}

//starts the game
function startGame(){
  gameNotStarted = false;
  gameRunning = true;
  gameOver = false;
  score = 0;
}

function pauseGame(){
  gameRunning = false;
  fill(0);
  text("Game Paused", windowWidth/2, FONTSIZE);
  text("Press G to continue", windowWidth/2, FONTSIZE*2);
}

// displays death screen
function deathScreen(){
  background(220);
  fill(0);
  text("You survived " + score + " balls before you were hit. Press G to play again.", windowWidth/2, windowHeight/2);
}


// reset game after it ends
function gameReset(){
  ballArray = [];
}