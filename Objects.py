import pygame as pg
import math

# constants
g = pg.Vector2(x=0, y=50)
e = 2.72
z = pg.Vector2(x=0, y=0)

radius = 7
separation = 6000
depth = 10000
max_pairs = 9

y_invert = pg.Vector2(x=1, y=-1)
x_invert = pg.Vector2(x=-1, y=1)

buoy_pairs = []
surface = pg.Surface


def draw_buoy_connections():
    for p in buoy_pairs:
        pg.draw.line(surface, (0, 255, 0), p[0].get_position(), p[1].get_position())


class Buoy:
    def __init__(self, position, velocity, buoys):
        self.acceleration = g
        self.pairs = list()

        self.position = position
        self.velocity = velocity
        self.buoys = buoys

    def get_position(self):
        return self.position

    def pair_up(self, buoys):
        if len(self.pairs) < max_pairs:
            for b in buoys:
                if b != self and b not in self.pairs \
                        and (b.get_position() - self.position).length_squared() < 150 * 150\
                        and len(b.pairs) < max_pairs:
                    self.pairs.append(b)
                    b.pairs.append(self)
                    pair = (self, b)
                    if pair not in buoy_pairs or (b, self) not in buoy_pairs:
                        buoy_pairs.append(pair)

    def shove_tug(self):
        force_vec = pg.Vector2(x=0, y=0)
        for p in self.pairs:
            r = self.position.distance_to(p.get_position())
            sigma = math.sqrt(separation)
            # force = 4 * depth * (math.pow(sigma/r, 4) - math.pow(sigma/r, 2))
            if r == 0:
                r += 0.001
                print("damp")
            force = 4 * depth * (4 * math.pow(sigma/r, 3) - 2 * (sigma/r)) * -sigma * math.pow(r, -2)

            # if datum - r < 0:
            #     force *= -1

            relative = (p.get_position() - self.position).normalize()
            force_vec += force * relative


        if force_vec.magnitude() > 5:
            force_vec.scale_to_length(5)
        self.acceleration = force_vec/0.01 - self.velocity * 10 * 0.1 + g

    def update(self, delta):
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
        self.pair_up(self.buoys)

        if self.position.y < 0 + radius:
            self.position = pg.Vector2(x=self.position.x, y=radius)
        if self.position.y > 1080 - radius:
            self.position = pg.Vector2(x=self.position.x, y=1080-radius)
        if self.position.x < 0 + radius:
            self.position = pg.Vector2(x=radius, y=self.position.y)
        if self.position.x > 1920 - radius:
            self.position = pg.Vector2(x=1920-radius, y=self.position.y)

        self.shove_tug()
        pg.draw.circle(surface, (255, 0, 0), [int(self.position.x), int(self.position.y)], radius)
