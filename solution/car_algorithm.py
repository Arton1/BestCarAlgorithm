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
from solution.evolutional_algorithm.population import Population
import time

# Creating first population and the track
class World(Framework):
    def __init__(self):
        super(World, self).__init__()
        create_track(self.world)
        self._population = Population()
        create_cars(self.world, self._population)
        self.time_start = time.time()

    # evaluates every genotype and deletes car objects
    def stop_simulation(self):
        while len(self.world.bodies) > 2:
            self.world.DestroyBody(self.world.bodies[2])

    def Keyboard(self, key):
        if key == Keys.K_t:
            self.stop_simulation()
        if key == Keys.K_c:
            self._population.set_fitness(self.world)
            self._population.print_information()
            self.stop_simulation()
            self._population.evolve()
            super(World, self).__init__()
            create_track(self.world)
            create_cars(self.world, self._population)
            self.time_start = time.time()

    def Step(self, settings):
        super(World, self).Step(settings)
        x = 10
        for i in range(2, 3 * len(self._population._candidates) + 2, 3):
            try:
                x = max(x, self.world.bodies[i].position[0])
            except IndexError:
                x = 10
        self.viewCenter = (x, 20)
        self.Print("frequency = %g hz, time = %g" %
                   (4, time.time() - self.time_start))


if __name__ == "__main__":
    main(World)
