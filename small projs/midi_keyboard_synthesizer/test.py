# import tkinter as tk
# from tkinter import ttk

import pyaudio
import wave
import sys
import mido
import time
import math
import numpy as np

sampling_rate = 44100
first_note = 21

CHUNK = 1024


def temp12t(note):
    return 440 * 2 ** ((note - 69) / 12)


class Note:
    def __init__(self, note, volume, start_time):
        self.note = note
        self.volume = volume
        self.time = start_time


class Program:
    def __init__(self):
        self.pedal = False
        self.notes = []
        self.clear_notes = []

        self.run()

    def remove_note(self, note):
        nt = next(n for n in self.notes if n.note == note)
        self.notes.remove(nt)

    def process_msg(self, msg):
        if msg.type == 'note_on':
            self.process_note(msg)
        elif (msg.type == 'control_change') and (msg.control == 64):
            if msg.value > 0:
                self.pedal = True
            else:
                for n in self.clear_notes:
                    self.remove_note(n)
                self.clear_notes.clear()

                self.pedal = False

    def process_note(self, msg):
        if msg.velocity == 0:
            if self.pedal:
                self.clear_notes.append(msg.note)
            else:
                self.remove_note(msg.note)

            return

        note = Note(msg.note, msg.velocity / 127, time.time())
        self.notes.append(note)

    def get_value(self, time):
        value = 0
        for n in self.notes:
            t = time - n.time
            f = temp12t(n.note)
            v = n.volume
            v *= math.sin(2 * math.pi * f * t)
            value += v

        if value > 1:
            value = 1
        return value

    def run(self):
        print("Choose one input:", ', '.join(mido.get_input_names()))
        input_name = input("Input port (leave empty for first one): ")
        pin = mido.open_input(input_name or mido.get_input_names()[0])

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sampling_rate,
                        output=True)

        samples = (np.sin(2*np.pi*np.arange(sampling_rate*1)*440/sampling_rate)
                   ).astype(np.float32)

        stream.write(0.5*samples)

        interval = 1 / sampling_rate
        last_time = time.time()
        while True:
            for msg in pin.iter_pending():
                self.process_msg(msg)

            t = time.time()
            if t - last_time < 1.4 * interval:
                continue

            t = last_time
            stream.write(np.array([self.get_value(t + interval),
                                  self.get_value(t + 2 * interval)]), 1024)
            last_time = last_time + 2 * interval

        stream.stop_stream()
        stream.close()


Program()
