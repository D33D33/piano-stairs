import pygame
import RPi.GPIO as GPIO

import serial
import time

onpi = True
numpins = 8
playguit = False

pygame.mixer.pre_init(channels=8, buffer=1024)
pygame.mixer.init()

class PianoStairs():

    def __init__(self):
        self.previnputs = [False] * numpins

        letters = ["c1", "d", "e", "f", "g", "a", "b", "c"][:numpins]
        self.piano_notes = [pygame.mixer.Sound("piano/"+letter+".wav") for letter in letters]
        guit_let = ["e", "f", "a", "d", "g", "b", "e2", "f2"][:numpins]
        self.guitar_notes = [pygame.mixer.Sound("guitar/"+letter+".wav") for letter in guit_let]

        GPIO.setmode(GPIO.BCM)
        self.pins = [7, 8, 25, 24, 23, 18, 11, 9][:numpins]
        [GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP) for p in self.pins]

    def play(self, i):
        if playguit:
            self.guitar_notes[i].play()
        else:

            self.piano_notes[i].play()

    def run(self):
        while True:
            time.sleep(0.12)
            if onpi:
                l = []
                for p in self.pins:
                    l.append('0' if GPIO.input(p) else '1')

                line = ''.join(l)
                print(line)
            else:
                line = raw_input()

            if len(line) < numpins:
                continue

            for i in range(numpins):
                curr = line[i] != '0'
                prev = self.previnputs[i]
                if curr and not prev:
                    self.play(i)
                self.previnputs[i] = curr

if __name__ == "__main__":
    pianoStairs = PianoStairs()
    pianoStairs.run()

