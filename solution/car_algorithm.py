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

from solution.models.car import *
from solution.models.track import *
from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape)
from .framework import (Framework, Keys, main)
import time

CAR_NUM = 10


# Creating first population and the track
class World(Framework):
    def __init__(self):
        super(World, self).__init__()
        ground = track(self.world)

        self.genes = []
        for i in range(0, CAR_NUM):
            self.genes.append(Genotype())

        for gene in self.genes:
            car_from_geneotype(self.world, Genotype(), offset=(10, 10))

        self.time_start = time.time()

    # evaluates every genotype and deletes car objects
    def stop_simulation(self):
        j = 0
        for i in range(2, 3 * CAR_NUM + 2, 3):
            self.genes[j].evaluation = self.world.bodies[i].position[0]
            j += 1

        print(self.genes)
        while len(self.world.bodies) > 2:
            self.world.DestroyBody(self.world.bodies[2])

    def create_generation(self):
        for i in range(0, CAR_NUM):
            car_from_geneotype(self.world, Genotype(), offset=(10, 10))
        self.time_start = time.time()

    def Keyboard(self, key):
        if key == Keys.K_t:
            self.stop_simulation()
        if key == Keys.K_c:
            self.create_generation()

    def Step(self, settings):
        super(World, self).Step(settings)

        x = 10
        for i in range(2, 3 * CAR_NUM + 2, 3):
            try:
                x = max(x, self.world.bodies[i].position[0])
            except IndexError:
                x = 10

        self.viewCenter = (x, 20)
        self.Print("frequency = %g hz, time = %g" %
                   (4 , time.time() - self.time_start))

    # TODO: genetic algorithm here


if __name__ == "__main__":
    main(World)
