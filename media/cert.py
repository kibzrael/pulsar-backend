import firebase_admin

from pulsar.settings import GS_BUCKET_NAME

firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsarinc-alpha",
    "private_key_id": "7f26b2026c1daad3fd8ab2f0881a33be2c2929af",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCEKaLxHHz6Rlo2\nuLGq+4lJZIEwcYDG5a/1ZJ7vbTTWKDBEfA9WHF0AsfsWIkmkTDrzMHSnEb9abaur\npjOr4gHJ9ZZhUS0TvCkHLDFHkZUfxez5j9xPdZ+frx1AIkvuYZBUsMEU5EYi9119\nxFw+4LEqAVuOpEqKDvFs2dw4rGnc0AEic5OcgSnFSkqpPs8toyNLjByRFDvmCEWJ\nF/59TuJMkKdkZtiwdwv9HjHJt1u6wnJf70hHapGZE0G7w9upwc8MykEiYPxY/C34\nU34ny9viBRD/az5DsxyKgV7mrzEu59O43Ik3trKvYDCpv2fvOLr1/hx0YMrbEAZD\nhnlr8631AgMBAAECggEAIMeN7zT0Z4PTBM8G3ARyztYDd98zBEH8REY+aF6C9Bn4\nLMhDaoVy6MT8JIeBEePJXD94s2ZiulxIr7RzjO5rqKqFr6H5ZvNsjqeemmRoov6N\nkfFlQH0JSAsgG2PWRuwCZwsG/LZIkgwd719oTL0gm+1FxumHRlpB9ZBMf279+8Lt\nQUO2NGLJmY/S2tqNRaiei20qxcT2SjK284x4mHOx7oembEt+r8OLZe9Ipt7u54y4\nPi4et1cmQmV4N7UTpQ4Z/ELCZYoZ3yBFTFJKWUSzx2qthdWHzec1YjQntUzCVxR9\n65uvqOf8Nja19fkyFhaXpV8N7VNX6EIMahZ46lR5qQKBgQC58Bs3N5j/A1NP8Hnl\npxYDYWd3qihvQrMEplZTUakbEXUFDqxXFwuL/fqgE7Fv7guPv1Z8gbDP10lN1yaD\naEO80p+62I48Q7iwj3oDX9FYrkwOkBtwciSkz/xWzhLQXpGo4HumKxwiu5t57qLw\nLbH+JVVJ5wh6sZ01MEGC4EW2rQKBgQC19kYtzGo8fmLO0WUEW+ZscYMuBhjSUy1b\nt+Rpwtv+LzA8IIlphsTo6htdzJEbyrRUS42YkXnGJHZPhPL3xBnarIZ/ZrgdplDb\ntezIFNqPfA1AzztN3WpdrEAPKAywEQh+++YyMxSwHe4rwbYr7UBTrnwA2FCiuch7\nY63ORB/laQKBgQCviAFZXk48KDqFU+Lvr43zgQe5i1SCvHfd4t3J6GR5XkCXlqOR\nz/qhnRH1/sFahmI5wQr3nUN64qWcK4l7MnoIDtql/HxCXjhDzh8EgndSfbDlapvM\nyqTXRlXU6NQQC8b8o3d3hmkYTP3Y3TTLAohvAXWDv+xcT8K2jKi70ddePQKBgFsn\nj4qb79B0RA11ipR/cVR8HQouVbrvnjZnTg7JZinU++XzKsNplzVTKfh4ZW01w9bC\nrqFypz1iwL4fTRRf8c/BQ/OIws1fpvwaDA9DmyXsMDt6VSwxsnpQsxqkpo6BSe9L\nQ8t8GW4M4GadOSSSSvpg25AUzXhnd46Qpd5B9HSZAoGAGFXYdbsnz2d7hoB3n+X6\nRnJVJF9i4Vf2Y4UMN+9xagUu6cp0wowYuc4e00NGyH6Dkg4zXsRhbd4gcjyCYRYc\n+lQq/yW2coXPjh2F7/PTsZpOvH17Ng+SPkMS9Uti1ihuZbesUgEF1+5ZtZDx4wef\nBO102GrQ5UrsPWSVj+ErpmU=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-uixb7@pulsarinc-alpha.iam.gserviceaccount.com",
    "client_id": "114189912538816830644",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-uixb7%40pulsarinc-alpha.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(firebase_certificate)
    try:
        firebase_admin.initialize_app(cred_object, {"storageBucket": GS_BUCKET_NAME})
    except:
        print("Already initialized")
