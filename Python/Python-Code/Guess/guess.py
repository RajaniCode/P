import random

# use six because input behaves differently in Python 3 and 2
import six

def main():
    secret = random.randint(1, 101)
    print("Guess secret number")
    print("Hint secret number is {}".format(secret))
    guess = six.moves.input("please input your number")
    print("Your guess is {}".format(guess))

    def compare(guess, secret):
        if guess == str(secret):
            print("you win")
        elif guess > secret:
            print("too big")
        elif guess < secret:
            print("too small")

    compare(guess, secret)

if __name__ == "__main__":
    main()
