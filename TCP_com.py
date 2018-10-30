import socket
import sys
import time
def init_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "PhysicsRuns0,Initialize"
    sock.sendto(MESSAGE, ("192.168.133.10", 8000))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Initialize: received message:", data
    time.sleep(5)

def config_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "PhysicsRuns0,Configure,FQNETConfig"
    sock.sendto(MESSAGE, ("192.168.133.10", 8000))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Configure: received message:", data
    time.sleep(5)

def start_ots(run_number,Delay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "PhysicsRuns0,Start, %d" % (run_number) 
    sock.sendto(MESSAGE, ("192.168.133.10", 8000))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Start: received message:", data
    if Delay: time.sleep(5)

def stop_ots(Delay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "PhysicsRuns0,Stop"
    sock.sendto(MESSAGE, ("192.168.133.10", 8000))
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "Stop: received message:", data
    if Delay: time.sleep(5)
