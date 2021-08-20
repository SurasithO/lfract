
# L-System Fractal Generator

An open-source CLI software for generating fractal images using the L-System.

## Features

- Rewrite and draw a 2D deterministic context-free L-System. (D0L)
- Support the following turtle commands:

|  Command  | Description | 
| :-------- | :----------- |
| F         | Draw a line forward *d* pixels in the current heading|
| f         | Move forward *d* pixels in the current heading without drawing a line|
| +         | Turn right by *δ* degrees |
| -         | Turn left by *δ* degrees |
| [         | Push the current turtle's state into a stack |
| ]         | Pop a turtle's state out of the stack |

- Support saving and previewing the output image
- Support changing the drawing line's width

## Background


L-System (Lindenmayer System) is a string rewriting system that uses an iterative process. An L-System starts with ***an axiom***, an initial string, that will be rewritten following a set of ***production rules*** which contains pairs of ***predecessors*** and ***successors***. For each iteration, each symbol or character will be replaced with its corresponding successor. Any symbols without a production rule will be replaced by themselves. For example,

> **Axiom:** N  
> **Production Rules:**
> |Predecessor|Successor|
> |:---|:---|
> |N|MNO|
> |O|#|
>
> **Iteration 0:** N  
> **Iteration 1:** MNO  
> **Iteration 2:** MMNO#  
> **Iteration 3:** MMMNO##  

For illustration, ```lfract``` reserves some characters for controlling a drawing pen called ***a turtle***. The turtle keeps track of its position and heading throughout the evaluation process. After some finite number of iterations, the resulting string will be evaluated and an image will be drawn. (Supported turtle commands are listed in the previous section)  

The current version of ```lfract``` supports only the deterministic and context-free version of the L-System. That is each rule has a probability of being applied of 1 and the location of each symbol in a string relative to other symbols doesn't matter.

## Installation

This software is available to download on The Python Package Index (PyPI) and can be installed through ```pip```.  

Start by making sure that ```pip``` is installed and up-to-date
> ```python -m pip install --upgrade pip```

Run the following command on your terminal

> ```pip install lfract```

## Usage

Invokes the program using ```lfract```. There are seven optional arguments as follows:

| Option |Description|
| :--- | :----- |
| -x, --axiom  | Initial string or axiom, required |
| -r, --rules  | Production rules. Uses "->" to seperate predecessor from successor, optional |
| -a, --angle  | Turning angle, *δ* (degrees), default = 90 |
| -d, --dist   | Distance, *d* (pixels), default = 100 |
| -n, --iters  | Number of iterations, default = 0 |
| -o, --output | Output path. If specified, the image will be saved to the given path, optional |
| -w, --width  | Width of the drawing pen (pixels), default = 1 |

The user must provide at least an axiom or the initial string to the L-System. All predecessors in the set of production rules must be unique. If there are duplicates, ```lfract``` will use the latest rule.

For the full usage description of ```lfract```, type:
> ```lfract --help```

## Examples

1. Hilbert curve by Prusinkiewicz and Hanan [1]
   > ```lfract -x X -r X->-YF+XFX+FY- Y->+XF-YFY-FX+ -a 90 -d 50 -n 5 -w 5```

![hilbert](/images/hilbert.jpeg)

2. Hexagonal tiling by Prusunkiewicz and Hanan [1]
   > ```lfract -x X -r X->[-F+F[Y]+F][+F-F[X]-F] Y->[-F+F[Y]+F][+F-F-F] -a 60 -d 50 -n 10 -w 4```

![hex](/images/hex.jpeg)

3. A fractal by Surasith Boonaneksap
   > ```lfract -x A -r A->fB+AF+Fff+Bf B->Bf-FffF-FfA-Afff -a 120 -n 7 -d 50 -w 5```

![ex1](/images/ex1.jpeg)

## Notes

  - ```lfract``` adopts the L-System formal definition from [1]. It also follows the terminologies used in [1][2][3].
  - Symbols in the L-System can be any Unicode characters.
  - Currently not support:
    - Stochastic L-System
    - Context-sensitive L-System
    - Parametric L-System

## Dependency

Pillow 4.0.0 (Depending on the Python's version, a more recent version may be required. Check [Pillow's documentation](https://pillow.readthedocs.io/en/stable/installation.html#python-support))

## License

MIT

## References

[1]: Prunsinkiewicz, Przemyslaw and Hanan, James; "Lecture Notes in Biomathematics: Lindenmayer Systems, Fractals, and Plants" [link](http://algorithmicbotany.org/papers/lsfp.pdf)  
[2]: Wikipedia; "L-system" [link](https://en.wikipedia.org/wiki/L-system)  
[3]: Santel, Jordan; "L-systems" [link](https://jsantell.com/l-systems/)  