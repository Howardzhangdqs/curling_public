import sys, os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import Camp.main as TargetDetectionCamp
import Curling.main as TargetDetectionCurling
import InsiderEdge.main as TargetDetectionInsiderEdge
import GetBattleGroundPos.main as GetBattleGroundPos

class TargetDetection:

    def __init__(self):
        self.CurlingDet = TargetDetectionCurling.Detector()

    def camp(self, img):
        img = img.copy()
        res, img, _ = TargetDetectionCamp.getCurrentCamp(img)
        return res, img

    def curling(self, img, threshold=0.3):
        img = img.copy()
        return self.CurlingDet.detect(img, threshold=threshold)

    def insiderEdge(self, img):
        return TargetDetectionInsiderEdge.detect(img)
    
    def GetBattleGroundPos(self, w, h, circle, boxes, classes):
        return GetBattleGroundPos.getPos(w, h, circle, boxes, classes)