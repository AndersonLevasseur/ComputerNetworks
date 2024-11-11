# ASK BEFORE ADDING IMPORTS
from socket import * 
from ssl import *
from base64 import * 
 
NL = "\r\n"         # newline
OK_CODE = "250"     # OK message number
SMTP_SERVER  =  "smtp.gmail.com"  # use the links to look this up!
SSL_TLS_PORT =  "465"  # use the links to look this up!
# do not copy in the Base64 encodings of these 2 strings!!!
# use the Python library to derive the encoding from the normal strings
USERNAME = "betty.the.jasperson"       # your fake gmail account
PASSWD = "rwkw wqke ilzg insj"         # you can obscure this when you hand in your code
RECIPIENT = "lydiabingamon@cedarville.edu"
EMAIL_HEADER = f"""From: {USERNAME}@gmail.com
To: {RECIPIENT}
Reply-To: {USERNAME}@gmail.com
Subject: SMTP Email"""
MESSAGE = 'Do you want a cool picture?'
# create a clientSocket and then the sslSocket
# this requires you to use the wrap_ function a little differently
# than the example in the API -- play around with it and you"ll figure it out
context = create_default_context()
    #create clientSocket
clientSock = create_connection((SMTP_SERVER, SSL_TLS_PORT))
    #create sslSocket
sslSocket = context.wrap_socket(clientSock, server_hostname=SMTP_SERVER)
# print cipher being used
print(sslSocket.cipher())
# use these functions to send and recv
def send(s) :
    sslSocket.send(s.encode())
    print("SENT:" + NL + s)
    
def recv(s="") :
    s += sslSocket.recv(1024).decode()
    print("RCVD:" + NL + s)

# send hello command...beware of NL gotcha!
send("EHLO localhost" + NL)

# here the server sends two messages with a short time gap in-between.
# the first is a greeting and the second is a series of 250 messages. 
# make sure you have received a 250 message before you “speak” again.
# to accomplish this, create a loop to receive 1 byte at a time (do not use the
# recv function above) until you receive the string "250" 
# build the bytes you receive onto a string, and then call the recv() function   
# passing the string you"ve accumulated as an argument.
# after this, for the remainder of the script, use the recv() function above
def recv_singleByte() :
    return sslSocket.recv(1).decode()
s = ""
while "250" not in s:
    s += recv_singleByte()

recv(s)
# now that it is your turn in the dialogue “to speak” again...
# send login command because Google makes you authenticate...

send("AUTH LOGIN" + NL)
recv()

# now follow the login prompts...
send(b64encode(USERNAME.encode()).decode() + NL)
recv()
# now that you are authenticated, you can start the normal SMTP dialogue
send(b64encode(PASSWD.encode()).decode() + NL)
recv()

send(f"MAIL FROM: <" + USERNAME + "@gmail.com>" + NL)
recv()

send(f"RCPT TO: <{RECIPIENT}>" + NL)
recv()

send("DATA" + NL)
recv()

send(EMAIL_HEADER + NL)
send(MESSAGE + NL + '.' + NL)
recv()

# send quit command
send("QUIT")
# close connection
sslSocket.close()
