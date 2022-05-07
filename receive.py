import socket
import wave
import os
s = socket.socket()

s.bind(('0.0.0.0', 8090))
s.listen(0)
i = 0
j = 0
while True:
    client, addr = s.accept()
    i += 1
    if i % 10 == 0:
        j += 1
    if os.path.isfile(f"raw/output{j-1}.raw"):
        os.replace(f"raw/output{j-1}.raw", f"raw/ready{j-1}.raw")
        print(f"File {j} ready.")
    while True:
        content = client.recv(32)
        if len(content) == 0:
            break
        else:
            with open(f"raw/output{j}.raw", "ab") as myfile:
                myfile.write(content)
            # with wave.open("test_new.wav", "wb") as out_f:
            #     out_f.writeframesraw(content)
    print(".")
    client.close()







# data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

# while data != '':
#     stream.write(data)
#     data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

# stream.stop_stream()
# stream.close()

# p.terminate()
