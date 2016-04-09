## Catalogue of Transformations

Most of the following transformations were taken from
[Beyond Photography: The Digital Darkroom](http://spinroot.com/pico/).
In the following no offense is meant to anyone (not
even to the politicians :P)

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
	new[x, y - gray(old[x, y]) * 0.1] = old[x, y]
![Nadella](images/catalogue/nadella.jpg "Nadella")
![Nadella Bentley](images/catalogue/nadella-bentley.jpg "Nadella Bentley")

[Back](../README.md).