import pygame as pg
import time

import Objects as Obj

pg.init()
pg.display.set_caption("Fluid")
screen = pg.display.set_mode((1920, 1080))

running = True
Obj.surface = screen
buoys = list()


def circle(x, y):
    pg.draw.circle(screen, (255, 255, 255), (x, y), 50)


for x in range(25):
    for y in range(10):
        buoys.append(Obj.Buoy(pg.Vector2(x=100 + 70 * x, y=300 + 70 * y), pg.Vector2(x=0, y=0), buoys))

previous = 0
delay = 1/200
while running:
    delta = time.perf_counter() - previous
    previous = time.perf_counter()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))
    for b in buoys:
        b.update(delta)
    # Obj.draw_buoy_connections()

    pg.display.flip()
    time.sleep(delay)
