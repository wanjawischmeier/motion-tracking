from multiprocessing import shared_memory as shm

shm_a = shm.SharedMemory(name="testfile", create=True, size=4)

buffer = shm_a.buf

#buffer[:4] = bytearray([12, 24, 48, 128])
#buffer[0] = 24
buffered_txt = b'test'#bytes("test", "utf-8")

for i in range(len(buffer)):
    buffer[i] = buffered_txt[i]

print(len(buffer))

for byte in buffer:
    print(byte)


input()
