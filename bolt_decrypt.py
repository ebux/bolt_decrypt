import sys
import os
import base64
import binascii

def decryptFile(fname):
    b = open(fname, 'rt', errors="ignore").read()

    # find key
    bolt_decrypt_start = b.find('bolt_decrypt')
    if (bolt_decrypt_start < 0):
        return

    keystart = b.find("'", bolt_decrypt_start)+1
    keyend = b.find("'", keystart)
    key = b[keystart:keyend]

    print ('bolt key: %s'%(key))

    # get data
    datastart = b.find('##!!!##')+7
    data = b[datastart:]

    print ('bolt data: %s'%(data))

    # decode data
    cipher = base64.b64decode(data)
    print (binascii.hexlify(cipher))

    # decrypt data
    decoded = ''
    for c in cipher:
        for k in key:
            c = (c-ord(k))&0xff
        decoded += chr(c)

    print ('decoded %s:'%(decoded))

    open(fname+'.dec', 'wt', errors="ignore").write(decoded)


# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(sys.argv[1]):
    path = root.split(os.sep)
    print((len(path) - 1) * '  ', os.path.basename(root))
    for file in files:
        print(len(path) * '  ', root, file)
        if (file[-3:] == 'php'):
            decryptFile(root+'\\'+file)
