# Surasith Boonaneksap Aug 5th, 2021
from math import sqrt
import unittest

from PIL import Image

from src.turtle import Turtle
from src.lsystem import LSystem

class TurtleTest(unittest.TestCase):
    def test_init(self):
        self.t = Turtle()
        self.assertEqual(self.t.heading, 90)
        self.assertEqual(self.t.pos, (0,0))

        self.t = Turtle(150, (1,1))
        self.assertEqual(self.t.heading, 150)
        self.assertEqual(self.t.pos, (1,1))

        self.t = Turtle(370, (-1,-1))
        self.assertEqual(self.t.heading, 10)
        self.assertEqual(self.t.pos, (-1,-1))

        self.t = Turtle(-50, (110,270))
        self.assertEqual(self.t.heading, 310)
        self.assertEqual(self.t.pos, (110,270))

    def test_forward(self):
        self.t = Turtle()
        self.t.forward()

        self.assertAlmostEqual(self.t.pos[0], 0)
        self.assertAlmostEqual(self.t.pos[1], 1)
        
        self.t.forward(5)
        self.assertAlmostEqual(self.t.pos[0], 0)
        self.assertAlmostEqual(self.t.pos[1], 6)
        
        self.t.forward(-7)
        self.assertAlmostEqual(self.t.pos[0], 0)
        self.assertAlmostEqual(self.t.pos[1], -1)
        
        self.t.forward(1.7224)
        self.assertAlmostEqual(self.t.pos[0], 0)
        self.assertAlmostEqual(self.t.pos[1], 0.7224)
        
    def test_turn(self):
        self.t = Turtle()
        self.t.turn(90)
        self.assertEqual(self.t.heading, 180)

        self.t.turn(90)
        self.assertEqual(self.t.heading, 270)

        self.t.turn(180)
        self.assertEqual(self.t.heading, 90)

        self.t.turn(-45)
        self.assertEqual(self.t.heading, 45)

        self.t.turn(-50)
        self.assertEqual(self.t.heading, 355)

        self.t.turn()
        self.assertEqual(self.t.heading, 85)

    def test_forward_turn(self):
        self.t = Turtle()
        self.t.turn(-30)
        self.t.forward()

        self.assertEqual(self.t.heading, 60)
        self.assertAlmostEqual(self.t.pos[0], 1/2)
        self.assertAlmostEqual(self.t.pos[1], sqrt(3)/2)

        self.t.forward(3)
        self.assertAlmostEqual(self.t.pos[0], 2)
        self.assertAlmostEqual(self.t.pos[1], 2*sqrt(3))

class LSystemTest(unittest.TestCase):
    def setUp(self):
        LSystem.TESTING = True

    def test_check_empty_stack(self):
        self.assertRaises(TypeError, LSystem.check_empty_stack, 1)
        
        self.assertTrue(LSystem.check_empty_stack("]"))
        self.assertTrue(LSystem.check_empty_stack("[[[]]]]"))
        self.assertTrue(LSystem.check_empty_stack("[]][][]"))
        self.assertTrue(LSystem.check_empty_stack("[F+[[F--F++][]]]]"))
        
        
        self.assertFalse(LSystem.check_empty_stack("[]"))
        self.assertFalse(LSystem.check_empty_stack("[][]"))
        self.assertFalse(LSystem.check_empty_stack("[[][[]]]"))
        self.assertFalse(LSystem.check_empty_stack("[F[+]+[F-[-]FF]-+]"))
        
    def test_init(self):
        l = LSystem("a", {"a":"b", "a":"c"}, 0, 1, 0, 1, None)
        
        self.assertEqual(l.axiom, "a")
        self.assertEqual(l.rules, {"a":"c"})
        self.assertEqual(l.angle, 0)
        self.assertEqual(l.dist, 1)
        self.assertEqual(l.iters, 0)
        self.assertEqual(l.width, 1)        
        self.assertEqual(l.output, None)
        
    def test_rewrite(self):
        l = LSystem("F", {"F":"-F+"}, 1, 1, 4, 1, None)
        self.assertEqual(l.result, "----F++++")
        
        l = LSystem("ab", {"a":"bfFa","b":"+-"}, 1, 1, 3, 1, None)
        self.assertEqual(l.result, "+-fF+-fFbfFa+-")
        
        l = LSystem("F", {"F":"[F]F"}, 1, 1, 3, 1, None)
        self.assertEqual(l.result, "[[[F]F][F]F][[F]F][F]F")
        
        self.assertRaises(RuntimeError,
                          l.__init__,
                          "[", {"[":"[F]"}, 1, 1, 5, 1, None)
        
    def test_eval(self):
        l = LSystem("FFFFF", {}, 0, 1, 0, 1, None)
        self.assertEqual(len(l.stack), 0)
        self.assertEqual(l.turtle.heading, 90)
        self.assertAlmostEqual(l.turtle.pos[0], 0)
        self.assertAlmostEqual(l.turtle.pos[1], 5)
        
        l = LSystem("FfFfFfF", {}, 0, 1, 0, 1, None)
        self.assertEqual(len(l.stack), 0)
        self.assertEqual(l.turtle.heading, 90)
        self.assertAlmostEqual(l.turtle.pos[0], 0)
        self.assertAlmostEqual(l.turtle.pos[1], 7)
        
        l = LSystem("F+F+F", {}, 90, 1, 0, 1, None)
        self.assertEqual(len(l.stack), 0)
        self.assertEqual(l.turtle.heading, 270)
        self.assertAlmostEqual(l.turtle.pos[0], 1)
        self.assertAlmostEqual(l.turtle.pos[1], 0)
        
        l = LSystem("F-F-F", {}, 45, 1, 0, 1, None)
        self.assertEqual(len(l.stack), 0)
        self.assertEqual(l.turtle.heading, 180)
        self.assertAlmostEqual(l.turtle.pos[0], -sqrt(2)/2-1)
        self.assertAlmostEqual(l.turtle.pos[1], sqrt(2)/2+1)
        
        l = LSystem("[[][[[]]", {}, 90, 1, 0, 1, None)
        self.assertEqual(len(l.stack), 2)
        self.assertEqual(l.turtle.heading, 90)
        self.assertAlmostEqual(l.turtle.pos[0], 0)
        self.assertAlmostEqual(l.turtle.pos[1], 0)
        
    def test_find_bound(self):
        l = LSystem("F-F-F-F-F-F-F-", {}, 45, 4, 0, 1, None)
        self.assertAlmostEqual(l.bound[0][0], 0)
        self.assertAlmostEqual(l.bound[0][1], 4*(sqrt(2)/2+1))
        self.assertAlmostEqual(l.bound[1][0], 4*(-1-sqrt(2)))
        self.assertAlmostEqual(l.bound[1][1], 4*(-sqrt(2)/2))
        
        l = LSystem("F[-F][F][+F]", {}, 90, 5, 0, 1, None)
        self.assertAlmostEqual(l.bound[0][0], 5)
        self.assertAlmostEqual(l.bound[0][1], 10)
        self.assertAlmostEqual(l.bound[1][0], -5)
        self.assertAlmostEqual(l.bound[1][1], 0)
        
    def test_draw(self):
        l = LSystem("F-F-F-F-F-F-F-", {}, 45, 4, 0, 1, None)
        self.assertAlmostEqual(l.result_img.size[0], int(4*(1+sqrt(2))))
        self.assertAlmostEqual(l.result_img.size[1], int(4*(1+sqrt(2))))
    
    def test_invalid_init(self):
        l = LSystem("M", {"M":"MM"}, 10, 1, 1, 1, None)
        
        self.assertRaises(TypeError, l.__init__)
        
        # Invalid axiom
        self.assertRaises(TypeError, 
                          l.__init__, 
                          1, {"M":"MM"}, 10, 1, 1, 1, None)
        
        # Invalid rules
        self.assertRaises(TypeError, 
                          l.__init__, 
                          "M", [1,2,3], 10, 1, 1, 1, None)
        
        self.assertRaises(ValueError, 
                          l.__init__, 
                          "M", {"MM":"M"}, 10, 1, 1, 1, None)
        
        # Invalid angle
        self.assertRaises(TypeError, 
                          l.__init__, 
                          "M", {"M":"MM"}, "10", 1, 1, 1, None)
        
        # Invalid dist
        self.assertRaises(TypeError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, (1,), 1, 1, None)
        
        # Invalid iters
        self.assertRaises(TypeError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, [1], 1, None)
        
        self.assertRaises(ValueError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, -1, 1, None)
        
        # Invalid width
        self.assertRaises(TypeError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, 1, '1', None)
        
        self.assertRaises(ValueError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, 1, -1, None)
        
        # Invalid output
        self.assertRaises(TypeError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, 1, 1, 1)
        
        self.assertRaises(ValueError,
                          l.__init__,
                          "M", {"M":"MM"}, 10, 1, 1, 1, "output")

if __name__ == "__main__":
    unittest.main()