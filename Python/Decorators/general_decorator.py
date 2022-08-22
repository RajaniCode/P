def all_weather(func):
    def inner(*args, **kwargs):
        print("Can decorate any function")
        return func(*args, **kwargs) #Note return function call with parameters
    return inner

@all_weather
def rain(x):
    print(" = ".join(["Rain in centimeters", str(x)]))

@all_weather
def shine(x, y):
    print(" = ".join(["Temperature in celsius", str(x)]))
    print(" = ".join(["Humidity in percentage", str(y)]))
    
rain(5)

shine(30, 60)
