def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata
