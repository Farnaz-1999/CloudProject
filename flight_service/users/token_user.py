from rest_framework_simplejwt.models import TokenUser

class CustomizedTokenUser(TokenUser):

    def __init__(self, token_payload):
        super().__init__(token_payload)
