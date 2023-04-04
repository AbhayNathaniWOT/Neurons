from cameo import Cameo as Cameo_Base
import matplotlib.pyplot as plt
from utils import add_strip

def slider_callback(s): pass

class Cameo(Cameo_Base):
    def __init__(self, filter, title) -> None:
        super().__init__(filter, title)
        self.apply_filter = filter

    def loop_Events(self, title):
        self._windowManager.apply_filter = self.apply_filter



def strip(frame, self):
    frame = add_strip(frame, 50, "top","white")
    return frame


if __name__ == "__main__":
    title = "Mask"
    Cameo(filter=strip, title=title).run()
