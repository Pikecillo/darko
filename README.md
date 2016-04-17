# DigiDark

**DigiDark** is an interpreter of image transformations inspired by *Popi* (Portable Pico), described
in the classical book
[Beyond Photography: The Digital Darkroom](http://spinroot.com/pico/)
by Gerard J. Holzmann.

**DigiDark** is written in Python. To run it you need to install [numpy](http://www.scipy.org/scipylib/download.html) and [OpenCV](opencv.org/downloads.html). Python 3 is not supported yet.

Have fun distorting some pictures with one-liners.

Please report any bugs to: mario.rincon.nigro@gmail.com

## Example transformations

Let's apply some transformations on the following picture of Richard Feynman 
(scientist/physics-professor/safe-cracker extraordinaire)

![Feynman](docs/images/feynman.jpg)

Getting DigiDark ready and loading the image

	import digidark.interpreter
	
	# Create an interpreter
	ddi = digidark.interpreter.Interpreter()
	
	# Load an image, and reads subpixels with bilinear interpolation
	ddi.load('feynman.jpg', sampling='bilinear')

Rotating the image by 45 degrees

	# Apply the transformation
	ddi.eval('new[x, y] = old[rect(r, a + rad(45))]')
	# Save result to a file
	ddi.save('feynman-rotated.jpg')

![Feynman](docs/images/feynman-rotated.jpg)

Zooming-in on the image

	ddi.eval('new[x, y] = old[rect(r / 2, a)]')
	ddi.save('feynman-zoomed.jpg')

![Feynman](docs/images/feynman-zoomed.jpg)

Mirroring and translating the image

	ddi.eval('new[x, y] = old[abs(X / 2 - x), y]')
	ddi.save('feynman-mirrored.jpg')

![Feynman](docs/images/feynman-mirrored.jpg)

Thresholding the image in 2-pixel blocks

	transformation = """
	    new[x, y] = gray(old[floor(x / 2) * 2, floor(y / 2) * 2]) > 150 ?
    	    rgb(255, 255, 255) : rgb(0, 0, 0)
	"""
	ddi.eval(transformation)
	ddi.save('feynman-icon.jpg')

![Feynman](docs/images/feynman-icon.jpg)

A Warhol-like mosaic

  	transformation = """
	    new[x, y] =
    	        old[x % (X / 2) * 2, y % (Y / 2) * 2] *
        	    ((x < X / 2 ?
            	        (y < Y / 2 ? rgb(255, 0, 0) : rgb(0, 255, 0)) :
            		(y < Y / 2 ? rgb(255, 255, 0) : rgb(0, 255, 255))) / Z)
	"""
	ddi.eval(transformation)
	ddi.save('feynman-mosaic.jpg')

![Feynman](docs/images/feynman-mosaic.jpg)

A funky late 60s or early 70s look

	transformation = """
	    new[x, y] =
    	        0.33 * ((gray(Z - old[x - 25, y]) / Z) * rgb(0, 0, 255)) +
    		0.33 * ((gray(Z - old[x, y]) / Z) * rgb(0, 255, 0)) +
    		0.33 * ((gray(Z - old[x + 25, y]) / Z) * rgb(255, 0, 0))
	"""
	ddi.eval(transformation)
	ddi.save('docs/images/feynman-lsd.jpg')

![Feynman](docs/images/feynman-lsd.jpg)

## Predefined Variables

Note: the origin of polar coordinates is at the center of the image. The origin of the
rectangular coordinates is at the top-left corner of the image.

**old**: original image

**new**: transformed image

**x**: current pixel's x in rectangular coordinates

**y**: current pixel's y in rectangular coordinates

**r**: current pixel's radius in polar coordinates

**a**: current pixel's angle (in radians) in polar coordinates

**cx**: x of center of image rectangular coordinates

**cy**: y of center of image rectangular coordinates

**R**: Half-length of image diagonal

**X**: Width of image

**Y**: Height of image

**Z**: Depth of image (255)

## Available operators

The following operators can be used within expressions

Arithmetic: +, -, *, /, **, %

Comparison: <, >, ==, !=, <=, >=

Logic: &&, ||

Trinary: cond ? texpr : fexpr

## Available functions

**rect(r, a) -> (x, y)**: Polar to rectangular coordinates

**polar(x, y) -> (r, a)**: Rectangular to polar coordinates

**sin(x)**: Sine

**cos(x)**: Cosine

**sqrt(x)**: Square root

**deg(x)**: Radians to degrees

**rad(x)**: Degrees to radians 

**gray(p)**: Gray level of pixel

**rgb(r, g, b)**: Color tuple

**ceil(x)**: Ceiling

**floor(x)**: Floor

## Catalogue of Transformations

See the catalogue of example transformations [here](docs/catalogue.md "Catalogue").
