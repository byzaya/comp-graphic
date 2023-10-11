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

    gluLookAt(10, 10, 10,
              0, 0, 0,
              0, 1, 0)

    # ДОДЕКАЭДР - текстура
    glPushMatrix()
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(-1.5, -1.5, -1.5)
    glutSolidDodecahedron()
    glPopMatrix()

    # ЦИЛИНДР - текстура
    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(-0.1, -0.50, -0.15)
    cyl = gluNewQuadric()
    gluQuadricTexture(cyl, GLU_LINE)
    gluCylinder(cyl, 3, 3, 6, 50, 50)
    glBegin(GL_POLYGON)
    for i in range(50):
        angle = 2 * 3.14159265 * i / 50
        x = 3 * numpy.sin(angle)
        y = 3 * numpy.cos(angle)
        glTexCoord2f(x / 6 + 0.5, y / 6 + 0.5)
        glVertex(x, y, 0)
    glEnd()
    glTranslatef(0, 0, 6)
    glBegin(GL_POLYGON)
    for i in range(50):
        angle = 2 * 3.14159265 * i / 50
        x = 3 * numpy.sin(angle)
        y = 3 * numpy.cos(angle)
        glTexCoord2f(x / 6 + 0.5, y / 6 + 0.5)
        glVertex(x, y, 0)
    glEnd()
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
        light_pos_y += 0.1
    if key == GLUT_KEY_F2:
        light_pos_y -= 0.1

    if key == GLUT_KEY_F3:
        diffuse_value += 0.1
    if key == GLUT_KEY_F4:
        diffuse_value -= 0.1

    if key == GLUT_KEY_F5:
        intensity += 0.1
    if key == GLUT_KEY_F6:
        intensity -= 0.1

    glutPostRedisplay()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Cylinder and Dodecahedron")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(display)
    glutSpecialFunc(rotating)
    texture_id = read_texture('img.png')
    initLight()
    glutMainLoop()
