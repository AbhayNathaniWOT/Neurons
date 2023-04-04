import cv2
import time
import numpy as np

class CaptureManager(object):

    def __init__(self,
                 capture,
                 apply_filter,
                 previewWindowManager=None,
                 shouldMirrorPreview=False,

                 ):
        self.apply_filter = apply_filter
        self.previewWindowManager = previewWindowManager
        self.shouldMirrorPreview = shouldMirrorPreview

        self._capture = capture
        self._channel = 0
        self._enteredFrame = False
        self._frame = None
        self._imageFileName = None
        self._videoFileName = None
        self._videoEncoding = None
        self._videoWriter = None

        self._startTime = None
        self._framesElapsed = int(0)
        self._fpsEstimate = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        if self._channel != value:
            self._channel = value
            self.frame = None

    @property
    def frame(self):
        if self._enteredFrame and self._frame is None:
            _, self._frame = self._capture.retrieve(self._frame, self.channel)
        return self._frame

    @property
    def isWritingImage(self):
        return self._imageFileName is not None

    @property
    def isWritingVideo(self):
        return self._videoFileName is not None

    def enterFrame(self):
        '''Capture Next Frame If Any'''
        if self._capture is not None:
            self._enteredFrame = self._capture.grab()

    def exitFrame(self):
        '''
            - Draw to the window.
            - Write to files
            - Release the Frame
        '''
        # Check whether any grabbed frame is retrievable
        # Getter may retrieve and cache the frame

        if self.frame is None:
            self._enteredFrame = False
            return
        # Update FPS estimate and related variables
        if self._framesElapsed == 0:
            self._startTime = time.time()
        else:
            timeElapsed = time.time() - self._startTime
            self._fpsEstimate = self._framesElapsed/timeElapsed
        self._framesElapsed += 1

        # Draw To the window if any
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirrored_frame = np.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirrored_frame)
            else:
                self.previewWindowManager.show(self._frame)
        # Write to the image file if any
        if self.isWritingImage:
            frame = self.apply_filter(self._frame)
            cv2.imwrite(self._imageFileName, frame)
            self._imageFileName = None
        # Write to video file if any
        self._writeVideoFrame()

        # Every operation on frame is done
        # Let's release the frame
        self._frame = None
        self._enteredFrame = False

    '''
        Below defined public methods
        writeImage, startWritingVideo, stopWritingVideo
        simply record parameters for file writing options
        Actual writing operations are postponed to the next call
        of exitFrame()
        Writing Handled by non-public method => _writeVideoFrame()
    '''

    def writeImage(self, filename):
        '''Write an next excited frame to an image file'''
        self._imageFileName = filename

    def startWritingVideo(self,
                          filename,
                          encoding=cv2.VideoWriter_fourcc(*'MP4V'),
                          ):
        ''' Start Writing excited frames to video file'''
        self._videoEncoding = encoding
        self._videoFileName = filename

    def stopWritingVideo(self):
        '''Stop Writing excited frames to a video file'''
        self._videoEncoding = None
        self._videoFileName = None
        self._videoWriter = None

    # Below are non-public Methods

    def _writeVideoFrame(self):
        '''  _writeVideoFrame Method creates|appends to a video file'''
        if not self.isWritingVideo:
            return
        if self._videoWriter is None:
            fps = self._capture.get(cv2.CAP_PROP_FPS)
            if fps == 0.0:
                # Capture's FPS is Unknown so use estimator
                if self._framesElapsed < 20:
                    # Wait until more frames to elapse so that
                    # estimate is stable
                    return
                else:
                    fps = self._fpsEstimate
            # size => tuple contains (int:WIDTH,int:HEIGHT) of frame
            
            size = (
                int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )
            # Initialize VideoWriter Object
            self._videoWriter = cv2.VideoWriter(self._videoFileName,
                                                self._videoEncoding,
                                                fps, size)
        # Ask the object to write the frame
        # frame = self.apply_filter(self._frame)
        frame = self._frame
        self._videoWriter.write(frame)


class WindowManger():
    def __init__(self,
                 windowName,
                 apply_filter,
                 keypressCallback=None,
                 ):
        self._keypressCallback = keypressCallback
        self._windowName = windowName
        self._isWindowCreated = False
        self.apply_filter = apply_filter

    ''' Properties '''
    @property
    def isWindowCreated(self):
        return self._isWindowCreated

    def createWindow(self):
        cv2.namedWindow(self._windowName)
        self._isWindowCreated = True

    def show(self, frame):
        frame = self.apply_filter(frame,self)
        
        cv2.imshow(self._windowName, frame)

    def destroyWindow(self):
        cv2.destroyWindow(self._windowName)
        self._isWindowCreated = False
    def processEvents(self):
        keycode = cv2.waitKey(1)
        if self._keypressCallback is not None and keycode != -1:
            # waitkey() returns 32bit value but ASCII is only 8bit
            # Thus remove the redundant value & keep only 8-LSB bits
            # Discard any non ASCII infon by GTK by &= 0...0 1111(F) 1111(F)
            keycode &= 0xFF
            # Now process this updated keypress code
            self._keypressCallback(keycode)
            
    ''' Enough for Simple '''            
    ''' Can be further expanded by adding mouseCallback property'''
    ''' Further use of Pygame's Window handling frameworks can work too'''
    ''' Eg for closing window when close button clickd'''
    
    

