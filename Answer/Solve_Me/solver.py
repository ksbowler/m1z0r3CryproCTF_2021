import gmpy2
from Crypto.Util.number import *
import time
import math
import gmpy2
import sympy

### first

f = open("output.txt")
a = f.readlines()
n = int(a[0].split()[-1])
e = int(a[1].split()[-1])
c = int(a[2].split()[-1])
hint = int(a[3].split()[-1])

tmp, ch = gmpy2.iroot(hint+2*n,2)
assert ch
mtmp, ch = gmpy2.iroot(hint-2*n,2)
assert ch
pp = int(tmp)-int(mtmp)
p = pp//2
assert n%p == 0
q = n//p
print("p=",p)
print("q=",q)
phi = (p-1)*(q-1)
d = inverse(e,phi)
print("c=",c)
print("d=",d)
print("n=",n)
st = time.time()
m = pow(c,d,n)
gl = time.time()
print(long_to_bytes(m))
print(gl-st)

### second

msg = long_to_bytes(m).decode().split("\n")[1]
print(msg)

c,n = msg.split("e")
c = int(c)
n = int(n)
bits = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011, 24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 43112609]
for x in bits:
	p = pow(2,x)-1
	if n%p == 0:
		print("bits=",x)
		q = n//p
		break
print("finish factorize!")
print("p=",p)
print("q=",q)
phi = (p-1)*(q-1)
e = 65537
d = inverse(e,phi)
m = pow(c,d,n)
mes = long_to_bytes(m)
print(mes)
