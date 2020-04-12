"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
from abc import ABC
from abc import abstractmethod
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 5

##########################################################################################

#This class is for creating a position for things like centers
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0
#this is to wrap the flying objects and their points back onto the screen        
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = x % SCREEN_WIDTH
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        self._y = y % SCREEN_HEIGHT
#This determines speed or velocity
class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0


#flyingObject is the parent class of targets and bullets and does draw, advance, and if it goes off screen functions.
class flyingObject():
    
#Creates the member data
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0
        self.alive = True
        self.texture = ''
        self.angle = 0
        
#Draws flying objects with their angle and texture as well
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius*2, self.radius*2, self.texture, self.angle)
#advances the flying objects that are passed in    
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
     
#This class is giving the classes being passed in through inheritance certain properties
class Target(ABC, flyingObject):
    def __init__(self):
        super().__init__()
        self.radius = BIG_ROCK_RADIUS
        self.center.y = random.randint(0,SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(BIG_ROCK_SPEED * -1, BIG_ROCK_SPEED)
        self.velocity.dy = random.uniform(BIG_ROCK_SPEED * -1, BIG_ROCK_SPEED)
        self.spin = BIG_ROCK_SPIN
#Gives other classes the chance to advance        
    def advance(self):
        super().advance()
        self.angle += self.spin
#creates a pre req that all classes must have in this inheritance to use this class        
    @abstractmethod
    def hit(self):
        pass


#A class for bullets
class Bullet(flyingObject):
    def __init__(self, ship):
        super().__init__()
        self.texture = arcade.load_texture("laser.png")
        self.radius = BULLET_RADIUS
        self.angle = (ship.angle + 90)
        self.center.x = ship.center.x
        self.center.y = ship.center.y
        self.velocity.dx = ship.velocity.dx
        self.velocity.dy = ship.velocity.dy
        self.life = BULLET_LIFE
#draws the bullets and their angle and texture    
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.texture.width, self.texture.height, self.texture, self.angle)
    
#initiates the bullet by firing it   
    def fire(self):
        self.velocity.dx += math.cos(math.radians(self.angle)) * BULLET_SPEED
        self.velocity.dy += math.sin(math.radians(self.angle)) * BULLET_SPEED
        
#this is used to advance the bullet   
    def advance(self):
        super().advance()
        self.life -= 1
        if self.life < 0:
            self.alive = False
#creates a big rock astroid and its respective properties  
class Big(Target):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("big.png")
#determines what happens if hit       
    def hit(self):
        self.alive = False
        return [Medium(self.center, self.velocity, 2), Medium(self.center, self.velocity, -2), Small(self.center, self.velocity, 5, 0)]
#creates a medium rock astroid and its respective properties
class Medium(Target):
    def __init__(self,center,velocity,y):
        super().__init__()
        self.velocity.dx = velocity.dx
        self.velocity.dy = velocity.dy + y
        self.texture = arcade.load_texture("medium.png")
        self.radius = MEDIUM_ROCK_RADIUS
        self.spin = MEDIUM_ROCK_SPIN
        self.center.x = center.x
        self.center.y = center.y
#determines what happens if hit       
    def hit(self):
        self.alive = False
        return [Small(self.center, self.velocity, 1.5, 1.5), Small(self.center, self.velocity, -1.5, -1.5)]
#creates a small rock astroid and its respective properties     
class Small(Target):
    def __init__(self, center, velocity, x, y):
        super().__init__()
        self.velocity.dx = velocity.dx + x
        self.velocity.dy = velocity.dy + y
        self.texture = arcade.load_texture("small.png")
        self.radius = SMALL_ROCK_RADIUS
        self.rotation_speed = SMALL_ROCK_SPIN
        self.center.x = center.x
        self.center.y = center.y
#determines what happens if hit    
    def hit(self):
        self.alive = False
        return []
     
#creates a class for the ship and its respective properties
class Ship(flyingObject):
    def __init__(self):
        super().__init__()
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.texture = arcade.load_texture("ship.png")
        self.radius = SHIP_RADIUS
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        self.angle = 0
#a function to turn the ship in terms of angles  
    def turn(self, t):
        self.angle -= t
#a function to thrust it forward or backward        
    def thrust(self, a):
        self.velocity.dx += math.cos(math.radians(self.angle + 90)) * a
        self.velocity.dy += math.sin(math.radians(self.angle + 90)) * a
        
        
        
        






##########################################################################################


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.bullets = []
        self.rocks = [Big(), Big(), Big(), Big(), Big()]
        self.ship = Ship()
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        if self.ship.alive:
            self.ship.draw()
        
        for i in self.rocks:
            i.draw()
            
        for j in self.bullets:
            j.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        for i in self.rocks:
            i.advance()
        for j in self.bullets:
            j.advance()
            
        self.ship.advance()

        # TODO: Check for collisions
        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for rock in self.rocks:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and rock.alive:
                    too_close = bullet.radius + rock.radius

                    if (abs(bullet.center.x - rock.center.x) < too_close and
                                abs(bullet.center.y - rock.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.rocks += rock.hit()
                        
        for rock in self.rocks:

            # Make sure they are both alive before checking for a collision
            if self.ship.alive and rock.alive:
                too_close = self.ship.radius + rock.radius

                if (abs(self.ship.center.x - rock.center.x) < too_close and
                            abs(self.ship.center.y - rock.center.y) < too_close):
                    # its a hit!
                    self.ship.alive = False
                    self.rocks += rock.hit()

                        # We will wait to remove the dead objects until after we
                        # finish going through the list
        for i in self.rocks:
            if not i.alive:
                self.rocks.remove(i)
        for j in self.bullets:
            if not j.alive:
                self.bullets.remove(j)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.turn(-1 * SHIP_TURN_AMOUNT)

        if arcade.key.RIGHT in self.held_keys:
            self.ship.turn(SHIP_TURN_AMOUNT)
            
        if arcade.key.UP in self.held_keys:
            self.ship.thrust(SHIP_THRUST_AMOUNT)

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust(-SHIP_THRUST_AMOUNT)

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass
        


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet(self.ship)
                bullet.fire()
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()