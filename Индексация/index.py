class index:
    def __init__(self):
        self.index = {}

    def add(self, key, value):
        path = self.index
        for char in key:
            if char not in path:
                path[char] = {}
            path = path[char]
        path['values'] = []
        path['values'].append(value)

    def search(self, key):
        path = self.index
        for char in key:
            if char in path:
                path = path[char]
            else:
                path = 'Nothing found.'
                break
        return path['values']

a = index()
a.add('qwerty', 'ytrewq')
print(a.search('qwerty'))
