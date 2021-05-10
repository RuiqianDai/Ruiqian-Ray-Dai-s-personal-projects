let GRAVITATIONAL_CONSTANT = 0.98;

let ballArray = [];

let gameRunning = true;

function setup() {
  createCanvas(windowWidth, windowHeight);
  window.setInterval(addBall,1000);
}

function draw() {
  background(220);
  if (gameRunning){
    displayBall();
    moveBall();
    collisionDetection();
  }
}

// drawing all balls
function displayBall(){
  for(let i = 0; i < ballArray.length; i++){
    fill(ballArray[i].color);
    circle(ballArray[i].x, ballArray[i].y, ballArray[i].radius);
  }
}

// creating balls
function addBall(){
  noStroke();
  let thisBall = {
    x: random(width),
    y: random(height),
    dx: random(-10, 10),
    dy: random(-10, 10),
    radius: random(25,50),
    color: color(random(255), random(255), random(255), random(255)),
  };
  ballArray.push(thisBall);
}

// moving each ball according to a random acceleration
function moveBall() {
  for (let i = 0; i < ballArray.length; i++){
    accelerationX = random(-10, 10);
    accelerationY = random(-10, 10);
    ballArray[i].dx += accelerationX;
    ballArray[i].dy += accelerationY;
    ballArray[i].x += ballArray[i].dx;
    ballArray[i].y += ballArray[i].dy;
  }
}

function collisionDetection(){
  for(let i=0; i<ballArray.length; i++){
    // mouse collision detection
    let mouseDistance = dist(mouseX, mouseY, ballArray[i].x, ballArray[i].y);
    if(mouseDistance <= ballArray[i].radius){
      console.log("You died.");
      gameRunning = false;
    }
  }
}


function windowResized(){
  setup();
}