from PIL import Image, ImageDraw

class bbox:
    def __init__(self, dots, dist):
        xs, ys = zip(*dots)
        self.x1 = min(xs) - dist
        self.y1 = min(ys) - dist
        self.x2 = max(xs) + dist
        self.y2 = max(ys) + dist

def find_dist(dot1, dot2):
    return ((dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2)**.5
    
def make_offset_curve(curve, matrix_height, matrix_width, dist):
    
    curve_bbox = bbox(curve, dist+1)
    
    offset_curve = []
    for y in range(curve_bbox.y1, curve_bbox.y2):
        print((y - curve_bbox.y1)/(curve_bbox.y2 - curve_bbox.y1))
        for x in range(curve_bbox.x1, curve_bbox.x2):
            closest_elem = min(curve, key=lambda dot: find_dist(dot, (x, y)))
            
            float_dist = find_dist((x,y), closest_elem)
            int_dist = int(float_dist)
            
            if int_dist == dist:
                offset_curve.append((x,y))
    
    return offset_curve

image = Image.open('test1.jpg') #Открываем изображение.
image.convert('RGBA')
draw = ImageDraw.Draw(image) #Создаем инструмент для рисования.
width = image.size[0] #Определяем ширину.
height = image.size[1] #Определяем высоту.
pix = image.load() #Выгружаем значения пикселей.

orig_curve = []
for x in range(width):
    for y in range(height):
        intens = sum(pix[x, y][0:2]) / 3
        if intens < 50:
            orig_curve.append((x,y))

print(len(orig_curve))
offset_curve = make_offset_curve(orig_curve, height, width, 10)
            
for dot in offset_curve:
    draw.point(dot, (255, 16, 210))

image.save("some_shit.jpg", "JPEG")
