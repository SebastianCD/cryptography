import random
import numpy as np
import os

def xgcd(a, n):
    u, v = a, n
    x1, x2 = 1, 0
    while(u != 1):
        q = v//u
        r = v - (q * u)
        x = x2 - (q * x1)
        v, u, x2, x1 = u, r, x1, x 
    return (x1 % n)

# d = determinante de la matrix
# n = tamaño del alfabeto
def gcd(d,n):
    if(n == 0): 
        return d
    else:
        return gcd(n, int(d) % int(n))

# kg = la llave generada
def KeyGeneration(n):
    kg = np.random.randint(0,n,(3,3))

    d = kg[0][0]*(kg[1][1]*kg[2][2]-kg[1][2]*kg[2][1])-kg[0][1]*(kg[1][0]*kg[2][2]-kg[1][2]*kg[2][0])+kg[0][2]*(kg[1][0]*kg[2][1]-kg[1][1]*kg[2][0])

    if(d!=0 and gcd(d,n)==1): 
        return kg
    else:
        return KeyGeneration(n) 

def InverseKey(kg,n):
    det_matrix = kg[0][0]*(kg[1][1]*kg[2][2]-kg[1][2]*kg[2][1])-kg[0][1]*(kg[1][0]*kg[2][2]-kg[1][2]*kg[2][0])+kg[0][2]*(kg[1][0]*kg[2][1]-kg[1][1]*kg[2][0])

    d_mod_n = det_matrix % int(n)
    d = xgcd(int(d_mod_n),n)

    co_fctr_1 = [(kg[1][1] * kg[2][2]) - (kg[1][2] * kg[2][1]),
                 -((kg[1][0] * kg[2][2]) - (kg[1][2] * kg[2][0])),
                 (kg[1][0] * kg[2][1]) - (kg[1][1] * kg[2][0])]

    co_fctr_2 = [-((kg[0][1] * kg[2][2]) - (kg[0][2] * kg[2][1])),
                 (kg[0][0] * kg[2][2]) - (kg[0][2] * kg[2][0]),
                 -((kg[0][0] * kg[2][1]) - (kg[0][1] * kg[2][0]))]

    co_fctr_3 = [(kg[0][1] * kg[1][2]) - (kg[0][2] * kg[1][1]),
                 -((kg[0][0] * kg[1][2]) - (kg[0][2] * kg[1][0])),
                 (kg[0][0] * kg[1][1]) - (kg[0][1] * kg[1][0])]

    cofac_matrix = [co_fctr_1, co_fctr_2, co_fctr_3]
    
    k1 = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            k1[j][i] = (d * (cofac_matrix[i][j] % n)) % n

    return k1

def IdentityMatrix(kg, K1, n):
    c = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                c[i][j] += kg[i][k] * K1[k][j]

    identity = [[0,0,0], [0,0,0], [0,0,0]]
    for i in range(3):
        for j in range(3):
            identity[i][j] = int(c[i][j]) % int(n)

    if(identity[0][0] == 1 and identity[1][1] == 1 and identity[2][2] == 1):
        return identity
    else:
        print("No se genera la matriz identidad")

def StoreKey(fileN, key):
    script_directory = os.path.dirname(__file__)
    file_path = f"{script_directory}/{fileN}.txt"
    f = open(file_path, 'w')
    b = "" 
    for i in range(3):
        for j in range(3):
            b+=str(key[i][j]) + ' '
        b+='\n'
        f.write(b)
        b=""
    f.close

def GetKey(fileN):
    script_directory = os.path.dirname(__file__)
    file_path = f"{script_directory}/{fileN}.txt"
    kread = np.genfromtxt(file_path)
    return kread

size = int(input('\n\nTamaño del alfabeto: '))
key = KeyGeneration(size)
print(f'\nKey que cifra: {key}')
kInversa = InverseKey(key,size)
print(f'\nKey que descifra: {kInversa}')
Identidad = IdentityMatrix(key,kInversa,size)
print(f'\nMatriz Identidad: {Identidad}')
