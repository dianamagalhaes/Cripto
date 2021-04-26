#!/usr/bin/python

import os, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
key=b'\x85/\xffz\x8b\xd0\x02\xc5X&\xd6\xc4|D\xa27N\x9c\x11\xbeuWm\xb1\xf7\xf7\xd7W\x86W\x8e\x9b'
hmackey=b'\xf0m\xf75\x9e\xa5\xad\xc6\xb8\xc0Q1\x9c\xb0\xca\xf0\x10\xaf\x00\xab\xf4\x9c\x10\x82\xb4\xde\x0cF2\x0e\x07\x05'


# Gera o nonce no terminal e guarda igual no enc.py e no dec.py
nonce = b'\xbb\xa6\\\xa0\xc1K\xca\xe8B\x9f \x05W\xf9\x9aP'

data={}

def rff(nomeficheiro):
  with open(nomeficheiro, 'rb') as f:
    return f.read()

def etm():

  # Inverte o modo encrypt-then-mac e faz print da mensagem descodificada
  
  data = rff("dados-etm.dat") # lê o ficheiro dados-etm.dat

  tag = data[-32:] # extrai a tag
  ct = data[:-32] # extrai o criptograma

  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  
  hh = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  hh.update(ct) # faz MAC do criptograma
  hh.verify(tag) # verifica a tag

  # se a tag estiver correta, decifra o criptograma.
  decryptor = cipher.decryptor() # vai buscar o algoritmo de decifragem
  dec = decryptor.update(ct) # decifra o criptograma
  
  print(dec.decode("utf-8")) # faz print da mensagem

def eam():
  data = rff("dados-eam.dat")
  ct=data[:-32]
  mac=data[-32:]
  
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  
  decryptor = cipher.decryptor() # vai buscar o algoritmo de decifragem
  dec = decryptor.update(ct)
  
  hh = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  hh.update(ct)
  hh.verify(mac)
  #o texto cifrado são os primeiros 32 bytes
  #decifrar o texto cifrado
  

  #verificar a tag
  
  print(dec.decode("utf-8"))
  # Inverter aqui o modo encrypt-and-mac
  # E fazer print da mensagem descodificada

def mte():
  data = rff("dados-mte.dat")    
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  mte = cipher.decryptor().update(data)
  mac = mte[-32:]
  #o texto limpo sao os 32 primeiros bytes
  mte = mte[:-32]
  h = hmac.HMAC(hmackey, hashes.SHA256(),backend=default_backend())
  h.update(mte)
  #verificar a tag
  h.verify(mac)
  
  print(mte)
  # Inverter aqui o modo mac-then-encrypt
  # E fazer print da mensagem descodificada

def main():

  if len(sys.argv) != 2:
    print("Please provide one of: eam, etm, mte")
  elif sys.argv[1] == "eam":
    eam()
  elif sys.argv[1] == "etm":
    etm()
  elif sys.argv[1] == "mte":
    mte()
  else:
    print("Please provide one of: eam, etm, mte")

if __name__ == '__main__':
  main()
