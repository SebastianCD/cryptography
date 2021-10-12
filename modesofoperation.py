#Integrantes del equipo
#Cipriano Sebastian
#Hernández Alvarado Abraham
#Arellano Munguia Jose Alejandro

import string    
import random 
import os
import math
import base64
from bitstring import BitArray

#Global Variables
#####################################################################
abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"
alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","{","<","¬","^",">","}"]
n=32
##############################################################

#Functions made by Cipriano Sebastian for the CBC mode
#####################################################################
def encryptCBC(plaintext, key):
    ciphertext = ''
    for i in range(len(plaintext)):
        x = ord(plaintext[i]) - 65
        y = ord(key[i]) - 65
        value = ((x + y) % 32)
        ciphertext = ciphertext + abc[value]
    return ciphertext

def decryptCBC(ciphertext, key):
    plaintext = ''
    for i in range(len(ciphertext)):
        x = ord(ciphertext[i])
        y = ord(key[i])
        value = chr(((x-y) % 32) + 65)
        plaintext = plaintext + value
    return plaintext

def sxor(a,b):    
    c = ''
    for i in range(len(a)):
        x = ord(a[i]) - 65
        y = ord(b[i]) - 65
        z = x^y
        c = c + abc[z]
    return c
#####################################################################

#Functions made by Hernández Alvarado Abraham for the CTR mode
#####################################################################
def fillTables(abc):
    getNum={}
    getLetter={}
    num=0
    for letra in abc:
        getNum[letra]=num
        getLetter[num]=letra
        num=num+1
    return getLetter,getNum
getLetter, getNum=fillTables(abc)

def getBlocks(cadena, blockSize):
    blocks=[]
    for i in range(0,len(cadena),blockSize):
        blocks.append(cadena[i:i+blockSize])
    return blocks

def encryptVigenere(plaintext, key):
    cipherText=""
    count=0
    for s in plaintext:
        cipherText=cipherText+getLetter[(getNum[s]+getNum[key[count%len(key)]])%n]
        count=count+1
    return cipherText

def CTRlikeString(ctr, size):
    ctrString=""
    digit=0
    i=0
    while ctr>0 or i<size :
        digit=ctr%10
        ctrString=ctrString+getLetter[digit]
        ctr=int(ctr/10)
        i=i+1
    return ctrString[::-1]


def encryptCTR(plaintext, key, ctr, size):
    cipherText=ctrToCipher=c=aux=st=""
    count=0
    subs=getBlocks(plaintext,size)
    for m in subs:
        ctrToCipher=CTRlikeString(ctr,size)
        c=encryptVigenere(ctrToCipher,key)
        for x in m:
            aux=aux+getLetter[getNum[x]^getNum[c[count%size]]]
            count=count+1
        cipherText=cipherText+aux
        aux=""
        ctr=ctr+1
    return cipherText
    

def decryptCTR(cipherText, key,ctr,size):
    plainText=m=enc=aux=ctrToCipher=""
    count=0
    blocks=getBlocks(cipherText,size)
    for c in blocks:
        ctrToCipher=CTRlikeString(ctr,size)
        enc=encryptVigenere(ctrToCipher,key)
        for x in c:
            m=m+getLetter[getNum[x]^getNum[enc[count%size]]]
            count=count+1
        plainText=plainText+m
        m=""
        ctr=ctr+1
    
    return plainText
#####################################################################

#Functions made by Arellano Munguia Jose Alejandro for the CFB mode
#####################################################################
def generateKey(string, key):
    key = list(key)
    if len(string) == len(key):
        return(key)
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))



#Para eliminar simbolos o caracteres que no pertenecen al alfabeto
def arreglarCadena(cadena):    
    newString = ""
    for i in cadena.upper():
        if alphabet.count(i)==1:
            newString+=i            
    return newString


#Vigeniere encryption
def encryption(string, key):
    encrypt_text = []
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % len(alphabet)
        #Specifying key in alphabet
        #encrypt_text.append(alphabet[str(x)])
        encrypt_text.append(alphabet[x])
    return("" . join(encrypt_text))  # .encode('utf-8')


#Vigeniere decryption
def decryption(encrypt_text, key):
    orig_text = []
    for i in range(len(encrypt_text)):
        x = (ord(encrypt_text[i]) - ord(key[i]) + len(alphabet)) % len(alphabet)
        orig_text.append(alphabet[str(x)])
    print(orig_text)
    return("" . join(orig_text))


def generateIV(keySize):
    number_of_strings = 1  # Solo una llave I.V.
    length_of_string = len(keySize)
    for x in range(number_of_strings):
        cadena = (''.join(random.choice(string.ascii_uppercase)
                          for _ in range(length_of_string)))
    return cadena

#Returns the key value
def GetKeyAlphabet(val):
    for key, value in alphabet.items():
        if ord(value) == val:
            return key
    return "key doesn't exist"


def plainTextToBinary(plainText):
    binaryPlainText = ""
    for character in range(0, len(plainText)):
        binaryPlainText = binaryPlainText + format(ord(plainText[character]), "08b")
    #print("Binario:  ", binaryPlainText)
    return binaryPlainText

def stringToList(cipheredText):
    li = list(cipheredText.split(" "))
    return li

def plaintextBlocks(plaintext, IVlength):
    ptBlocks = []
    #In case we need to complete
    if len(plaintext)%IVlength != 0:
        plaintext += 'Z'*(IVlength-len(plaintext)%IVlength)
    #Partitioning
    for i in range(math.floor(len(plaintext)/IVlength)):
        ptBlocks.append(plaintext[(i*IVlength):((i+1)*IVlength)])
    return ptBlocks


def CFBencrypt(vKey, plainText):
    #Generating random IV(Nounce)
    ivNOUNCE = generateIV(vKey)
    #So we don't modify the original NOUNCE value
    iv = ivNOUNCE

    print("IV NOUNCE: ", ivNOUNCE)

    #Obtaining the blocks of the plaintext
    ptBlocks = plaintextBlocks(plainText, len(iv))

    #Making plaintext to binary
    #NOTE: Don't forget to take on count the added words
    binaryPlaintext = plainTextToBinary("" . join(ptBlocks))

    cipherTextFinal = []

    
    startIndex = 0
    stIdx = 0
    #ITERATING THROUGH THE BLOCKS
    print(">> Blocks to work on:", ptBlocks)
    for i in range(0, len(ptBlocks)):
        print(">> Working on block: ", ptBlocks[i], "\n")
        if(i >= 1):
            iv = ''.join(cipherTextFinal[stIdx:stIdx+4])
            stIdx += 4
        for j in range(0, len(ptBlocks[i])):
            #Generating Vigeniere Key
            encipherdVigeniereKey = encryption(iv, Vkey)

            #Converting the Vigeniere key to binary so we can work on bit level
            vigeniereKeyBinary = plainTextToBinary(encipherdVigeniereKey)

            cipherText = alphabet[int((alphabet.index(chr(int((binaryPlaintext[startIndex:startIndex+8]), 2))) ^ int((vigeniereKeyBinary[:8]), 2))%len(alphabet))]
            startIndex += 8
            cipherTextFinal.append(cipherText)

            #Replacing the first character from IV
            iv = iv[0:0]+iv[0+1:]
            #Adding the ciphertext
            iv = iv + cipherText

    f = open("cipherText.txt", "w+")
    f.write(''.join(cipherTextFinal))
    f.close()
    return ivNOUNCE


def decrypt(iv, encipheredText, key):
    #Obtaining the blocks of the plaintext
    ctBlocks = plaintextBlocks(encipheredText, len(iv))

    binaryCiphertext = plainTextToBinary(encipheredText)

    plainTextFinal = []
    startIndex = 0
    stIdx = 0
    #ITERATING THROUGH THE BLOCKS
    print(">> Blocks to work on:", ctBlocks)
    for i in range(0, len(ctBlocks)):
        print(">> Working on block: ", ctBlocks[i], "\n")
        #For the next blocks
        if(i >= 1):
            iv = ctBlocks[i-1]
            #stIdx += 4
        for j in range(0, len(ctBlocks[i])):
            
            vigeniereKey = encryption(iv, key)
            
            vigeniereKeyBinary = plainTextToBinary(vigeniereKey)
            
            plainText = alphabet[int((alphabet.index(chr(int((binaryCiphertext[startIndex:startIndex+8]), 2))) ^ int((vigeniereKeyBinary[:8]), 2))%len(alphabet))]

            #Aniadir el caracter proporcionado
            plainTextFinal.append(plainText)

            #Replacing the first character from IV
            iv = iv[0:0]+iv[0+1:]
            iv = iv + alphabet[int((binaryCiphertext[startIndex:startIndex+8]), 2)%len(alphabet)]

            
            startIndex += 8

    print("FINAL OUTPUT: ", ''.join(plainTextFinal))
####################################################################

#General functions to all the modes

def leerDocumento(filetext):
    f = open (filetext,'r')
    mensaje = f.read()
    f.close()
    return mensaje

def almacenarDocumento(filetext,text):
    f = open (filetext,'w')
    f.write(text)
    f.close()
####################################################################

#Main program
if __name__ == "__main__":
    print("Mode of operation CBC")
    filetext=input("Enter the filename of the plaintext: ")
    filecip=input("Enter the filename to be ciphered: ")
    filedec=input("Enter the filename to be deciphered:")
    key=input("Key: ")
    iv=input("Vector: ")

    text = leerDocumento(filetext)
    text = text[0:len(text)-1]

    cifrado = ''

    auxiv = iv

    if len(text)%len(key) != 0:
        ext = ''.join((random.choice(string.ascii_uppercase) for x in range(len(key)-len(text)%len(key)))) 
        text = text + ext

    for i in range(0,len(text),len(iv)):
        aux = text[i:i+len(iv)]
        aux2 = sxor(aux,iv)
        aux3 = encryptCBC(aux2,key)
        cifrado = cifrado + aux3
        iv = aux3

    almacenarDocumento(filecip,cifrado)

    descifrado=''

    for j in range(0,len(cifrado),len(auxiv)):
        aux = cifrado[j:j+len(auxiv)]
        iv2 = auxiv
        auxiv = aux
        aux2 = decryptCBC(aux, key)
        aux3 = sxor(aux2,iv2)
        descifrado = descifrado + aux3

    almacenarDocumento(filedec,descifrado)
#############################################################################
    print("\nMode of operation CTR")
    filetext=input("Enter the filename of the plaintext: ")
    filecip=input("Enter the filename to be ciphered: ")
    filedec=input("Enter the filename to be deciphered:")
    key=input("Key: ")
    block=len(key)
    ctr=int(input("Counter (number): "))

    text = leerDocumento(filetext)
    text = text[0:len(text)-1]

    cifrado=encryptCTR(text,key,ctr,block)

    almacenarDocumento(filecip,cifrado)

    text1=leerDocumento(filecip)
    text1=text1[0:len(text1)-1]

    descifrado=''

    descifrado=decryptCTR(text1,key,ctr,block)

    almacenarDocumento(filedec,descifrado)

#########################################################################
    print("\nMode of operation CFB")
    # ENCRYPTION SECTION
    fileNamePlaintext = input('Enter the filename to be ciphered: ')
    file = open(fileNamePlaintext+'.txt', mode='r')
    # read all lines at once
    plainText = file.read()
    # close the file
    file.close()
    pt = arreglarCadena(plainText)
    #Asking for the key
    Vkey = input('Enter the vigenere Key: ')
    ivNonce = CFBencrypt(Vkey, pt)

    # DECRYPTION SECTION
    fileNameEncipheredtext = input('Name of the enciphered file: ')
    file = open(fileNameEncipheredtext+'.txt', mode='r')
    # read all lines at once
    encipheredText = file.read()
    # close the file
    file.close()
    #Asking for the key
    Vkey = input('Enter the vigenere Key: ')
    decrypt(ivNonce, encipheredText, Vkey)
