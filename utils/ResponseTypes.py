from enum import Enum

# Enum para os tipos de resposta do servidor
class ResponseTypes(Enum):
    NO_HAVE_MESSAGES: int = 443344,
    HAVE_NEW_MESSAGES: int = 442233