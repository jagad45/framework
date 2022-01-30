import os
import random
import sys
from string import ascii_letters, punctuation
from threading import Thread
from time import sleep

class Wordlist:
    def __init__(self, filename: str = "") -> None:
        self.threads = [
            {"thread": None, "running": True, "index": 0},
            {"thread": None, "running": True, "index": 0},
            {"thread": None, "running": True, "index": 0}
        ]
        self.filename = filename
        self.string = ascii_letters
        self.temps = []
        self.index = 0
        self.speed = 0
        self.skipp = 0

        if os.path.isfile(self.filename) is False:
            _ = open(self.filename, "w")
            _.close()

    def isRunning(self):
        for thread in self.threads:
            if thread["running"]: return True

    def destroy(self):
        for thread in self.threads:
        	thread["thread"].join()
        	thread["thread"] = None
        	thread["running"] = False
        sys.exit()

    def generate_string(self):
        temp = ""
        for x in range(random.randint(1, 32)):
            temp += random.choice(self.string)
        return temp

    def calculate_speed(self):
        while True:
            old = len(self.temps)
            sleep(1)
            new = len(self.temps)
            self.speed = (new - old)

    def save(self):
        while self.isRunning():
            with open(self.filename, "a") as File:
                try:
                    File.write(self.temps[self.index] + "\n")
                    File.close()
                    self.index += 1
                except KeyboardInterrupt:
                    File.close()
                    self.destroy()
                except IndexError: pass

    def start(self, index=0):
        while self.threads[index]["running"]:
            try:
                s = self.generate_string()
                if s in self.temps:
                    self.skipp += 1
                else:
                    self.temps.append(s)
            except KeyboardInterrupt:
                self.destroy()

    def run(self):
        max_worker = os.cpu_count()
        print (f"Use {max_worker} threads")
        for x in range(max_worker):
            th = Thread(target=self.start, args=(x, ))
            th.setDaemon(True)
            th.start()

        speed = Thread(target=self.calculate_speed)
        speed.setDaemon(True)
        speed.start()

        saver = Thread(target=self.save)
        saver.setDaemon(True)
        saver.start()
        while self.isRunning():
            print (f"Processing job: {len(self.threads)} generated: {len(self.temps)} saved: {self.index} speed: {self.speed}/s skip: {self.skipp}" + " " * 5, end="\r")
        speed.join()
        saver.join()
        
output = input("Output name: ")
wordlist = Wordlist(os.path.join("system/wordlist", output))
wordlist.run()
