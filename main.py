import pygame, os, math, time, random
from pygame.locals import *
import numpy as np

pygame.init()

def waitFor( milliseconds ):
    time_now    = pygame.time.get_ticks()
    finish_time = time_now + milliseconds

    while time_now < finish_time:

        for event in pygame.event.get():
            if ( event.type == pygame.QUIT ):
                pygame.event.post( pygame.event.Event( pygame.QUIT ) )      
                break
            elif ( event.type == pygame.KEYDOWN ):
                if ( event.key == pygame.K_ESCAPE ):
                    break   


        pygame.display.update()            
        pygame.time.wait( 300 )
        time_now = pygame.time.get_ticks() 

def main():
    ball_pos=[740,360]
    ball_vel=[5,5]
    COLOUR=(255,255,255)
    col_val=225

    bar1_pos=[150,290]
    bar2_pos=[1300,290]

    p1_win=0
    p2_win=0
    newVelocity=0
    timer_con=True

    player_col=[(230,93,93),(92,229,193)]
    player_text="Draw"



    main_flag=True
    flag=True
    temp=0
    win=pygame.display.set_mode((1480,720))
    pygame.display.set_caption('MINIMALIST PONG')

    font=pygame.font.Font(os.path.join("Assets","gfx","Madrutana.otf"), 400)
    text=font.render('0   0',True,(225,225,225))
    textRect=text.get_rect()

    font2=pygame.font.Font(os.path.join("Assets","gfx","Madrutana.otf"), 300)
    time_text=font2.render('3',True,(225,225,225))
    timetext_rect=time_text.get_rect()
    timetext_rect.center=(745,360)

    font3=pygame.font.Font(os.path.join("Assets","gfx","Madrutana.otf"), 40)
    clock_text=font3.render('00:00',True,(100,100,100))
    clocktext_rect=clock_text.get_rect()
    clocktext_rect.center=(742,30)
    
    font4=pygame.font.Font(os.path.join("Assets","gfx","Madrutana.otf"), 45)
    winner_text=font4.render(player_text,True,(225,225,225))
    winner_rect=winner_text.get_rect()
    winner_rect.center=(742,680)


    bg=pygame.image.load(os.path.join("Assets","gfx","BG.png"))
    bar1=pygame.image.load(os.path.join("Assets","gfx","Bar1.png"))
    bar2=pygame.image.load(os.path.join("Assets","gfx","Bar2.png"))


    hit=pygame.mixer.Sound(os.path.join("Assets","sfx","hit.wav"))
    music=pygame.mixer.music.load(os.path.join("Assets","sfx","music.mp3"))
    hit.set_volume(0.2)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    timer_counter=0
    timer_flag=False

    run =True

    while run:
        win.blit(bg,(0,0))
        win.blit(bar1,bar1_pos)
        win.blit(bar2,bar2_pos)
        win.blit(text, textRect)

        if timer_con:
            n=3
            while n>0 :
                win.blit(bg,(0,0))
                win.blit(bar1,bar1_pos)
                win.blit(bar2,bar2_pos)
                time_text=font2.render(str(n),True,(225,225,225))
                timetext_rect=time_text.get_rect()
                timetext_rect.center=(740,360)
                win.blit(time_text,timetext_rect)
                waitFor(750)
                pygame.display.update()
                n=n-1

            timer_con=False

        # Quit Event
        for event in pygame.event.get():
            if event.type == QUIT:
                run=False
            if event.type==MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                print(pos)
        keys=pygame.key.get_pressed()
        
        if main_flag:
            start_time=time.time()
            main_flag=False

        # Quit Event 2
        if keys[pygame.K_ESCAPE]:
            run=False
        
        # Bar 1 Movement
        if keys[pygame.K_w]:
            if bar1_pos[1]-7 > 0:
                bar1_pos[1]=bar1_pos[1]-7
        if keys[pygame.K_s]:
            if bar1_pos[1]+7 < 580:
                bar1_pos[1]=bar1_pos[1]+7
        
        # Bar 2 Movement
        if keys[pygame.K_UP]:
            if bar2_pos[1]-7 > 0:
                bar2_pos[1]=bar2_pos[1]-7
        if keys[pygame.K_DOWN]:
            if bar2_pos[1]+7 < 580:
                bar2_pos[1]=bar2_pos[1]+7

        # Ball Render / Movement
        pygame.draw.circle(win,COLOUR,ball_pos,15)
        ball_pos=np.add(ball_pos,ball_vel)

        # Collision with wall Detection(Win/Lose)
        if ball_pos[0]>=1415:
            ball_pos=[740,360]
            bar1_pos=[150,290]
            bar2_pos=[1300,290]
            p1_win+=1
            col_val=225
            timer_con=True
            main_flag=True
            ball_vel=[random.choice([-5,5]),random.randint(-5,5)]

        elif ball_pos[0]<=55:
            ball_pos=[740,360]
            bar1_pos=[150,290]
            bar2_pos=[1300,290]
            p2_win+=1
            col_val=225
            timer_con=True
            main_flag=True
            ball_vel=[random.choice([-5,5]),random.randint(-5,5)]


        # Ball y velocity reverse on collision with wall
        if ball_pos[1]>=705 or ball_pos[1]<=15:
            ball_vel[1]=0-ball_vel[1]

        # Collision with bars detection
        if ball_pos[0]>=150 and ball_pos[0]<=181:
            if ball_pos[1]>=bar1_pos[1] and ball_pos[1]<=bar1_pos[1]+140 and flag:

                newVelocity=round((abs(((bar1_pos[1]*2+140)/2)-ball_pos[1])/140)*10,2)

                if ball_pos[1]>(bar1_pos[1]*2+140)/2:
                    ball_vel[1]=newVelocity
                else :
                    ball_vel[1]=-newVelocity

                ball_vel[0]=0-ball_vel[0]

                pygame.mixer.Sound.play(hit)
                flag=False
                temp=0

        elif ball_pos[0]>=1300 and ball_pos[0]<=1329 :

            if ball_pos[1]>=bar2_pos[1] and ball_pos[1]<=bar2_pos[1]+140 and flag:

                newVelocity=round((abs(((bar2_pos[1]*2+140)/2)-ball_pos[1])/140)*10,2)

                if ball_pos[1]>(bar2_pos[1]*2+140)/2:
                    ball_vel[1]=newVelocity
                else :
                    ball_vel[1]=-newVelocity

                ball_vel[0]=0-ball_vel[0]
                pygame.mixer.Sound.play(hit)
                temp=0
                flag=False

        # Infinite x velocity sign change detection / nullifier
        temp=temp+1
        if temp==10:
            flag=True

        win_show=str(p1_win)+"  "+str(p2_win)
        if col_val>=28:
            text=font.render(win_show,True,(col_val,col_val,col_val))
            col_val-=5.05
        textRect=text.get_rect()
        textRect.center=(745,360)       

        end_time=time.time()

        clocktime=time.strftime("%M:%S", time.gmtime(end_time-start_time))

    
        if p1_win>p2_win:
            player_text='Winning: Player 1'
            winner_text=font4.render(player_text,True,player_col[0])
            clock_text=font3.render(clocktime,True,player_col[1])
        elif p2_win>p1_win:
            player_text='Winning: Player 2'
            winner_text=font4.render(player_text,True,player_col[1])
            clock_text=font3.render(clocktime,True,player_col[0])
        else:
            player_text='Draw'
            winner_text=font4.render(player_text,True,(225,225,225))
            clock_text=font3.render(clocktime,True,(225,225,225))
        
        clocktext_rect=clock_text.get_rect()
        clocktext_rect.center=(740,30)
        win.blit(clock_text,clocktext_rect)

        speed_timer=int(round(time.time()))

        curr_timer=round(speed_timer-start_time)

        if curr_timer%10==0 and curr_timer<=60 and ball_vel[0]<0 and timer_flag:
            ball_vel[0]-=2
            timer_counter=0
            timer_flag=False
        elif curr_timer%10==0 and curr_timer<=60 and ball_vel[0]>0 and timer_flag:
            ball_vel[0]+=2
            timer_flag=False
            timer_counter=0

        timer_counter+=1

        if timer_counter> 100:
            timer_flag=True
        winner_rect=winner_text.get_rect()
        winner_rect.center=(742,685)
        win.blit(winner_text,winner_rect)


        pygame.time.wait(16)
        pygame.display.update()
        
    pygame.quit()

main()
