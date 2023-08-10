from ctypes import cdll
import ctypes

class soSocket():

    def __init__(self, soPath):
        self.cur = cdll.LoadLibrary(soPath)
    

class SoftData(soSocket):
    def SendData(self, length, data):
        self.cur.test.restype = ctypes.POINTER(ctypes.c_bool)
        arr = (ctypes.c_bool * 5)(True, False, True, False, True)
        res = self.cur.test(arr, 5)
        print([res[i] for i in range(5)])

SoftData("./bin/SoftData.so").SendData()