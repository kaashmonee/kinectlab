from pykinect2 import PyKinectV2, PyKinectRuntime
from pykinect2.PyKinectV2 import *

import _ctypes
import ctypes
import pygame
import sys
import math

class GameRuntime(object):
    def __init__(self):
        pygame.init()
        self.done = False

        # writing a screen
        self.screenWidth = 1920
        self.screenHeight = 1080

        # creates a window for pygame to display a window to the user
        # uses pygame.HWSURFACE to tell pygame to use graphcis harware (GPU)
        # pygame.doublebuffer - memory managemeent to deal with hidef pictures
        # last parameter - image depth
        self.screen = pygame.display.set_mode((self.screenWidth//2, self.screenHeight//2),
                                               pygame.HWSURFACE | pygame.DOUBLEBUF, 32)

        # defining a clock to specify FPS
        self.clock = pygame.time.Clock()

        # getting Kinect data/parameters

        # this line turns on the kinect
        self.kinect = PyKinectRuntime.PyKinectRuntime(
            PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body
            )

        self.bodies = None

        # creatse a surface for the kinect to draw on
        self.frameSurface = pygame.Surface(
            (self.kinect.color_frame_desc.Width, self.kinect.color_frame_desc.Height), 0, 32)

        self.cur_right_hand_height = 0
        self.cur_left_hand_height = 0
        self.prev_right_hand_height = 0
        self.prev_left_hand_height = 0


        self.birdHeight = 0


        self.flap = 0

    
    def drawBird(self):
        pygame.draw.circle(self.frameSurface, (200, 200, 0), int(self.screenWidth/2), int(self.screenHeight - self.birdHeight), 40)


    # rendering from kinect and taking to our frame in our app
    def drawColorFrame(self, frame, targetSurface):
        # creating a lock on the location so it doesn't change until we actually read it. Not sure what 'it' is
        targetSurface.lock()

        # storing address in memory
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        # moving from the kinects subscription endpoint to the application memory (some location that the app can move)
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        # we create 1mb of memory because we're processing images, so we have to get rid of that memory so our ram doesn't
        # shit itself
        del address

        targetSurface.unlock()

        

    # main game loop
    def run(self):
        # ----------- Main Program Loop -------------- #
        while not self.done:
            # 1. handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True


            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.drawColorFrame(frame, self.frameSurface)
                # getting rid of the frame and python's automatic garbage collection will deal with it
                frame = None


            # calculating game physics
            # constant gravity
            self.birdHeight -= 5
            # flap
            self.birdHeight += self.flap * 250
            if self.birdHeight <= 0:
                self.birdHeight = 0
            if self.birdHeight >= self.screenHeight:
                self.birdHeight = self.screenHeight

            
            # calculating the height to width ratio
            heightToWidth = float(self.frameSurface.get_height()) / self.frameSurface.get_width()
            target_height = int(heightToWidth * self.screenWidth)
            surfaceToDraw = pygame.transform.scale(self.frameSurface, (self.screen.get_width(), target_height))


            # not actually sure what this does
            self.screen.blit(surfaceToDraw, (0, 0))
            surfaceToDraw = None
            pygame.display.update()


            # drawing ball
            self.drawBird()


            # setting the application to 60 fps
            self.clock.tick(60)


            # taking the body frame data from the kinect and storing it into a local variable
            # we are basically 'subscribiing' to the data it's sending
            if self.kinect.has_new_body_frame():
                self.bodies = self.kinect.get_last_body_frame()
                # ensuring that there actually are bodies in the frame
                if self.bodies is not None:
                    for i in range(0, self.kinect.max_body_count):
                        # creating a temporary variable to store the body
                        body = self.bodies.bodies[i]

                        # if it's not tracking the body, skip that data point and don't use it
                        if not body.is_tracked:
                            continue

                        joints = body.joints

                        # if the joints are being tracked, print it
                        if joints[PyKinectV2.JointType_HandRight].TrackingState == PyKinectV2.TrackingState_Tracked:
                            self.cur_right_hand_height = joints[PyKinectV2.JointType_HandRight].Position.y

                        if joints[PyKinectV2.JointType_HandLeft].TrackingState == PyKinectV2.TrackingState_Tracked:
                            self.cur_left_hand_height = joints[PyKinectV2.JointType_HandLeft].Position.y

                        # creating the flap value
                        self.flap = (self.prev_right_hand_height - self.cur_right_hand_height) +\
                                    (self.prev_left_hand_height - self.cur_left_hand_height)


                        # avoiding negative flap values
                        self.flap = max(self.flap, 0)


                        # setting the current value to the previous value
                        self.prev_left_hand_height = self.cur_left_hand_height
                        self.prev_right_hand_height = self.cur_right_hand_height

                        print("Flap:", self.flap)

                        # quick notes on coordinate system for kinect: 
                        # +x: along the right side of the bar
                        # +y: up towards the ceiling
                        # +z: away from the kinect into the person
        
        # exits the while loop and quits here
        pygame.quit()

game = GameRuntime()
game.run()