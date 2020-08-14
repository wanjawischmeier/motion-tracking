from multiprocessing import shared_memory as shm
from random import randint
from time import sleep

printEnabled = False

shm_a = shm.SharedMemory(name="testfile", create=True, size=8)

buffer = shm_a.buf

count = 0
txt = b'test'

# index:
# [0]   - count
# [1]   - randint(0, 50)
# [2]   - randint(50, 100)
# [3]   - 24
# [4:7] - test

while True:
    count += 1
    buffer[0] = count

    buffer[1] = randint(0, 50)
    buffer[2] = randint(50, 100)

    buffer[3] = 24

    for byte in range(len(txt)):
        buffer[4 + byte] = txt[byte]

    # Printing current buffer

    print("Buffer:")
    for byte in buffer:
        print(byte)
    print("_" *10)

    sleep(0.01)
