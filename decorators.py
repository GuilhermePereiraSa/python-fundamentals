
def log(func):
    def wrapper():
        print("Executando... ")

        func()

        print("Finalizado")
    return wrapper()


@log
def hello() -> None:
    print("hello!")


def main():
    hello()


if __name__ == "__main__":
    hello()
