import sys, os

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import TrackRectificate.main as Rectificate


def SceneClassification(img):
    return Rectificate.SceneClassification(img)


def SceneRectificate(img, PreserveWidth=True):
    img = img.copy()
    img2, tl, tr, bl, br = Rectificate.rectificate.find(img)
    return Rectificate.rectificate.trans(img, tl, tr, bl, br, PreserveWidth=PreserveWidth)
