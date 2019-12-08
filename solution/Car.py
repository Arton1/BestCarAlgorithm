from math import sqrt

from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)

from .framework import (Framework, Keys, main)

def new_car(world, wheel_radius = 1.2,  density=1.0, offset = (0,0),
            wheel_friction=0.9, wheel_axis=(0.0, 1.0), wheel_torques=[200.0, 10.0],
            wheel_drives=[True, False], hz=4.0, zeta=0.7, **kwargs):
    x_offset, y_offset = offset

    chassis = world.CreateDynamicBody(position=(x_offset, y_offset))
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

    wheels, springs = [], []

    wheel = world.CreateDynamicBody(
        position=(x_offset + 1, y_offset - wheel_radius - 3),
        fixtures=b2FixtureDef(
            shape=b2CircleShape(radius=wheel_radius),
            density=density,
            groupIndex=-1
        )
    )

    spring = world.CreateWheelJoint(
        bodyA=chassis,
        bodyB=wheel,
        localAnchorA=(1, -3),
        localAnchorB=(0, 0),
        axis=(1, 0),
        motorSpeed=-10.0,
        maxMotorTorque=200,
        enableMotor=True,
        frequencyHz=hz,
        dampingRatio=1000,
    )

    wheels.append(wheel)
    springs.append(spring)

    wheel = world.CreateDynamicBody(
        position=(x_offset - 3, y_offset - wheel_radius - 0),
        fixtures=b2FixtureDef(
            shape=b2CircleShape(radius=wheel_radius),
            density=density,
            groupIndex=-1
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
