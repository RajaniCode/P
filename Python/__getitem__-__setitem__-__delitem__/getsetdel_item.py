class Colors(object):
    def __init__(self):
        self.data = {"Red": 1, "Green": 2, "Blue": 3}
    def __getitem__(self, item):
        print("getitem")
        return self.data[item]
    def __setitem__(self, item, value):
        print("setitem")
        self.data[item] = value
    def __delitem__(self, item):
        print("delitem")
        del self.data[item]

rgb = Colors()
print(rgb["Red"])
rgb["Blue"] = 300
print(rgb["Blue"])
print(rgb["Green"])
del rgb["Green"]

