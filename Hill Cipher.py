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
    return gcd(n, int(n) % int(d))

# kg = la llave generada
def KeyGeneration(n):
    kg = [[0,0,0], [0,0,0], [0,0,0]]

    for i in range(3):
        for j in range(3):
            kg[i][j] = random.randint(0, n-1)

    d = kg[0][0]*(kg[1][1]*kg[2][2]-kg[1][2]*kg[2][1])-kg[0][1]*(kg[1][0]*kg[2][2]-kg[1][2]*kg[2][0])+kg[0][2]*(kg[1][0]*kg[2][1]-kg[1][1]*kg[2][0])

    if d != 0: 
        if gcd(d,n) == 1:
            return kg
        else:
            return KeyGeneration(n)

def InverseMatrix(kg,n):
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
            identity[i][j] = c[i][j] % n

    if(identity[0][0] == 1 and identity[1][1] == 1 and identity[2][2] == 1):
        return identity

def StoreKey(file_name, key):
    script_directory = os.path.dirname(__file__)
    file_path = f"{script_directory}/{file_name}.txt"
    f = open(file_path, 'w')
    f.write(str(key))
    f.close
    return file_name

def GetKey(file_name):
    script_directory = os.path.dirname(__file__)
    file_path = f"{script_directory}/{file_name}.txt"
    f = open(file_path)
    f.close
    return key

# key = [[10,22,17],[10,7,6],[15,8,7]]
# inverse_key = [[25,18,13], [6,3,20], [25,10,20]]

print('\n\nTamaño del alfabeto: 26')
# size_alphabet = int(input('\n\nTamaño del alfabeto: '))
size_alphabet = 26
key = KeyGeneration(size_alphabet)

print('Nombre del archivo: keyHillCipher')
# file_name = input('Nombre del archivo: ')
file_name = 'keyHillCipher'
StoreKey(file_name, key)
key_file = GetKey(file_name)
print(f'\nKey que cifra: {key_file}')

inverse_key = InverseMatrix(key_file, size_alphabet)
print(f'\nKey que decifra (matrix inversa): {inverse_key}')

print(f'\nMatriz identidad: {IdentityMatrix(key_file, inverse_key, size_alphabet)}\n')