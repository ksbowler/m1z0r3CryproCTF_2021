import socketserver  
import socket, os
import binascii
from Crypto.Util.number import *
import random
import math
from my_secrets import flag, enc_msg

first = "Here you are.\n"
opt = "\n1) Get encrypted clue\n2) Encrypt your message\n3) Go up one floor\n4) Exit\n"
inv = "Invalid option!!\n"
invmsg = "Invalid your message!!\n"

def send_msg(s, msg):  
	enc = msg.encode()  
	s.send(enc)

def level1(s,mes):
	#7倍するやつ
	m = hex(bytes_to_long(mes.encode()))[2:]
	if len(m)%2 == 1: m = "0"+m
	send_msg(s,"\nNow, you are on the ground floor.\n")
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			enc = ""
			for i in range(0,len(m),2):
				val = (int(m[i:i+2],16)*7)%256
				val = hex(val)[2:]
				if len(val) == 1: val = "0"+val
				enc += val
			send_msg(s,enc+"\n")
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					ret = ""
					for i in range(0,len(your_msg),2):
						val = (int(your_msg[i:i+2],16)*7)%256
						val = hex(val)[2:]
						if len(val) == 1: val = "0"+val
						ret += val
					send_msg(s,first)
					send_msg(s,ret+"\n")
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the first floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)
	
def level2(s,mes):
	#1バイトの換字暗号
	m = hex(bytes_to_long(mes.encode()))[2:]
	if len(m)%2 == 1: m = "0"+m
	send_msg(s,"\nNow, you are on the first floor.\n")
	cha = [i for i in range(256)]
	random.shuffle(cha)
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			enc = ""
			for i in range(0,len(m),2):
				val = cha[int(m[i:i+2],16)]
				val = hex(val)[2:]
				if len(val) == 1: val = "0"+val
				enc += val
			send_msg(s,enc+"\n")
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					ret = ""
					for i in range(0,len(your_msg),2):
						val = cha[int(your_msg[i:i+2],16)]
						val = hex(val)[2:]
						if len(val) == 1: val = "0"+val
						ret += val
					send_msg(s,first)
					send_msg(s,ret+"\n")
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the second floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)

def level3(s,mes):
	#xorするやつ
	m = hex(bytes_to_long(mes.encode()))[2:]
	if len(m)%2 == 1: m = "0"+m
	send_msg(s,"\nNow, you are on the second floor.\n")
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			enc = ""
			for i in range(0,len(m),2):
				key = random.randrange(256)
				val = int(m[i:i+2],16)^key
				key = hex(key)[2:]
				if len(key) == 1: key = "0"+key
				val = hex(val)[2:]
				if len(val) == 1: val = "0"+val
				enc += key+val
			send_msg(s,enc+"\n")
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					ret = ""
					for i in range(0,len(your_msg),2):
						key = random.randrange(256)
						val = int(your_msg[i:i+2],16)^key
						key = hex(key)[2:]
						if len(key) == 1: key = "0"+key
						val = hex(val)[2:]
						if len(val) == 1: val = "0"+val
						ret += key+val
					send_msg(s,first)
					send_msg(s,ret+"\n")
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the third floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)

def level4(s,mes):
	#c = pow(m,e,p)のやつ
	m = bytes_to_long(mes.encode())
	e = 17
	while True:
		p = getPrime(256)
		d = inverse(e,p-1)
		if (e*d)%(p-1) == 1: break
	send_msg(s,"\nNow, you are on the third floor.\n")
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			enc = pow(m,e,p)
			enc = hex(enc)[2:]
			if len(enc)%2 == 1: enc = "0" + enc
			send_msg(s,enc+"\n")
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					send_msg(s,first)
					ret = pow(tmp,e,p)
					ret = hex(ret)[2:]
					if len(ret)%2 == 1: ret = "0" + ret
					send_msg(s,ret+"\n")
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the fourth floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)

def level5(s,mes):
	#nの素数が共通のやつ
	m = bytes_to_long(mes.encode())
	e = 23
	while True:
		p,q,r = getPrime(256),getPrime(256),getPrime(256)
		if math.gcd((p-1)*(q-1),e) == 1 and math.gcd((r-1)*(q-1),e) == 1 and math.gcd((p-1)*(r-1),e) == 1:
			primes = [p,q,r]
			break

	send_msg(s,"\nNow, you are on the fourth floor.\n")
	cnt = 0
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			if cnt%3 == 0: n = primes[0]*primes[1]
			elif cnt%3 == 1: n = primes[0]*primes[2]
			else: n = primes[2]*primes[1]
			c = pow(m,e,n)
			enc = hex(c)[2:]
			if len(enc)%2 == 1: enc = "0" + enc
			send_msg(s,enc+"\n")
			cnt += 1
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					send_msg(s,first)
					if cnt%3 == 0: n = primes[0]*primes[1]
					elif cnt%3 == 1: n = primes[0]*primes[2]
					else: n = primes[2]*primes[1]
					c = pow(tmp,e,n)
					ret = hex(c)[2:]
					if len(ret)%2 == 1: ret = "0" + ret
					send_msg(s,ret+"\n")
					cnt += 1
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the fifth floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)
		#cnt += 1

def level6(s,mes):
	#Common Modulus Attackのやつ
	m = bytes_to_long(mes.encode())
	while True:
		p = getPrime(256)
		q = getPrime(256)
		e1 = getPrime(8)
		e2 = getPrime(8)
		if e1 != e2 and math.gcd(e1,(p-1)*(q-1)) == 1 and math.gcd(e2,(p-1)*(q-1)) == 1:
			n = p*q
			break
	send_msg(s,"\nNow, you are on the fifth floor.\n")
	cnt = 0
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			if cnt%2 == 0: c = pow(m,e1,n)
			else: c = pow(m,e2,n)
			enc = hex(c)[2:]
			if len(enc)%2 == 1: enc = "0" + enc
			send_msg(s,enc+"\n")
			cnt += 1
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					send_msg(s,first)
					if cnt%2 == 0: c = pow(tmp,e1,n)
					else: c = pow(tmp,e2,n)
					ret = hex(c)[2:]
					if len(ret)%2 == 1: ret = "0" + ret
					send_msg(s,ret+"\n")
					cnt += 1
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the sixth floor.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)
		#cnt += 1

def level7(s,mes):
	#Hastadのやつ
	m = bytes_to_long(mes.encode())
	n_list = []
	prime_list = []
	e = 7
	while len(n_list) < 7:
		p = getPrime(256)
		q = getPrime(256)
		if math.gcd(e,(p-1)*(q-1)) == 1:
			if p in prime_list: continue
			if q in prime_list: continue
			if m**e < p*q: continue
			prime_list.append(p)
			prime_list.append(q)
			n = p*q
			n_list.append(n)
	send_msg(s,"\nNow, you are on the sixth floor.\n")
	cnt = 0
	while True:
		send_msg(s,opt)
		send_msg(s,">>> ")
		recv = s.recv(4096).decode().strip()
		if recv == "1":
			send_msg(s,first)
			c = pow(m,e,n_list[cnt%7])
			enc = hex(c)[2:]
			if len(enc)%2 == 1: enc = "0" + enc
			send_msg(s,enc+"\n")
			cnt += 1
		elif recv == "2":
			send_msg(s,"Your message (hex): ")
			your_msg = s.recv(4096).decode().strip()
			if len(your_msg)%2 == 1: send_msg(s,invmsg)
			else:
				try:
					tmp = int(your_msg,16)
					if tmp < 0:
						send_msg(s,invmsg)
						continue
					send_msg(s,first)
					c = pow(tmp,e,n_list[cnt%7])
					ret = hex(c)[2:]
					if len(ret)%2 == 1: ret = "0" + ret
					send_msg(s,ret+"\n")
					cnt += 1
				except: send_msg(s,invmsg)
				
				
		elif recv == "3":
			send_msg(s,"OK. Go to the rooftop.\n")
			return True

		elif recv == "4":
			send_msg(s,"See you.\n")
			return False
		else: send_msg(s,inv)
		#cnt += 1

def Rooftop(s):
	send_msg(s,"\nNow, you are on rooftop.\n")
	send_msg(s,"Input a flag (string)\n")
	send_msg(s,">>> ")
	usr_flag = s.recv(4096).decode().strip()
	if flag == usr_flag:
		send_msg(s,"Correct! A helicopter finds you!\n")
	else:
		send_msg(s,"Incorrect. You vanish into the night.\n")
	return

def main(s):
	#print("Func main")
	#recv = s.recv(4096).decode().strip()
	welcome = "Welcome to mytery house.\nThe exit was closed for good.\nYou should go to rooftop to esape from here.\nBe careful, once you go upstairs, you cannot go back.\nIf you go to the rooftop, ou can wave a flag and a helicoper will find you.\nBut the flag is broken.\nIts frgments are on each floor.\nYou shoud fix them.\nIf you put them back together, one pice is missing.\nYou will have to make up for it.\n\n"
	send_msg(s, welcome)
	ch = level1(s,enc_msg[0])
	if not ch: return
	ch = level2(s,enc_msg[1])
	if not ch: return
	ch = level3(s,enc_msg[2])
	if not ch: return
	ch = level4(s,enc_msg[3])
	if not ch: return
	ch = level5(s,enc_msg[4])
	if not ch: return
	ch = level6(s,enc_msg[5])
	if not ch: return
	ch = level7(s,enc_msg[6])
	if not ch: return

	Rooftop(s)
	return

class TaskHandler(socketserver.BaseRequestHandler):  
	def handle(self):  
		main(self.request)  

if __name__ == '__main__':  
	socketserver.ThreadingTCPServer.allow_reuse_address = True  
	server = socketserver.ThreadingTCPServer(('127.0.0.1', 4500), TaskHandler)  
	server.serve_forever()
