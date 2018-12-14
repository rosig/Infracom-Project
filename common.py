def calcChecksum(content):
    pos = len(content)
    if (pos & 1):
        pos -= 1
        sum = ord(content[pos])
    else:
        sum = 0
    
    while pos > 0:
        pos -= 2
        sum = (ord(content[pos+1]) << 8) + ord(content[pos])
    
    sum = sum & 0xffff
    mask = (1 << 16) - 1
    onescomp = sum ^ mask

    return chr(onescomp & 0xff00) + chr(onescomp & 0x00ff)