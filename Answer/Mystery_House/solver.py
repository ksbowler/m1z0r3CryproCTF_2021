from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
import math
import gmpy2
import random
from sympy.ntheory.modular import crt
import base64

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

def gcdExtended(a, b): 
    # Base Case 
    if a == 0 :  
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y
	
#HOSTはIPアドレスでも可
HOST, PORT = "6.tcp.ngrok.io", 10919
s, f = sock(HOST, PORT)
for _ in range(10): print(read_until(f))

# --level1--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
enc = read_until(f).strip()
m1 = ""
for i in range(0,len(enc),2):
	tmp = (int(enc[i:i+2],16)*inverse(7,256))%256
	m1 += chr(tmp)
print("Message 1 =",m1)
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f))

# --level2--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
"""
s.send(b"1\n")
print(read_until(f)) # Here you are
enc = read_until(f).strip()
m2 = ""
cha = []
for x in range(256):
	print("x =",x)
	for _ in range(5): read_until(f) # option message
	sen = hex(x)[2:]
	if len(sen) == 1: sen = "0"+sen
	read_until(f,">>> ")
	s.send(b"2\n")
	read_until(f,"(hex): ")
	s.send(sen.encode()+b"\n")
	read_until(f) # Here you are
	t = read_until(f).strip()
	cha.append(t)

for i in range(0,len(enc),2):
	for j in range(len(cha)):
		if enc[i:i+2] == cha[j]:
			m2 += chr(j)
			break
	
print("Message 2 =",m2)
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
"""
s.send(b"3\n")
print(read_until(f))

m2 = "RlZXV5aXzbGth"

# --level3--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
enc = read_until(f).strip()
m3 = ""
for i in range(0,len(enc),4):
	tmp = int(enc[i:i+2],16)^int(enc[i+2:i+4],16)
	m3 += chr(tmp)
print("Message 3 =",m3)


for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f))

# --level4--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
enc = int(read_until(f).strip(),16)

# find e
for _ in range(5): read_until(f) # option message
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(b"02\n")
read_until(f) # Here you are
t = int(read_until(f).strip(),16)
e = 1
while True:
	if 2**e == t:
		print("find!")
		print("e =",e)
		break
	e += 1

# find p
for _ in range(5): read_until(f) # option message
x1 = random.randrange(2**200)
sen = hex(x1)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t1 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x2 = random.randrange(2**200)
sen = hex(x2)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t2 = int(read_until(f).strip(),16)
p = math.gcd(x1**e-t1,x2**e-t2)
while not isPrime(p):
	for _ in range(5): read_until(f) # option message
	x = random.randrange(2**200)
	sen = hex(x)[2:]
	if len(sen)%2 == 1: sen = "0"+sen
	read_until(f,">>> ")
	s.send(b"2\n")
	read_until(f,"(hex): ")
	s.send(sen.encode()+b"\n")
	read_until(f) # Here you are
	t = int(read_until(f).strip(),16)
	p = math.gcd(p,x**e-t)

#find mes
d = inverse(e,p-1)
m4 = pow(enc,d,p)
m4 = long_to_bytes(m4).decode()
print("Message 4 =",m4)
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f))              

# --level5--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c1 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c2 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c3 = int(read_until(f).strip(),16)

# find e
for _ in range(5): read_until(f) # option message
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(b"02\n")
read_until(f) # Here you are
t = int(read_until(f).strip(),16)
e = 1
while True:
	if 2**e == t:
		print("find!")
		print("e =",e)
		break
	e += 1

# find p,q,r
for _ in range(5): read_until(f) # option message
x1 = random.randrange(2**200)
sen = hex(x1)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t1 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x2 = random.randrange(2**200)
sen = hex(x2)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t2 = int(read_until(f).strip(),16)
p = math.gcd(x1**e-t1,x2**e-t2)

for _ in range(5): read_until(f) # option message
x3 = random.randrange(2**200)
sen = hex(x3)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t3 = int(read_until(f).strip(),16)
q = math.gcd(x1**e-t1,x3**e-t3)
r = math.gcd(x3**e-t3,x2**e-t2)
if isPrime(p) and isPrime(q) and isPrime(r):
	print("Find all primes")
else:
	cnt = 0
	while True:
		for _ in range(5): read_until(f) # option message
		x3 = random.randrange(2**200)
		sen = hex(x3)[2:]
		if len(sen)%2 == 1: sen = "0"+sen
		read_until(f,">>> ")
		s.send(b"2\n")
		read_until(f,"(hex): ")
		s.send(sen.encode()+b"\n")
		print(read_until(f)) # Here you are
		t3 = int(read_until(f).strip(),16)
		if cnt%3==0: p = math.gcd(p,x3**e-t3)
		elif cnt%3==1: q = math.gcd(q,x3**e-t3)
		else: r = math.gcd(r,x3**e-t3)
		if isPrime(p) or isPrime(q) or isPrime(r):
			print("Find all primes")
			break
		cnt += 1
print("primes =",[p,q,r])
print("ct =",[c1,c2,c3])
print("e=",e)

#find mes
d1 = inverse(e,(p-1)*(q-1))
d2 = inverse(e,(p-1)*(r-1))
d3 = inverse(e,(r-1)*(q-1))
c_candi = [c1,c2,c3]
d_candi = [d1,d2,d3]
n_candi = [p*q,p*r,q*r]
mes_candi = []
for i in range(3):
	for j in range(3):
		for k in range(3):
			tm = pow(c_candi[i],d_candi[j],n_candi[k])
			tm = long_to_bytes(tm)
			mes_candi.append(tm)
"""
tm = pow(c1,d1,p*q)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c1,d2,p*r)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c1,d3,q*r)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c2,d1,p*q)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c2,d2,p*r)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c2,d3,q*r)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c3,d1,p*q)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c3,d2,p*r)
tm = long_to_bytes(tm)
mes_candi.append(tm)
tm = pow(c3,d3,r*q)
tm = long_to_bytes(tm)
mes_candi.append(tm)
"""
for tm in mes_candi:
	print(tm)
	if len(tm) == 13:
		m5 = tm.decode()
		print("Message 5 =",m5)
		break
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f)) 

# --level6--
for _ in range(2): print(read_until(f)) # arrival message
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c1 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c2 = int(read_until(f).strip(),16)


# find e
for _ in range(5): read_until(f) # option message
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(b"02\n")
read_until(f) # Here you are
t = int(read_until(f).strip(),16)
e1 = 1
while True:
	if 2**e1 == t:
		print("find!")
		print("e1 =",e1)
		break
	e1 += 1
for _ in range(5): read_until(f) # option message
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(b"02\n")
read_until(f) # Here you are
t = int(read_until(f).strip(),16)
e2 = 1
while True:
	if 2**e2 == t:
		print("find!")
		print("e2 =",e2)
		break
	e2 += 1
# find n
for _ in range(5): read_until(f) # option message
x1 = random.randrange(2**200)
sen = hex(x1)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t1 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x2 = random.randrange(2**200)
sen = hex(x2)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t2 = int(read_until(f).strip(),16)
n = math.gcd(x1**e1-t1,x2**e2-t2)

e_list = [e1,e2]
for y in range(20):
	for _ in range(5): read_until(f) # option message
	x3 = random.randrange(2**200)
	sen = hex(x3)[2:]
	if len(sen)%2 == 1: sen = "0"+sen
	read_until(f,">>> ")
	s.send(b"2\n")
	read_until(f,"(hex): ")
	s.send(sen.encode()+b"\n")
	read_until(f) # Here you are
	t3 = int(read_until(f).strip(),16)
	n = math.gcd(n,x3**e_list[y%2]-t3)

#find mes
gc,x,y = gcdExtended(e1,e2)
print(gc,x,y)
print(c1,c2)
print(n)
if x < 0:
	m6 = (pow(inverse(c1,n),-x,n)*pow(c2,y,n))%n
else:
	m6 = (pow(inverse(c2,n),-y,n)*pow(c1,x,n))%n
print(m6)
print(long_to_bytes(m6))
m6 = long_to_bytes(m6).decode()
print("Message 6 =",m6)
	
for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f)) 


# --level7--
for _ in range(2): print(read_until(f)) # arrival message
# find e
for _ in range(5): read_until(f) # option message
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(b"02\n")
print(read_until(f)) # Here you are
t = int(read_until(f).strip(),16)
e = 1
while True:
	if 2**e == t:
		print("find!")
		print("e =",e)
		break
	e += 1

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c1 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c2 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c3 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c4 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c5 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c6 = int(read_until(f).strip(),16)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"1\n")
print(read_until(f)) # Here you are
c7 = int(read_until(f).strip(),16)

# find n_list

for _ in range(5): read_until(f) # option message
x1 = random.randrange(2**200)
sen = hex(x1)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t1 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x2 = random.randrange(2**200)
sen = hex(x2)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t2 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x3 = random.randrange(2**200)
sen = hex(x3)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t3 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x4 = random.randrange(2**200)
sen = hex(x4)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t4 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x5 = random.randrange(2**200)
sen = hex(x5)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t5 = int(read_until(f).strip(),16)


for _ in range(5): read_until(f) # option message
x6 = random.randrange(2**200)
sen = hex(x5)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t6 = int(read_until(f).strip(),16)

for _ in range(5): read_until(f) # option message
x7 = random.randrange(2**200)
sen = hex(x5)[2:]
if len(sen)%2 == 1: sen = "0"+sen
read_until(f,">>> ")
s.send(b"2\n")
read_until(f,"(hex): ")
s.send(sen.encode()+b"\n")
read_until(f) # Here you are
t7 = int(read_until(f).strip(),16)
print("t7 =",t7)
n_list = [x1**e-t1,x2**e-t2,x3**e-t3,x4**e-t4,x5**e-t5,x6**e-t6,x7**e-t7]

for cnt in range(140):
	print("cnt =",cnt)
	for _ in range(5): read_until(f) # option message
	x = random.randrange(2**200)
	sen = hex(x)[2:]
	if len(sen)%2 == 1: sen = "0"+sen
	read_until(f,">>> ")
	s.send(b"2\n")
	read_until(f,"(hex): ")
	s.send(sen.encode()+b"\n")
	read_until(f) # Here you are
	t = int(read_until(f).strip(),16)
	n_list[cnt%7] = math.gcd(n_list[cnt%7],x**e-t) 

print(n_list,[c1,c2,c3,c4,c5,c6,c7])
mes5,large_n = crt(n_list,[c1,c2,c3,c4,c5,c6,c7])
print(mes5,large_n)
m7,ch = gmpy2.iroot(mes5,e)
print(m7,ch)

print(m7)
print(long_to_bytes(m7))
m7 = long_to_bytes(m7).decode()
print("Message 7 =",m7)

for _ in range(5): print(read_until(f)) # option message
print(read_until(f,">>> "))
s.send(b"3\n")
print(read_until(f)) 

#--rooftop--
print(read_until(f))
mes = m1+m2+m3+m4+m5+m6+m7
enc = ""
print(mes)
for i in range(len(mes)):
	enc += mes[(81*i)%len(mes)]
enc += "="
print(enc)
flag = base64.b64decode(enc.encode())
print(flag)
print(read_until(f))
print(read_until(f,">>> "))
s.send(flag+b"\n")
print(read_until(f))

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

