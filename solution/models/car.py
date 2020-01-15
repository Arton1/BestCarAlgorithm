import math
from solution.evolutional_algorithm.genotype import Genotype

from Box2D import (b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                   b2_pi)


def create_cars(world, population, offset=(10, 5)):
    springs = []
    for genotype in population._candidates:
        springs.append(create_car(world, genotype, offset))
    return springs


def create_car(world, genotype, offset):
    x_offset, y_offset = offset
    points = []
    wheels = []
    springs = []
    wheel_radius, wheel_speed, wheel_friction, engine_torque = genotype._wheel_properties

    y_offset = 0
    for x, y in genotype._vectors:
        y_offset = max(y_offset, abs(math.sin(x)*y))
        points.append((math.cos(x) * y, math.sin(x) * y))

    y_offset += max(wheel_radius[0], wheel_radius[1]) + 0.5
    chassis = world.CreateDynamicBody(position=(x_offset, y_offset), userData="car_chassis")
    for index in range(Genotype.AMOUNT_OF_VERTICES):
        chassis.CreatePolygonFixture(vertices=[(0, 0), points[index % Genotype.AMOUNT_OF_VERTICES], points[(index + 1) % Genotype.AMOUNT_OF_VERTICES]], groupIndex=-1,
                                     density=50, restitution = 0
                                    )

    # x_offset, y_offset = offset
    for i in range(0, 2):
        x, y = points[genotype._wheel_vertices[i]]
        wheel = world.CreateDynamicBody(
            position=(x_offset + x, y_offset - wheel_radius[i] - y),
            fixtures=b2FixtureDef(
                shape=b2CircleShape(radius=wheel_radius[i]),
                density=1,
                groupIndex=-1,
                friction=wheel_friction[i],
                restitution = 0
            ),
            userData="car_wheel"
        )
        spring = world.CreateWheelJoint(
            bodyA=chassis,
            bodyB=wheel,
            localAnchorA=(x, y),
            localAnchorB=(0, 0),
            axis=(1, 0),
            motorSpeed=-wheel_speed[i],
            maxMotorTorque=engine_torque[i],
            enableMotor=True,
            frequencyHz=60,
            dampingRatio=0,
        )
        wheels.append(wheel)
        springs.append(spring)
    return springs


def nice_car(world, wheel_radius=1.2, density=1.0, offset=(0, 0),
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
            groupIndex=-1,
            friction=1000,
        )
    )
    spring = world.CreateWheelJoint(
        bodyA=chassis,
        bodyB=wheel,
        localAnchorA=(1, -3),
        localAnchorB=(0, 0),
        axis=(1, 0),
        motorSpeed=-10,
        maxMotorTorque=200,
        enableMotor=False,
        frequencyHz=60,
        dampingRatio=1.0,
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
        motorSpeed=-10,
        axis=(1, 0),
        maxMotorTorque=200,
        enableMotor=False,
        frequencyHz=60,
        dampingRatio=1.0
    )
    wheels.append(wheel)
    springs.append(spring)
    return springs
