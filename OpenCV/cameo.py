import cv2
from managers import WindowManger, CaptureManager
import filters


def show_slider(x): print(x)
class Cameo(object):
    def __init__(self,filter,title) -> None:
        self.title = title
        self._windowManager = WindowManger(title,apply_filter=filter, keypressCallback=self.onKeypress)
        self._captureManager = CaptureManager(
            cv2.VideoCapture(0),filter, self._windowManager, True)
        
    def window_changes(self,title):
        pass
    def loop_Events(self,title):
        pass
    
    def run(self):
        ''' Run the Main Loop'''
        self._windowManager.createWindow()
        self.window_changes(self.title)
        while self._windowManager.isWindowCreated:
            self._captureManager.enterFrame()
            frame = self._captureManager.frame
            # TODO: Filter the frame (Chapter 3).
            self.loop_Events(self.title)
            self._captureManager.exitFrame()
            self._windowManager.processEvents()
    
    def Keypress_Events(self,keycode):
        print(keycode)
        
    
    def onKeypress(self, keycode):
        if keycode == 32:  # space
            self._captureManager.writeImage('screenshot.png')
        elif keycode == 9 or keycode == 118:  # tab and 'v'
            if not self._captureManager.isWritingVideo:
                self._captureManager.startWritingVideo(
            'ss.mp4')
            else:
                self._captureManager.stopWritingVideo()
        elif keycode == 27 or keycode == 113:  # escape or Q pressed
            self._windowManager.destroyWindow()
        else: 
            self.Keypress_Events(keycode)
            
            
            
if __name__ == "__main__":
    Cameo(filter=filters.BGR2GRAY,title="gray").run()
    
