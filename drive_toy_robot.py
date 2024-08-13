from toy_robot import MarsRover

if __name__ == '__main__':
    rover = MarsRover()

    userInput = input('Type a command or "END" to exit: ')

    while userInput.upper() != "END":
        output = rover.recieve_command(userInput)
        if output is not None:
            print(output)
        userInput = input('Type a command or "END" to exit: ')
