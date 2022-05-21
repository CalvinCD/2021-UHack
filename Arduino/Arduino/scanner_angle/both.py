import serial
import time
import schedule
import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

points_list = []

def main():
    pygame.init()
    pygame.display.set_caption('Constellations')
    display = (1280,720)
    scree = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

    sphere = gluNewQuadric() 
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(80, (display[0]/display[1]), 1, 400.0)

    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()

    # init mouse movement and center mouse on screen
    displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
    mouseMove = [0, 0]
    pygame.mouse.set_pos(displayCenter)

    up_down_angle = 0.0
    paused = False
    run = True
    frame_counter = 0

    #Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False
                if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    paused = not paused
                    pygame.mouse.set_pos(displayCenter) 
            if not paused: 
                if event.type == pygame.MOUSEMOTION:
                    mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                pygame.mouse.set_pos(displayCenter) 

        if not paused: 
            # get keys
            keypress = pygame.key.get_pressed()
            #mouseMove = pygame.mouse.get_rel()
        
            # init model view matrix
            glLoadIdentity()

            # apply the look up and down
            up_down_angle += mouseMove[1]*0.1
            glRotatef(up_down_angle, 1.0, 0.0, 0.0)

            # init the view matrix
            glPushMatrix()
            glLoadIdentity()

            # apply the movment 
            if keypress[pygame.K_w]:
                glTranslatef(0,0,0.1)
            if keypress[pygame.K_s]:
                glTranslatef(0,0,-0.1)
            if keypress[pygame.K_d]:
                glTranslatef(-0.1,0,0)
            if keypress[pygame.K_a]:
                glTranslatef(0.1,0,0)
            if keypress[pygame.K_c]:
                glTranslatef(0,-0.1,0)
            if keypress[pygame.K_z]:
                glTranslatef(0,0.1,0)

            # apply the left and right rotation
            glRotatef(mouseMove[0]*0.1, 0.0, 1.0, 0.0)

            # multiply the current matrix by the get the new view matrix and store the final vie matrix 
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            glPushMatrix()

            glColor4f(0.5, 0.5, 0.5, 1)

            #----------------planets---------------------------
            #eaerth
            glTranslatef(0, 0, 0)
            glColor4f(0.1, 0.35, 0.9, 1)
            gluSphere(sphere, 1.0, 32, 16) 
            
            #the moon
            glTranslatef(1.5, 1.5, -.1)
            glColor4f(.8, .8, .8, 1)
            gluSphere(sphere, .3, 32, 16) 

            #mars
            glTranslatef(12, 2, -6)
            glColor4f(0.5, 0.2, 0.2, 1)
            gluSphere(sphere, 0.8, 16, 8) 

            #uranus
            glTranslatef(0, -15, 10)
            glColor4f(0.4, 0.2, 0.75, .6)
            gluSphere(sphere, 1.8, 32, 16)

            #sun
            glTranslatef(-40, 30, -3)
            glColor4f(0.9, 0.7, 0.05, 1)
            gluSphere(sphere, 7, 32, 16)

            #--------------------------------------------------

            glPopMatrix()
            
            if (frame_counter % 3 == 0):
                arduino = serial.Serial('/dev/cu.usbmodem1301', 115200)
                arduino_data = arduino.readline()
                try:
                    decoded_values = arduino_data.decode("utf-8")
                    list_values = decoded_values.split()
                    distance = float(list_values[0]) / 2
                    actual_pitch = math.radians(float(list_values[1]))
                    actual_roll = math.radians(float(list_values[2]))
                    actual_yaw = math.radians(float(list_values[3]))
                    yaw = actual_roll
                    pitch = actual_pitch
                    print("p: {} r: {} y: {}".format(pitch, actual_roll, yaw))
                    x = -1 * distance * math.sin(yaw) * math.cos(pitch)
                    z = -1 * distance * math.sin(pitch)
                    y = distance * math.cos(yaw) * math.cos(pitch)
                    points_list.append((x, y, z))
                    print("{} {} {}".format(x, y, z))
                except:
                    print("decode exception XD")

            frame_counter = frame_counter + 1

            glEnable(GL_POINT_SMOOTH)
            glPointSize(3)
            
            for x in range(len(points_list) - 1):
                glBegin(GL_POINTS)
                glColor3d(1, 1, 1)
                glVertex3d(points_list[x + 1][0], points_list[x + 1][1], points_list[x + 1][2])
                glEnd()

                glBegin(GL_LINES)
                glColor3d(1, .05, 0.50)
                glVertex3d(points_list[x][0], points_list[x][1], points_list[x][2])
                glVertex3d(points_list[x + 1][0], points_list[x + 1][1], points_list[x + 1][2])
                glEnd()
            
            glFlush()

            pygame.display.flip()
            pygame.time.wait(10)


main()
