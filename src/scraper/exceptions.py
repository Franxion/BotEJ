class EasyJetAPIError(Exception):
    """Base exception for all API-related errors."""
    pass

class RateLimitError(EasyJetAPIError):
    """Raised when we hit API rate limits."""
    pass

class APIResponseError(EasyJetAPIError):
    """Raised when we get an unexpected response from the API."""
    pass