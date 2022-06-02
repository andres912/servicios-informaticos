from project.models.enableable_object import EnableableObject
from project import db, bcrypt
from datetime import datetime

from project.models.role import Role


class User(EnableableObject):
    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using Flask-Bcrypt)
        * registered_on - date & time that the user registered

    REMEMBER: Never store the plaintext password in a database!
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    role = db.relationship("Role", backref=db.backref("user", lazy="dynamic"))
    is_visible = db.Column(db.Boolean, nullable=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(60), nullable=True)
    lastname = db.Column(db.String(60), nullable=True)

    @property
    def permissions(self):
        return self.role.permissions

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        role: Role,
        is_visible: bool = True,
        name: str = None,
        lastname: str = None,
    ):
        """
        Create a new User object using the email address and hashing the
        plaintext password using Bcrypt.
        """
        self.username = username
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        self.registered_on = datetime.now()
        self.role = role
        self.is_visible = is_visible
        self.name = name
        self.lastname = lastname
        self.last_activity_at = datetime.now()

    def _update(
        self,
        username: str = None,
        email: str = None,
        password: str = None,
        role: int = None,
        is_visible: bool = None,
        name: str = None,
        lastname: str = None,
        is_deleted: bool = None,
        last_activity_at: "datetime" = None,
        **kwargs,
    ) -> None:
        self.username = username if username else self.username
        self.email = email if email else self.email
        if password:
            self.hashed_password = bcrypt.generate_password_hash(password).decode(
                "utf-8"
            )
        self.role = role if role else self.role
        self.is_visible = is_visible if is_visible is not None else self.is_visible
        self.name = name if name else self.name
        self.lastname = lastname if lastname else self.lastname
        self.last_activity_at = (
            last_activity_at if last_activity_at is not None else self.last_activity_at
        )
        super()._update(**kwargs)

    def is_correct_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.hashed_password, password)

    def set_password(self, password: str):
        self.hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    def __repr__(self):
        return f"<User: {self.email}, {self.username}, {self.role}>"

    def get_id(self) -> str:
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

    def touch(self) -> None:
        self.update(last_activity_at=datetime.now())
