import random
from PIL import Image, ImageDraw
import matplotlib.mlab as mlab

mode = input('mode: ').strip()
image = Image.open('lenna-256.jpg') #Открываем изображение.
image.convert('RGBA')
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

if mode == 'gray':
    for i in range(width):
        print(i)
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            draw.point((i, j), (S, S, S))
    image.save("gray.jpg", "JPEG")

elif mode == 'negative':
    for i in range(width):
        print(i)
        for j in range(height):
            a = 255-pix[i, j][0]
            b = 255-pix[i, j][1]
            c = 255-pix[i, j][2]
            draw.point((i, j), (a, b, c))
    image.save("negative.jpg", "JPEG")

elif mode == 'sepia':
    depth = int(input('depth: '))
    for i in range(width):
        print(i)
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a + b + c) // 3
            a = S + depth * 2
            b = S + depth
            c = S
            if a > 255: a = 255
            if b > 255: b = 255
            draw.point((i, j), (a, b, c))
    image.save("sepia.jpg", "JPEG")

elif mode == 'noise':
    noisemode = input('noisemode (bw or color): ')
    factor = int(input('factor: '))
    for i in range(width):
        print(i)
        for j in range(height):
            if noisemode == 'bw':
                rand = random.randint(-factor, factor)
                a = pix[i, j][0] + rand
                b = pix[i, j][1] + rand
                c = pix[i, j][2] + rand
            elif noisemode == 'color':
                a = pix[i, j][0] + random.randint(-factor, factor)
                b = pix[i, j][1] + random.randint(-factor, factor)
                c = pix[i, j][2] + random.randint(-factor, factor)
            if a > 255: a = 255
            elif a < 0: a = 0
            if b > 255: b = 255
            elif b < 0: b = 0
            if c > 255: c = 255
            elif c < 0: c = 0
            draw.point((i, j), (a, b, c))
    image.save("noise.jpg", "JPEG")

elif mode == 'bw':
    factor = int(input('factor: '))
    for i in range(width):
        print(i)
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            S = (a+b+c) // 3
            if S > factor:
                S = 255
            else:
                S = 0
            draw.point((i, j), (S, S, S))
    image.save("bw.jpg", "JPEG")
    
elif mode == 'make yellow':
    for i in range(width):
        print(i)
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            a = pix[i, j][3]
            draw.point((i, j), (r, g, 0, a))
            
    image.save('yellow.png')
            
elif mode == 'gauss':
    sigma = 1 #int(input('sigma: '))
    max_half_ampl = 4
    coeff = 2
    
    new_image = image
    draw = ImageDraw.Draw(new_image)
    
    for x in range(width):
        print(str(x/width*100) + '%')
        for y in range(height):
            r, g, b = pix[x, y][0:3]
            for i in range(x - max_half_ampl, x + max_half_ampl + 1):
                for j in range(y - max_half_ampl, y + max_half_ampl + 1):
                    if not (i != x and j != y) and 0 < i < width - 1 and 0 < j < height - 1:
                        nr, ng, nb = pix[i, j][0:3]
                        dist = ((x-i)**2 + (y-j)**2)*0.5
                        alpha = mlab.normpdf(dist, 0, sigma) * coeff
                        
                        nr = int(r * alpha + nr * (1 - alpha))
                        ng = int(g * alpha + ng * (1 - alpha))
                        nb = int(b * alpha + nb * (1 - alpha))
                        
                        draw.point((i,j), (nr, ng, nb))
                        
    new_image.save('gauss.jpg')
                    
                    
                    
                    
                    

