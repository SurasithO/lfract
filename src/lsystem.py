# Surasith Boonaneksap File Created Aug 3rd 2021

from math import inf
from copy import deepcopy
import re

from PIL import Image, ImageDraw

from .turtle import Turtle
from .arg_handling import _arg_handling

class LSystem:
    """
    Store the state and evaluate an L-System

    Attributes
    ----------
    axiom : str
        The initial string or an axiom
    rules : dict {str : str}
        The production rules
    angle : float or int
        The angle ẟ (degrees) turned for each turning command
    dist : float or int
        The distance (pixels) travelled for each forward command
    iters : int
        The number of iterations
    result : str
        The result after rewriting
    result_img : Image
        The final image adfter drawing
    bound : tuple of tuple of ints
        The max and min of the image
    width : int
        The width of the drawing pen
    turtle : Turtle
        The current turtle state
    stack : list
        A stack used to support [ and ] command
    output : str
        The output filename
    """
    TESTING = False

    def __init__(self, axiom, rules, angle, dist, iters, width, output):
        """
        Initialize variables necessary for evaluating an L-system.
        Rewrite and draw a representation of that L-system.

        Parameters
        ----------
        axiom : str
            The initial string or an axiom
        rules : dict {str : str}
            The production rules
        angle : float or int
            The angle ẟ (degrees) turned for each turning command
        dist : float or int
            The distance (pixels) travelled for each forward command
        iters : int
            The number of iterations
        width : int
            The width of the drawing pen
        output : str
            The output file
        """
        
        _arg_handling(axiom, str)
        _arg_handling(rules, dict, 
                      [re.compile("."), re.compile(".*")],
                      err_msg="Invalid rules. "
                      "The predecessor can only have one symbol.")
        _arg_handling(angle, float)
        _arg_handling(dist, float)
        _arg_handling(iters, int, [0,inf], err_msg="The number of iterations "
                      "must be a positive integer.")
        _arg_handling(width, int, [0,inf], err_msg="The pen width must be a "
                      "positive integer.")
        if output:
            _arg_handling(output, str, re.compile(".+\..+"))

        self.axiom      = axiom
        self.rules      = rules
        self.angle      = angle
        self.dist       = dist
        self.iters      = iters

        self.result     = ""
        self.result_img = None
        self.bound      = ((0,0), (0,0)) # (max, min)
        self.width      = width

        self.turtle     = None
        
        self.stack      = []

        self.output     = output

        self._rewrite()
        self._find_bound()
        self._draw()
    
    def _rewrite(self):
        """
        Rewriting the axiom according to the given rules and arguments

        Symbols, including constants, without a production rule have an 
        identity property. That is the symbol will be converted to itself.

        Warnings
        --------
        This method is private and should only be called only once after
        initialization.
        
        Raise
        -----
        RuntimeError
            Raise when the resulting L-System have an incorrect number
        of brackets
        """

        self.result = self.axiom

        for i in range(self.iters):
            iter_result = ""

            for c in self.result:
                try:
                    iter_result += self.rules[c]
                except KeyError:
                    iter_result += c

            self.result = iter_result
        
        if(self.check_empty_stack(self.result)):
            raise RuntimeError("This L-system will pop an empty stack")
    
    def _eval(self, symbol):
        """
        Evaluate a symbol and command the turtle

        Parameter
        ---------
        symbol : char
            A variable or a constant

        Warnings
        --------
        This method modified the current state of the
        turtle and the stack.
        """

        if (symbol in "Ff"):
            self.turtle.forward(self.dist)
            
        elif (symbol == "+"):
            self.turtle.turn(-self.angle)

        elif (symbol == "-"):
            self.turtle.turn(+self.angle)

        elif (symbol == "["):
            self.stack.append( deepcopy(self.turtle) )
        
        elif (symbol == "]"):
            self.turtle = self.stack.pop()
        
        return self.turtle.pos

    def _find_bound(self):
        """
        Find the boundary of the canvas
        
        Warnings
        --------
        This method is private and should only be called
        after the rewriting process is completed.
        """
        
        self.turtle = Turtle()
        self.stack  = []

        max_ = [0, 0]
        min_ = [0, 0]

        for c in self.result:
            x, y = self._eval(c)

            max_ = [max(x, max_[0]), max(y, max_[1])]
            min_ = [min(x, min_[0]), min(y, min_[1])]
        
        self.bound = (tuple(max_), tuple(min_))

    def _draw(self):
        """
        Draw the lines as instructed on the string

        The output, if specified, will be saved to
        the given filename. Otherwise, the result
        will be shown after completion.
        
        Warnings
        --------
        This method is private and should only be called
        after the boundary of the image is found and the
        rewriting process is completed.
        
        Notes
        -----
        The image size after drawing must be at least (1, 1)
        """

        self.turtle = Turtle()
        self.stack = []

        img_width  = int(abs(self.bound[0][0] - self.bound[1][0]))
        img_height = int(abs(self.bound[0][1] - self.bound[1][1]))

        self.result_img = Image.new("1", (img_width, img_height))

        canvas = ImageDraw.Draw(self.result_img)

        _, min_ = self.bound
        
        start_x, start_y = 0, 0
        for c in self.result:
            x, y = self._eval(c)
            
            if c == "F":
                # Coordinates Correction
                # - The image's lowest point in the image is 0, 0
                # - y coordinate is inverted (for graphical coordinates)
                start_x_adj = start_x - min_[0]
                start_y_adj = img_height - (start_y - min_[1])

                x_adj       = x - min_[0]
                y_adj       = img_height - (y - min_[1])

                canvas.line([start_x_adj, start_y_adj, x_adj, y_adj], 
                            fill = 1, 
                            width = self.width)

            start_x, start_y = x, y
        
        if (not LSystem.TESTING):
            if (self.result_img.size[0] < 1 
                    or self.result_img.size[1] < 1):
                print("The image size must be at least (1,1)")
            else:
                print("done")
                if self.output:
                    self.result_img.save(self.output)
                else:
                    self.result_img.show()
              
    @staticmethod  
    def check_empty_stack(input):
        """
        Check if the L-system will pop an empty stack.
        
        As the L-system is being evaluated, there are more
        closing brackets ("[") than opening bracket ("]")
        at some point.
        
        Parameter
        ---------
        input: str
            An L-system string
        
        Return
        ------
        bool
            True if there's an attempt to pop an empty stack.
        False otherwise.
        """
        
        _arg_handling(input, str)
        
        unpaired_bracket = 0
        
        for c in input:
            if c == "[":
                unpaired_bracket += 1
            elif c == "]":
                unpaired_bracket -= 1
                
            if unpaired_bracket < 0:
                return True
        
        return False