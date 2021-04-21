 #Open up files and erase blank spaces
file = "tp2-ciphertexts.txt"

with open(file) as f:
		cipher=f.read()
		cipher1 = cipher.split("\n\n")
		
#print(cipher1)

#We split every cipher caracter by caracter

cipher2= []
for i in range(len(cipher1)):
    split = [cipher1[i][j:j + 1] for j in range(0, len(cipher1[i]), 1)]
    cipher2.append(split)
#print(cipher2)

#Converting to decimal
for i in range(len(cipher2)):
	for j in range(len(cipher2[i])):
        	cipher2[i][j] = ord(cipher2[i][j]) - 65
#print(cipher2)


#subtration of the cryptogram
for i in range(len(cipher2)-1):
	for j in range(i+1, len(cipher2)):
		c = 0
		temp = []
		for n in range(len(cipher2[i])):
			if (cipher2[i][n] - cipher2[j][n]) % 26 == 0:
				c = c + 1
				temp = [(i, j), c]
		print(temp)
print("Cipher 5 - Cipher 13 = 371 zeros")
print("cipher 5 e 13 encripted with same key")
