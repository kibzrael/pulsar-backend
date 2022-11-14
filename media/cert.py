import firebase_admin


firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsar-2217f",
    "private_key_id": "60076137269dbc10a6a214da07bd37479e6277ff",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC37iiRYSWjUePn\nCfZiX3O4c4i4viOhEvkXFhHwWJdxtQh6SQrgMZxDJQU46Yix6yBCrmREfNdZQZjo\nflcoe/qAXl7JQUMHGnSPhLf/7nZEr8+EHQh0R86JLMswivA6NJI0RjmQKFVWgF8A\n2ersN3BnQHL3w5DFqzsKeB0BXI9yJFRcki380G8C9ATFsDA6+jPJ+OsS9/BlzuUY\nTmlPN9Ip+ccjKwoPJcYRGePMauTQCDJ4N/43g37HwujzlUz3jloQdT5xQkQ4tieB\nRfsNfREIxNYJEjrlCpT75VgOdLx2xSXHJxV1PdMIEo2RlrkVAsIjvZje0oO3WnAJ\nddbcR/+zAgMBAAECggEAHahl2zdOcdzJAl6dX3RjvPjIMX3bUeQ0zQ+uedJXLSsT\nQGCZw9fMChmkk244r/OpYocrPM3ijY5hwQ9qL2l6VYuh/hKrY7BU3jV40+hYIrA0\npmlmDRXtDDpwUxX8MW57qrkuG/wc8pNFfmYlFszDr6p5P1FF/VGkdgYzKx6JNM63\n1SInvSkZ9kICfzYV4MXHRBI1CXjX8nkrAb87xFmNtZL6vaADGUxyBHc04wmMqfWF\nO2rgxmtGOSbqqvnpvpA19yTwNh/CDIq9eORaMGyIXUUj03oKVI0QtM22cCkPYSGq\njmEmjrJh1LRkRePsjSdW0a10yLTrHKR6QBOXdmkcEQKBgQDgUGIQDkdjgfgPEavt\nBhl7M2/r2PTkPD4H4LK/fSLAkdlJhbgU7RGCuLY2V/IXRSBABU5tJx5tteRLciC7\nfOLi0k0jNatvy9EK0BKDYVccrS8qZt0YAJhYTvi0LY+Fz2c+dXfqufguIoxhmyuX\nL/wAu8MCmJW2KrxKSRloOxGf4wKBgQDR6WzQ+QRAXd7Vu4+RRphDMj5O2b5oRWXa\nTNXst3BcKyIR3u+REDZEgp7gHbkRScjAoZd5jvI2Itw1jtBHlKoe32oG1WhvLlBx\nCoxDVtumF0HfglSV1ry/X6wP3ZB/Nz1BbHXQs8OBbcLnpxmwSeDtsICjYFK7LEi1\nLO4iP2CJ8QKBgG1CeiF78wXjHqKoZufy2qKJ8XAdo1swhL5tkmN3XmASKpaHTZzT\nxH253vcla0QuZYEJlKPSNB4YRPUCyDLKp/D3op8N201/J3lu1DWuSjIroRe0Nukk\nERCilr2cm5X/6jggG6L3po1CQsKgRGFF/CeXTWuMSxAKTOCaLof4jaMlAoGBALcr\nnczsvwz73MtdE/aNR6i7WyurTj/m7u4DRll96QpEiUJW624GW5SE9uZSiX/QhuGx\nIGDun+UlnksOCCmuTJUMF5VG/A6ot4Es1yCb1qeke9LyA6WM8L9+WMKvcLvSFB3W\n6yfm9Z8njIBgjEYM8b332wi1sPurtPaD8njoHPHBAoGANeNNFP0OTIG1NG2lIdYk\nSk3KS8bykTExvSaVHQyv309L6eF27bT+jRFedW/iJMBGAx9/B5OB/Oorsqeu3JAP\n22egQFm+/2FVb2RU2NRJZwDXOoDg4mRKzWssb1yKR30DjfJpnPXSkeSZ+Owr2QpU\nc/ZBuvEQlnS7QUEkLVWbEGk=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-rddlj@pulsar-2217f.iam.gserviceaccount.com",
    "client_id": "101307726227485938631",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-rddlj%40pulsar-2217f.iam.gserviceaccount.com"
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(
        firebase_certificate)
    try:
        firebase_admin.initialize_app(cred_object, {
            'storageBucket': 'pulsar-2217f.appspot.com'
        })
    except:
        print('Already initialized')
