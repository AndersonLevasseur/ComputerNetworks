from socket import *
import os
import struct
import time
import select

# Utilize these constants where they belong in the code!
ICMP_ECHO_REQUEST =  8 # type 8 code 0
IP_ICMP_PROTOCOL  =  1
ICMP_ECHO_REPLY   =  0 # type 0 code 0
ICMP_ECHO_CODE    =  0 # type 0 code 0

def checksum(byteString):
    csum = 0
    countTo = (len(byteString) // 2) * 2 # floor division
    count = 0
    while count < countTo:
        thisVal = byteString[count+1] * 256 + byteString[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff 
        count = count + 2
        
    if countTo < len(byteString): # catches the last byte for odd length str
        csum = csum + byteString[len(byteString) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr, seqNum):
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        print("[*] Received packet of length:", len(recPacket))

        # ********************************************
        #Fetch the IP header data you need
        # Need - IP, TTL, Upper Layer ICMP?, Data, Valid checksum, echo reply?, 
        pack = recPacket.unpack("bbHHh")
        print(pack.at(2))
        check = pack.at(2) + checksum(recPacket)
        print(check)
        #Print IP data
        print()
        #Fetch the ICMP header data you need

        #Print ICMP data
        print()
        #Return total time elapsed in ms
        return time.time() - startedSelect
        # ********************************************

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID, seqNum):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum.
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seqNum)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    print(header + data)
    myChecksum = checksum(header + data)
    myChecksum = htons(myChecksum)
    
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, seqNum)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout, seqNum):
    icmp = getprotobyname("icmp")

    mySocket = socket(AF_INET, SOCK_RAW, icmp);

    myID = os.getpid() & 0xFFFF #Returns the current process id
    sendOnePing(mySocket, destAddr, myID, seqNum)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr, seqNum)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    #timeout=1 means: If one second goes by without a reply from the server,
    #the client assumes that either the client’s ping or the server’s pong is lost
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python")
    print("")
    #Send ping requests to a server separated by approximately one second
    for i in range(1,5) :
        print("[*] Sending ping", i, "...")
        delay = doOnePing(dest, timeout, i)
        print("[*] Delay:", delay, "ms")
        print() # printing blank line
        time.sleep(1)# one second
    print("Done Pinging " + dest)
 
    
ping("www.google.com")

        
