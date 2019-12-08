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
from math import sqrt

from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)



def new_car(world, offset, wheel_radius, wheel_separation, density=1.0,
               wheel_friction=0.9, wheel_axis=(0.0, 1.0), wheel_torques=[200.0, 10.0],
               wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    x_offset, y_offset = offset

    chassis = world.CreateDynamicBody(position = (x_offset, y_offset))
    chassis.CreatePolygonFixture(vertices=[(0, 0), (0, 2), (1, 3)], groupIndex=-1, density=1, friction=0.3,
                                restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (1, 3), (3, 3)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (3, 3), (2, 1)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (2, 1), (4, 0)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (4, 0), (1, -1)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (1, -1), (1, -3)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (1, -3), (-1, -1)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (-1, -1), (-3, 0)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (-3, 0), (-2, 2)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)
    chassis.CreatePolygonFixture(vertices=[(0, 0), (-2, 2), (0, 2)], groupIndex=-1, density=1, friction=0.3,
                                 restitution=0.3)

    wheels, springs = [],[]

    wheel = world.CreateDynamicBody(
        position=(x_offset + 1, y_offset - wheel_radius -3),
        fixtures=b2FixtureDef(
            shape=b2CircleShape(radius=wheel_radius),
            density=density,
            groupIndex = -1
        )
    )

    spring = world.CreateWheelJoint(
        bodyA=chassis,
        bodyB=wheel,
        localAnchorA = (1,-3),
        localAnchorB = (0,0),
        axis=(1,0),
        motorSpeed=-10.0,
        maxMotorTorque=200,
        enableMotor=True,
        frequencyHz=hz,
        dampingRatio=1000,
    )

    wheels.append(wheel)
    springs.append(spring)

    wheel = world.CreateDynamicBody(
        position=(x_offset -3 , y_offset - wheel_radius - 0),
        fixtures=b2FixtureDef(
            shape=b2CircleShape(radius=wheel_radius),
            density=density,
            groupIndex = -1
        )
    )

    spring = world.CreateWheelJoint(
        bodyA=chassis,
        bodyB=wheel,
        localAnchorA=(-3, 0),
        localAnchorB=(0, 0),
        axis=(1, 0),
        motorSpeed=-10.0,
        maxMotorTorque=200,
        enableMotor=True,
        frequencyHz=hz,
        dampingRatio=1000
    )

    wheels.append(wheel)
    springs.append(spring)
    return chassis, wheels, springs

class Car (Framework):
    name = "Car"
    description = "Keys: left = a, brake = s, right = d, hz down = q, hz up = e"
    hz = 4
    zeta = 0.7
    speed = 50
    bridgePlanks = 20

    def __init__(self):
        super(Car, self).__init__()

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

        car, wheels, springs = new_car(self.world, offset=(
            4.0, 20.0), wheel_radius=1.3, wheel_separation=2.0)

        car1, wheels1, springs1 = new_car(self.world, offset=(
            4.0, 30.0), wheel_radius=1.3, wheel_separation=2.0)
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
        super(Car, self).Step(settings)
        self.viewCenter = (self.car.position.x, 20)
        self.Print("frequency = %g hz, damping ratio = %g" %
                   (self.hz, self.zeta))

if __name__ == "__main__":
    main(Car)