
import machine
import network
import utime
from utime import sleep_us, ticks_ms, ticks_us, ticks_diff
import time
from time import sleep
from machine import Pin, I2C,PWM, ADC
from math import sqrt
import os
import sys
import ssd1306
from random import getrandbits, seed


# configure oled display I2C SSD1306
i2c = I2C(-1, Pin(5), Pin(4))   # SCL, SDA
display = ssd1306.SSD1306_I2C(128, 64, i2c)

#--------- pin layout

btnLeft = Pin(12, Pin.IN, Pin.PULL_UP)
btnRight = Pin(13, Pin.IN, Pin.PULL_UP)
btnUp = Pin(14, Pin.IN, Pin.PULL_UP)
btnDown = Pin(2, Pin.IN, Pin.PULL_UP)
btnA = Pin(0, Pin.IN, Pin.PULL_UP)
buzzer = Pin(15, Pin.OUT)

tones = {
    'c4': 262,
    'd4': 294,
    'e4': 330,
    'f4': 349,
    'f#4': 370,
    'g4': 392,
    'g#4': 415,
    'a4': 440,
    "a#4": 466,
    'b4': 494,
    'c5': 523,
    'c#5': 554,
    'd5': 587,
    'd#5': 622,
    'e5': 659,
    'f5': 698,
    'f#5': 740,
    'g5': 784,
    'g#5': 831,
    'a5': 880,
    'b5': 988,
    'c6': 1047,
    'c#6': 1109,
    'd6': 1175,
    ' ': 0
}


def playTone(tone, tone_duration, total_duration):
            beeper = PWM(buzzer, freq=tones[tone], duty=512)
            utime.sleep_ms(tone_duration)
            beeper.deinit()
            utime.sleep_ms(int(total_duration * 1000)-tone_duration)
            


class Ball(object):
    """Ball."""

    def __init__(self, x, y, x_speed, y_speed, display, width=7, height=7,
                 frozen=False):
        """Initialize ball.

        Args:
            x, y (int):  X,Y coordinates.
            x_speed, y_speed (int):  Initial XY speeds.
            display (SSD1306): OLED display.
            width (Optional int): Ball width (default 7).
            height (Optional int): Ball height (default 7).
            frozen (boolean): Indicates if ball is frozen (default false).
        """
        self.x = x
        self.y = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.prev_x = x
        self.prev_y = y
        self.width = width
        self.height = height
        self.center = width // 2
        self.max_x_speed = 3
        self.max_y_speed = 3
        self.frozen = frozen
        self.display = display
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_speed2 = 0.0
        self.y_speed2 = 0.0
        self.created = ticks_ms()

    def clear(self):
        """Clear ball."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 0)

    def clear_previous(self):
        """Clear prevous ball position."""
        self.display.fill_rect(self.prev_x, self.prev_y,
                                self.width, self.height, 0)

    def draw(self):
        """Draw ball."""
        self.clear_previous()
        self.display.fill_rect( self.x, self.y,
                                 self.width, self.height,1)

    def set_position(self, paddle_x, paddle_y, paddle_x2, paddle_center):
        """Set ball position."""
        self.prev_x = self.x
        self.prev_y = self.y
        # Check if frozen to paddle
        if self.frozen:
            # Freeze ball to top center of paddle
            self.x = paddle_x + (paddle_center - self.center)
            self.y = paddle_y - self.height
            if ticks_diff(ticks_ms(), self.created) >= 2000:
                # Release frozen ball after 2 seconds
                self.frozen = False
            else:
                return
        self.x += int(self.x_speed) + int(self.x_speed2)
        self.x_speed2 -= int(self.x_speed2)
        self.x_speed2 += self.x_speed - int(self.x_speed)

        self.y += int(self.y_speed) + int(self.y_speed2)
        self.y_speed2 -= int(self.y_speed2)
        self.y_speed2 += self.y_speed - int(self.y_speed)

        # Bounces off walls
        if self.y < 15:
            self.y = 15
            self.y_speed = -self.y_speed
        if self.x + self.width >= 122:
            self.x = 123 - self.width
            self.x_speed = -self.x_speed
        elif self.x < 5:
            self.x = 5
            self.x_speed = -self.x_speed

        # Check for collision with Paddle
        if (self.y2 >= paddle_y and
           self.x <= paddle_x2 and
           self.x2 >= paddle_x):
            # Ball bounces off paddle
            self.y = paddle_y - (self.height + 1)
            ratio = ((self.x + self.center) -
                     (paddle_x + paddle_center)) / paddle_center
            self.x_speed = ratio * self.max_x_speed
            self.y_speed = -sqrt(max(1, self.max_y_speed ** 2 - self.x_speed ** 2))

        self.x2 = self.x + self.width - 1
        self.y2 = self.y + self.height - 1


class Brick(object):
    """Brick."""

    def __init__(self, x, y, color, display, width=12, height=2):
        """Initialize brick.

        Args:
            x, y (int):  X,Y coordinates.
            color (string):  Blue, Green, Pink, Red or Yellow.
            display (SSD1351): OLED display.
            width (Optional int): Block width (default 12).
            height (Optional int): Block height (default 6).
        """
        self.x = x
        self.y = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.center_x = x + (width // 2)
        self.center_y = y + (height // 2)
        self.color = color
        self.width = width
        self.height = height
        self.display = display
        self.draw()

    def bounce(self, ball_x, ball_y, ball_x2, ball_y2,
               x_speed, y_speed,
               ball_center_x, ball_center_y):
        """Determine bounce for ball collision with brick."""
        x = self.x
        y = self.y
        x2 = self.x2
        y2 = self.y2
        center_x = self.center_x
        center_y = self.center_y
        if ((ball_center_x > center_x) and
           (ball_center_y > center_y)):
            if (ball_center_x - x2) < (ball_center_y - y2):
                y_speed = -y_speed
            elif (ball_center_x - x2) > (ball_center_y - y2):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x > center_x) and
              (ball_center_y < center_y)):
            if (ball_center_x - x2) < -(ball_center_y - y):
                y_speed = -y_speed
            elif (ball_center_x - x2) > -(ball_center_y - y):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x < center_x) and
              (ball_center_y < center_y)):
            if -(ball_center_x - x) < -(ball_center_y - y):
                y_speed = -y_speed
            elif -(ball_center_x - x) > -(ball_center_y - y):
                y_speed = -y_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed
        elif ((ball_center_x < center_x) and
              (ball_center_y > center_y)):
            if -(ball_center_x - x) < (ball_center_y - y2):
                y_speed = -y_speed
            elif -(ball_center_x - x) > (ball_center_y - y2):
                x_speed = -x_speed
            else:
                x_speed = -x_speed
                y_speed = -y_speed

        return [x_speed, y_speed]

    def clear(self):
        """Clear brick."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 0)

    def draw(self):
        """Draw brick."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 1)


class Life(object):
    """Life."""

    def __init__(self, index, display, width=12, height=2):
        """Initialize life.

        Args:
            index (int): Life number (1-based).
            display (SSD1351): OLED display.
            width (Optional int): Life width (default 12).
            height (Optional int): Life height (default 4).
        """
        margin = 5
        self.display = display
        self.x = display.width - (index * (width + margin))
        self.y = 3
        self.width = width
        self.height = height
        self.draw()

    def clear(self):
        """Clear life."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 0)

    def draw(self):
        """Draw life."""
        self.display.fill_rect(self.x, self.y,
                                 self.width, self.height,1)


class Paddle(object):
    """Paddle."""

    def __init__(self, display, width=25, height=2):
        """Initialize paddle.

        Args:
            display (SSD1351): OLED display.
            width (Optional int): Paddle width (default 25).
            height (Optional int): Paddle height (default 8).
        """
        self.x = 51
        self.y = 120
        self.x2 = self.x + width - 1
        self.y2 = self.y + height - 1
        self.width = width
        self.height = height
        self.center = width // 2
        self.display = display

    def clear(self):
        """Clear paddle."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 0)

    def draw(self):
        """Draw paddle."""
        self.display.fill_rect(self.x, self.y,
                                 self.width, self.height,1)

    def h_position(self, x):
        """Set paddle position.

        Args:
            x (int):  X coordinate.
        """
        if(x != self.x):  # Check if paddle moved
            prev_x = self.x  # Store previous x position
            self.x = x
            self.x2 = x + self.width - 1
            self.y2 = self.y + self.height - 1
            self.draw()
            # Clear previous paddle
            if x > prev_x:
                self.display.fill_rect(prev_x, self.y,
                                        x - prev_x, self.height, 0)
            else:
                self.display.fill_rect(x + self.width, self.y,
                                        (prev_x + self.width) -
                                        (x + self.width),
                                        self.height, 0)
        else:
            self.draw()


class Powerup(object):
    """Power-up."""

    def __init__(self, x, y, display, width=16, height=16):
        """Initialize power-up.

        Args:
            x, y (int):  X,Y coordinates.
            display (SSD1351): OLED display.
            width (Optional int): Power-up width (default 16).
            height (Optional int): Power-up height (default 16).
        """
        if x > display.width - (5 + width):
            x = display.width - (5 + width)
        self.x = x
        self.y = y
        self.x2 = x + width - 1
        self.y2 = y + height - 1
        self.prev_y = y
        self.width = width
        self.height = height
        self.display = display
        self.y_speed = 2
        self.collected = False

    def clear(self):
        """Clear power-up."""
        self.display.fill_rect(self.x, self.y, self.width, self.height, 0)

    def clear_previous(self):
        """Clear prevous power-up position."""
        self.display.fill_rect(self.x, self.prev_y, self.width, self.height, 0)

    def draw(self):
        """Draw power-up."""
        self.clear_previous()
        self.display.fill_rect(self.x, self.y, self.width, self.height,1)

    def set_position(self, paddle_x, paddle_y, paddle_x2, paddle_center):
        """Set power-up position."""
        self.prev_y = self.y
        self.y += self.y_speed

        # Check for collision with Paddle
        if (self.y2 >= paddle_y and
           self.x <= paddle_x2 and
           self.x2 >= paddle_x):
            self.collected = True

        self.y2 = self.y + self.height - 1


class Score(object):
    """Score."""

    def __init__(self, display):
        """Initialize score.

        Args:
            display (SSD1351): OLED display.
        """
        margin = 5
        self.display = display
        self.display.text('SCORE:', margin, 0, 1)
        self.x = 5 + margin
        self.y = 0
        self.value = 0
        self.draw()

    def draw(self):
        """Draw score value."""
        self.display.text( str(self.value), self.x, self.y,1)
        
    def game_over(self):
        """Display game over."""
        self.display.text('GAME OVER', (self.display.width // 2) - (9 // 2),
                               int(self.display.height / 1.5), 1)

    def increment(self, points):
        """Increase score by specified points."""
        self.value += points
        self.draw()

    def reset(self):
        """Reset score."""
        self.value = 0
        self.display.fill_rect(self.x, self.y, self.display.width - self.x,
                                7, 0)


def load_level(level, display):
  
    bricks = []
    for row in range(12, 28, 4):
        brick_color = 1
        for col in range(16, 112, 12):
            bricks.append(col, row, brick_color, display)
    return bricks
    

def main():
    """Initialize display."""
 
    # Initialize ADC on pin A0
    adc = ADC(0)
    # Set attenuation 0-2V (Will use resistor to limit pot to 2V).
    # adc.atten(ADC.ATTN_6DB)

    # Seed random numbers
    seed(ticks_us())

    # Generate bricks
    MAX_LEVEL = const(9)
    level = 1
    bricks = load_level(level, display)

    # Initialize paddle
    paddle = Paddle(display)

    # Initialize score
    score = Score(display)

    # Initialize balls
    balls = []
    # Add first ball
    balls.append(Ball(59, 111, -2, -1, display, frozen=True))

    # Initialize lives
    lives = []
    for i in range(1, 3):
        lives.append(Life(i, display))

    # Initialize power-ups
    powerups = []

    try:
        while True:
            timer = ticks_us()
            # Set paddle position to ADC spinner (scale 6 - 98)
            paddle.h_position(adc.read() // 44 + 5)
            # Handle balls
            score_points = 0
            for ball in balls:
                # Position
                ball.set_position(paddle.x, paddle.y,
                                  paddle.x2, paddle.center)

                # Check for collision with bricks if not frozen
                if not ball.frozen:
                    prior_collision = False
                    ball_x = ball.x
                    ball_y = ball.y
                    ball_x2 = ball.x2
                    ball_y2 = ball.y2
                    ball_center_x = ball.x + ((ball.x2 + 1 - ball.x) // 2)
                    ball_center_y = ball.y + ((ball.y2 + 1 - ball.y) // 2)
                    # Check for hits
                    for brick in bricks:
                        if(ball_x2 >= brick.x and
                           ball_x <= brick.x2 and
                           ball_y2 >= brick.y and
                           ball_y <= brick.y2):
                            # Hit
                            if not prior_collision:
                                ball.x_speed, ball.y_speed = brick.bounce(
                                    ball.x,
                                    ball.y,
                                    ball.x2,
                                    ball.y2,
                                    ball.x_speed,
                                    ball.y_speed,
                                    ball_center_x,
                                    ball_center_y)
                                prior_collision = True
                            score_points += 1
                            brick.clear()
                            bricks.remove(brick)

                    # Generate random power-ups
                    if score_points > 0 and getrandbits (4) == 7:
                        powerups.append(Powerup(ball.x, 64, display))

                # Check for missed
                if ball.y2 > display.height - 3:
                    ball.clear_previous()
                    balls.remove(ball)
                    if not balls:
                        # Clear powerups
                        powerups.clear()
                        # Lose life if last ball on screen
                        if len(lives) == 0:
                            score.game_over()
                        else:
                            # Subtract Life
                            lives.pop().clear()
                            # Add ball
                            balls.append(Ball(59, 112, 2, -3, display,
                                         frozen=True))
                else:
                    # Draw ball
                    ball.draw()
            # Update score if changed
            if score_points:
                score.increment(score_points)
            # Handle power-ups
            for powerup in powerups:
                powerup.set_position(paddle.x, paddle.y,
                                     paddle.x2, paddle.center)
                powerup.draw()
                if powerup.collected:
                    # Power-up collected
                    powerup.clear()
                    # Add ball
                    balls.append(Ball(powerup.x, 112, 2, -1, display,
                                 frozen=False))
                    powerups.remove(powerup)
                elif powerup.y2 > display.height - 3:
                    # Power-up missed
                    powerup.clear()
                    powerups.remove(powerup)

            # Check for level completion
            if not bricks:
                for ball in balls:
                    ball.clear()
                balls.clear()
                for powerup in powerups:
                    powerup.clear()
                powerups.clear()
                level += 1
                if level > MAX_LEVEL:
                    level = 1
                bricks = load_level(level, display)
                balls.append(Ball(59, 111, -2, -1, display, frozen=True))
            display.show()
            # Attempt to set framerate to 30 FPS
            timer_dif = 33333 - ticks_diff(ticks_us(), timer)
            if timer_dif > 0:
                sleep_us(timer_dif)
    except KeyboardInterrupt:
        display.cleanup()


main()

