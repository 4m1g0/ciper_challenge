#! /usr/bin/python3

import sys
from unidecode import unidecode

ALFABETO = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main(argv):
    if len(argv) < 2:
        print("Error. Usage: descifrador <key> <input> [<output>]")
        sys.exit(2)
    try:
        ifile = open(argv[1], 'r', encoding='utf-8')
    except:
        print ("Error. file '" + argv[1] + "' doesn't exist")
        sys.exit(3)
    
    if len(argv[0]) != 26:
        print ("Error. Key must be 26 chars long")
        sys.exit(5)
    
    key = argv[0].upper()
    if normalize(key) != key:
        print ("Error. invalid Key")
        sys.exit(5)
    
    plainText = ifile.read()
    ifile.close()
    plainText = normalize(plainText)
    encryptedText = encrypt(plainText, key)
    
    if len(argv) > 2:
        ofile = open(argv[2], 'w', encoding='utf-8')
        ofile.write(encryptedText)
        ofile.close()
    else:
        print(encryptedText)
# end

def normalize(text):
    tmp = unidecode(text).upper()
    tmp = ''.join([c for c in tmp if c in ALFABETO])
    return tmp

def encrypt(text, key):
    tmp = text
    tmp = huffman(text, key)
    tmp = sustitucionSimple(tmp, key)
    return tmp

def sustitucionSimple(text, key):
    return ''.join([ALFABETO[key.index(c)] for c in text])

def huffman(text, key):
    level1 = 3
    level2 = 6
    level3 = 8
    correspondencia = list(key[:level1]) #1
    for i in key[level1:level2]: #2
        for j in key[:level1]:
            correspondencia.append(i+j)
        for j in key[level2:level3]:
            correspondencia.append(i+j)
    tmp = 0
    for i in key[level2:level3]: #3
        for k in range(3):
            j = correspondencia[level1:]
            correspondencia.append(i+j[tmp])
            tmp = (tmp+6)%15
        tmp += 1

    correspondencia.append(key[level2]+key[level2])
    correspondencia.append(key[level2+1]+key[level2+1])
    
    #print(len(correspondencia))
    #print('\n'+str(correspondencia)+'\n')
    
    block = ''
    plain = ''
    for c in text:
        block += c
        if block in correspondencia:
            plain += ALFABETO[correspondencia.index(block)]
            block = ''
        if len(block) > 3:
            print('Error: ' + block + ' pattern not found')
            block = ''
            
    return plain

if __name__ == "__main__":
   main(sys.argv[1:])
