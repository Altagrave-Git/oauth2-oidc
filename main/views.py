from django.shortcuts import render
from users.models import User
import requests
import random
import string
import base64
import hashlib
from django.contrib.auth import login
from . import settings as config

CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET

CODE_VERIFIER = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
CODE_VERIFIER = base64.urlsafe_b64encode(CODE_VERIFIER.encode('utf-8'))

CODE_CHALLENGE = hashlib.sha256(CODE_VERIFIER).digest()
CODE_CHALLENGE = base64.urlsafe_b64encode(CODE_CHALLENGE).decode('utf-8').replace('=', '')

auth_url = "https://echonetwork.app/o/authorize/?response_type=code&code_challenge={}&code_challenge_method=S256&client_id={}&redirect_uri=http://127.0.0.1:8000".format(CODE_CHALLENGE, CLIENT_ID)

def index(request):
    authorization_code = request.GET.get("code")

    oauth = {}
    userdata = {}
    context = {
        "auth_url": auth_url,
        "oauth": oauth,
        "user": userdata
    }

    if authorization_code:
        token_url = "https://echonetwork.app/o/token/"
        token_data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "client_id": CLIENT_ID,
            "redirect_uri": "http://127.0.0.1:8000",
            "code_verifier": CODE_VERIFIER,
            "response_type": "token",
            "algorithm": "RS256",
            "scope": "openid read write",
        }
        token_response = requests.post(token_url, data=token_data)
        print(token_response.json())

        for key, item in token_response.json().items():
            oauth[key] = item

        if token_response.json().get('access_token'):
            endpoint = 'https://www.echonetwork.app/o/userinfo/'
            data = {
                "access_token": token_response.json().get('access_token'),
            }
            response = requests.post(endpoint, data=data)
            print(response.json())

            for key, item in response.json().items():
                userdata[key] = item

        return render(request, "main/index.html", context=context)
        
    return render(request, "main/index.html", context=context)