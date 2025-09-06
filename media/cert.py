import firebase_admin

from pulsar.settings import GS_BUCKET_NAME

firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsar-mvp",
    "private_key_id": "",
    "private_key": "",
    "client_email": "firebase-adminsdk-ciwpn@pulsar-mvp.iam.gserviceaccount.com",
    "client_id": "114816136358794778494",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ciwpn%40pulsar-mvp.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(firebase_certificate)
    try:
        firebase_admin.initialize_app(cred_object, {"storageBucket": GS_BUCKET_NAME})
    except:
        print("Already initialized")
