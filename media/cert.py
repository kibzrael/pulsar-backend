import firebase_admin

from pulsar.settings import GS_BUCKET_NAME

firebase_certificate: dict = {
    "type": "service_account",
    "project_id": "pulsar-mvp",
    "private_key_id": "ea9c7f10ee4cd315c1513c8d403b2feb897ca30d",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCGtPCvaifYUQXd\n5Aq6h4vlxw090Fx2nxV58ryPldAzbMxPZUTFkkWPZ7/YBZMGIjJMYt6lcFjM16n3\npJ6Jnmbt04bWPTDQ7rXMx5n/gFSpAKAr2/Scxl4kqPi6wgkgBlVNieXmgW/FYKsq\nX/5n1kFN5a451rllAy+wIYqDgc6vhUfvSL00VGUEYqdnD36KgNE4pbpwcQ/mS4IU\nP4X7sV066sjyDoMLiIWjuWBUDdw/ElNvt3utaKy+npKU+PV8oRPxSFt7VfgFnIfe\nuA9gTlnUAfvYXNjDdTtd9Sf20iduENZDKjPNm2aEAbwqSdlnJukrp89jJI2mJzrH\nQANcewUlAgMBAAECggEAAOQ8LpEHi/s3THlop8TjZGUtnYHeRsu1Pu4gGNwvOVPo\nQ0NCkgMuki0n3CRnTXRW/GHwIsysTcjEn3a3tOX3PO44N31GsC9QRTdx+bqt9MNk\nC/5D73CxqVDz+npzyII6OM3nl1+2b2o9H8XsX2AP5RXW0hutdPFxNJt4OPgYN9mp\nw66oCjhPmd24p+bRCByu0ymQ0qM8DLZSQ7DU5edQYKcNZmQLxGWwur57btMNwWLG\nFIsKkOYEpPDAp5EnvdOc9aKEPJcRUcHLoSmBWJ08BhMj7qo9JHZpG5Z+iTQGzBRE\nScSoT1MfNaPg0/uUPKbvRCEjZ4NIOZbq6mJcI3GuWQKBgQC6fgUOaTUYeKmF1lob\ngisHlQBrbvWiVlas4VbM6B4XlkV7pJrfD7LD3ScCmOgiF+XXKT1fBlnacgU908Ag\nuRdb7hWT1nIKxnu/Cu42B93ogquQnnveidnv2kpzYalDmtx9i8EIf1rTcme7ZNZp\nqlflfumMpNTuOXwmDvFDCKv3jQKBgQC46dweah9B0VMDZHWvNfL3UtpJuLS27SMH\np2rPXYU8g8iJGBIEOFsRWBRA7OE3dYF+mL0JEFv3EE/LfedZRlp7ORGCYUe5aY4J\n7A4DLeWp8S92HLXb27u27pSltgbOOGLnOsNGwrW1lqPoXCedC/ElktSrHrLucJFn\ndxNGazpx+QKBgB+VVg/hu29AiB01dx8vhVAMaPzI1uq+SoGOzB95tBb0iSHud5gN\nVY4cNw4WjUGw4Gj3AADG15LKOp8E7IXeMtmL0bWu3LN8d9qb5EncPTWyY5HjdUD0\nAafARVmTEZJ0eKD+eRuSTfR/bJfs9O8CPU6NlsoN5E3QCHl9kFh08ILFAoGBAJfB\nTaYkX9yrRt6c3rxZoTn65CzmimEqArqwWkcusD72xGhGudp+ybZVO+IAxeC27fyQ\nq2s54s/DskkF3gz1YSKJtmXzImL3Ttuzv9g6Haa3ysS7UUDLd6Xs7U+GMNWjjv/H\nySVUfL43j/MNVnFbsJ+ufhylyCFJfvuTzNzY+ZE5AoGAT0GakgWjDxghNW5Jz5Bh\nJ2pruui34VrlgjPRgpx/yWLXwmUcITZrDgiFgB6KhTP8be3nlGq2Wlrt/9bw177F\npjOIJ3XOu0ZW2cDCGsf5KZgNyWDQ0M9GnkX4o3X4uXToU0yTyp6tZtqVbKpW97l+\nbCI04zqiOuMR3PX27QiwxA8=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ciwpn@pulsar-mvp.iam.gserviceaccount.com",
    "client_id": "114816136358794778494",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ciwpn%40pulsar-mvp.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}


def firebase_initialization():
    cred_object = firebase_admin.credentials.Certificate(firebase_certificate)
    try:
        firebase_admin.initialize_app(cred_object, {"storageBucket": GS_BUCKET_NAME})
    except:
        print("Already initialized")
