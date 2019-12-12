from Box2D import (b2EdgeShape, b2FixtureDef, b2PolygonShape)
def track(world):
    ground = world.CreateStaticBody(
        shapes=b2EdgeShape(vertices=[(-20, 0), (20, 0)])
    )
    x, y1, dx = 20, 0, 5
    vertices = [0, 0, 0, 1, 2.5, 1.5, 0, 0, 2, 5, 9, 7, 5, 0, -3, -2, 0, 3, 6, -10, 0, 0, 0]
    for y2 in vertices:  # iterate through vertices twice
        ground.CreateEdgeFixture(
            vertices=[(x, y1), (x + dx, y2)],
            density=0,
            friction=100,
        )
        y1 = y2
        x += dx

    return ground