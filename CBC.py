import string    
import random 

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"

def encrypt(plaintext, key):
    ciphertext = ''
    for i in range(len(plaintext)):
        x = ord(plaintext[i]) - 65
        y = ord(key[i]) - 65
        value = ((x + y) % 32)
        ciphertext = ciphertext + abc[value]
    return ciphertext

def decrypt(ciphertext, key):
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

def leerDocumento(filetext):
    f = open (filetext,'r')
    mensaje = f.read()
    f.close()
    return mensaje

def almacenarDocumento(filetext,text):
    f = open (filetext,'w')
    f.write(text)
    f.close()

filetext=input("Nombre del archivo de plaintext: ")
filecip=input("Nombre del archivo de texto cifrado: ")
filedec=input("Nombre del archivo de texto descifrado:")
key=input("Llave: ")
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
    aux3 = encrypt(aux2,key)
    cifrado = cifrado + aux3
    iv = aux3

almacenarDocumento(filecip,cifrado)

descifrado=''

for j in range(0,len(cifrado),len(auxiv)):
    aux = cifrado[j:j+len(auxiv)]
    iv2 = auxiv
    auxiv = aux
    aux2 = decrypt(aux, key)
    aux3 = sxor(aux2,iv2)
    descifrado = descifrado + aux3

almacenarDocumento(filedec,descifrado)