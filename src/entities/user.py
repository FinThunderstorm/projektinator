from utils.validators import validate_uuid4


class User:
    """Class representating user in the system.

    Attributes:
            user_id (str): unique identification string for user, in uuid4 format.
                                     If not given, generates automatically.
            username (str): represents user's unique username
            user_role (int): user's role code, 1 is base role.
            password_hash (str): user's password as encrypted string
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email address
            profile_image (str, optional): users profile image, placeholder currently - waits
                                           implementation to be specified more exactly.
    """

    def __init__(self, user_id: str, username: str, user_role: int, password_hash: str,
                 firstname: str, lastname: str, email: str,
                 profile_image: str = None):
        """Constructor for User, creates new user.

        Args:
            user_id (str): unique identification string for user, in uuid4 format.
                                     If not given, generates automatically.
            username (str): represents user's unique username
            user_role (int): user's role code, 1 is base role.
            password_hash (str): user's password as encrypted string
            firstname (str): user's firstname
            lastname (str): user's lastname
            email (str): user's email address
            profile_image (str, optional): users profile image, placeholder currently - waits
                                           implementation to be specified more exactly.
        """
        self.user_id = validate_uuid4(user_id)
        self.username = username
        self.user_role = user_role
        self.password_hash = password_hash
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.profile_image = profile_image or "defaultimage"

    # INSERT INTO ja loppuun RETURNING id
    # palauttaa id kentän.
