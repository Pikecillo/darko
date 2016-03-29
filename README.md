# DigiDark

**DigiDark** is an interpreter of image transformations inspired by *Popi* (Portable Pico), described
in the classical book
[Beyond Photography: The Digital Darkroom](http://spinroot.com/pico/)
by Gerard J. Holzmann.

Have fun distorting some pictures with one-liners.

## Example

The following code rotates an image by 180 degrees

	import digidark.interpreter
	
	ddi = digidark.interpreter.Interpreter()
	
	ddi.load('images/foo.jpg', sampling='bilinear')
	ddi.eval('new[x, y] = old[rect(r, a + rad(180))]')
	ddi.save('images/upsidedown-foo.jpg')

## Available operators

The following operators can be used in transformations: +, -, *, /, **, %

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

## Available functions

**rect(r, a) -> (x, y)**: Polar to rectangular coordinates

**polar(x, y) -> (r, a)**: Rectangular to polar coordinates

**sin(x)**: Sine

**cos(x)**: Cosine

**deg(x)**: Radians to degrees

**rad(x)**: Degrees to radians 

**avg(p)**: Gray level of pixel

**ceil(x)**: Ceiling of x

**floor(x)**: Floor of x

## Catalogue of Transformations

Most of the following transformations were taken from Beyond Photography:
The Digital Darkroom. In the following no offense is meant to anyone (even
politicians :P)

###  Twist
	new[x, y] = old[rect(r, a - r / 50)]
![Putin](images/catalogue/putin.jpg "Putin")
![Putin Twist](images/catalogue/putin-twist.jpg "Putin Twist")

###  Bath
	new[x, y] = old[x + (x % 32) - 16, y]
![Merkel](images/catalogue/merkel.jpg "Merkel")
![Merkel Bath](images/catalogue/merkel-bath.jpg "Merkel Bath")

###  Wave
	new[x, y] = old[x + 10 * sin(rad(y) * 10), y]
![Obama](images/catalogue/obama.jpg "Obama")
![Obama Wave](images/catalogue/obama-wave.jpg "Obama Wave")

### Funhouse
	new[x, y] = old[x + sin(rad(x)) * 150, y + sin(rad(y * 1.18)) * 89]
![Jinping](images/catalogue/jinping.jpg "Jinping")
![Jinping Funhouse](images/catalogue/jinping-funhouse.jpg "Jinping Funhouse")

###  Pond
	new[x, y] = old[x, y + 10 * sin(rad(y) * 10)]
![Cameron](images/catalogue/cameron.jpg "Cameron")
![Cameron Pond](images/catalogue/cameron-pond.jpg "Cameron Pond")

### Negative
	new[x, y] = Z - old[x, y]
![Cook](images/catalogue/cook.jpg "Cook")
![Cook Negative](images/catalogue/cook-negative.jpg "Cook Negative")

###  Spiralbath
	new[x, y] = old[x, y + (deg(a) + r / 4) % 64 - 16]
![Gates](images/catalogue/gates.jpg "Gates")
![Gates Spiralbath](images/catalogue/gates-spiralbath.jpg "Gates Spiralbath")

###  Fisheye
	new[x, y] = old[rect(1.5 * r ** 2 / R, a)]
![Bezos](images/catalogue/bezos.jpg "Bezos")
![Bezos](images/catalogue/bezos-fisheye.jpg "Bezos Fisheye")

###  Caricature
	new[x, y] = old[rect(0.5 * sqrt(r * R), a)]
![Page](images/catalogue/page.jpg "Page")
![Page Caricature](images/catalogue/page-caricature.jpg "Page Caricature")

### Curly
	new[x, y] = old[x + 10 * sin(rad(y) * 5), y + 10 * sin(rad(x) * 5)]
![Brin](images/catalogue/brin.jpg "Brin")
![Brin Curly](images/catalogue/brin-curly.jpg "Brin Curly")

###  Sink
	new[x, y] = old[rect(r + 10 * sin(rad(r) * 10), a - r / 50)]
![Ma](images/catalogue/ma.jpg "Ma")
![Ma Sink](images/catalogue/ma-sink.jpg "Ma Sink")

### T2000
	new[x, y] = old[rect(1.5 * r ** 2 / R + 10 * sin(rad(r) * 10), a)]
![Zuckerberg](images/catalogue/zuckerberg.jpg "Zuckerberg")
![Zuckerberg T2000](images/catalogue/zuckerberg-t2000.jpg "Zuckerberg T2000")

### Pixel
	new[x, y] = old[floor(x / 10) * 10, floor(y / 10) * 10]
![Musk](images/catalogue/musk.jpg "Musk")
![Musk](images/catalogue/musk-pixel.jpg "Musk Pixel")

###  Bentley
	new[x, y - avg(old[x, y]) * 0.1] = old[x, y]
![Nadella](images/catalogue/nadella.jpg "Nadella")
![Nadella Bentley](images/catalogue/nadella-bentley.jpg "Nadella Bentley")
