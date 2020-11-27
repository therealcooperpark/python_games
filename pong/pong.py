#! /usr/bin/env python3
'''
Make the game... pong!
'''

import turtle # Manages the screen stuff


class Paddle(turtle.Turtle):
    def __init__(self, shape, color, w_mult, h_mult, x, y):
        super().__init__()
        self.speed(0)
        self.shape(shape)
        self.color(color)
        self.penup()
        self.shapesize(w_mult, h_mult)
        self.goto(x, y)

    # Move up function
    def move_up(self):
        y = self.ycor() + 20
        if (y + 50) <= 300:
            self.sety(y)


    # Move down function
    def move_down(self):
        y = self.ycor() - 20
        if (y - 50) >= -300:
            self.sety(y)


class Ball(Paddle):
    def __init__(self, shape, color, w_mult, h_mult, x, y, dx, dy):
        super().__init__(shape, color, w_mult, h_mult, x, y)
        self.dx = dx
        self.dy = dy

    def move_ball(self):
        ''' Move the ball '''
        global score_a, score_b, pen

        x = ball.xcor() + ball.dx
        y = ball.ycor() + ball.dy

        ball.setx(x), ball.sety(y)

        # Check borders
        if y > 290: # Upper border
            ball.sety(290)
            ball.dy *= -1

        if y < -290: # Lower border
            ball.sety(-290)
            ball.dy *= -1

        if x > 390: # left wall
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear()
            pen.write('Player 1: {0}\tPlayer 2: {1}'.format(score_a, score_b), align = 'center', font = ('Courier', 24, 'normal'))

        if x < -390: # Right wall
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write('Player 1: {0}\tPlayer 2: {1}'.format(score_a, score_b), align = 'center', font = ('Courier', 24, 'normal'))


# Make window
win = turtle.Screen()
win.title('Pong')
win.bgcolor('Black')
win.setup(width=800, height=600)
win.tracer(0)


# Make objects
paddle_a = Paddle('square', 'white', 5, 1, -350, 0)
paddle_b = Paddle('square', 'white', 5, 1, 350, 0)
ball = Ball('square', 'white', 1, 1, 0, 0, 2, 2)


# Pen (score tracking)
score_a = 0
score_b = 0

pen = turtle.Turtle()
pen.speed(0)
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write('Player 1: {0}\tPlayer 2: {1}'.format(score_a, score_b), align = 'center', font = ('Courier', 24, 'normal'))

# Keyboard bindings
win.listen()
win.onkeypress(paddle_a.move_up, 'w') # Player 1
win.onkeypress(paddle_a.move_down, 's') # Player 1
win.onkeypress(paddle_b.move_up, 'Up') # Player 2
win.onkeypress(paddle_b.move_down, 'Down') # Player 2

# Main game loop
while True:
    win.update()

    ## Move the ball
    ball.move_ball()

    ## Paddle/Ball collisions

    # Paddle a check
    if ball.xcor() < -340 \
    and ball.xcor() > -350 \
    and ball.ycor() < (paddle_a.ycor() + 50) \
    and ball.ycor() > (paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1

    # Paddle b check
    if ball.xcor() > 340 \
    and ball.xcor() < 350 \
    and ball.ycor() < (paddle_b.ycor() + 50) \
    and ball.ycor() > (paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1

    if score_a == 3:
        print('Player 1 wins!')
        break
    if score_b == 3:
        print('Player 2 wins!')
        break
