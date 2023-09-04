import os


class File:
    """
    Класс для работы с файлами в контексте.

    Args:
        path (str): Путь к файлу.
        method (str): Режим открытия файла ('r' - чтение, 'w' - запись, 'a' - добавление, 'rw' - чтение и запись).

    Attributes:
        path (str): Путь к файлу.
        meth_to_open (int): Флаги для открытия файла на основе переданного метода.
        file: Дескриптор файла.

    Raises:
        FileExistsError: Возникает, если передан недопустимый метод.

    Methods:
        __enter__: Метод для открытия файла в контексте.
        __exit__: Метод для закрытия файла в контексте.
        write(data: str) -> None: Записывает данные в файл.
        read() -> str: Считывает данные из файла.

    Example:
        with File('example.txt', 'w') as file:
            file.write('Hello, World!')
            data = file.read()
            print(data)
    """

    def __init__(self, path: str, method: str) -> None:
        """
        Инициализирует объект File.

        Args:
            path (str): Путь к файлу.
            method (str): Режим открытия файла ('r' - чтение, 'w' - запись, 'a' - добавление, 'rw' - чтение и запись).

        Raises:
            FileExistsError: Возникает, если передан недопустимый метод.
        """
        self.meth_to_open = None
        if method.lower() == 'r':
            self.meth_to_open = os.O_RDONLY
        elif method.lower() == 'w':
            self.meth_to_open = os.O_WRONLY
        elif method.lower() == 'a':
            self.meth_to_open = os.O_APPEND
        elif method.lower() == "rw":
            self.meth_to_open = os.O_RDWR
        else:
            raise FileExistsError

        self.path = path
        self.file = None

    def __enter__(self):
        """
        Метод для открытия файла в контексте.

        Returns:
            File: Экземпляр класса File.
        """
        if os.path.exists(self.path):
            self.file = os.open(path=self.path, flags=self.meth_to_open)
        elif self.meth_to_open in (os.O_WRONLY, os.O_APPEND, os.O_RDWR):
            self.file = os.open(path=self.path, flags=os.O_CREAT)
        else:
            raise FileExistsError

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Метод для закрытия файла в контексте.
        """
        os.close(self.file)

    def write(self, data: str) -> None:
        """
        Записывает данные в файл.

        Args:
            data (str): Данные для записи.
        """
        data = bytes(data, encoding='utf-8')
        os.write(self.file, data)

    def read(self) -> str:
        """
        Считывает данные из файла.

        Returns:
            str: Считанные данные в виде строки.
        """
        return os.read(self.file, 1024, ).decode('utf-8')
