from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

xrot = 0.0
yrot = 0.0

change = 0.0

cone_angle = -180.0
sphere_angle = 45.0


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluPerspective(45, (800 / 600), 1, 1000)

    gluLookAt(300, 400, 300,
              10, 100, 150,
              0, 1, 0)

    glPushMatrix()
    glTranslatef(10, 10, 0)
    if change == 1:
        glRotatef(cone_angle, 0, 0, 1)  # 2 задание
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glColor3f(1.0, 0.0, 0.0)
    glutWireCone(100, 150, 50, 50)
    glPopMatrix()

    glPushMatrix()
    if change == 1:
        glRotatef(sphere_angle, 1, 0, 0)  # 2 задание
    glRotatef(xrot, 1, 0, 0)
    glRotatef(yrot, 0, 1, 0)
    glTranslatef(10, 10, 150)
    glColor3f(0.0, 0.0, 1.0)
    glutWireSphere(50, 50, 50)
    glPopMatrix()

    glutSwapBuffers()


def rotating(key, x, y):
    global xrot
    global yrot
    global change

    if key == GLUT_KEY_UP:
        xrot -= 2.0
    if key == GLUT_KEY_DOWN:
        xrot += 2.0
    if key == GLUT_KEY_LEFT:
        yrot -= 2.0
    if key == GLUT_KEY_RIGHT:
        yrot += 2.0
    if key == GLUT_KEY_F1:
        change = 1
    if key == GLUT_KEY_F2:
        change = 0

    glutPostRedisplay()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Cone and Sphere")
    glEnable(GL_DEPTH_TEST)

    glutDisplayFunc(display)
    glutSpecialFunc(rotating)

    glutMainLoop()
