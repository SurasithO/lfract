"""
Fractal generator using deterministic and context-free
L-system. (D0L)

This script is the entry point to command-line interface
of the software. Users must at least provide an axiom 
to an L-system in order to generate an image. Production 
rules, turning angle, distance, and the number of 
iterations are optional. 

Any unicode characters can be used as a variable except
the following constants that will be used to command
a turtle:

F = move forward and draw a line for d pixels
f = move forward without drawing a line for d pixels
+ = turn right by ẟ degrees
- = turn left by ẟ degrees
[ = push the turtle state to a stack
] = pop the turtle state out of the stack

This software requires Pillow 4.0.0 to draw and process
an image (May need a more recent version depending on
the Python's version)

Author: Surasith Boonaneksap

References:
- https://link-springer-com.ezproxy.lib.vt.edu/content/pdf/10.1007%2F978-1-4757-1428-9.pdf
- https://en.wikipedia.org/wiki/L-system
- https://jsantell.com/l-systems/
"""

#Surasith Boonaneksap Start on July 31st, 2021

__version__ = "1.0.0"

import argparse

from .lsystem import LSystem

DESCRIPTION = """

Fractal generator using deterministic and context-free
L-system. (D0L)

"""

def rules_parser(rules):
    """
    Convert a list of rules to a dictionary
    with predecessor as the key and successor
    as its value.

    Each rule must be in the form of
    "[predecessor]->[successor]"

    Parameter
    ---------
    rules: list of str
        A list containing production rules
    
    Return
    ------
    dict {str: str}
        The production rules in a dictionary
    """

    if not rules:
        return {}
    
    result = {}
    for r in rules:
        key, val = r.split("->")
        result[key] = val
    return result

# Fractal Generator with L-system
def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    
    parser.add_argument("-x", "--axiom", 
                        required=True, 
                        type=str, 
                        help="initial string or axiom, required")
    
    parser.add_argument("-r", "--rules", 
                        nargs='+', 
                        type=str, 
                        help='production rules. Uses "->" to '
                             'seperate predecessor from successor, optional')
    
    parser.add_argument("-a", "--angle", 
                        default=90, 
                        type=float, 
                        help="turning angle, ẟ (degrees), default = 90")
    
    parser.add_argument("-d", "--dist", 
                        default=100, 
                        type=float, 
                        help="distance (pixels), default = 100")
    
    parser.add_argument("-n", "--iters", 
                        default=0, 
                        type=int, 
                        help="number of iterations, default = 0")
    
    
    
    parser.add_argument("-o", "--output", 
                        type=str, 
                        help="output path. "
                             "If specified, the image will be saved "
                             "to the given path, optional")
    
    parser.add_argument("-w", "--width", 
                        default=1,
                        type=int, 
                        help="width of the drawing pen (pixels)"
                             ", default = 1")
    
    parser.add_argument("-v", "--version", 
                        action="version", 
                        version=f"lfract {__version__}")

    input = parser.parse_args()

    LSystem(input.axiom, 
            rules_parser(input.rules), 
            input.angle, 
            input.dist, 
            input.iters, 
            input.width, 
            input.output)

if __name__ == "__main__":
    main()