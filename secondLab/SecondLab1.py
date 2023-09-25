import PIL
import numpy
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

xrot = 0.0
yrot = 0.0

light_pos_y = 0.0
diffuse_value = 0.0
intensity = 1.0

# прозрачный объект (параметр 0.5 и выше) - ШАР
# отполированный объект (макс значение) - КОНУС
# матовый объект - КУБ
# текстурированный объект - ЦИЛИНДР

def initLight():
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    setLightParams()

def read_texture(filename):
    img = PIL.Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.uint8)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture_id

def setLightParams():
    glLightfv(GL_LIGHT0, GL_POSITION, [500, light_pos_y, 300, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [-1 * diffuse_value, diffuse_value, 1, 1])
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, intensity)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    setLightParams()
    glLoadIdentity()

    gluPerspective(45, (800 / 600), 1, 1000)

    gluLookAt(300, 300, 300,
              100, 100, 100,
              0, 1, 0)

    # КОНУС - отполированный
    glPushMatrix()
    glTranslatef(10, 10, 0)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.5, 0.5, 0.5, 0.5])
    glMaterialfv(GL_FRONT, GL_SHININESS, 128)
    glColor3f(0, 0, 1)
    glutSolidCone(100, 150, 50, 50)
    glPopMatrix()

    # ШАР - полупрозрачный
    glPushMatrix()
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(150, 150, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glColor4f(1, 0, 1, 0.2)
    glutSolidSphere(50, 50, 50)
    glDisable(GL_BLEND)
    glPopMatrix()

    # КУБ - матовый
    glPushMatrix()
    glTranslatef(-400, -200, 0)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 0])
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)
    glColor3f(1, 1, 1)
    glutSolidCube(150)
    glPopMatrix()

    # ЦИЛИНДР - текстура
    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(-100, 100, -150)
    cyl = gluNewQuadric()
    gluQuadricTexture(cyl, GLU_LINE)
    gluCylinder(cyl, 50, 50, 120, 50, 50)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glutSwapBuffers()


def rotating(key, x, y):
    global xrot
    global yrot
    global light_pos_y
    global diffuse_value
    global intensity


    if key == GLUT_KEY_UP:
        xrot -= 2.0
    if key == GLUT_KEY_DOWN:
        xrot += 2.0
    if key == GLUT_KEY_LEFT:
        yrot -= 2.0
    if key == GLUT_KEY_RIGHT:
        yrot += 2.0
    if key == GLUT_KEY_F1:
        light_pos_y += 2
    if key == GLUT_KEY_F2:
        light_pos_y -= 2

    if key == GLUT_KEY_F3:
        diffuse_value += 2
    if key == GLUT_KEY_F4:
        diffuse_value -= 2

    if key == GLUT_KEY_F5:
        intensity += 2
    if key == GLUT_KEY_F6:
        intensity -= 2

    glutPostRedisplay()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Cone Sphere Cube Cylinder")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutSpecialFunc(rotating)
    texture_id = read_texture('img.png')
    initLight()
    glutMainLoop()
