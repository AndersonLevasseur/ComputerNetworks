# Hardcoded for 2 users, 4 number code 

C1 = [1,1,-1,1]
C2 = [-1,1,-1,-1]

ENCODING_MAP = {(1, 1, 1, 1, 1)      : 'A',
                (1, 1, 1, 1, -1)     : 'B',
                (1, 1, 1, -1, 1)     : 'C',
                (1, 1, 1, -1, -1)    : 'D',
                (1, 1, -1, 1, 1)     : 'E',
                (1, 1, -1, 1, -1)    : 'F',
                (1, 1, -1, -1, 1)    : 'G',
                (1, 1, -1, -1, -1)   : 'H',
                (1, -1, 1, 1, 1)     : 'I',
                (1, -1, 1, 1, -1)    : 'J',
                (1, -1, 1, -1, 1)    : 'K',
                (1, -1, 1, -1, -1)   : 'L',
                (1, -1, -1, 1, 1)    : 'M',
                (1, -1, -1, 1, -1)   : 'N',
                (1, -1, -1, -1, 1)   : 'O',
                (1, -1, -1, -1, -1)  : 'P',
                (-1, 1, 1, 1, 1)     : 'Q',
                (-1, 1, 1, 1, -1)    : 'R',
                (-1, 1, 1, -1, 1)    : 'S',
                (-1, 1, 1, -1, -1)   : 'T',
                (-1, 1, -1, 1, 1)    : 'U',
                (-1, 1, -1, 1, -1)   : 'V',
                (-1, 1, -1, -1, 1)   : 'W',
                (-1, 1, -1, -1, -1)  : 'X',
                (-1, -1, 1, 1, 1)    : 'Y',
                (-1, -1, 1, 1, -1)   : 'Z',
                (-1, -1, 1, -1, 1)   : ' ',
                (-1, -1, 1, -1, -1)  : ',',
                (-1, -1, -1, 1, 1)   : '.',
                (-1, -1, -1, 1, -1)  : "'",
                (-1, -1, -1, -1, 1)  : '?',
                (-1, -1, -1, -1, -1) : '!'}

in_file = open("PA4_transmission.txt", "r").readline()

M1 = []
M2 = []
i = 0
j = 1
user_1_char = 0
user_2_char = 0
mess_1 = ()
mess_2 = ()

neg = False
kar = 0
for char in in_file:
    kar += 1
    if char == ",":
        continue
    elif char == "-":
        neg = True
        continue
    
    int_char = int(char)
    if neg:
        int_char *= -1
        neg = False    
    
    user_1_char += int_char * C1[i]
    user_2_char += int_char * C2[i]
    
    i += 1
    if i % 4 == 0:
        mess_1 += (int(user_1_char / 4),)
        mess_2 += (int(user_2_char / 4),)
        user_1_char = 0
        user_2_char = 0
        i = 0
        j += 1

    if j % 6 == 0:
        M1.append(mess_1)
        mess_1 = ()
        M2.append(mess_2)
        mess_2 = ()
        j = 1

def intToStr(m1):
    message = ""
    if len(m1) == 5:
        message += str(ENCODING_MAP.get(m1))
    return message

message = ""
for char_tuple in M1:
    message += intToStr(char_tuple)    
print(f"User 1 Message: {message}")

message = ""

for char_tuple in M2:
    message += intToStr(char_tuple)    
print(f"User 2 Message: {message}")
