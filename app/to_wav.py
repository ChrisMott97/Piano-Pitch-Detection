import wave
import glob
import os

while True:
    for f in glob.glob("raw/ready*.raw"):
        with open(f, "rb") as inp_f:
            data = inp_f.read()
            with wave.open("wav/"+f.split(".")[0]+".wav", "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(2) # number of bytes
                out_f.setframerate(16000)
                out_f.writeframesraw(data)
            os.remove(inp_f.name)
