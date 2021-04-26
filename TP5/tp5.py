
e = 17
n = 213271

# Fatorizar n para obter p e q (valores cuja multiplicação resulta em n)
def fatores_primos(n):
    i = 2
    resultado = []
    while i <= n:
        if (n % i) == 0:
            resultado.append(i)
            n = n / i
        else:
            i = i + 1
    return resultado
 
# Fatorização
fatores = fatores_primos(n)
p = fatores[0]
q = fatores[1]

#print("p =" , p )
#print("q =", q)
       
# Calcula o maior divisor comum de a e b
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    
# Calcula o menor multiplo comum entre a e b   
def lcm(a,b):
    return ((a*b) // gcd(a,b))

# Minimo Múltiplo Comum de p e q    
t = lcm(p-1,q-1)    

# Codificard e acordo com o esquema apresentado 
def codificar(l1,l2,l3):
    return 729*l1 + 27*l2 + l3
    
# Descodificar de acordo com o esquema apresentado
def descodificar(n):
    l3 = n % 27
    x = n - l3
    l1 = x // 729
    x1 = x - l1*729
    l2 = x1 // 27
    return (l1,l2,l3)
    
# Conversao de numeros para caracteres
def converter(n):
   # Enunciado: caracter espaco = nº26
    if n == 26:
        return ' '       
    else:
        return chr(n+65)


def decifrar(ciphertext,d,n):
    resultado = ""
    for c in ciphertext:
        #descodificar o conjunto de  numeros
        l1,l2,l3 = descodificar((c**d) % n)
        #para cada um dos 3 numeros obtidos, converter cada um em caracteres
        resultado += converter(l1)
        resultado += converter(l2)
        resultado += converter(l3)
    return resultado

# ler ficheiro  
numeros = []
with open('2.txt') as f:
	while linha := f.readline():
		numero = int(linha)
		numeros.append(numero)
            
# Calculo da chave privada d com o inverso modular de (e mod t)
d = pow(e, -1,t)

# Decifrar tudo e obter o texto limpo
plaintext = decifrar(numeros,d,n)
print(plaintext)


