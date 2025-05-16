class AuthenticationError(Exception):
    """Custom error class for authentication errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 401, 
        error_code: str = "AUTHENTICATION_ERROR"
    ):
        """
        Initialize an authentication error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Error code from API
        """
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.name = "AuthenticationError"


class CreditError(Exception):
    """Custom error class for credit-related errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 402,
        error_code: str = "CREDIT_ERROR",
        credits_remaining: int = 0
    ):
        """
        Initialize a credit error.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Error code from API
            credits_remaining: Number of credits remaining
        """
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.credits_remaining = credits_remaining
        self.name = "CreditError"
