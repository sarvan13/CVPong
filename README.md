# CVPong
This is my attempt at creating the classic game of Pong but with the added twist of using motion capture so that the player controls the paddle with their hand rather than keys. 

<p float="center">
  <img src="https://sarvangill.ca/docs/PONG-home.png" width="500" />
  <img src="https://sarvangill.ca/docs/PONG-game.png" width="500" /> 
</p>

The background images of the game were both generated using AI and took off the internet, the fonts I also found online for free. I actually decided to remove the background in the game so these are actually old images of the basic game. The final game has 4.5 game modes! 

### Demo Video
```CVPong/video-demo.mkv```

**Note:** In the video I say that the last game mode is "spaghetti code", I am not referring to the code in general here but I am specifically talking about the Double Trouble mode which is unfinished as I described. There are two copies of the game and I would like to submit the one without "Double Trouble" as my official subission due to it having much better code quality. This is explained better in the next section. 

**Note2:** In the video the second grey power up appears to do nothing - this is not a bug, it is the intended behaviour. You can see that as I get the power up the ball contacts the other paddle. The power up slows the ball down for a short time OR until it hits a paddle/wall. The second condition is what happened on the second grey power up!

## Running the game

### Getting the code
Before I get into running the game - let me explain what to clone from the repo. The main branch is this one you are looking at `beta`. Please clone this branch.

This branch actually contains 2 copies of the game. The main game lives within `CVPong/GameV2`. This includes the first 4 game modes. It *DOES NOT* contain the last game mode "Double Trouble". The game with "Double Trouble" lives within `CVPong/Beta/GameV2`. I have labelled the game with the "Double Trouble" mode a beta version, not because the game mode doesnt work (it does) but because I made this game mode fully knowing that it would expose all the flaws in my code and lead to some hacky development. I do see value in acknowledging areas of improvement and instead of just telling you where I could improve - I present this game mode and this super uninspiring code changes that I had to make to get it working. So if you are judging my code quality please look in `CVPong/GameV2` and not `CVPong/Beta/GameV2`. 

### Dependencies
Before we run the game we need to make sure we have the correct tools installed. The game makes use of three major libraries that is pygame (game development), openCV (camera input), and media pipe (hand detection).

#### Windows
The game was developed on Windows and the dependencies were installed using powershell.

I am assuming that python is already downloaded on the system, this means that we can use pip and the command line to install these libraries with the following command:

``` pip install pygame opencv-python mediapipe ```

#### Mac OS
I want to note that I did all of my development on a Windows machine but I was able to borrow an M1 Macbook Air to test on as well. There is one big issue that I came across in this testing and that is that the newest version of `mediapipe` does not seem to work on the M1 chip. The other thing is that `mediapipe` officially only supports up to Python 3.10. For this reason I downgraded python to `Python-3.9`. You can also just install `Python-3.9`using `Homebrew`.

You can install both `pygame` and `open-cv` packages normally as we did before, however for M1 Macbooks we need to install Mediapipe version `0.10.9`, so:

``` pip3.9 install mediapipe==0.10.9 ```

This command uses the pip installation that is installed with `Python-3.9`.

Now I suspect downgrading to `Python-3.9` is not necessary as my Windows machine is running `Python-3.11`. However, I have only tested out this environment. On the other hand, downgrading `mediapipe` to `0.10.9` is **absolutely necessary** as I have confirmed that the newest version of mediapipe does not run properly on M1. 

### Run the game

Now that the dependencies are installed we just need to run the game - and to do that is quite simple.

First make sure you are inside the correct directory of the game you want to try so either `cd /install/path/CVPong/GameV2` or `cd /install/path/CVPong/Beta/GameV2`. Once inside the directory simply run:

``` python pong.y ```

(this might be `python3` or `python3.9` depending on your environemnt)

That should do it. Enjoy the game!

## Game Instructions
In all game modes you can select whether to use motion capture or to use the keyboard on a menu screen before the game. Use your right hand to control the paddle unless the instructions below say otherwise. The game can be paused using escape or by moving your right hand over to the left third of the screen. Try to keep your hands upright so the game can tell the difference between left and right! There are basic physics that include the paddles velocity when the ball is hit which is explained further below.

### Classic
Your classic game of pong playing against a computer. You can use your right hand to control the paddle or the arrow keys - there is a menu screen to select. Game is first to 7 points.

### Infinite
This is game mode is what was described by the task in its most basic form. Control the paddle with your right hand and play pong against the wall. Game ends when you miss the ball. Game of trying to get a high score.

### Two Player
Remove the computer from the classic game mode and add another hand and you have the two player mode. Right hand controls right paddle, left hand controls left paddle. Game is first to 7 points.

### Arcade
This is the classic game modes but with power ups! The game will randomly spit out little balls that are power ups if your paddle touches it.
- `Grey:Slow` - slows the ball for a brief period of time (or until the ball contacts a wall or paddle) before returning to its original speed
- `Ice:Freeze` - freezes the computers paddle for a brief period of time
- `Green:Grab` - allows the user to grab the ball and then release it at a new angle and the original speed
#### Grab Power Up Control
There is a sweeping line that indicates the balls trajectory on release when it is stuck on your paddle. To release the ball on the keyboard all you have to do is click the space bar.

If you are using hand detection, then in order to grab the ball you must show the screen a closed fist - your paddle will go green when it detects that you have the power up and that your fist is closed. To release the ball simply open your hand!

### Double Trouble
**Only in the `Beta/GameV2` version**
Here all 4 walls have paddles. Your left hand controls the top paddle and your right hand controls the right paddle. Keep your hands upright as rotating them will confuse the game as to which hand is which if they aren't straight. On the keyboard you control both paddles at once with the up and down arrows, that is the top and right paddle lose their individuality and now only work as one.


## Game Notes
Unfortunately I was not able to keep the Mac I borrowed for the entire week so I wasn't able to test some things on other platforms. One thing that I think could be impacted by this is the closed and open hand detection. I have a feeling that the resolution of the camera will impact whether my threshold I have set here. The threshold is quite robust on my 2018 Surface Book but you might need to move your hand slightly farther away from the camera for this if your resolution is higher than mine.

## Physics
### Background (Feel free to skip)
This part below is mostly for my understanding and the justification of my decisions. For the actual implementation in the game - see the next section. 

Interestingly in the problem statement it was mentioned that friction was needed in order to include the velocity of the paddle to the ball. This is indeed true for realistic scenarios, however in games often times we need to bend a few rules of physics in order to make it a more enjoyable experience. Because of this, I have cherry picked certain physics laws to make the game seem somwhat real but still enjoyable. Friction is needed if we want to include a change in momentum due to rotation or due to the paddle. However, friction will also take away some of the balls momentum as well. Here are some big constraints that I have employed on the game:

- Paddle has infinite mass (balls momentum has no impact on the paddles motion)
- Ball is completely elastic - it does not lose energy upon collision with the paddle
- There is no slipping when the ball collides with the paddle
- The ball instantly reflects back off the paddle

Now let me explain the reasoning for these constraints. I think the first one is obvious, I want the player to be in full control of the paddle - it would be annoying for the ball to start moving something you are supposed to have control over. The ball being completely elastic and not loosing energy upon collision is essentially me making sure that the ball isnt forever slowing down and losing energy to friction. Now the last next constraint might cause a bit of a problem. Frankly, I don't really want to deal with a ball sliping as the physics gets a bit more complicated and I dont think thats the main purpose of this project. The reason that this could be a problem is that slipping is what makes a spinning ball gain speed off a wall. In reality when a spinning ball contacts a wall, assuming it is not moving on the wall, the ball remains spining (this is slipping) the friction force acts opposite of the direction of the spin. So a spinning ball can accelerate off the wall using this friction force and remain spinning in the same direction as before as the torque from the friction force doesnt completely stop the spin of the ball. But if we say theres no slipping then we are saying that the wall instantly nullifies the balls torque forcing it to a stop. The friction force from the wall would then produce a torque on the ball that would spin it in the opposite direction. Essentially the effect of this constraint is that a spinning ball will always reverse its direction upon contact with the paddle and the increases in speeed are greater than what we would see in real life. I am not too sure how I will do this yet. I think I may use energy but not sure how I will calculate it without slipping if I am saying it is instatenous - this might just have to be an arbritary lurch and require me forgoing physics equations entriely. Usually we would have to consider the time of contact and calculate the angular velocity using the net torque and then we could get the additional linear velocity. I might consider making my own friction constant that tells me how much of the angular velocity I should remove and convert to linear velocity and maybe this will give more realistic results. Ie I might ignore some physics laws here for gameplay purposes. 

### Paddle Ball Interaction
Those were a lot of words, but in the game itself its not too complicated. At the very basics what I did was I added the paddles vertical speed to the balls vertical speed, while making sure that the ball doesnt lose energy. Without the physics, I simply had the ball bouncing off the paddle and gaining a very small amount of both horizontal and vertical velocity (about 5% of the initial velocity). To add the paddle and ball interaction, I took this resultant velocity without the physics and I simply added the vertical velocity of the paddle. Well kinda...

So I dont want the ball to lose energy and if the paddle is moving in an opposing direction in most cases the ball would lose energy in the real world. So what I did at first was I put all the energy lost from the vertical velocity back into the horizontal velocity of the ball. I enforced the following equation:

${v_{xf}}^2 + {v_{yf}}^2 \geq {v_{xi}}^2 + {v_{yi}}^2$

The way I did this at first was by checking if $\lvert{v_{yf}}\rvert <  \lvert{v_{yi}}\rvert$. If this was true I calculated the new x velocity using the equation above. If this was false then I already had more energy so I didn't care to add anything to the x velocity. I then capped the max energy gained by clamping $\lvert{v_{yf}} - {v_{yi}}\rvert$ to some value that seemed reasonable in the game (so it didnt get too crazy).

Now this worked, but it felt a bit off because the angles weren't what I was expecting as a user and obviously it skewed the game to the ball having large y velocities. This made me realize that it was the angle that mattered more to me as a player than the speed itself. So my final decision was to calculate the angle first and then clamp the magnitude of the resulting vector.

$\theta =$ atan2 $\left({v_{y-ball}} + {v_{y-paddle}}, {v_{x-ball}}\right)$

Keep in mind that ${v_{yf}} = {v_{y-ball}} + {v_{y-paddle}}$ and that the energy of the ball at this point is equal to the magnitude of its total velocity. So to clamp the total energy gain I set an aritrary `MAX_SPEED_INC` constant that capped the maximum amount of energy that the ball could gain. So I enforced: $0$ < ${v_{xf}}^2 + {v_{yf}}^2 - {v_{xi}}^2 + {v_{yi}}^2$ < `MAX_SPEED_INC`. What this means is that I essentially check the new magnitude of the velocity vector and force it to be at least equal to the previous length, but also put a cap on it if it is too large (dont want too much speed increase). Then with this new magnitude and the $\theta$ as calculated before, I get the new x and y velocities of the ball and it maintains a much more reasonable angle while not losing any energy or gaining too much energy. 





