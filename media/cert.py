import firebase_admin
from pulsar.settings import GS_BUCKET_NAME

firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsarinc-dev",
    "private_key_id": "4216e6e074fec25eaec187e9f5a539e81c41c446",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDO190qNiWPMZ7N\nFl2TUkHsQZlyfk5pSVOrVQGtZS3KmWOtgfYw/zZEdiswDQSOcH9lsMDo3lkNgqCP\nVKUlPjNI7JdfBOGyTWxxW6ewGVsVkgnj9FJXgfw3plQy+jtVG2MVKEj7dKbhk08x\nQydNtHJiupY+pHlVnTge493AGWey451Pxr42C/K/HTBrXCzlWZCkBROQeBGYMpQe\nzwvtYBjVCvGDIdgFKhPF3Gl1AgQ3SIkbcgYlZGmT15mPbltmBx6URebq90IDkMHI\n6BCsshMlVhsbwyBGO315DMnr5CjaaN9Dlglv+DFbRkrVIG2NSc21a/QAM0xq596s\nX3noBXkFAgMBAAECggEALefotOKZiWM43El3cSfTa6zPcoKnwmQ8xoyyN5p6BDnw\nzmRGkG9DywPy59IrzbUYASiuV8BpQT9ZhRYDJPXeCfRAUB1UPe9C/xGZcNLfzTTB\nLy9dSwCVSoCGtV2l52iRn/N15yDnnK7F56gAxBUlQdYpXDPCngarmud1opnA0wmd\nC2DQNw7mTqN1QR78Ooy+PHitDY4g2xU9RueAQSYgiMXVYhUH+quEnd6uXzQCn0/H\nythdUHKie2pQxCE13+eZlGCBpLzfkrVPNKtjxV5xgmBT2/Q/snIpJPy5wLX6y3Vw\nDevmprurhDkbE5Stt3kQEuxO7C4JQpZai8uf1hsx4QKBgQDp7WAvaDt3qP+sv1Om\nxWYlbHe1oh6tGf/A/Iz+OzYw4hJaSkX6TtEsQlvHYwRrcbLIl+JpIEkYxFK+5M2g\nRPM4Z0fHBD5s+RJwEhNLZF7Kvqd3OnlBjeMzeco6dAINW2UC+R+V8PantTqFAreR\nU/xsEICiQXBZWWo3RA1xfVQFyQKBgQDiXEKx79oREZ0aRQxazOl17pT2DGzjAILm\nofi1jv23dhs1T818Pua0+cXekL44YrKve7DXI+iXlOCjSY+tC/dgsY76DkdopYVp\n6lHim/oaXHoLql941fyY7tdKJk80TiJe7vVOS4TMVseePmkwfhtQ2oGT8yi5yQA/\nZznotI/nXQKBgG7+ar0Tv+OvFGFrBs4Cq8zmAob0PYn05B01t9CJV9Up73tX8owq\nCaXudo3MtbQlZqc3Kf6niwdtX7Wj6s046g7BMpWDtfsO02jJqs4C+ddJTzyLSi2I\nnV03VHUXxkGANBWNDyeeBerdWr7x4xfZudOsoNxcIGrEulkuuRI4XT3BAoGAae+B\nqyK0LI7Qtm2gJZKGpBGfFzOjde1UVblx2w5rgQO+IgoSAdayQ/os90dILr1KIMRD\nc7wza1VaeDDCE9toz5Dpd+9czgXA1Vu7LNGQj+u9ll4KxlNnHu+QQ/x/ztvOTB2L\nIjRHlxX53/4XXoF2KTXJtML0yVXfTszxlg2C12UCgYBQdbWvUpTr1K4VY0Tc+VuR\njJhvqBOEnTKo6/4HCHIc4IkL2XqA7788H2277uVdIU4RqdbOS0un8lt38Xxt0rJC\nXP2cpqicynw3SxuIVXKkxdDIFF9wclb5Z/gJsBNthMaTHAKAtjEpLJbFowNVgTeK\nHV1p3zDez3gZyiGMoFoVrw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-tfdhy@pulsarinc-dev.iam.gserviceaccount.com",
    "client_id": "111690714956048151828",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-tfdhy%40pulsarinc-dev.iam.gserviceaccount.com",
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(firebase_certificate)
    try:
        firebase_admin.initialize_app(cred_object, {"storageBucket": GS_BUCKET_NAME})
    except:
        print("Already initialized")
