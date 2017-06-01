# Mycroft Skill to take a Picture with the Raspberry Pi Camera by Nold 2017

# pip install picamera
import pygame.camera
import pygame.image
import datetime

from time import sleep
from os.path import dirname, join, abspath

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import play_wav

import subprocess
import psutil

__author__ = 'nold'

logger = getLogger(__name__)


class WebcamPictureSkill(MycroftSkill):
    picture_path = '/home/hersche/Bilder/Mycroftpics'
    enable_timer = 'no'
    resolution = '720p'

    def __init__(self):
        super(WebcamPictureSkill, self).__init__(name="WebcamPictureSkill")

    def initialize(self):


        intent_fromCam = IntentBuilder("PictureFromCameraIntent").require("PictureFromCameraKeyword").require("nrOfCamera").build()
        self.register_intent(intent_fromCam, self.handle_intent_fromCam)
        
        intent = IntentBuilder("PictureIntent").require("PictureKeyword").build()
        self.register_intent(intent, self.handle_intent)

        if self.config:
            self.picture_path = self.config.get('picture_path', '/tmp')
            self.enable_timer = self.config.get('enable_timer', 'yes')
            self.resolution = self.config.get('resolution', '720p')

        sound_path = dirname(abspath(__file__)) + '/res/wav/'
        self.beep_sound = sound_path + 'beep.wav'
        self.shutter_sound = sound_path + 'shutter.wav'

        pygame.camera.init()
        

    def handle_intent_fromCam(self, message):
        today = datetime.datetime.today()
        try:
            cameraNr = int(message.data.get("nrOfCamera"))
            if(cameraNr>0):
                cameraNr=cameraNr-1
            if len(pygame.camera.list_cameras())>cameraNr:
                self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[cameraNr])
                self.cam.start()
                self.speak("cheese 66")
                sleep(1)
                if 'yes' in self.enable_timer:
                    play_wav(self.beep_sound)
                    sleep(0.5)
                    play_wav(self.beep_sound)
                    sleep(0.5)
                    play_wav(self.beep_sound)
                    sleep(0.5)
                #play_wav(self.shutter_sound)
                self.speak("took picture from camera "+(cameraNr+1))
                try:
                    img = self.cam.get_image()
                    pygame.image.save(img,str(self.picture_path) + '/image-' +
                                        today.strftime('%Y-%m-%d_%H%M%S') + '.jpg')
                    self.cam.stop()
                except:
                    self.cam.stop()
                    self.speak("Sorry. My camera is currently broken!")
            else:
                self.speak("Sorry, no webcams found.")
                
        except:
            self.speak("Sorry. A fail happend ")



    def handle_intent(self, message):
        notRunning=True
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "motion":
                if notRunning:
                    subprocess.call(['killall','motion'])
                    notRunning=False
        today = datetime.datetime.today()
        try:
            if len(pygame.camera.list_cameras())>0:
                self.cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
                self.cam.start()
                self.speak("cheese")
                sleep(1)
                if 'yes' in self.enable_timer:
                    play_wav(self.beep_sound)
                    sleep(0.5)
                    play_wav(self.beep_sound)
                    sleep(0.5)
                    play_wav(self.beep_sound)
                    sleep(0.5)
                play_wav(self.shutter_sound)
                try:
                    img = self.cam.get_image()
                    pygame.image.save(img,str(self.picture_path) + '/image-' +
                                        today.strftime('%Y-%m-%d_%H%M%S') + '.jpg')
                    self.cam.stop()
                    
                    if notRunning==False:
                        subprocess.call(['motion'])
                except:
                    self.cam.stop()
                    self.speak("Sorry. My camera is currently broken!")
            else:
                self.speak("Sorry, no webcams found.")
                
        except:
            self.speak("Sorry. My camera is currently broken!")

    def stop(self):
        pass

def create_skill():
    return WebcamPictureSkill()


