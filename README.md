# DigiDark

**DigiDark** is an interpreter of image transformations inspired by *Popi* (Portable Pico), described
in the classical book
[Beyond Photography: The Digital Darkroom](http://spinroot.com/pico/)
by Gerard J. Holzmann.

**DigiDark** is written in Python. To run it you need to install [numpy](http://www.scipy.org/scipylib/download.html) and [OpenCV](opencv.org/downloads.html)  

Have fun distorting some pictures with one-liners.

Please report any bugs to: mario.rincon.nigro@gmail.com

## Example

The following code rotates an image by 180 degrees

	import digidark.interpreter
	
	ddi = digidark.interpreter.Interpreter()
	
	ddi.load('images/foo.jpg', sampling='bilinear')
	ddi.eval('new[x, y] = old[rect(r, a + rad(180))]')
	ddi.save('images/upsidedown-foo.jpg')

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

The following operators can be used in transformations: +, -, *, /, **, %

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

**choice(c, t, f)**: Return t if c evaluates to true, f otherwise

**ceil(x)**: Ceiling

**floor(x)**: Floor

## Catalogue of Transformations

See the catalogue [here](docs/catalogue.md "Catalogue").
