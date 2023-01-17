import firebase_admin


firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsar-inc-1",
    "private_key_id": "63e2e59e3be08fb5db9d2d70d2a6519c0f89556e",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDCArnziQ4kgq7r\npzx6CeuwJp1IbK4S5+DjpP9SHyS9vJaE87MdZvOcb4d+ZtACXPeJGyzC4yCXPAkd\nOHvN/ssYipdZwEVPDkorKoz9SKa3Q8/AnVnTc5qpVSgoutTlI6yiPcNF12+xxQKh\n0k3jOtzg0LDvc21OBz+uUyNgSO98gxQSYpURd+mi1NztqnszhKDCczrEdtVALXWQ\n2De6Up/XmJoXGZYQML0FEzOp8qP1TMhIJAKN1GyQUV8mqD5yqknaLvdAO1hewfPe\nnoOjKL9qJAg+AKKvJESDRh+vWxbmx9OTfUimJGixpzQx8Hr26SYcdObHprYX5ErC\nbpQJDLCNAgMBAAECggEAKo38iZ2LW5jKk2foTQB2EPo3T5Z/DCiOXIBpfHLWVUPT\nZDAsHovhbXPNLX2RrKMFrK4oQEsfb+y8NwuXpFR56dUkY4xX54JD5Hn92OShpNsb\n66zX8hiOWQwTtfNdFTGhASk49s3Ncxm6fRIrAWd84VcFKFCSLiZK4orb3JfC5/Va\niwpdHvh40eZB4IhjxKWyn8wuUz4SamoNKekfxaclYiwM78mGNKxNx27uDMzzELd2\n7j/tce0lgPT63psFkcimS441eXBAnhT4hu4sGVdr6YKHQCuv1lByRrY803iwLhBq\nlj5TU2pxuroxf6+7eVpntIR0zvBLY27eiSOiS2zDJQKBgQDotqRCIbBWeTULptWw\n5IaIfYu0ENJqDw3zrtI9cDDLxYz15li+R9cSkCCNvLlubwbDkH+3ujjGCQ8njtmt\nuHTwUJF9NxjD5Rmx8zUGTV6zkUFdl1kZ6pKM+Z6rsSvhrd1h6n6+lec4AO/R5sOF\nE/KpTGJQ97j9CE/oZ+59hdpdJwKBgQDVbKVDppxkerlFJM/VhwKqs4SGhB8gcKyK\nvAhDSpi8hZAQnNgHqqwBVRNRiTpHrXF1yjNxq4KWBJHg6FuJLhFf8e30I2zytn/E\nehU3483n/+Ds9UfrUjbq7kgqwDySFM6UYBZJNXILN75FmyHvHiSuqSPRdt2QiHpv\n/qz51uV9KwKBgAbeDO7eq6OBpC0Z2UiFFetFOTAxJuR2WUUNraqeevIofEZta8UB\nvbkQg8VrAlXd9OckhoBXgIFnlwjl0EquHNVSq1h0nch6JE36DWCIO/k0mic25iw7\nneOHIkWSzua0CMpw7xiUt+QRMwKQushclFamqGgXR2BANIt5NbKClrUVAoGAS5F1\njteehoFhulbHdD6ithhsM0jy0IS0w0bC0jjGjfHoyckPQN+wmaQq+/LP/PMvulpH\nDteAnGev02fSiWcTZdp+u7QTbnkqEkJ74tc5YA0c8ioDNhJdOZ/3U5PPnpXZc3X2\nTiOrZsdtCq5cPJN6v5FKCm/BEd0RJTiSvL/XcBMCgYAH0BK644xSF7UgzHy4/4ob\nKNFxncR+paxLP55Zfvd7LYMf5Ygal/kufcP5vAuys1f8QT1uVfflMknK54Fdbwkn\n2/Y9ELJISSDWyFoaYsqxEWTU22wRsbJeNU4JriXI5GY5Ia/Do94TwIDiiOKp72BV\nez9Y34HKH8bA7a87nS2FVw==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-i6jpf@pulsar-inc-1.iam.gserviceaccount.com",
    "client_id": "110984677114082682729",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-i6jpf%40pulsar-inc-1.iam.gserviceaccount.com",
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(firebase_certificate)
    try:
        firebase_admin.initialize_app(
            cred_object, {"storageBucket": "pulsar-inc-1.appspot.com"}
        )
    except:
        print("Already initialized")
