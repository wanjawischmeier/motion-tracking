from multiprocessing import shared_memory as shm
from random import randint
from time import sleep
#from tracking import *


def CheckForRequest():
    try:
        result = hand_positions
    except Exception as e:
        result = "Unknown Error: " + str(e)
    
    print('[Python]\t|  Eval:\t|  ' + result)




class DataStream:
    def __init__(self, shm_name = "motion_tracking_data_stream"):
        self.__shm = shm.SharedMemory(name = shm_name, create=True, size = 6)
        self.__buffer = self.__shm.buf
        self.__buffer[0] = 1        # Comment this line out later, to only start writing when 'read' byte is set to true by C#

        # self.read     = 0         # Will be set to True by C# if it wants to recieve data |   [0]         (Should not actually be set here)
        self.hand_l_pos_x      = 0  # The x position                                        |   [1]
        self.hand_l_pos_y      = 0  # The y position                                        |   [2]        self.hand_l_pos_x      = 0     # The x position                                        |   [1]
        self.hand_r_pos_x      = 0  # The x position                                        |   [3]        self.hand_l_pos_x      = 0     # The x position                                        |   [1]
        self.hand_r_pos_y      = 0  # The y position                                        |   [4]
        self.tracked    = 0         # How many hands are tracked (from 0 to 2)              |   [5]

    def __get_read(self):             return self.__buffer[0]
    def __set_read(self, value):      self.__set_buffer(0, value)

    def __get_hand_l_pos_x(self):            return self.__buffer[1]
    def __set_hand_l_pos_x(self, value):     self.__set_buffer(1, value)

    def __get_hand_l_pos_y(self):            return self.__buffer[2]
    def __set_hand_l_pos_y(self, value):     self.__set_buffer(2, value)

    def __get_hand_r_pos_x(self):            return self.__buffer[3]
    def __set_hand_r_pos_x(self, value):     self.__set_buffer(3, value)

    def __get_hand_r_pos_y(self):            return self.__buffer[4]
    def __set_hand_r_pos_y(self, value):     self.__set_buffer(4, value)

    def __get_tracked(self):          return self.__buffer[5]
    def __set_tracked(self, value):   self.__set_buffer(5, value)

    def __set_buffer(self, index, _value):
        if self.read:   self.__buffer[index] = _value
        else: print("Unable to write to stream, 'read' is not enabled!")

    read =          property(__get_read, __set_read)
    hand_l_pos_x =  property(__get_hand_l_pos_x, __set_hand_l_pos_x)
    hand_l_pos_y =  property(__get_hand_l_pos_y, __set_hand_l_pos_y)
    hand_r_pos_x =  property(__get_hand_r_pos_x, __set_hand_r_pos_x)
    hand_r_pos_y =  property(__get_hand_r_pos_y, __set_hand_r_pos_y)
    tracked =       property(__get_tracked, __set_tracked)

tst = DataStream()

print("starting")

while True:
    tst.hand_l_pos_x = randint(0, 255)
    tst.hand_l_pos_y = randint(0, 255)
    tst.hand_r_pos_x = randint(0, 255)
    tst.hand_r_pos_y = randint(0, 255)
    sleep(.2)
    #print(tst.hand_l_pos_x)