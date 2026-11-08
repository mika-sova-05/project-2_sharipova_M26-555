
import prompt


def welcome() -> None:
    print("***")

    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")

        command = prompt.string("Введите команду: ")

        if command == "exit":
            print("До свидания!")
            break
        elif command == "help":
            continue
        else:
            print("Неизвестная команда.")