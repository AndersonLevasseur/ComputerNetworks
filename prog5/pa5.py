#based on code from https://github.com/Vinay609/Two-Player-Pong
import os, pygame, sys, random, socket, struct
    
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
        
    if ball.right <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
        
    if ball.left >= width:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top- player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
        
    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

def player_animation():
    player.y += player_speed
    
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height

def opponent_animation():
    opponent.y += opponent_speed
    
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height

def ball_start():
    global ball_speed_y, ball_speed_x, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (width//2, height//2)

    if current_time - score_time < 1000:
        number_three = game_font.render("3",False,light_grey)
        screen.blit(number_three,(width//2 - 5,height//2 + 30))
    if 1000 < current_time - score_time < 2000:
        number_two = game_font.render("2",False,light_grey)
        screen.blit(number_two,(width//2 - 5,height//2 + 30))
    if 2000 < current_time - score_time < 3000:
        number_one = game_font.render("1",False,light_grey)
        screen.blit(number_one,(width//2 - 5,height//2 + 30))

    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 4 * random.choice((-1,1))
        ball_speed_x = 4 * random.choice((-1,1))
        score_time = None


CLIENT_CONNECTED = False
#global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
print(sys.argv[0])
if len(sys.argv) < 2: 
    print('starting server...')
    #NOTE: giving a 0 port, allows the socket library to use a randomly selected AND open port
    serverPort = 0
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((socket.gethostbyname(socket.gethostname()), serverPort))
    print('connect client by starting: ')
    print(sys.argv[0], str(serverSocket.getsockname()[0]) + ":" + str(serverSocket.getsockname()[1]))

    WINDOW_TITLE = "Pong SERVER " + str(serverSocket.getsockname()[0]) + ":" + str(serverSocket.getsockname()[1])
    SERVER = True
    CLIENT_CONNECTED = False
elif len(sys.argv) < 3:
    print('starting server...')    
    ip_port = sys.argv[1].split(':')
    serverIP = ip_port[0]
    serverPort = int(ip_port[1])

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #The client will quit abruptly if it doesn't receive a datagram from the socket in 0.5s
    clientSocket.settimeout(0.5)

    
    WINDOW_TITLE = "Pong CLIENT"
    SERVER = False

pygame.init()
clock = pygame.time.Clock()
    
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(WINDOW_TITLE)

ball = pygame.Rect(width//2 - 7, height//2 - 7, 15, 15)
player = pygame.Rect(width - 10, height//2 - 35, 5, 70)
opponent = pygame.Rect(5, height//2 - 35, 5, 70)

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 6 * random.choice((-1,1))
ball_speed_y = 6 * random.choice((-1,1))
player_speed = 0
opponent_speed = 0

player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None,25)

score_time = True

INITIALIZE = True
seq_num_send = 0
seq_num_rec = 0

while True:
    #Get Keyboard Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
                            
            if event.key == pygame.K_DOWN:
                player_speed += 5
            if event.key == pygame.K_UP:
                player_speed -= 5
                
        if event.type == pygame.KEYUP:
                            
            if event.key == pygame.K_DOWN:
                player_speed -= 5
            if event.key == pygame.K_UP:
                player_speed += 5
    
    
    if SERVER:
        if not CLIENT_CONNECTED: #only display waiting message first time we get here
            screen.fill(bg_color) # clear screen
            player_text = game_font.render("waiting for client to connect", False, light_grey)
            screen.blit(player_text,(345,235))
            pygame.display.flip()
            CLIENT_CONNECTED = True
        

        #handle server messaging here
        if INITIALIZE:
            data, client = serverSocket.recvfrom(1024)
            seed = pygame.time.get_ticks()
            random.seed(seed)
            serverSocket.sendto(str(-1).encode() + ",".encode() + str(seed).encode(), client)
            serverSocket.settimeout(.001)
            INITIALIZE = False
        
        try:
            data, client = serverSocket.recvfrom(1024)
            rec = data.decode()
            if seq_num_rec <= int(rec.split(',')[0]):
                seq_num_rec, opponent_speed = map(int, data.decode().split(','))
                seq_num_rec += 1
            elif int(rec.split(',')[0]) == -1:
                seed = pygame.time.get_ticks()
                random.seed(seed)
                serverSocket.sendto(str(-1).encode() + ",".encode() + str(seed).encode(), client)        
            else:
                print(seq_num_rec, ":", int(rec.split(',')[0]), "not equal")
            while True:
                serverSocket.recvfrom(1024)
        except:
            print(seed)

        data = str(seq_num_send) + "," + str(player_score) + "," + str(opponent_score) + "," + str(player_speed)
        seq_num_send += 1
        serverSocket.sendto(data.encode(), client)
    else:
        #handle client messaging here
        data = str(seq_num_send) + "," + str(player_speed)
        seq_num_send += 1
        clientSocket.sendto(data.encode(), (serverIP, serverPort))
        if INITIALIZE:
            done = False
            while not done:
                print(f"almost")
                data, server = clientSocket.recvfrom(1024)
                print(f"rec")
                seq_num_rec += 1
                if int(data.decode().split(',')[0]) == -1:
                    seed = int(data.decode().split(',')[1])
                    print(data.decode().split(',')[1])
                    print(int(seed))
                    random.seed(seed)
                    done = True
                else:
                    print(f"seq num : {data.decode().split(',')[0]} : {data.decode().split(',')[0] == -1}")
                    data = str(-1)
                    clientSocket.sendto(data.encode(), (serverIP, serverPort))
                print("here")
                clientSocket.settimeout(.1)
            INITIALIZE = False
        
        try:
            rec_data, server = clientSocket.recvfrom(1024)
            rec = rec_data.decode()
            if seq_num_rec <= int(rec.split(',')[0]):
                seq_num_rec, opponent_score, player_score, opponent_speed = map(int, rec.split(','))
                seq_num_rec += 1
            else:
                print(seq_num_rec, ":", int(rec.split(',')[0]), "not equal")
            while True:
                clientSocket.recvfrom(1024)
        except:
            print(f"except {seq_num_rec}")
    
    #Update game object states
    ball_animation()
    player_animation()
    opponent_animation()

    #draw
    screen.fill(bg_color) # clear screen
    pygame.draw.rect(screen,light_grey,player) # draw player
    pygame.draw.rect(screen,light_grey,opponent) #draw opponent
    pygame.draw.ellipse(screen,light_grey,ball) # draw ball
    pygame.draw.aaline(screen,light_grey,(width//2,0),(width//2,height)) #draw dividing line

    if score_time:
        ball_start() #Initialize ball for another set

    #draw player score    
    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text,(345,235))

    #draw opponent score
    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text,(285,235))

    #buffer swap: takes what was drawn to the back buffer
    # and swaps it with the front buffer (e.g. the one we "see")
    pygame.display.flip()

    #locks frame update rate at 60Hz
    clock.tick(60) 

