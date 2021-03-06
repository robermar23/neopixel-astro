print("NeoAstro says Hello!")

# Circuit Playground NeoPixel

# D4 - Left Button A
# D5 - Right Button B
# D7 - Slide Switch
# D8 - Built-in 10 NeoPixels
# D13 - Red LED
# D27 - Accelerometer interrupt
# D25 - IR Transmitter
# D26 - IR Receiver
# A0 - Speaker analog output
# A8 - Light Sensor
# A9 - Temperature Sensor
# A10 - IR Proximity Sensor

import time
import random
import board
import neopixel
from adafruit_circuitplayground.express import cpx

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def color_chase(color, wait, pixels):
    pixels.fill(OFF)
    #pixels.show()
    for i in range(len(pixels)):
        pixels[i] = color
        if wait > 0: time.sleep(wait)
        pixels.show()
    #time.sleep(0.1)
 
 
def rainbow_cycle(wait, pixels):
    inner_max = len(pixels)
    for j in range(255):
        for i in range(inner_max):
            rc_index = (i * 256 // inner_max) + j * 5
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)
 
 
def rainbow(wait, pixels):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = wheel(idx & 255)
        pixels.show()
        time.sleep(wait)
 
 # a random color 0 -> 224
def random_color():
    return random.randrange(0, 7) * 32

def set_brightness(cpx, pixels):
    print ("Light: " + str(cpx.light))
    tmp_light=100
    if cpx.light < 100:
        tmp_light = cpx.light
    brightness_percent = 100 - tmp_light
    if brightness_percent == 100:
        brightness_percent = 99
    brightness = brightness_percent/100
    pixels.brightness = brightness
    print ("Brightness: " + str(brightness))

pixels_outer = neopixel.NeoPixel(board.A2, 60, brightness=0.5, auto_write=False)

print("Have pixels")

# choose which demos to play
# 1 means play, 0 means don't!
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

color_chase_demo = 1
flash_demo = 0
rainbow_demo = 0
rainbow_cycle_demo = 0
selected_color = RED
current_speed = 0.025
speed_stepper = 0.01

turned_on = False


print("About to enter loop")

while True:
    
    turned_on = cpx.switch
    
    if cpx.button_a:
        current_speed+= speed_stepper
        print("Speed decreased to " + str(current_speed))
        #cpx.play_tone(250, 1)
        
    elif cpx.button_b:
        if current_speed >= 0:
            current_speed-= speed_stepper
            print("Speed increased to " + str(current_speed))
        else:
            print("Speed at max")
        #cpx.play_tone(350, 1)
        
    
    print("Current Speed: " + str(current_speed))

    if turned_on:

        set_brightness(cpx, pixels_outer)
        set_brightness(cpx, cpx.pixels)
        
        if color_chase_demo:
            #random_rgb = (random_color(), random_color(), random_color())
            print ("RGB: " + str(selected_color))
            color_chase(selected_color, current_speed, pixels_outer)  # Increase the number to slow down the color chase
            color_chase(selected_color, current_speed, cpx.pixels)
        if flash_demo:

            print("Start flash demo")
            sleep_time = 0.2

            pixels_outer.fill(RED)
            pixels_outer.show()
            time.sleep(sleep_time)
            pixels_outer.fill(GREEN)
            pixels_outer.show()
            
            time.sleep(sleep_time)
            pixels_outer.fill(BLUE)
            pixels_outer.show()
            
            time.sleep(sleep_time)
            pixels_outer.fill(WHITE)
            pixels_outer.show()
            
            time.sleep(sleep_time)
    
        if rainbow_cycle_demo:
            rainbow_cycle(0.1,  pixels_outer)  # Increase the number to slow down the rainbow.
            rainbow_cycle(0.1,  cpx.pixels)  # Increase the number to slow down the rainbow.
    
        if rainbow_demo:
            rainbow(0.04, pixels_outer)  # Increase the number to slow down the rainbow.
            rainbow(0.04, cpx.pixels)  # Increase the number to slow down the rainbow.

        if cpx.touch_A1:
            selected_color = GREEN
            print('Touched 1!')

        #A2 is used by the neopixels    
        # elif cpx.touch_A2:
        
        elif cpx.touch_A3:
            print('Touched 3!')
            selected_color = BLUE

        elif cpx.touch_A4:
            print('Touched 4!')
            
        elif cpx.touch_A5:
            print('Touched 5!')
            
        elif cpx.touch_A6:
            print('Touched 6!')
        elif cpx.touch_A7:
            print('Touched 7!')
    else:
        pixels_outer.fill(OFF)
        pixels_outer.show()
        cpx.pixels.fill(OFF)
        cpx.pixels.show()
        print("not on")

    #time.sleep(0.2)