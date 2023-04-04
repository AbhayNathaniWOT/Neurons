from cameo import Cameo as Cameo_Base
import matplotlib.pyplot as plt
import cv2

i = 0
while i < 1:

    plt.pause(0.0001)
    i = 1 if i == 0 else 0
    print("On image", i)


def slider_callback(s): pass


class Cameo(Cameo_Base):
    def __init__(self, filter, title) -> None:
        super().__init__(filter, title)
        self.apply_filter = filter

    def Keypress_Events(self, keycode):
        print("Key_pressed", keycode)

    def loop_Events(self, title):
        self._windowManager.apply_filter = self.apply_filter

    def window_changes(self, title):
        
        self._windowManager.init_plot = True
        
        


def histogram(frame, self):
    if self.init_plot:
        plt.ion()
        self.fig, self.ax = plt.subplots()
        
        self.line_b, = self.ax.plot(
            cv2.calcHist(
        [frame], [0], None, [256], [0, 256]), c="b")
        self.line_g, = self.ax.plot(
            cv2.calcHist(
        [frame], [1], None, [256], [0, 256]), c="g")
        self.line_r, = self.ax.plot(
            cv2.calcHist(
        [frame], [2], None, [256], [0, 256]), c="r")
        self.ax.set_xlim(0, 256)
        self.init_plot = False
        
    self.line_b.set_ydata(cv2.calcHist(
        [frame], [0], None, [256], [0, 256]))
    self.line_g.set_ydata(cv2.calcHist(
        [frame], [1], None, [256], [0, 256]))
    self.line_r.set_ydata(cv2.calcHist(
        [frame], [2], None, [256], [0, 256]))
    self.fig.canvas.draw()
    self.fig.canvas.flush_events()

    return frame


if __name__ == "__main__":
    title = "Histogram"
    Cameo(filter=histogram, title=title).run()
