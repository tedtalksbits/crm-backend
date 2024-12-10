from rest_framework.authentication import TokenAuthentication

class BearerTokenAuthentication(TokenAuthentication):
    """
    Custom authentication class to support 'Bearer' and 'Token' prefixes.
    """
    keyword = 'Bearer'