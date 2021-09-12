class EmptyValueException(Exception):
    """Class for exception raised if given value is empty.
    """

    def __init__(self, source: str, message: str = "Given value can not be empty"):
        """Initializes class with error source and message

        Args:
            source (str): source where exception is raised, required
            message (str, optional): option to give custom exception message. Defaults to "Given value can not be empty".
        """
        self.source = source
        self.message = message

    def __str__(self) -> str:
        """used to print exception message

        Returns:
            str: formatted exception message
        """
        return f"Error: {self.message} in {self.source}"


class ValueShorterThanException(Exception):
    """Class for exception raised if given value is shorter than asked
    """

    def __init__(self, source: str, length: int, message: str = "Given value can not be shorter than"):
        """Initializes class with error source, asked length and message

        Args:
            source (str): source where exception is raised, required
            length (int): asked length for value, required
            message (str, optional): option to give custom exception message. Defaults to "Given value can not be shorter than".
        """
        self.source = source
        self.length = length
        self.message = message

    def __str__(self) -> str:
        """used to print exception message

        Returns:
            str: formatted exception message
        """
        return f"Error: {self.message} {self.length} in {self.source}"


class DatabaseException(Exception):
    """Class for exception raised if error given while operating with database
    """

    def __init__(self, source: str, message: str = "Something went wrong while saving into database:"):
        """Initializes class with given source and message.

        Args:
            source (str): source where exception is raised
            message (str, optional): option to give custom exception message. Defaults to "Something went wrong while saving into database:".
        """
        self.source = source
        self.message = message

    def __str__(self) -> str:
        """used to print exception message

        Returns:
            str: formatted exception message
        """
        return f"{self.message} {self.source}"


class UserNotExistingException(Exception):
    """Class for exception raised if user is not found
    """

    def __init__(self, message: str = "User not found. Please check your input and try again."):
        """Intializes class with message

        Args:
            message (str, optional): option to give custom exception message. Defaults to "User not found. Please check your input and try again.".
        """
        self.message = message

    def __str__(self) -> str:
        """used to print exception message

        Returns:
            str: formatted exception message
        """
        return f"Error: {self.message}"


class LoginException(Exception):
    """Class for exception raised if username or password is not correct
    """

    def __init__(self, message: str = "Login failed."):
        """Initializes class with message

        Args:
            message (str, optional): option to give custom exception message. Defaults to "Login failed.".
        """
        self.message = message

    def __str__(self) -> str:
        """used to print exception message.

        Returns:
            str: formatted exception message
        """
        return self.message


class UsernameDuplicateException(Exception):
    """Class for exception raised if username is already in use.
    """

    def __init__(self, message: str = "Username is already taken."):
        """Initializes class with message

        Args:
            message (str, optional): option to give custom exception message. Defaults to "Username is already taken.".
        """
        self.message = message

    def __str__(self) -> str:
        """used to print exception message.

        Returns:
            str: formatted exception message
        """
        return self.message
