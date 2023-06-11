from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

def parse_msg(block):
    msgs = ""
    address_offset=int(0)
    for cw in range(int(len(block)/32)):
        cws = block[32 * cw:32 * (cw + 1)]
        # Skip the idle word
        if cws.startswith("10101010101010101010101010101010"):
            print("  Preamble: " + cws)
            continue
        if cws.startswith("01111100110100100001010111011000"):
            print("  Sync:     " + cws)
            address_offset=0
            continue    
        if cws.startswith("01111010100010011100000110010111"):
            print("  Idle:     " + cws)
            address_offset = address_offset +1
            continue
        if cws[0] == "0":
            addr, type, crc = cws[1:19], cws[19:21], cws[21:32]
            print("  Addr:     0 " + addr, type, crc)
            address_msb = int(cws[1:19],2)
            address_msb = address_msb << 3
            address = int(address_offset/2) + address_msb
            continue
        else:
            msg, crc = cws[1:21], cws[21:32]
            #print("  Msg: " + cws)
            print("  Msg:      1 " + msg, crc)
            msgs += msg

    print("This Message was addressed to", address)

    # Split long string to 7 chars blocks
    bits = [msgs[i:i+7] for i in range(0, len(msgs), 7)]

    print("Message consists of 7-bit words: ")
    print(bits)

    # Get the message
    msg = ""
    for b in bits:
        b1 = b[::-1]  # Revert string
        value = int(b1, 2)
        msg += chr(value)

    print("Message decodes in ASCII as:", msg)
    print()

# First filter the received data in Audacity and split stereo to mono keeping only one channel.
fs, data = wavfile.read("pager3.wav")


#Normalize amplitude to +/- 1:
normal = data / max(data)
print(fs)
plt.plot(normal, label="input")
baud = 1200
ppm = 0
bit_length = int(48000/baud*(1+ppm/1000000))

start = 0
for p in range(2*bit_length):
    if (data[p] < -50) and (data[p+1] > 50):
        start = p
        break
# Bits frame
bits_str = "1"
bits = np.zeros(data.size)
sync = np.zeros(data.size)
next_bit = start + bit_length
for p in range(0, data.size):
    if(p==next_bit):
        bits[p] = 1
        bits_str += "1" if data[p] > 0 else "0"
        next_bit = next_bit + bit_length
        
    if (data[p] < -50) and (data[p+1] > 50) and p>start+1:
        next_bit = int(p + bit_length/2)
        sync[p] = 1

#print(bits_str)
parse_msg(bits_str)

plt.plot(bits, label="bits")
plt.plot(sync, label="sync")
plt.legend(loc="upper left")
#plt.show()

