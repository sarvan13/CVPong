# CVPong
This is my attempt at creating the classic game of Pong but with the added twist of using motion capture so that the player controls the paddle with their hand rather than keys. 

## Running the game
### Dependencies
Before we run the game we need to make sure we have the correct tools installed. The game makes use of three major libraries that is pygame (game development), openCV (camera input), and media pipe (hand detection).

I am assuming that python is already downloaded on the system, this means that we can use pip and the command line to install these libraries with the following command:

``` pip install pygame opencv-python mediapipe ```

### Run the game

Now that the dependencies are installed we just need to run the game - **no GOOD game to run yet lol**

``` python <insert-game-name> ```

## Physics

Interestingly in the problem statement it was mentioned that friction was needed in order to include the velocity of the paddle to the ball. This is indeed true for realistic scenarios, however in games often times we need to bend a few rules of physics in order to make it a more enjoyable experience. Because of this, I have cherry picked certain physics laws to make the game seem somwhat real but still enjoyable. Friction is needed if we want to include a change in momentum due to rotation or due to the paddle. However, friction will also take away some of the balls momentum as well. Here are some big constraints that I have employed on the game:

- Paddle has infinite mass (balls momentum has no impact on the paddles motion)
- Ball is completely elastic - it does not lose energy upon collision with the paddle
- There is no slipping when the ball collides with the paddle
- The ball instantly reflects back off the paddle

Now let me explain the reasoning for these constraints. I think the first one is obvious, I want the player to be in full control of the paddle - it would be annoying for the ball to start moving something you are supposed to have control over. The ball being completely elastic and not loosing energy upon collision is essentially me making sure that the ball isnt forever slowing down and losing energy to friction. Now the last next constraint might cause a bit of a problem. Frankly, I don't really want to deal with a ball sliping as the physics gets a bit more complicated and I dont think thats the main purpose of this project. The reason that this could be a problem is that slipping is what makes a spinning ball gain speed off a wall. In reality when a spinning ball contacts a wall, assuming it is not moving on the wall, the ball remains spining (this is slipping) the friction force acts opposite of the direction of the spin. So a spinning ball can accelerate off the wall using this friction force and remain spinning in the same direction as before as the torque from the friction force doesnt completely stop the spin of the ball. But if we say theres no slipping then we are saying that the wall instantly nullifies the balls torque forcing it to a stop. The friction force from the wall would then produce a torque on the ball that would spin it in the opposite direction. Essentially the effect of this constraint is that a spinning ball will always reverse its direction upon contact with the paddle and the increases in speeed are greater than what we would see in real life. I am not too sure how I will do this yet. I think I may use energy but not sure how I will calculate it without slipping if I am saying it is instatenous - this might just have to be an arbritary lurch and require me forgoing physics equations entriely. Usually we would have to consider the time of contact and calculate the angular velocity using the net torque and then we could get the additional linear velocity. I might consider making my own friction constant that tells me how much of the angular velocity I should remove and convert to linear velocity and maybe this will give more realistic results. Ie I might ignore some physics laws here for gameplay purposes. 
