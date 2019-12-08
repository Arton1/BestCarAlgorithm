#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
# Python version by Ken Lauer / sirkne at gmail dot com
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
# 1. The origin of this software must not be misrepresented; you must not
# claim that you wrote the original software. If you use this software
# in a product, an acknowledgment in the product documentation would be
# appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
# misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

from .framework import (Framework, Keys, main)
from .bridge import create_bridge
from solution.Car import *

from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)




class World (Framework):
    name = "Car"
    description = "Keys: left = a, brake = s, right = d, hz down = q, hz up = e"
    hz = 4
    zeta = 0.7
    speed = 50
    bridgePlanks = 20

    def __init__(self):
        super(World, self).__init__()

        # The ground -- create some terrain
        ground = self.world.CreateStaticBody(
            shapes=b2EdgeShape(vertices=[(-20, 0), (20, 0)])
        )

        x, y1, dx = 20, 0, 5
        vertices = [0.25, 1, 4, 0, 0, -1, -2, -2, -1.25, 0]
        for y2 in vertices * 2:  # iterate through vertices twice
            ground.CreateEdgeFixture(
                vertices=[(x, y1), (x + dx, y2)],
                density=0,
                friction=0.6,
            )
            y1 = y2
            x += dx

        x_offsets = [0, 80, 40, 20, 40]
        x_lengths = [40, 40, 10, 40, 0]
        y2s = [0, 0, 5, 0, 20]

        for x_offset, x_length, y2 in zip(x_offsets, x_lengths, y2s):
            x += x_offset
            ground.CreateEdgeFixture(
                vertices=[(x, 0), (x + x_length, y2)],
                density=0,
                friction=0.6,
            )

        # Teeter
        body = self.world.CreateDynamicBody(
            position=(140, 0.90),
            fixtures=b2FixtureDef(
                shape=b2PolygonShape(box=(10, 0.25)),
                density=1.0,
            )
        )

        self.world.CreateRevoluteJoint(
            bodyA=ground,
            bodyB=body,
            anchor=body.position,
            lowerAngle=-8.0 * b2_pi / 180.0,
            upperAngle=8.0 * b2_pi / 180.0,
            enableLimit=True,
        )

        # Bridge
        create_bridge(self.world, ground, (2.0, 0.25),
                      (161.0, -0.125), self.bridgePlanks)

        # Boxes
        for y_pos in [0.5, 1.5, 2.5, 3.5, 4.5]:
            self.world.CreateDynamicBody(
                position=(230, y_pos),
                fixtures=b2FixtureDef(
                    shape=b2PolygonShape(box=(0.5, 0.5)),
                    density=0.5,
                )
            )

        car, wheels, springs = new_car(self.world, offset= (10, 40))

        car1, wheels1, springs1 =new_car(self.world,offset=(10,40))
        self.car = car
        self.wheels = wheels
        self.springs = springs

        self.car1 = car1
        self.wheels1 = wheels1
        self.springs1 = springs1

    def Keyboard(self, key):
        if key == Keys.K_a:
            self.springs[0].motorSpeed = self.speed
        elif key == Keys.K_s:
            self.springs[0].motorSpeed = 0
        elif key == Keys.K_d:
            self.springs[0].motorSpeed = -self.speed
        elif key in (Keys.K_q, Keys.K_e):
            if key == Keys.K_q:
                self.hz = max(0, self.hz - 1.0)
            else:
                self.hz += 1.0

            for spring in self.springs:
                spring.springFrequencyHz = self.hz

    def Step(self, settings):
        super(World, self).Step(settings)
        self.viewCenter = (self.car1.position.x, 20)
        self.Print("frequency = %g hz, damping ratio = %g" %
                   (self.hz, self.zeta))

if __name__ == "__main__":
    main(World)