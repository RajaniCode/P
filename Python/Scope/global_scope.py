def func():
    global num
    num = num + 1

def main():
    global num
    num = 1
    func()
    print(num)

num = 0
main()


'''
2
'''
