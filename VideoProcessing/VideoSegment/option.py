import numpy as np
import os
import portion as P


class DefaultOption(object):

    def __init__(self):
        self.STATE_POSITION = np.linspace(203, 367, 8).astype(int).tolist()
        self.STATE_VERTICAL = (37, 62)
        self.STATE_OFFSET = 3
        self.VIDEO_PATH = os.path.join(
            os.path.dirname(__file__), '../../videos/target2.tiny.mp4')

        self.CurlingInterval_offset = 5

        def CurlingInterval_build(axis, offset): return P.closed(
            axis - offset, axis + offset)

        # 红色冰壶
        self.CurlingInterval_red = [
            P.closed(82, 90),
            P.closed(175.8, 181),
            P.closed(142, 153.6)
        ]

        # 黄色冰壶
        self.CurlingInterval_yel = [
            P.closed(157, 166.5),
            P.closed(113, 120),
            P.closed(161, 170.5)
        ]

        self.debug = True


OPT = DefaultOption()
