from Game import Game


def main():
    print("Welcome, to NumberLink Console Game!\nPlease, enter your name\n")

    answer = input()
    name = answer

    print("\nHello, {} \n\nWrite: \n* START to start new game\n"
          "* HELP to see information about the game\n* EXIT to exit the application \n".format(name))

    while answer != "START":
        answer = input()
        if answer == "HELP":
            print("\nNumberLink:\n\nThe player has to pair up all the matching numbers on the grid "
                  "with single continuous lines (or paths). \n"
                  "The lines cannot branch off or cross over each other, "
                  "and the numbers have to fall at the end of each line (i.e., not in the middle).\n"
                  "\nWrite: \n* START to start new game\n"
                  "* HELP to see information about the game\n* EXIT to exit the application \n")

        elif answer == "EXIT":
            print("\nGoodbye, see you again")
            break
        elif answer != "START":
            print("\nIncorrect command, please use the following ones:\n\n Write: \n* START to start new game\n"
                  "* HELP to see information about the game\n* EXIT to exit the application\n\n")

    if answer == "START":
        preparing_for_game(name)


def choose_level():
    print("\nPlease, choose complexity of your game.\n\nPrint: \n* EASY for easy game\n\n"
          "complexity hard will be available later\n")
    while True:
        answer = input()
        if answer == "EASY":
            return answer
            break
        else:
            print(
                "\nIncorrect command. You should choose game complexity.\n"
                "Print: \n* EASY for easy game\n\n"
                "Complexity hard will be available later\n")


def choose_form():
    print("\nNow,please, choose form for your game fild\n\nPrint:\n* SQUARE to choose square field\n"
          "* RECTANGLE to choose rectangle field\n\nField form hexagon will be will available later\n")

    while True:
        answer = input()
        if answer == "SQUARE" or answer == "RECTANGLE":
            return answer
            break
        else:
            print(
                "\nIncorrect command. You should choose field form.\n"
                "Print:\n* SQUARE to choose square field\n"
                "* RECTANGLE to choose rectangle field\n")


def choose_size(form):
    print("Now,please, choose size for your game fild\n\nIf your field form is:\n* SQUARE enter one number\n"
          "* RECTANGLE enter two numbers in one line\n\nNumbers should be integer and more than zero\n")
    size = []
    while True:
        answer = input().strip()
        numbers = answer.split(" ")

        if len(numbers) > 2:
            print("\nYou've entered too much numbres!\nIf your field form is:\n* SQUARE enter one number\n"
                  "* RECTANGLE enter two numbers in one line\n\nNumbers should be integer and more than zero\n")
            continue

        elif len(numbers) == 0:
            print(""
                  "\nYou should choose size for your game field\n\nIf your field form is:\n* SQUARE enter one number\n"
                  "* RECTANGLE enter two numbers in one line\n\nNumbers should be integer and more than zero\n")
            continue

        elif len(numbers) == 1 and form == "RECTANGLE":
            print("\nYou have not entered enough numbers!\nYour field form is {}, please,"
                  "enter two numbers in one line\n\nNumbers should be integer and more than zero\n".format(form))
            continue

        elif len(numbers) > 1 and form == "SQUARE":
            print("\nYou've entered too much numbres!\nYour field form is {}, please,"
                  "enter one number.\n\nNumber should be integer and more than zero\n".format(form))
            continue
        else:
            flag = True
            for num in numbers:
                if not is_digit(num):
                    print(
                        "\nYou've printed not a number or not integer!"
                        "If your field form is:\n* SQUARE enter one number\n"
                        "* RECTANGLE enter two numbers in one line\n\nNumbers should be integer and more than zero\n")
                    flag = False
                    size = []
                    break

                if is_digit(num) and int(num) < 1:
                    print("\nYou've printed numbers, which is less than zero or equals!"
                          "If your field form is:\n* SQUARE enter one number\n"
                          "* RECTANGLE enter two numbers in one line\n\nNumbers should be integer and more than zero\n")
                    flag = False
                    size = []
                    break

                else:
                    size.append(int(num))

        if not flag:
            continue

        return size


def print_change_mess(complexity, form, size):
    print("\nYour game complexity was changed to {}".format(complexity))
    print("Now your game parameters are:\n"
          "Complexity: {}\nForm: {}".format(complexity, form))
    if len(size) == 1:
        print("Size: [{} , {}]".format(size[0], size[0]))
    else:
        print("Size: {} x {}".format(size[0], size[1]))

    print("\nPrint:\n"
          "* OK if everything is ok and you are ready to start\n"
          "* LEVEL to change complexity of your game\n"
          "* FORM to change form of game field\n"
          "* SIZE to change size of your game field\n")


def check_game_parameters(name, complexity, form, size):
    print("\nGood, now you are ready for the game!\n\n"
          "Please check your game parameters.\n"
          "Complexity: {}\nForm: {}".format(complexity, form))

    if len(size) == 1:
        print("Size: {} x {}".format(size[0], size[0]))
    else:
        print("Size: {} x {}".format(size[0], size[1]))

    print("\nPrint:\n"
          "* OK if everything is ok and you are ready to start\n"
          "* LEVEL to change complexity of your game\n"
          "* FORM to change form of game field\n"
          "* SIZE to change size of your game field\n")

    while True:
        answer = input()
        if answer == "OK":
            break
        elif answer == "LEVEL":
            complexity = choose_level()
        elif answer == "FORM":
            f = form
            form = choose_form()

            if f != form:
                print("You've changed your form, but now you have to set new size!")
                size = choose_size(form)

        elif answer == "SIZE":
            size = choose_size()

        else:
            print("\nIncorrect command. "
                  "\nPrint:\n"
                  "* OK if everything is ok and you are ready to start\n"
                  "* LEVEL to change complexity of your game\n"
                  "* FORM to change form of game field\n"
                  "* SIZE to change size of your game field\n")
            continue

        print_change_mess(complexity, form, size)

    print("\n Let's start our game!")
    start_game(name, complexity, form, size)


def preparing_for_game(name):
    print("\nYou start a new game!")

    complexity = choose_level()

    print("\nYour game complexity is {}".format(complexity))

    form = choose_form()

    print("\nYour game form is {}".format(form))

    size = choose_size(form)

    check_game_parameters(name, complexity, form, size)


def is_digit(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def start_game(name, complexity, form, size):
    game = Game(name, complexity, form, size)
    game.start()


if __name__ == "__main__":
    main()
