import inspect
import time
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
# Set BPM
bpm = (float(60)/float(102))
bpm_ref = bpm
bpm_sec = bpm/4
#print(bpm)


#build the color func
def color(B,G,R):
    color = Adafruit_WS2801.RGB_to_color(B,G,R)
    return color


# Set default colors
pink = color(255, 0, 255)
cyan = color(255, 255, 0)
red = color(0, 0, 255)
lime = color(0, 255, 0)
blue = color(255, 0, 0)
white =	color(255,255,255)
yellow = color(0,255,255)
silver = color(192,192,192)
gray = color(128,128,128)
maroon = color(0,0,128)
olive = color(0,128,128)
green = color(0,128,0)
purple = color(128,0,128)
teal = color(128,128,0)
navy = color(128,0,0)
        
# Configure the count of pixels:
PIXEL_COUNT = 192
STRIP_SIZE = 32
 
# Hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)




# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)
 
# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, wait=0.1):
    for i in range(pixels.count()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_cycle(pixels, wait=0.005):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((i * 256 // pixels.count()) + j) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def rainbow_colors(pixels, wait=0.05):
    for j in range(256): # one cycle of all 256 colors in the wheel
        for i in range(pixels.count()):
            pixels.set_pixel(i, wheel(((256 // pixels.count() + j)) % 256) )
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def brightness_decrease(pixels, wait=0.01, step=1, color=pink):
    for j in range(int(256 // step)):
        for i in range(pixels.count()):
            r, g, b = pixels.get_pixel_rgb(i)
            r = int(max(0, r - step))
            g = int(max(0, g - step))
            b = int(max(0, b - step))
            pixels.set_pixel(i, color)
        pixels.show()
        if wait > 0:
            time.sleep(wait)
 
def appear_from_back(pixels, color=green):
    
    sequence = range(pixels.count())
    target = bpm/35.98
    
    pos = 0
    for i in sequence:
        
        for j in reversed(range(i, STRIP_SIZE)):
            start=time.time()
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, color)
                pixels.set_pixel(k+STRIP_SIZE, color)
                pixels.set_pixel(k+(STRIP_SIZE*2), color)
                pixels.set_pixel(k+(STRIP_SIZE*3), color)
                pixels.set_pixel(k+(STRIP_SIZE*4), color)
                pixels.set_pixel(k+(STRIP_SIZE*5), color)
            # set then the pixel at position j
            pixels.set_pixel(j, color)
            pixels.set_pixel(j+STRIP_SIZE, color)
            pixels.set_pixel(j+(STRIP_SIZE*2), color)
            pixels.set_pixel(j+(STRIP_SIZE*3), color)
            pixels.set_pixel(j+(STRIP_SIZE*4), color)
            pixels.set_pixel(j+(STRIP_SIZE*5), color)
            pixels.show()
            pixels.clear()
            end = time.time()
            diff = max(0,target-(end-start))
            #print(diff)
            time.sleep(diff)
        
def disappear_from_back(pixels, color=green):
    target = bpm/35.98
    for i in reversed(range(0,STRIP_SIZE)):
        for j in range(i, STRIP_SIZE):
            start = time.time()
            pixels.clear()
            # first set all pixels at the begin
            for k in range(i):
                pixels.set_pixel(k, color)
                pixels.set_pixel(k+STRIP_SIZE, color)
                pixels.set_pixel(k+(STRIP_SIZE*2), color)
                pixels.set_pixel(k+(STRIP_SIZE*3), color)
                pixels.set_pixel(k+(STRIP_SIZE*4), color)
                pixels.set_pixel(k+(STRIP_SIZE*5), color)
            # set then the pixel at position j
            pixels.set_pixel(j, color)
            pixels.set_pixel(j+STRIP_SIZE, color)
            pixels.set_pixel(j+(STRIP_SIZE*2), color)
            pixels.set_pixel(j+(STRIP_SIZE*3), color)
            pixels.set_pixel(j+(STRIP_SIZE*4), color)
            pixels.set_pixel(j+(STRIP_SIZE*5), color)
            pixels.show()
            end = time.time()
            diff = max(0,target-(end-start))
            #print(diff)
            time.sleep(diff)
    pixels.clear()
    pixels.show()
            
def pixel_player(pixels,color=pink):
    #mixer.music.play()
    #time.sleep(.1)
    for ins in instructions:
        pixels.set_pixel(ins[0], color)
        pixels.show()
        time.sleep(ins[1])
        pixels.clear()
    
    
def alternator(pixels, color1=pink,color2=cyan):
    target = bpm
    
    start = time.time()
    for i in range(0,PIXEL_COUNT):
        if (i % 2) == 0:
            pixels.set_pixel(i, color1)
    pixels.show()
    end = time.time()
    diff = target-(end-start)
    time.sleep(diff)
    pixels.clear()
    
    start = time.time()
    for i in range(0,PIXEL_COUNT):   
        if (i % 2) != 0:
            pixels.set_pixel(i, color2)
    pixels.show()
    end = time.time()
    diff = target-(end-start)
    time.sleep(diff)
    pixels.clear()
    
    
def pong(pixels, color=pink):
    for i in list(range(0,PIXEL_COUNT))+list(reversed(range(0,PIXEL_COUNT)))[1::][::1]:
        pixels.set_pixel(i, color)
        pixels.show()
        time.sleep(bpm_sec/PIXEL_COUNT)
        pixels.clear()
    
def strip_pong(pixels, color1=pink, color2=cyan):
    sequence = list(range(0,STRIP_SIZE))+list(reversed(range(0,STRIP_SIZE)))
    total = bpm*2
    target = total/len(sequence)
    adj = 0
    for i in sequence:
        start = time.time()
        pixels.set_pixel(i, color1)
        pixels.set_pixel(i+STRIP_SIZE, color2)
        pixels.set_pixel(i+(STRIP_SIZE*2), color1)
        pixels.set_pixel(i+(PIXEL_COUNT/2), color2)
        pixels.set_pixel(i+(PIXEL_COUNT/2)+STRIP_SIZE, color1)
        pixels.set_pixel(i+(PIXEL_COUNT/2)+(STRIP_SIZE*2), color2)
        pixels.show()
        pixels.clear()
        end=time.time()
        diff = max(0,target-(end-start)-adj)
        time.sleep(diff)
        end = time.time()
        adj = max(0,end-start-target)

        
def mid_pong(pixels, color1=pink, color2=cyan):
    top = PIXEL_COUNT/2

    for i in list(range(0,top))+list(reversed(range(0,top)))[1::][::1]:
        pixels.set_pixel(i, color1)
        pixels.set_pixel(PIXEL_COUNT-(i+1), color2)
        pixels.show()
        time.sleep(bpm_sec/top)
        pixels.clear()
        
def cross_pong(pixels, color1=pink, color2=cyan):
    top = STRIP_SIZE/2
    sequence = list(range(0,top+1))+list(reversed(range(1,top)))+list(range(0,top+1))+list(reversed(range(1,top)))
    total = bpm*2
    target = total/len(sequence)
    adj = 0
    counter = 0
    
    for i in sequence:
        counter += 1
        if counter <= top:
            start = time.time()
            pixels.set_pixel(i, color1)
            pixels.set_pixel(i+STRIP_SIZE, color1)
            pixels.set_pixel(i+(2*STRIP_SIZE), color1)
            pixels.set_pixel(i+(3*STRIP_SIZE), color1)
            pixels.set_pixel(i+(4*STRIP_SIZE), color1)
            pixels.set_pixel(i+(5*STRIP_SIZE), color1)
            pixels.set_pixel(STRIP_SIZE-i, color2)
            pixels.set_pixel((2*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((3*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((4*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((5*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((6*STRIP_SIZE-1)-i, color2)
            pixels.show()
            pixels.clear()
            end=time.time()
            diff = max(0,target-(end-start)-adj)
            time.sleep(diff)
            end = time.time()
            adj = max(0,end-start-target)
            
            
        elif counter <= STRIP_SIZE:
            start = time.time()
            pixels.set_pixel(i, color2)
            pixels.set_pixel(i+STRIP_SIZE, color2)
            pixels.set_pixel(i+(2*STRIP_SIZE), color2)
            pixels.set_pixel(i+(3*STRIP_SIZE), color2)
            pixels.set_pixel(i+(4*STRIP_SIZE), color2)
            pixels.set_pixel(i+(5*STRIP_SIZE), color2)
            pixels.set_pixel(STRIP_SIZE-i, color1)
            pixels.set_pixel((2*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((3*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((4*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((5*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((6*STRIP_SIZE-1)-i, color1)
            pixels.show()
            pixels.clear()
            end=time.time()
            diff = max(0,target-(end-start)-adj)
            time.sleep(diff)
            end = time.time()
            adj = max(0,end-start-target)
            
        elif counter <= STRIP_SIZE+top:
            start = time.time()
            pixels.set_pixel(i, color1)
            pixels.set_pixel(i+STRIP_SIZE, color1)
            pixels.set_pixel(i+(2*STRIP_SIZE), color1)
            pixels.set_pixel(i+(3*STRIP_SIZE), color1)
            pixels.set_pixel(i+(4*STRIP_SIZE), color1)
            pixels.set_pixel(i+(5*STRIP_SIZE), color1)
            pixels.set_pixel(STRIP_SIZE-i, color2)
            pixels.set_pixel((2*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((3*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((4*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((5*STRIP_SIZE-1)-i, color2)
            pixels.set_pixel((6*STRIP_SIZE-1)-i, color2)
            pixels.show()
            pixels.clear()
            end=time.time()
            diff = max(0,target-(end-start)-adj)
            time.sleep(diff)
            end = time.time()
            adj = max(0,end-start-target)
            
        else:
            start = time.time()
            pixels.set_pixel(i, color2)
            pixels.set_pixel(i+STRIP_SIZE, color2)
            pixels.set_pixel(i+(2*STRIP_SIZE), color2)
            pixels.set_pixel(i+(3*STRIP_SIZE), color2)
            pixels.set_pixel(i+(4*STRIP_SIZE), color2)
            pixels.set_pixel(i+(5*STRIP_SIZE), color2)
            pixels.set_pixel(STRIP_SIZE-i, color1)
            pixels.set_pixel((2*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((3*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((4*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((5*STRIP_SIZE-1)-i, color1)
            pixels.set_pixel((6*STRIP_SIZE-1)-i, color1)
            pixels.show()
            pixels.clear()
            end=time.time()
            diff = max(0,target-(end-start)-adj)
            time.sleep(diff)
            end = time.time()
            adj = max(0,end-start-target)


        
def halfs(pixels, color1=red, color2=cyan):
    target = bpm

    start = time.time()
    for j in list(range(0,STRIP_SIZE))+list(range(STRIP_SIZE,STRIP_SIZE*2))+list(range(STRIP_SIZE*2,STRIP_SIZE*3)):
        pixels.set_pixel(j, color1)
    pixels.show()
    end = time.time()
    diff = max(0,target-(end-start))
    time.sleep(diff)
    pixels.clear()
    pixels.show()
    start = time.time()
    for k in list(range(STRIP_SIZE*3,STRIP_SIZE*4))+list(range(STRIP_SIZE*4,STRIP_SIZE*5))+list(range(STRIP_SIZE*5,STRIP_SIZE*6)):
        pixels.set_pixel(k, color2)
    pixels.show()
    end = time.time()
    diff = max(0,target-(end-start))
    time.sleep(diff)
    pixels.clear()
    pixels.show()
        
def strobe(pixels, beats=1, color=red):
    target = bpm/beats*.99836269
    
    start = time.time()
    for i in range(1,PIXEL_COUNT):
        pixels.set_pixel(i, color)
    pixels.show()
    end = time.time()
    diff = max(0,target-(end-start))
    time.sleep(diff)
    start = time.time()
    pixels.clear()
    pixels.show()
    end = time.time()
    diff = max(0,target-(end-start))
    time.sleep(diff)
    
def star_pong(pixels, color1=blue, color2=pink):
    sequence = list(range(1, PIXEL_COUNT-STRIP_SIZE))+list(range(STRIP_SIZE,STRIP_SIZE+STRIP_SIZE))+list(range(PIXEL_COUNT-STRIP_SIZE,PIXEL_COUNT))+list([PIXEL_COUNT+1,PIXEL_COUNT+2])+list(reversed(range(PIXEL_COUNT-STRIP_SIZE,PIXEL_COUNT)))+list(reversed(range(STRIP_SIZE,STRIP_SIZE+STRIP_SIZE)))+list(reversed(range(1, PIXEL_COUNT-STRIP_SIZE)))+list([0,-1,-2])
    total = bpm*14*.99774883
    target = total/len(sequence)
    adj = 0
    counter = 0
    for i in sequence:
        counter += 1
        start = time.time()
        if i > PIXEL_COUNT:
            pixels.set_pixel(PIXEL_COUNT-1, color1)
            if i == PIXEL_COUNT+1:
                pixels.set_pixel(PIXEL_COUNT-3, color2)
            elif i == PIXEL_COUNT+2:
                pixels.set_pixel(PIXEL_COUNT-2, color2)
        elif i > 0:
            pixels.set_pixel(i, color1)
            if counter <= PIXEL_COUNT+STRIP_SIZE:
                if i > 1:
                    pixels.set_pixel(i-1, color2)
                    if i > 2:
                        pixels.set_pixel(i-2, color2)
                        if i > 3:
                            pixels.set_pixel(i-3, color2)                            
            elif counter > PIXEL_COUNT+STRIP_SIZE:
                if counter > (PIXEL_COUNT+STRIP_SIZE+3):
                    pixels.set_pixel(i+1, color2)
                    if counter > (PIXEL_COUNT+STRIP_SIZE+4):
                        pixels.set_pixel(i+2, color2)
                        if counter > (PIXEL_COUNT+STRIP_SIZE+5):
                            pixels.set_pixel(i+3, color2)
        else:
            pixels.set_pixel(1, color1)
            if i > -1:
                pixels.set_pixel(3, color2)
            elif i > -2:
                pixels.set_pixel(2, color2)
        
        pixels.show()
        pixels.clear()
        end = time.time()
        diff = max(0,target-(end-start)-adj)
        time.sleep(diff)
        end = time.time()
        adj = max(0,end-start-target)
        
def star_blast(pixels, color1=cyan, color2=pink):
    sequence = range(0,PIXEL_COUNT)
    target = ((bpm*6)/(len(sequence)*2))*.86913871
    start = time.time()
    for i in sequence:
        pixels.set_pixel(i, color1)
        pixels.show()
        end = time.time()
        diff = max(0,target-(end-start))
        time.sleep(diff)
    start = time.time()
    for l in sequence:
        pixels.set_pixel(l, color2)
        pixels.show()
        end = time.time()
        diff = max(0,target-(end-start))
        time.sleep(diff)

def strip(pixels, color=pink, note=3, strip=1):
    strips = PIXEL_COUNT/STRIP_SIZE
    startAt = ((strip-1)*32)
    target = (bpm/4)*note*.96898301

    start = time.time()
    for i in range(startAt,startAt+STRIP_SIZE):
        pixels.set_pixel(i, color)
    pixels.show()
    end = time.time()
    diff = max(0,target-(end-start))
    time.sleep(diff)
    pixels.clear()
    pixels.show()

        
def builder(color=purple,note=16):
    sequence1 = range(0, PIXEL_COUNT/2)
    sequence2 = range(PIXEL_COUNT/2, (PIXEL_COUNT/2)+STRIP_SIZE)
    total = bpm*note*0.99645502
    target = total/(len(sequence1)+len(sequence2))
    adj = 0 
    
    for i in sequence1:
        start = time.time()
        pixels.set_pixel(i, color)
        pixels.show()
        end = time.time()
        diff = max(0,target-(end-start)-adj)
        time.sleep(diff)
        adj = max(0,end-start-target)
    for k in sequence2:
        start = time.time()
        k2 = (PIXEL_COUNT+(2*STRIP_SIZE))-k
        pixels.set_pixel(k, color)
        pixels.set_pixel(k2, color)
        pixels.set_pixel(k+(2*STRIP_SIZE), color)
        pixels.show()
        end = time.time()
        diff = max(0,target-(end-start)-adj)
        time.sleep(diff)
    pixels.clear()
    pixels.show()
    
def strip_reverse(color=red):
    sequence = range(0, STRIP_SIZE)
    total = bpm*.98
    target = total/len(sequence)
    
    start = time.time()
    for i in reversed(sequence):
        pixels.set_pixel(i, color)
        pixels.set_pixel(i+STRIP_SIZE, color)
        pixels.set_pixel(i+(STRIP_SIZE*2), color)
        pixels.set_pixel(i+(STRIP_SIZE*3), color)
        pixels.set_pixel(i+(STRIP_SIZE*4), color)
        pixels.set_pixel(i+(STRIP_SIZE*5), color)
        pixels.show()
    end = time.time()
    diff = max(0,total-(end-start))
    time.sleep(diff)   
    pixels.clear()
    pixels.show()
     

def strip_build(color=red):
    sequence = range(0, STRIP_SIZE)
    total = bpm*.98
    target = total/len(sequence)
    
    start = time.time()
    for i in sequence:
        
        pixels.set_pixel(i, color)
        pixels.set_pixel(i+STRIP_SIZE, color)
        pixels.set_pixel(i+(STRIP_SIZE*2), color)
        pixels.set_pixel(i+(STRIP_SIZE*3), color)
        pixels.set_pixel(i+(STRIP_SIZE*4), color)
        pixels.set_pixel(i+(STRIP_SIZE*5), color)
        pixels.show()
    end = time.time()
    diff = max(0,total-(end-start))
    time.sleep(diff)    
    pixels.clear()
    pixels.show()
    

    
        
        

if __name__ == "__main__":
    pixels.clear()
    pixels.show()
    time.sleep(bpm*4)
    builder()

    strip(pixels, color=red, note=3, strip=1)
    strip(pixels, color=red, note=3, strip=2)
    strip(pixels, color=red, note=3, strip=3)
    time.sleep(bpm)
    
    strip(pixels, color=cyan, note=3, strip=1)
    strip(pixels, color=cyan, note=3, strip=2)
    strip(pixels, color=cyan, note=3, strip=3)
    strip(pixels, color=cyan, note=2, strip=4)
    strip(pixels, color=cyan, note=3, strip=5)
    time.sleep((bpm/4)*3) 
    
    strip(pixels, color=blue, note=2, strip=1)
    strip(pixels, color=blue, note=3, strip=4)
    strip(pixels, color=blue, note=3, strip=2)
    strip(pixels, color=blue, note=4, strip=3)
    strip(pixels, color=blue, note=4, strip=5)
    strip(pixels, color=blue, note=3, strip=6)
    time.sleep((bpm/4)*15)

    strip(pixels, color=pink, note=3, strip=1)
    strip(pixels, color=pink, note=3, strip=4)
    strip(pixels, color=pink, note=3, strip=6)
    time.sleep(bpm)
    
    strip(pixels, color=yellow, note=3, strip=1)
    strip(pixels, color=yellow, note=3, strip=2)
    strip(pixels, color=yellow, note=3, strip=3)
    strip(pixels, color=yellow, note=2, strip=5)
    strip(pixels, color=yellow, note=2, strip=6)
    time.sleep(bpm)
    
    strip(pixels, color=silver, note=2, strip=3)
    strip(pixels, color=silver, note=3, strip=4)
    strip(pixels, color=silver, note=3, strip=6)
    strip(pixels, color=silver, note=2, strip=5)
    strip(pixels, color=silver, note=3, strip=2)
    strip(pixels, color=silver, note=3, strip=1)
    strip(pixels, color=silver, note=2, strip=3)
    strip(pixels, color=silver, note=3, strip=4)
    time.sleep((bpm/4)*13)
    star_pong(pixels)
    star_pong(pixels)
    star_blast(pixels)
    
    strobe(pixels,beats=8)
    strobe(pixels,beats=8)
    strobe(pixels,beats=8)
    strobe(pixels,beats=8)
    halfs(pixels,color1 = pink, color2 = purple)
    halfs(pixels,color1 = purple, color2 = maroon)
    halfs(pixels)
    halfs(pixels,color2=pink)
    halfs(pixels)
    halfs(pixels,color2=pink)
    halfs(pixels)
    halfs(pixels,color2=pink)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    alternator(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    strip_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    cross_pong(pixels)
    strobe(pixels,beats=4)
    strobe(pixels,beats=4)
    strobe(pixels,beats=4)
    strobe(pixels,beats=4)
    time.sleep(bpm)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    time.sleep(bpm*5.99)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    time.sleep(bpm*5.99)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    time.sleep(bpm*5.98)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    time.sleep(bpm*4)
    strip_build()
    #strobe(pixels,beats=6.02)
    #strobe(pixels,beats=6.02)
    #strobe(pixels,beats=6.03)
    #time.sleep(bpm)
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    
    
    strip_build()
    strip_reverse()
    strip_build()
    strip_reverse()
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    
    
    strip_build()
    strip_reverse()
    strip_build()
    strip_reverse()
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    
    
    strip_build()
    strip_reverse()
    strip_build()
    strip_reverse()
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strobe(pixels,beats=4.03)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip(pixels, color=blue, note=.62, strip=6)
    strip(pixels, color=blue, note=.62, strip=5)
    strip(pixels, color=blue, note=.62, strip=4)
    strip(pixels, color=blue, note=.62, strip=3)
    strip(pixels, color=blue, note=.62, strip=2)
    strip(pixels, color=blue, note=.62, strip=1)
    strip_build()
    strip_reverse()
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    strobe(pixels,beats=4.02)
    #start = time.time()
    rainbow_cycle(pixels, wait=(bpm/28))
    rainbow_cycle(pixels, wait=(bpm/28))
    #end = time.time()
    #print(end-start)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=6)
    strip(pixels, color=blue, note=.94, strip=3)
    strip(pixels, color=pink, note=.94, strip=6)
    strip(pixels, color=red, note=.94, strip=6)
    strip(pixels, color=yellow, note=.94, strip=5)
    strip(pixels, color=green, note=.94, strip=2)
    strip(pixels, color=blue, note=.94, strip=5)
    strip(pixels, color=pink, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=1)
    strip(pixels, color=silver, note=.94, strip=4)
    strip(pixels, color=purple, note=.94, strip=6)
    strip(pixels, color=pink, note=.94, strip=3)
    strip(pixels, color=blue, note=.94, strip=6)
    strip(pixels, color=green, note=.94, strip=4)
    strip(pixels, color=yellow, note=.94, strip=1)
    strip(pixels, color=red, note=.94, strip=4)
    strip(pixels, color=silver, note=.94, strip=5)
    strip(pixels, color=red, note=.94, strip=2)
    strip(pixels, color=yellow, note=.94, strip=5)
    appear_from_back(pixels)
    disappear_from_back(pixels)
    #strip_build(color=green)
    strip_build(color=green)
    strobe(pixels, beats=2.0, color = green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=4.0,color=green)
    
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=4.0,color=green)
    
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=4.0,color=green)
    
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=4.0,color=green)
    
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=2.67)
    strobe(pixels,beats=4.0)
    
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=2.67,color=pink)
    strobe(pixels,beats=4.0,color=pink)
    
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=2.67,color=green)
    strobe(pixels,beats=4.0,color=green)
    
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=2.67,color=cyan)
    strobe(pixels,beats=4.0,color=cyan)
    
    strip(pixels, color=red, note=3, strip=1)
    strip(pixels, color=red, note=3, strip=2)
    strip(pixels, color=red, note=3, strip=3)
    time.sleep(bpm)
    
    strip(pixels, color=cyan, note=3, strip=1)
    strip(pixels, color=cyan, note=3, strip=2)
    strip(pixels, color=cyan, note=3, strip=3)
    strip(pixels, color=cyan, note=2, strip=4)
    strip(pixels, color=cyan, note=3, strip=5)
    time.sleep((bpm/4)*3) 
    
    strip(pixels, color=blue, note=2, strip=1)
    strip(pixels, color=blue, note=3, strip=4)
    strip(pixels, color=blue, note=3, strip=2)
    strip(pixels, color=blue, note=4, strip=3)
    strip(pixels, color=blue, note=4, strip=5)
    strip(pixels, color=blue, note=3, strip=6)
    time.sleep((bpm/4)*15)

    strip(pixels, color=pink, note=3, strip=1)
    strip(pixels, color=pink, note=3, strip=4)
    strip(pixels, color=pink, note=3, strip=6)
    time.sleep(bpm)
    
    strip(pixels, color=yellow, note=3, strip=1)
    strip(pixels, color=yellow, note=3, strip=2)
    strip(pixels, color=yellow, note=3, strip=3)
    strip(pixels, color=yellow, note=2, strip=5)
    strip(pixels, color=yellow, note=2, strip=6)
    time.sleep(bpm)
    
    strip(pixels, color=silver, note=2, strip=3)
    strip(pixels, color=silver, note=3, strip=4)
    strip(pixels, color=silver, note=3, strip=6)
    strip(pixels, color=silver, note=2, strip=5)
    strip(pixels, color=silver, note=3, strip=2)
    strip(pixels, color=silver, note=3, strip=1)
    strip(pixels, color=silver, note=2, strip=3)
    strip(pixels, color=silver, note=3, strip=4)
    time.sleep((bpm/4)*9)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strip(pixels, color=cyan, note=.62, strip=6)
    strip(pixels, color=cyan, note=.62, strip=5)
    strip(pixels, color=cyan, note=.62, strip=4)
    strip(pixels, color=cyan, note=.62, strip=3)
    strip(pixels, color=cyan, note=.62, strip=2)
    strip(pixels, color=cyan, note=.62, strip=1)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=2.0, color = blue)
    strobe(pixels, beats=2.0, color = pink)
    strobe(pixels, beats=4.0)
    strobe(pixels, beats=4.0)
    strobe(pixels, beats=4.0)
    strobe(pixels, beats=4.0)
    
    
    
    
    
    





    

    
    
    #strip_build()
    #i = 0
    #while i <= 2:
    #    strobe(pixels)
    #    alternator(pixels)
    #    halfs(pixels)
    #    i+=1
    #double_pong(pixels)
    
    
        #print(pixels._pixels)
        #pixels.set_pixels(off)
        #pixels.show()
        #pixels.clear()
        #lol = 1
        #while lol <= 25:
        #strobe(pixels)
        #    lol += 1
        #halfs(pixels)
        #cross_pong(pixels)
        #mid_pong(pixels)
        #double_pong(pixels)
        #
        #i += 1
    #brightness_decrease(pixels)
    #pixels.show()
    pixels.clear()
    
    #pixels.set_pixel(31,pink)
    #pixels.show()