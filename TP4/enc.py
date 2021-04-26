import os, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from getpass import getpass
key=b'\x85/\xffz\x8b\xd0\x02\xc5X&\xd6\xc4|D\xa27N\x9c\x11\xbeuWm\xb1\xf7\xf7\xd7W\x86W\x8e\x9b'
hmackey=b'\xf0m\xf75\x9e\xa5\xad\xc6\xb8\xc0Q1\x9c\xb0\xca\xf0\x10\xaf\x00\xab\xf4\x9c\x10\x82\xb4\xde\x0cF2\x0e\x07\x05'

# mesmo nonce
nonce = b'\xbb\xa6\\\xa0\xc1K\xca\xe8B\x9f \x05W\xf9\x9aP'
msg = b"Isto e uma mensagem nao muito secreta"

def w2f(nomeficheiro, data):
  with open(nomeficheiro, 'wb') as f:
    f.write(data)

def etm():
  # Implementar aqui o modo encrypt-then-mac
  #Utilizar ChaCha20 para cifrar a mensagem 
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor()
  ct = encryptor.update(msg) + encryptor.finalize()

  #gerar a Mac para adicionar à mensagem cifrada
  h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  h.update(ct)
  tag=h.finalize()

  data=ct+tag
  w2f("dados-etm.dat", data)


def mte():
  # Implementar aqui o modo mac-then-encrypt

  hh = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  hh.update(msg)
  tag = hh.finalize()

  mt = msg+tag
  
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor()

  ct = encryptor.update(mt) + encryptor.finalize()

  dados = ct

  w2f("dados-mte.dat", ct)
    


def eam():
  # Implementar aqui o modo encrypt-then-mac
  #Utilizar ChaCha20 para cifrar a mensagem 
  algorithm = algorithms.ChaCha20(key, nonce)
  cipher = Cipher(algorithm, mode=None, backend=default_backend())
  encryptor = cipher.encryptor()
  ct = encryptor.update(msg) + encryptor.finalize()

  #gerar a Mac para adicionar à mensagem cifrada
  h = hmac.HMAC(hmackey, hashes.SHA256(), backend=default_backend())
  h.update(ct)
  tag=h.finalize()

  data=ct+tag
  w2f("dados-eam.dat", data)


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
