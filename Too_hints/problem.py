from Crypto.Util.number import *
import random
flag = open("flag.txt","rb").read()
while True:
	p = getPrime(256)
	q = getPrime(256)
	phi = (p-1)*(q-1)
	n = p*q
	e = getRandomNBitInteger(20)
	d = inverse(e,phi)
	if (e*d)%phi == 1:
		d1 = d%(p-1)
		d2 = d%(q-1)
		if isPrime(d2):
			break
t1 = (d1+e)
t2 = (d2*e)
t3 = (d1*e)
t4 = (d2+e)
print("n=",p*q)
print("hint1=",(t1*t2)%n)
print("hint2=",(t3*t4)%n)
print("ct=",pow(bytes_to_long(flag),e,n))
