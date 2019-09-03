import random, time

while True:
    key = input()
    if key == 'сложение':   
        while True:
            first = random.randint(100, 1000)
            second = random.randint(100, 1000)
            print('{}, {}'.format(first, second))
            t = time.time()
            key = input('Сумма: ')
            t = time.time() - t
            
            if int(key) == first + second:
                print('Правильно. Время: {}.'.format(t))
            else:
                print('Неправильно. Время: {}, ответ: {}'.format(round(t, 2), first + second))
                
            key = input()
            if key == 'всё':
                break
            
    elif key == 'квадрат':
        while True:
            number = random.randint(10,100)
            print('x - {}'.format(number))
            t = time.time()
            key = input('x^2: ')
            t = time.time() - t
            
            if int(key) == number**2:
                print('Правильно. Время: {}.'.format(t))
            else:
                print('Неправильно. Время: {}, ответ: {}'.format(round(t, 2), number**2))
            
            key = input()
            if key == 'всё':
                break
            
    elif key == 'умножение':
        while True:
            first = random.randint(10, 100)
            second = random.randint(10, 100)
            print('{}, {}'.format(first, second))
            t = time.time()
            key = input('Произведение: ')
            t = time.time() - t
            
            if int(key) == first * second:
                print('Правильно. Время: {}.'.format(t))
            else:
                print('Неправильно. Время: {}, ответ: {}'.format(round(t, 2), first * second))
                
            key = input()
            if key == 'всё':
                break
            
    elif key == 'всё':
        break