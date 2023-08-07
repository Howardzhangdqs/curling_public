import numpy as np
import os
import portion as P


class DefaultOption(object):

    def __init__(self):
        self.STATE_POSITION = np.linspace(203, 367, 8).astype(int).tolist()
        #np.linspace(203, 319, 6).astype(int).tolist()
        #np.linspace(203, 367, 8).astype(int).tolist()
        #np.linspace(203, 343, 7).astype(int).tolist()
        self.STATE_VERTICAL = (37, 62)
        self.STATE_OFFSET = 3
        self.VIDEO_PATH = os.path.join(
            os.path.dirname(__file__), '../video/target.min.mp4')

        self.CurlingInterval_offset = 5

        CurlingInterval_build = lambda axis, offset: P.closed(axis - offset, axis + offset)

        # 红色冰壶
        self.CurlingInterval_red = [
            P.closed(82, 90),
            P.closed(176, 181),
            P.closed(142, 153.6)
            #CurlingInterval_build(178, self.CurlingInterval_offset),
            #CurlingInterval_build(149, self.CurlingInterval_offset)
        ]

        # 黄色冰壶
        self.CurlingInterval_yel = [
            P.closed(157, 166.5),
            P.closed(113, 120),
            P.closed(161, 170.5)
            #CurlingInterval_build(116, self.CurlingInterval_offset),
            #CurlingInterval_build(167, self.CurlingInterval_offset)
        ]

        self.debug = True


OPT = DefaultOption()
