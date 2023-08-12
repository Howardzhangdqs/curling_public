import Camp.main as TargetDetectionCamp
import Curling.main as TargetDetectionCurling
import InsiderEdge.main as TargetDetectionInsiderEdge

class TargetDetection:

    def __init__(self):
        self.CurlingDet = TargetDetectionCurling.Detector()

    def camp(img):
        img = img.copy()
        res, _, _ = TargetDetectionCamp.getCurrentCamp(img)
        return res

    def curling(self, img, threshold=0.3):
        img = img.copy()
        return self.CurlingDet.detect(img, threshold=threshold)

    def insiderEdge(self, img):
        return TargetDetectionInsiderEdge(img)
