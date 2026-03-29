import math
import sys
from PIL import Image


def computeMandelbrotImage(name, borders, size, maxIter):
    img = Image.new('RGB', size, "black")
    computeMandelbrot(img, borders, maxIter)
    img.save(name)


def computeMandelbrot(img, borders, maxIter):
    pixels = img.load()

    setPixels(pixels, borders, img.size, maxIter)


def setPixels(pixels, borders, size, maxIter):
    start = borders[0]
    end = borders[1]
    progressIncrement = size[0] / 50
    progressIterator = 0.0
    for i in range(size[0]):
        if (i > progressIterator):
            print('Progress : ', 100 * progressIterator / size[0], '%', sep='')
            progressIterator += progressIncrement
        for j in range(size[1]):
            pixels[i, j] = computeColor(start, end, size, (i, j), maxIter)

    print("Done")


def computeColor(start, end, size, iter, maxIter):
    c = getComplex(start, end, size, iter)
    i = computeNumberMandelbrotIterations(c, maxIter)

    if math.isnan(i):
        i = sys.maxsize

    return getColorsFromIterations(i, maxIter)


def getComplex(start, end, size, iter):
    x = end[0] - start[0]
    y = end[1] - start[1]
    a = (x * iter[0]) / size[0] + start[0]
    b = (y * iter[1]) / size[1] + start[1]
    return complex(a, b)


def computeNumberMandelbrotIterations(c, maxIter):
    z = 0j
    i = 0

    while (z.real * z.real + z.imag * z.imag <= 4.0) and (i < maxIter):
        z = z ** 2 + c
        i += 1

    return i


def getColorsFromIterations(iter, maxIter):
    # r = int(510 / (2 - (iter / maxIter)) - 255)
    # g = int(280.5 / (11 - (10 * iter / maxIter)) - 25.5)
    # b = int(318.75 / (5 - (4 * iter / maxIter)) - 63.75)
    r = g = b = int(255 * iter / maxIter)

    return (r, g, b)


name = "mandelbrot9.png"
start = (-0.264, 0.842)
end = (-0.254, 0.852)
# start = (-2, -2)
# end = (1, 2)
borders = (start, end)
size = (8000, 8000)
maxIter = 100
computeMandelbrotImage(name, borders, size, maxIter)

name = "mandelbrot10.png"
start = (-0.27, 0.84)
end = (-0.25, 0.86)
borders = (start, end)
computeMandelbrotImage(name, borders, size, maxIter)

name = "mandelbrot11.png"
start = (-0.3, 0.8)
end = (-0.2, 0.9)
borders = (start, end)
computeMandelbrotImage(name, borders, size, maxIter)

name = "mandelbrot12.png"
start = (-0.3, 0.7)
end = (0, 1)
borders = (start, end)
computeMandelbrotImage(name, borders, size, maxIter)
