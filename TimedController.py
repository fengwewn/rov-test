import time
import threading
from LowController import LowController

class TimedController:

    def __init__(self):
        self.LowController = LowController()

    def timedForwards(self, force, mS):
        self.LowController.forwards(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedBackwards(self, force, mS):
        self.LowController.backwards(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedTurnLeftByLeftWheel(self, force, mS):
        self.LowController.turnLeftByLeftWheel(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedTurnRightByLeftWheel(self, force, mS):
        self.LowController.turnRightByLeftWheel(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedTurnLeftByRightWheel(self, force, mS):
        self.LowController.turnLeftByRightWheel(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedTurnRightByRightWheel(self, force, mS):
        self.LowController.turnRightByRightWheel(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedRotateClockwise(self, force, mS):
        self.LowController.rotateClockwise(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def timedRotateAntiClockwise(self, force, mS):
        self.LowController.rotateAntiClockwise(force)
        thread = threading.Thread(target = self.timedStop, args = [mS])
        thread.start()

    def rotate90Clockwise(self) :
        #self.timedRotateClockwise(30, 230)
        self.timedRotateClockwise(20, 280)

    def rotate90AntiClockwise(self):
        #self.timedRotateAntiClockwise(30, 230)
        self.timedRotateAntiClockwise(20, 280)

    def timedStop(self, mS):
        time.sleep(mS/1000)
        self.LowController.stop()