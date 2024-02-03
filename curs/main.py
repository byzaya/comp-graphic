import math
import random

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

emitter_position = (0, -5, 1)


def draw_cone():
    glPushMatrix()
    glColor3f(0.6, 0, 0.2)
    glTranslatef(0, 0, -2)
    slices = 50
    stacks = 50
    radius1 = 0
    radius2 = 3
    h = 7
    gluCylinder(gluNewQuadric(), radius1, radius2, h, slices, stacks)
    glPopMatrix()


# Функция отрисовки плитки
def draw_tiles(v=((4, -10, 4), (-4, -10, 4), (-4, -10, 0), (4, -10, 0))):
    glPushMatrix()
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    for vertex in v:
        glVertex3fv(vertex)
    glEnd()
    glPopMatrix()


# Инициализация Pygame
pygame.init()

# Параметры экрана
width, height = 800, 600

# Параметры эмиттера (плоскость)

# Параметры частиц
particle_count = 1_000
particle_size_range = (5, 10)
particle_speed_range = (1, 5)
particle_lifetime_range = (1, 10)

# Параметры столкновения
collision_cone_angle = 30  # угол конуса столкновения в градусах
collision_cone_distance = 100  # расстояние конуса столкновения


# Основной класс для частиц
class Particle:
    def __init__(self):
        self.a = random.uniform(0, 2 * math.pi)
        self.radius = 0
        self.x = (-self.radius * math.cos(self.a))
        self.y = -5 + (-self.radius * math.sin(self.a))
        self.z = 1 + random.uniform(-1, 2)
        self.position = [self.x, self.y, self.z]
        self.counter = 0
        self.is_handle = False

        self.track_size = random.randint(10, 40)
        self.track = [self.position, [self.position[0], self.position[1], self.position[2]]]

        self.lifetime = random.randint(1, 6)

    def handle_collision(self):
        if self.lifetime < 0:
            return

        cone_center = (0, 0, -2)
        cone_axis = (0, 0, 1)
        particle_position = self.position

        particle_to_cone = [particle_position[i] - cone_center[i] for i in range(3)]

        particle_to_cone = [coord / max(1e-5, math.sqrt(sum(c ** 2 for c in particle_to_cone))) for coord in
                            particle_to_cone]

        angle = math.degrees(math.acos(sum(a * b for a, b in zip(cone_axis, particle_to_cone))))

        if 0 <= angle <= collision_cone_angle and math.sqrt(
                sum((a - b) ** 2 for a, b in zip(cone_center, particle_position))) <= collision_cone_distance:
            self.is_handle = True
            self.track[1] = [self.position[0], self.position[1], self.position[2]]
            self.track_size = random.randint(2, 4)

    def update(self, dtime):
        if self.lifetime < 0:
            return
        self.counter += dtime
        self.handle_collision()  # Обработка столкновения
        if self.is_handle:
            self.radius += 1 / 64
        else:
            self.radius -= 1 / 64
        if self.radius < 3.75:

            self.x = (-self.radius * math.cos(self.a))
            self.y = -5 + (-self.radius * math.sin(self.a))
            self.z = 1 + random.uniform(-1, 2)
            self.position = [self.x, self.y, self.z]

            if self.track_size != 0:
                self.track_size -= 1/8
            else:
                self.track[1][0] += (-self.radius * math.cos(self.a))
                self.track[1][1] += -5 + (-self.radius * math.sin(self.a))
                self.track[1][2] += 1 + random.uniform(-1, 2)


        self.lifetime -= dtime

    def distance_to_emitter(self):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(emitter_position, self.position)))

    def calculate_particle_color(self):
        color = 0.5
        distance = self.distance_to_emitter()
        brightness = 5 * (1.0 - min(distance / 10.0, 1.0)) ** 2
        return color * brightness

    def draw(self):
        if self.lifetime < 0:
            return
        color = self.calculate_particle_color()

        glLineWidth(3)
        glBegin(GL_LINES)
        if self.is_handle:
            glColor4f(0, 1, 0, 0.1)
        else:
            glColor4f(color, color, color, 0.1)
        glVertex3f(self.track[0][0], self.track[0][1], self.track[0][2])
        glVertex3f(self.track[1][0], self.track[1][1], self.track[1][2])
        glEnd()

        glPointSize(3)
        glBegin(GL_POINTS)
        if self.is_handle:
            glColor3f(0, 1, 0)
        else:
            glColor3f(color, color, color)
        x, y, z = self.position
        glVertex3f(x, y, z)
        glEnd()


# Основная функция
def main():
    glutInit()
    display = (width, height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | OPENGLBLIT)
    glShadeModel(GL_FLAT)
    glEnable(GL_COLOR_MATERIAL)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30, (display[0] / display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(50, 0, 0, 0, 0, 0, 0, 0, 1)

    last_time = pygame.time.get_ticks()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    particles = [Particle() for _ in range(particle_count)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    glRotatef(10, 0, 1, 0)
                if event.key == pygame.K_DOWN:
                    glRotatef(-10, 0, 1, 0)
                if event.key == pygame.K_LEFT:
                    glRotatef(10, 0, 0, 1)
                if event.key == pygame.K_RIGHT:
                    glRotatef(-10, 0, 0, 1)

        current_time = pygame.time.get_ticks()
        dtime = (current_time - last_time) / 1000.0
        last_time = current_time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        draw_tiles()
        draw_cone()

        # Обновление и отрисовка частиц
        for particle in particles:
            particle.update(dtime)
            glPushMatrix()
            glTranslatef(*particle.position)  # установка позиции частицы в трехмерном пространстве
            particle.draw()
            glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
