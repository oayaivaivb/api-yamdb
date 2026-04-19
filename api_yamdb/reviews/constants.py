USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (USER, 'Аутентифицированный пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]

MAX_ROLE_LEN = max(len(role) for role, _ in ROLE_CHOICES)

MAX_USERNAME_LEN = 150
MAX_EMAIL_LEN = 254
MAX_BIO_LEN = 500
MAX_CONFIRMATION_CODE_LEN = 6
MAX_NAME_LEN = 256
MAX_SLUG_LEN = 50
