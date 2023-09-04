import os


class File:
    """
    Класс для работы с файлами в контексте.

    Args:
        path (str): Путь к файлу.
        mode (str): Режим открытия файла ('r' - чтение, 'w' - запись, 'a' - добавление, 'r+','w+' - чтение и запись).

    Attributes:
        path (str): Путь к файлу.
        method (int): Флаги для открытия файла на основе переданного метода.
        mode (str): Режим открытия файла
        file: Дескриптор файла.

    Raises:
        ValueError: Возникает, если передан недопустимый метод.
        FileExistsError: Возникает, если передан недопустимый путь файлу
    Methods:
        __enter__: Метод для открытия файла в контексте.
        __exit__: Метод для закрытия файла в контексте.
        write(data: str) -> None: Записывает данные в файл.
        read() -> str: Считывает данные из файла.

    Example:
        with File('example.txt', 'w+') as file:
            file.write('Hello, World!\n')
            data = file.read()
            print(data)
    """

    def __init__(self, path: str, mode: str = 'r') -> None:
        """
        Инициализирует объект File.

        Args:
            path (str): Путь к файлу.
            mode (str): Режим открытия файла ('r' - чтение,
                                              'w' - запись,
                                              'a' - добавление,
                                              'r+','w+' - чтение и запись).

        Raises:
            ValueError: Возникает, если передан недопустимый метод.
        """
        self.mode = mode.lower()
        if self.mode == 'r':
            self.method = os.O_RDONLY
        elif self.mode == 'w':
            self.method = os.O_WRONLY
        elif self.mode == 'a':
            self.method = os.O_RDWR
        elif self.mode == "r+" or 'w+':
            self.method = os.O_RDWR
        else:
            raise ValueError("Передан недопустимый метод: {}".format(mode))

        self.path = os.path.join(os.path.abspath(path))
        self.file = None

    def __enter__(self) -> 'File':
        """
        Метод для открытия файла в контексте.

        Returns:
            File: Экземпляр класса File.
        """
        if os.path.exists(self.path):
            self.file = os.open(path=self.path, flags=self.method)
            self.opened_file = os.fdopen(self.file, mode=self.mode, encoding='utf-8')

        elif self.method in (os.O_WRONLY, os.O_APPEND, os.O_RDWR):
            self.file = os.open(self.path, flags=self.method | os.O_CREAT)
            self.opened_file = os.fdopen(self.file, mode=self.mode, encoding='utf-8')

        else:
            raise FileExistsError(f"Файл '{self.path}' не найден.")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Метод для закрытия файла в контексте.
        """
        if not self.opened_file.closed:
            self.opened_file.close()

    def write(self, data: str) -> None:
        """
        Записывает данные в файл.
        Args:
            data (str): Данные для записи.
        """
        self.opened_file.write(data)

    def read(self, n=516) -> str:
        """
        Считывает данные из файла.
        Returns:
            str: Считанные данные в виде строки.

        """
        return self.opened_file.read(n)


def main():
    with File('example.txt', 'w+') as file:
        file.write('Hello, World!\n')
        data = file.read()
        print(data)


if __name__ == '__main__':
    main()
