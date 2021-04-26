#!/usr/bin/python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES
import sys
# import relevant cryptographic primitives
backend=default_backend()
AES_BLOCK_LENGTH = 16 # bytes
AES_KEY_LENGTH = 32 # bytes
iv=b'\x87\x93\x96\x07B\xa9\xee\xffo^\xa1`\x89uYH'
key=b"\x889 \x8f\xd9'\x90S\xc2\xae\x98\x02\x8d\x13\xa1\x8e\x97c\xf4i2\xaa\xa3<\x8f\xf4$\x8dUD\xabm"
msg=b'\xb3\xf8L\xe5\x18\x10\xc3\x01\xc5`\x08X\xdaM+O\x8a7y\xa7\xdaO=\xb1(\x1e|xF\xf4\xd0\xfa'
bloco1=msg[:16]
bloco2=msg[-16:]



# Insecure CBCMAC.
def cbcmac(key, msg):
  if not _validate_key_and_msg(key, msg): return False
  XOR=xor(msg,iv)
  cipher = Cipher(algorithms.AES(key), modes.CBC(XOR), backend)
  encryptor = cipher.encryptor()
  tag = encryptor.update(bloco2) + encryptor.finalize()
  print("Sou a primeira tag criada:\n",tag)
  return tag

  # Implement CBCMAC with either a random IV, or with a tag consisting of all
  # ciphertext blocks.

  # return tag

def verify(key, msg, tag):
  if not _validate_key_and_msg(key, msg): return False
  new_mensagem= b'\x8a7y\xa7\xdaO=\xb1(\x1e|xF\xf4\xd0\xfa'
  new_msg= (new_mensagem+bloco2)
  xor1= xor(iv, new_msg)  
  xor2= xor(xor1,new_msg)
  print(xor2)
  tag_verify=xor2
  if tag_verify==tag:
    return True
  else:
    return False
  # If parameters are valid, then recalculate the mac.
  # Implement this recalculation.

  # return True/False
def xor(data, key): 
    return bytes([a ^ b for a, b in zip(data, key)])


# Receives a pair consisting of a message, and a valid tag.
# Outputs a forged pair (message, tag), where message must be different from the
# received message (msg).
# ---> Note that the key CANNOT be used here! <---
def produce_forgery(msg, tag):
  # Implement a forgery, that is, produce a new pair (m, t) that fools the
  # verifier.
  new_mensagem= b'\x8a7y\xa7\xdaO=\xb1(\x1e|xF\xf4\xd0\xfa'
  new_msg= (new_mensagem+bloco2)
  xor1= xor(iv, new_msg)  
  xor2= xor(xor1,new_msg)
  new_tag=xor2
  return(new_msg, new_tag)



  

def check_forgery(key, new_msg, new_tag, original_msg):
  if new_msg == original_msg:
    print("Having the \"forged\" message equal to the original " +
        "one is not allowed...")
    return False

  if verify(key, new_msg, new_tag) == True:
    print("MAC successfully forged!")
    return True
  else:
    print("MAC forgery attempt failed!")
    return False

def _validate_key_and_msg(key, msg):
  if type(key) is not bytes:
    print("Key must be array of bytes!")
    return False
  elif len(key) != AES_KEY_LENGTH:
    print("Key must be have %d bytes!" % AES_KEY_LENGTH)
    return False
  if type(msg) is not bytes:
    print("Msg must be array of bytes!")
    return False
  elif len(msg) != 2*AES_BLOCK_LENGTH:
    print("Msg must be have %d bytes!" % (2*AES_BLOCK_LENGTH))
    return False
  return True

def main():
  tag = cbcmac(key, msg)
  # Should print "True".
  print(verify(key, msg, tag))


  (mprime, tprime) = produce_forgery(msg, tag)


  # GOAL: produce a (message, tag) that fools the verifier.
  check_forgery(key, mprime, tprime, msg)

if __name__ == '__main__':
  main()
