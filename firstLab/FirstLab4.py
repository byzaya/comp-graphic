from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

xrot = 0.0
yrot = 0.0


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluPerspective(45, (800 / 600), 1, 1000)

    gluLookAt(300, 400, 300,
              10, 100, 150,
              0, 1, 0)

    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glColor3f(1.0, 0.0, 0.0)
    glutWireCube(100)
    glPopMatrix()

    glPushMatrix()

    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(0, 0, 100)
    glColor3f(0.0, 0.0, 1.0)
    glutWireSphere(50, 50, 50)
    glPopMatrix()

    glutSwapBuffers()


def rotating(key, x, y):
    global xrot
    global yrot

    if key == GLUT_KEY_UP:
        xrot -= 2.0
    if key == GLUT_KEY_DOWN:
        xrot += 2.0
    if key == GLUT_KEY_LEFT:
        yrot -= 2.0
    if key == GLUT_KEY_RIGHT:
        yrot += 2.0

    glutPostRedisplay()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Cube and Sphere")
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutSpecialFunc(rotating)

    glutMainLoop()
