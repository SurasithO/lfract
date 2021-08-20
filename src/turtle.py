# Surasith Boonaneksap File Created Aug 3rd 2021

from math import cos, sin, radians

class Turtle:
    """
    A class keeping a state of a turtle

    A turtle is an object used to represent a pen
    on a drawing board. It always move in a straight
    line according to its heading.

    Attributes
    ----------
    heading : float
        The current heading (degrees) of the turtle
    pos : tuple of ints
        The current coordinates, (x,y), of the turtle
    """

    def __init__(self, heading = 90, pos = (0,0)):
        """
        Initializing the turtle state

        Parameters
        ----------
        heading : float or int, default = 90
            The initial heading
        pos : tuple of ints, default = (0,0)
            The initial position
        """
        
        self.heading = heading % 360
        self.pos = pos # x, y
        
    def __eq__(self, obj):
        """Two Turtle objects are equal if all its attributes are equal"""
        
        return (self.heading == obj.heading and 
                self.pos[0] == obj.pos[0] and
                self.pos[1] == obj.pos[1])

    def forward(self, dist = 1):
        """
        Moving the turtle forward [dist] pixels in the heading direction
        
        Parameters
        ----------
        dist : float or int, default = 1
            The distance (pixels) that will be traveled
        """

        rad = radians(self.heading)
        self.pos = (self.pos[0] + cos(rad)*dist, 
                    self.pos[1] + sin(rad)*dist)
    
    def turn(self, deg = 90):
        """
        Change the heading of the turtle

        Parameters
        ----------
        deg : float or int, default: 90
            The angle (degrees) to change the current heading

        Notes
        -----
        The heading will always have a value between [0,360]
        """

        self.heading = (self.heading + deg) % 360