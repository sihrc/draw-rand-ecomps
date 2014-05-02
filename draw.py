"""
Draws images of capacitors and resistors

author: chris @ sihrc
"""

import cv2
import numpy as np
from random import randint
from random import choice
import math

class Component:
    def __init__(self, size = 512, thickness = 5, error = 20, id = 0):
        self.img = np.ones((size,size,3), np.uint8) * 255 
        self.size = size
        self.thickness = thickness
        self.error = error
        self.id = id 

    def drawLine(self, start, end):
        cv2.line(self.img, start, end, (0,0,0), self.thickness)
        return end

    def pt(self, x, y):
        x = int (x)
        y = int (y)
        lowx = x - self.error if x > self.error else 0
        highx = x + self.error if x < self.size else self.size
        lowy = y - self.error if y > self.error else 0
        highy = y + self.error if y < self.size else self.size
        return (randint(lowx,highx), randint(lowy, highy))

    def show(self):
        cv2.imshow("capacitor%d" % self.id, self.img)
        cv2.waitKey(0)

class Capacitor(Component):
    """

    --| |--

    """
    def draw(self):
        section = self.size/5
        half = self.size/2

        start_1 = self.pt(0,            half)
        end_1   = self.pt(section,      half)
        self.drawLine(start_1, end_1)
    
        start_2 = self.pt(section,      0)
        end_2   = self.pt(section,      self.size)
        self.drawLine(start_2, end_2)

        start_3 = self.pt(3*section,    0)
        end_3   = self.pt(3*section,    self.size)
        self.drawLine(start_3, end_3)

        start_4 = self.pt(3*section,    half)
        end_4   = self.pt(self.size,    self.size/2)
        self.drawLine(start_4, end_4)

class Resistor(Component):
    """

    --/\/\/\---

    """
    def __init__(self, length, theta, error = 20):
        Component.__init__(self)
        self.length = length
        self.theta = theta
        self.error = error

    def draw(self):
        half = self.size/2
        first_section = randint(int(self.size/5), int(self.size/3))

        start  = self.pt(0,            half)
        prev   = self.pt(first_section,      half)
        self.drawLine(start, prev)

        count = 0
        direction = choice([1,-1])
        canFinish = False
        size = 1
        dx = 0
        limit = self.size - first_section * 2
        while (dx < limit):
            next_ = self.next(prev, 1, size * direction)
            next_ = self.pt(next_[0], next_[1])
            dx += next_[0] -prev[0]
            prev = self.drawLine(prev, next_)
            print dx
            direction *= -1
            size = 2
        
        if size == 2:
            next_ = self.next(prev, 1, direction)
            prev = self.drawLine(prev, self.pt(next_[0], next_[1]))

        self.drawLine(prev, self.pt(self.size, half))


    
    def next(self, start, X, Y):
        randTheta = self.theta/math.pi * 180
        randTheta = randint(randTheta - 15, randTheta + 15)
        randTheta = randTheta/180.0  * math.pi
        dx = self.length * math.sin(randTheta/2)
        dy = self.length * math.cos(randTheta/2)
        return (start[0] + abs(X) * dx, start[1] + Y * dy) 








if __name__ == "__main__":
    # Error is the error for where the points deviate from calculated
    cap = Capacitor(error = 20)
    cap.draw()
    cap.show()
    
    #Theta math.pi/5 is the angle on the resistors
    res = Resistor(100, math.pi/5, error = 30)
    res.draw()
    res.show()
