from Crypto.Util.number import *

f = open("email.txt","rb")
a = f.readlines()
mes = a[0]+a[1]
print(mes)
m = bytes_to_long(mes)
g = open("private_key.txt")
p = int(g.readline().strip())
q = int(g.readline().strip())
n = p*q
assert m < n
e = 0x10001
c = pow(m,e,n)
hint = p**2+q**2
print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
print(f"hint = {hint}")
