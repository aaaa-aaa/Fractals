'''
Date: 10/25/18
Description: Running this programs generates png images of 3 different fractals, 2 from the mandelbrot set and 1 of a fractal tree.
Credits:
Thanks to Knute Broady for telling me about the ImageDraw and ImageOps module.
Thanks to Kevin Xie for suggesting that I can add a pattern to areas, and for telling me that range() starts from 0 by default.
This made my code a little more concise, allowing me to do range(imgx) instead of range(0,imgx).
Thanks to Eyad Almoamen for suggesting that I can make the rainbow cycle through more than once.

I referred to the following websites:
Learned more about tuples here: https://www.tutorialspoint.com/python/python_tuples.htm
Found the colorsys HSV to RGB converter here: https://docs.python.org/2/library/colorsys.html#module-colorsys
Learned about ImageDraw here: https://pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html
Found the getpixel function, allowing me to replace the tree here: https://pillow.readthedocs.io/en/5.1.x/reference/Image.html
Found image filters here: https://pillow.readthedocs.io/en/5.1.x/reference/ImageFilter.html
Found image operations here: https://pillow.readthedocs.io/en/5.1.x/reference/ImageOps.html
Found the code for the fractal tree here: https://rosettacode.org/wiki/Fractal_tree#Python

Honor Pledge: On my honor, I have neither given nor received unauthorized aid. Anan Aramthanapon

Explanation:
I improved on the basics we discussed in class in the following ways:
First, I experimented heavily with the HSV colorspace and I was able to achieve pretty rainbow colors thanks to it.
I also did a lot of work with trigonometry and circle to create circular patterns for fills.
I flipped the y coordinate so that 0,0 is the bottom left. This makes it easier to zoom into the desired area of the Mandelbrot Set.
I did not do the Julia Set, but I made a fractal tree instead for my third fractal.
This required me to learn how to make it image in a way other than graphing, as the fractal tree is not described on a graph.
To do this, I learned a new way to add colors to images in PILLOW: ImageDraw.
I also learned the functions of two other PILLOW modules: ImageFilter and ImageOps, to further enhance my images.
The image filter allowed me to smooth out my second image.
The border function from ImageOps allowed me to add a border to my third image.
'''

from PIL import Image, ImageFilter, ImageDraw, ImageOps
import colorsys
import math

# Functions for more complicated fills
def bwfill(x,y,placex,placey): # Creates a black and white gradient based around the center, flipping directions every 15 degrees.
	radius = (x**2 + y**2)**0.5 # Finds distance from the image center
	if x == 0: # To avoid diving by 0 error:
		angle = math.pi/2 # If x is 0, then the angle is 90 degrees
	else:
		angle = math.atan(y/x) # If x is not 0, use arctan to find the angle.
	angleindex = angle//(math.pi/12) # New index every 15 degrees.
	gradient = 255*((x**2+y**2)**0.5)/(2)**0.5 # Maps the distance from the origin to a color value. Changes the range from (0 to 2**0.5) to (0 to 255)
	if angleindex%2 == 0: # For every other gradient:
		gradient = 255 - gradient # Flip the direction of the gradient.
	gradient = int(gradient) # To avoid float error when doing putpixel.
	image2.putpixel((placex,placey),(gradient,gradient,gradient)) # R = G = B makes the gradient black and white

def rainbowWheel(x,y,placex,placey,shift): # Picks a color based on the angle the point makes from the origin
	if x == 0: # To avoid diving by 0 error:
		angle = math.pi/2 # If x is 0, then the angle is 90 degrees
	else:
		angle = math.atan(y/x) # If x is not 0, use arctan to find the angle.
	if angle < 0:
		angle = math.pi + angle # changes the range from (-pi/2 to pi/2) to (0 to pi)
	if shift == True: # The second rainbow wheel is just the first with a shifted H value.
		H = angle/math.pi + 0.66 # Shifts the H value in the HSV for adjacent rings to "rotate" the second rainbow wheel. I found that a shift by 0.66 looks the nicest.
	else:
		H = angle/math.pi # Maps the angle to an H value.
	floatRGB = (colorsys.hsv_to_rgb(H,1,255)) # Convert HSV to RGB
	tupRGB = (int(floatRGB[0]),int(floatRGB[1]),int(floatRGB[2])) # Make the RGB value an integer and a tuple.
	image3.putpixel((placex,placey),tupRGB) # Color in.

# Function for recursion: Drawing the fractal tree.
def drawTree(x,y,angle,iterations):
	c = imgx/256 # Constant multiplier changes with image size.
	if iterations != 0: # When branches are still allowed to grow.
		xnew = x + int(math.cos(math.radians(angle)) * iterations * c) # Finds new x coordinate using trigonometry
		ynew = y - int(math.sin(math.radians(angle)) * iterations * c) # Finds new y coordinate
		draw3 = ImageDraw.Draw(image3)
		draw3.line([(x,y),(xnew,ynew)],(255,0,0),1) # I draw the tree in red here just as a placeholder. All the red gets replaced later on.
		drawTree(xnew,ynew,angle+21,iterations-1) # Recursions
		drawTree(xnew,ynew,angle-21,iterations-1)

'''
Much of the code for the drawing of the fractal tree has been adapted from https://rosettacode.org/wiki/Fractal_tree#Python
This code creates a new x,y coordinate from the 4 parameters.
The distance between the new coordinate and the old depends on the iteration (the "branch number" of the tree) and the constant c.
I made the constant c scale with image resolution so that the tree remains the same height regardless of resolution.
The draw.line() then draws a line from the original x,y coordinate to the new x,y coordinate
I have experimented with making the branch thickness scale with the iteration like the branch length, but that looked bad so I decided to make the thickness 1
A thickness of 1 is the thinnest line possible and shows as much of the details of the tree as possible.
From the new coordinate, the function recurses, now using that coordinate as the starting point
The function recurses twice, shifting the angle from the original by 21 degrees each.
I have experimented with different amounts of angles shifts. 21 is the highest I can go without having my 2 trees come too close and overlap.
The larger the angle, the more spread out the tree is, and the easier it is to see details, so I went with the largest possible angle.
With each recursion, the iteration number goes down so the branches become shorter.
'''

imgx,imgy = 512,512 # Dimensions for the first image

#Makes image1
image1 = Image.new("RGB",(imgx,imgy))
xmin,xmax = 0.27415,0.2746
ymin,ymax = -0.00649,-0.00604
boxno = 32 # Number of boxes in checkerboard.
for xcoord in range(imgx): # For every x value:
	xfrac = xcoord*(xmax-xmin)/imgx + xmin # Remap the (0 to imgx) to (xmin to xmax).
	index1 = xcoord//(imgx//boxno) # Splits the board into boxno number of columns.
	for ycoord in range(imgy): # For every y value:
		yfrac = (imgy-ycoord)*(ymax-ymin)/imgy + ymin # Remap the (imgy to 0) to (xmin to xmax). Flips the y coordinate so bottom left is 0,0.
		index2 = ycoord//(imgy//boxno) # Splits the board into boxno number of rows.
		count = 0 # Counter for number of iterations
		zx,zy = 0,0 # Starting z values
		while True:
			if count == 256 or (zx**2 + zy**2)**0.5 > 2: # Once the math is iterated 256 times or the value escapes, stop.
				break
			else: # Does the fractal math
				zx,zy = zx**2 - zy**2 + xfrac,2*zx*zy + yfrac
				count += 1 # Add 1 to iteration counter
		if count == 256: # Anything that "doesn't escape" (I only checked to 256) gets a checkerboard fill.
			if (index1+index2)%2 == 1: # If the column number + row number is odd.
				image1.putpixel((xcoord,ycoord),(255,255,255)) # Make it white
				# If it is even, don't do anything, so it remains black.
		else: # Everything that escapes gets a HSV rainbow fill.
			H = count/255 # Remaps count as H by changing the range from (0 to 255) to (0 to 1).
			H = H*3 # Multiplying by 3 causes the rainbow to cycle 3 times instead of 1.
			floatRGB = (colorsys.hsv_to_rgb(H,1,255)) # Convert HSV to RGB.
			tupRGB = (int(floatRGB[0]),int(floatRGB[1]),int(floatRGB[2])) # Make the RGB value integers and a tuple.
			image1.putpixel((xcoord,ycoord),tupRGB) # Color in.
image1.save("fractalfinal1.png","PNG")

#Makes image2
image2 = Image.new("RGB",(imgx,imgy))
xmin,xmax = -0.67622,-0.67582
ymin,ymax = -0.3624,-0.3620
for xcoord in range(imgx): # For every x value:
	xfrac = xcoord*(xmax-xmin)/imgx + xmin # Remap the (0 to imgx) to (xmin to xmax).
	xcir = xcoord*2/imgx - 1 # Remap the (0 to imgx) to (-1 to 1).
	for ycoord in range(imgy): # For every y value:
		yfrac = (imgy-ycoord)*(ymax-ymin)/imgy + ymin # Remap the (imgy to 0) to (ymin to ymax). Flips the y coordinate so bottom left is 0,0.
		ycir = ycoord*2/imgy - 1 # Remap the (0 to imgy) to (1 to -1).
		count = 0 # Counter for number of iterations
		zx,zy = 0,0 # Starting z values
		while True:
			if count == 256 or (zx**2 + zy**2)**0.5 > 2: # Once the math is iterated 256 times or the value escapes, stop.
				break
			else: # Does the fractal math
				zx,zy = zx**2 - zy**2 + xfrac,2*zx*zy + yfrac
				count += 1 # Add 1 to iteration counter
		if count <= 180: # Anything that escaped in 180 or fewer iterations gets the bwfill.
			bwfill(xcir,ycir,xcoord,ycoord)
		elif count == 256: # Anything that "doesn't escape" (I only checked to 256) gets black.
			image2.putpixel((xcoord,ycoord),(0,0,0))
		else: # Everything else gets an HSV rainbow fill.
			H = count/255 # Remaps count as H by changing the range from (0 to 255) to (0 to 1).
			floatRGB = (colorsys.hsv_to_rgb(H,1,255)) # Convert HSV to RGB.
			tupRGB = (int(floatRGB[0]),int(floatRGB[1]),int(floatRGB[2])) # Make the RGB value integers and a tuple.
			image2.putpixel((xcoord,ycoord),tupRGB) # Color in.
image2 = image2.filter(ImageFilter.SMOOTH_MORE) # Applies a smoothing filter to image.
image2.save("fractalfinal2.png","PNG")

#Makes image3
image3 = Image.new("RGB",(imgx,imgy))
drawTree(imgx/2,imgy/2,270,15) # Draw a fractal tree upwards with 15 iterations
drawTree(imgx/2,imgy/2,90,15) # Draw a fractal tree downwards with 15 iterations
for xcoord in range(imgx): # For every x value:
	xcir = xcoord*2/imgx - 1 # Remaps x coordinate system to (-1 to 1)
	for ycoord in range(imgy): # For every y value:
		ycir = (imgy-ycoord)*2/imgy - 1 # Remaps y coordinate system to (1 to -1)
		radius = (xcir**2 + ycir**2)**0.5 # Radius of point from center of image
		rstep = 0.05 # Distance between each ring and the next
		index = (radius//rstep) # Stores the "ring number" of every pixel
		pixcolor = image3.getpixel((xcoord,ycoord)) # Gets the pixel color of location
		if pixcolor == (255,0,0): # If the pixel is red (from drawTree):
			index += 1 # Add 1 to the index
		if index%2 == 0: # Mod 2 of index allows for 2 rainbow wheels. Depending on whether the index is even or odd, it is filled with a different rainbow wheel.
			rainbowWheel(xcir,ycir,xcoord,ycoord,True) # Wheel 1
		else:
			rainbowWheel(xcir,ycir,xcoord,ycoord,False) # Wheel 2
border = int(imgx/32) # Border thickness scales with image resolution.
image3 = ImageOps.expand(image3,border,(255,255,255)) # Add a white border around image.
image3 = ImageOps.expand(image3,border,(0,0,0)) # Then add a black border around image.
image3.save("fractalfinal3.png","PNG")