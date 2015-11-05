# Implementation of classic arcade game Pong

import simplegui
import random

WIDTH = 600
HEIGHT = 400       
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = True
RIGHT = False
ball_radius = 20
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_vel, ball_pos
    ball_vel[0] = random.randrange(1, 4)
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
    ball_vel[1] = -random.randrange(1, 4)
    ball_pos = [WIDTH/2, HEIGHT/2]


def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    score1 = score2 = paddle1_vel = paddle2_vel = 0
    paddle1_pos = paddle2_pos = HEIGHT/2
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel
  
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball 
    # if ball collides with upper or bottom wall it bounces
    if ball_pos[1] + ball_radius >= HEIGHT or ball_pos[1] - ball_radius <= 0:
        ball_vel[1] = -ball_vel[1]
    #if ball collides with left or right gutter outside of the paddle it respawns from the center towards the opposite gutter
    #and the opponent wins a point
    if ball_pos[0]-ball_radius <= PAD_WIDTH and (ball_pos[1] > paddle1_pos+PAD_HEIGHT/2 or ball_pos[1] < paddle1_pos-PAD_HEIGHT/2):
        spawn_ball(RIGHT)
        score2 += 1
    if ball_pos[0]+ball_radius >= (WIDTH - PAD_WIDTH) and (ball_pos[1]+ball_radius/2 > paddle2_pos+PAD_HEIGHT/2 or ball_pos[1] < paddle2_pos-PAD_HEIGHT/2):
        spawn_ball(LEFT)
        score1 += 1
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    canvas.draw_circle(ball_pos, ball_radius, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= PAD_HEIGHT/2 and paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT/2:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= PAD_HEIGHT/2 and paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT/2:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_line([PAD_WIDTH/2, paddle1_pos + PAD_HEIGHT/2], [PAD_WIDTH/2, paddle1_pos - PAD_HEIGHT/2], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH/2, paddle2_pos+PAD_HEIGHT/2], [WIDTH - PAD_WIDTH/2, paddle2_pos - PAD_HEIGHT/2], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide 
    # increase velocity after each collision
    if ball_pos[0]-ball_radius <= PAD_WIDTH and (ball_pos[1] <= paddle1_pos+PAD_HEIGHT/2 or ball_pos[1] >= paddle1_pos-PAD_HEIGHT/2):
        ball_vel[0] = ball_vel[0]*1.1
        ball_vel[1] = ball_vel[1]*1.1
        ball_vel[0] = -ball_vel[0]
    if ball_pos[0]+ball_radius >= (WIDTH - PAD_WIDTH) and (ball_pos[1] <= paddle2_pos+PAD_HEIGHT/2 or ball_pos[1] >= paddle2_pos-PAD_HEIGHT/2):
        ball_vel[0] = ball_vel[0]*1.1
        ball_vel[1] = ball_vel[1]*1.1
        ball_vel[0] = -ball_vel[0] 
        
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/4], 20, "White")
    canvas.draw_text(str(score2), [0.75*WIDTH, HEIGHT/4], 20, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def restart():
    new_game()


frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart game", restart);


new_game()
frame.start()
