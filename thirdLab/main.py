import math
import time

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


#  texture function
def read_texture(filename):
    img = Image.open(filename)
    img_data = np.array(list(img.getdata()), np.int64)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


def current_milli_time():
    return round(time.time() * 1000)


def init():
    global xrot, yrot, zrot, move, special_value, globalScale, xdebug, ydebug, zdebug
    global radius, height, slices, stacks, angle

    xrot = 0
    yrot = 0
    zrot = 0

    xdebug = 0
    ydebug = 0
    zdebug = 0

    special_value = 0

    move = 0

    globalScale = 0.6

    radius = 8
    height = 5
    slices = 64
    stacks = 64
    angle = 90


def keyboard(key, *args):
    global xrot, yrot, zrot, move, globalScale, xdebug, ydebug, zdebug, special_value
    if key == b'q':
        xdebug += 0.5
    if key == b'a':
        xdebug -= 0.5
    if key == b'w':
        ydebug += 0.5
    if key == b's':
        ydebug -= 0.5
    if key == b'e':
        zdebug += 0.5
    if key == b'd':
        zdebug -= 0.5
    if key == b'+':
        globalScale += 0.1
    if key == b'-':
        globalScale -= 0.1
    print(f"cords:{xrot}, {yrot}, {zrot}")
    print(f"scale:{globalScale}")
    print(f"move:{move}")
    print(f"debug:{xdebug}, {ydebug}, {zdebug}")
    print(f"c:{special_value}")
    glutPostRedisplay()

def special_keys(key, *args):
    global xrot, yrot, zrot, move, globalScale, xdebug, ydebug, zdebug, special_value
    if key == GLUT_KEY_UP:
        xrot += 1
    if key == GLUT_KEY_DOWN:
        xrot -= 1
    if key == GLUT_KEY_LEFT:
        yrot += 1
    if key == GLUT_KEY_RIGHT:
        yrot -= 1
    if key == GLUT_KEY_F1:
        zrot += 0.1
    if key == GLUT_KEY_F2:
        zrot -= 0.1
    if key == GLUT_KEY_F3:
        special_value += 0.01
    if key == GLUT_KEY_F4:
        special_value -= 0.01
    if key == GLUT_KEY_F5:
        move = 0
        prev_frame_time = current_milli_time()
        while move < 500:
            frame_time = current_milli_time()
            if move <= 100:
                if frame_time - prev_frame_time < 15:
                    continue
            if 100 < move <= 200:
                if frame_time - prev_frame_time < 15:
                    continue
            if 200 < move <= 300:
                if frame_time - prev_frame_time < 15:
                    continue
            if 300 < move <= 400:
                if frame_time - prev_frame_time < 15:
                    continue
            if 400 < move <= 500:
                if frame_time - prev_frame_time < 15:
                    continue
            if 500 < move <= 600:
                if frame_time - prev_frame_time < 15:
                    continue
            if 600 < move <= 700:
                if frame_time - prev_frame_time < 15:
                    continue
            if 700 < move <= 800:
                if frame_time - prev_frame_time < 15:
                    continue
            move += 1
            prev_frame_time = current_milli_time()
            display_scene()
        # move = 0
    print(f"cords:{xrot}, {yrot}, {zrot}")
    print(f"scale:{globalScale}")
    print(f"move:{move}")
    print(f"debug:{xdebug}, {ydebug}, {zdebug}")
    print(f"c:{special_value}")
    glutPostRedisplay()


def draw_floor(x_cord, y_cord, z_cord, x_roll_angle, y_roll_angle, z_roll_angle, scale):
    glPushMatrix()
    glTranslatef(x_cord, y_cord, z_cord)
    glRotatef(x_roll_angle, 1, 0, 0)
    glRotatef(y_roll_angle, 0, 1, 0)
    glRotatef(z_roll_angle, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    floor_texture = read_texture('2.jpg')
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glScale(scale, scale, scale)
    glBegin(GL_QUADS)
    glTexCoord(1, 1)
    glVertex3f(1, 0, 1)
    glTexCoord(1, 0)
    glVertex3f(1, 0, -1)
    glTexCoord(0, 0)
    glVertex3f(-1, 0, -1)
    glTexCoord(0, 1)
    glVertex3f(-1, 0, 1)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glRotatef(x_roll_angle, -1, 0, 0)
    glRotatef(y_roll_angle, 0, -1, 0)
    glRotatef(z_roll_angle, 0, 0, -1)
    glTranslatef(-x_cord, -y_cord, -z_cord)
    glPopMatrix()


def draw_cylinder(x_cord, y_cord, z_cord, x_roll_angle, y_roll_angle, z_roll_angle, height, slices, stacks):
    glPushMatrix()
    glTranslatef(x_cord, y_cord, z_cord)
    glRotatef(x_roll_angle, 1, 0, 0)
    glRotatef(y_roll_angle, 0, 1, 0)
    glRotatef(z_roll_angle, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    cylinder_texture = read_texture('1.jpg')
    glBindTexture(GL_TEXTURE_2D, cylinder_texture)
    glTranslatef(0, height, 0)
    glRotatef(angle, 1, 0, 0)
    cylinder = gluNewQuadric()
    gluCylinder(cylinder, radius, radius, height, slices, stacks)  # построение цилиндра без дисков
    glRotatef(180, 1, 0, 0)  # поворот на 180 по х
    gluDisk(cylinder, 0.0, radius, slices, 1)  # построение первого диска
    glRotatef(180, 1, 0, 0)  # поворот на 180 по х
    glTranslatef(0.0, 0.0, height)  # смещение на высоту по z
    gluDisk(cylinder, 0.0, radius, slices, 1)  # построение второго диска
    glTranslatef(0.0, 0.0, -height)  # смещение на высоту по z
    glDisable(GL_TEXTURE_2D)
    glRotatef(x_roll_angle, -1, 0, 0)
    glRotatef(y_roll_angle, 0, -1, 0)
    glRotatef(z_roll_angle, 0, 0, -1)
    glTranslatef(-x_cord, -y_cord, -z_cord)
    glPopMatrix()


def draw_dodecahedron(x_cord, y_cord, z_cord, x_roll_angle, y_roll_angle, z_roll_angle):
    glPushMatrix()
    yellow = [1.0, 1.0, 0.0, 1.0]
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, yellow)
    glTranslatef(x_cord, y_cord, z_cord)
    glRotatef(x_roll_angle, 1, 0, 0)
    glRotatef(y_roll_angle, 0, 1, 0)
    glRotatef(z_roll_angle, 0, 0, 1)
    glutSolidDodecahedron()
    glRotatef(x_roll_angle, -1, 0, 0)
    glRotatef(y_roll_angle, 0, -1, 0)
    glRotatef(z_roll_angle, 0, 0, -1)
    glTranslatef(-x_cord, -y_cord, -z_cord)
    glPopMatrix()




def display_scene():
    global xrot, yrot, zrot, move, globalScale, xdebug, ydebug, zdebug, special_value, radius, height, slices, stacks, angle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glRotatef(zrot, 0, 0, 1)
    glScalef(globalScale, globalScale, globalScale)

    draw_floor(0, 0, 0, 0, 0, 0, 10)
    draw_cylinder(0, 0, 0, 0, 0, 0, height, slices, stacks)

    # draw_dodecahedron(0.0, 5 + math.sqrt(2), 0.0, 0 + xdebug, 0 + ydebug, 30.0 + zdebug)
    # draw_dodecahedron(0.0, 5 + math.sqrt(2), 1.4, 64.5 + xdebug, -19.5 + ydebug, 35.0 + zdebug)
    # draw_dodecahedron(1.4, 5 + math.sqrt(2), 1.4, 65.5 + xdebug, -87.5 + ydebug, 40.0 + zdebug)
    # draw_dodecahedron(1.4, 5 + math.sqrt(2), 2.8, 120.0 + xdebug, -124.5 + ydebug, 32.0 + zdebug)
    # draw_dodecahedron(1.4, 5 + math.sqrt(2), 2.8, 114.5 + xdebug, -54.5 + ydebug, 24.0 + zdebug)

    # вперед
    if move <= 100:
        draw_dodecahedron(0.0 + move * (0.0 / 100),
                          5 + math.sqrt(2) + move * (-0.05 / 100),
                          0 + move * (1.4 / 100),
                          0 + move * (64.5 / 100),
                          0 + move * (-19.5 / 100),
                          30 + move * (5.0 / 100))
    # направо
    if 100 < move <= 200:
        draw_dodecahedron(0.0 + (move - 100) * (1.4 / 100),
                          5 + math.sqrt(2) - 0.05 + (move - 100) * (0.05 / 100),
                          1.4 + (move - 100) * (0.0 / 100),
                          64.5 + (move - 100) * (1.0 / 100),
                          -19.5 + (move - 100) * (-68.0 / 100),
                          35.0 + (move - 100) * (5.0 / 100))
    # вперед
    if 200 < move <= 300:
        draw_dodecahedron(1.4 + (move - 200) * (0 / 100),
                          5 + math.sqrt(2) + (move - 200) * (-0.05 / 100),
                          1.4 + (move - 200) * (1.4 / 100),
                          65.5 + (move - 200) * (54.5 / 100),
                          -87.5 + (move - 200) * (-37.0 / 100),
                          40.0 + (move - 200) * (-8.0 / 100))
    # налево
    if 300 < move <= 400:
        draw_dodecahedron(1.4 + (move - 300) * (-1.4 / 100),
                          5 + math.sqrt(2) - 0.05 + (move - 300) * (0.05 / 100),
                          2.8 + (move - 300) * (0 / 100),
                          120 + (move - 300) * (-5.5 / 100),
                          -124.5 + (move - 300) * (70.0 / 100),
                          32.0 + (move - 300) * (-8.0 / 100))
    # назад
    if 400 < move <= 500:
        draw_dodecahedron(0 + (move - 400) * (0 / 100),
                          5 + math.sqrt(2) + (move - 400) * (-0.05 / 100),
                          2.8 + (move - 400) * (-1.4 / 100),
                          114.5 + (move - 400) * (2.0 / 100),
                          -54.5 + (move - 400) * (-30.0 / 100),
                          24.0 + (move - 400) * (54.5 / 100))

    glPopMatrix()
    glutSwapBuffers()


def init_glut(args):
    glutInit(args)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(350, 200)
    glutCreateWindow('OpenGL Lab 3')


def set_rendering_options():
    glClearColor(1, 1, 1, 1)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def configure_lighting():
    lightZeroPosition = [10, 4, 10, 1]
    lightZeroColor = [8, 1, 8, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, .1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, .05)
    glEnable(GL_LIGHT0)


def set_display_callbacks():
    glutDisplayFunc(display_scene)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)


def configure_projection():
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 50)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(20, 20, 20, 0, 0, 0, 0, 1, 0)
    glPushMatrix()


def main():
    init_glut(sys.argv)
    init()
    set_rendering_options()
    configure_lighting()
    set_display_callbacks()
    configure_projection()
    glutMainLoop()


if __name__ == '__main__':
    main()
