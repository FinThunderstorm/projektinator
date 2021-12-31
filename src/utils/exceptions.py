class EmptyValueException(Exception):
    """Class for exception raised if given value is empty.
    """

    def __init__(self,
                 source: str,
                 message: str = "Given value can not be empty"):
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

    def __init__(self,
                 source: str,
                 length: int,
                 message: str = "Given value can not be shorter than"):
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

    def __init__(
            self,
            source: str,
            message: str = "Something went wrong while saving into database:"):
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


class NotExistingException(Exception):
    """Class for exception raised if given object is not found
    """

    def __init__(
            self,
            eobject: str = "Object",
            message: str = "not found. Please check your input and try again."):
        """Intializes class with message

        Args:
            eobject (str, optional): option to give custom object name. Defaults to "Object".
            message (str, optional): option to give custom exception message. Defaults to "not found. Please check your input and try again.".
        """
        self.object = eobject
        self.message = message

    def __str__(self) -> str:
        """used to print exception message

        Returns:
            str: formatted exception message
        """
        return f"Error: {self.object} {self.message}"


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


class UnvalidInputException(Exception):
    """Class for execption raised if unvalid input given
    """

    def __init__(self,
                 message: str = "Unvalid input",
                 reason: str = "unexpected value",
                 source: str = "given source"):
        """Initializes class with message, reason and source

        Args:
            message (str, optional): option to give custom exception message. Defaults to "Unvalid input".
            reason (str, optional): option to give custom reason. Defaults to "unexpected value".
            source (str, optional): option to give custon source where exception occured. Defaults to "given source".
        """
        self.message = message
        self.source = source
        self.reason = reason

    def __str__(self) -> str:
        """used to print exception message.

        Returns:
            str: formatted exception message
        """
        return f"Error: {self.message} caused by {self.reason} in {self.source}"
