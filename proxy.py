import thread
import socket
import time
from urlparse import urlparse

HOST='127.0.0.1'
PORT=8080
BUFMAX=8192


def proxy(conn, addr):
		
		
	packet=conn.recv(BUFMAX)
		
			
	while True:
	
		if(packet.find('HTTP') == -1):
			continue
		host=packet.split('\r\n')
		dest=host[0].split(' ')
	
		if(dest[1].find("http") != -1):
			dest_domain=urlparse(dest[1]).hostname
			if( urlparse(dest[1]).port == None):
				p=80
			else:
				p= urlparse(dest[1]).port
		
		else: 
	
			if(dest[1].find(":") == -1):
				dest_domain=dest[1]
				p=80
			else:
				a=dest[1].split(":")
				dest_domain=a[0]
				p=int(a[1])
		
		dest_ip=socket.gethostbyname(dest_domain)
		

		c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		c.connect((dest_ip,p))
	
		
		
		c.send(packet)
			
		while True:	
			data=c.recv(BUFMAX)		
			
			time.sleep(1)
			
			if(len(data)>0):
				conn.send(data)
				time.sleep(1)
				continue
			
			conn.close()
			c.close()
			break
	            

			
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
   
while True:
	
	conn, addr=s.accept()
	
	time.sleep(1)
	thread.start_new_thread(proxy,(conn,addr))
	continue