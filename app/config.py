class Config:
    """ Email regex pattern, maximum email length, and password character requirements. """
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    EMAIL_LENGTH = 50
    PASSWORD_CHAR = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    UPLOAD_FOLDER_PROFILE = 'uploads/profile'
    UPLOAD_FOLDER_EQUIPMENT = 'uploads/equipment'
    UPLOAD_FOLDER_LAND = 'uploads/land'
    