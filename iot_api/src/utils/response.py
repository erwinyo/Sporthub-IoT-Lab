from enum import Enum

class Response(Enum):
    NOT_FOUND = "Resource not found"
    UNAUTHORIZED = "Unauthorized access"
    BAD_REQUEST = "Bad request"
    INVALID_INPUT = "Invalid input"
    SERVER_ERROR = "Internal server error"
    FORBIDDEN = "Forbidden"
    SUCCESS = "Operation completed successfully"