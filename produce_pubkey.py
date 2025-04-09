from yubihsm import YubiHsm
from yubihsm.defs import CAPABILITY, ALGORITHM
from yubihsm.objects import AsymmetricKey
from yubihsm.core import serialization as serial

hsm = YubiHsm.connect("http://localhost:12345")
session = hsm.create_session_derived(1, "password")

key = AsymmetricKey.generate(
        session,
        0,
        "New Asymmetric Key",
        1,
        CAPABILITY.SIGN_ECDSA,
        ALGORITHM.EC_P256
)

pub_key = key.get_public_key()


with open("public_key.pem", 'w') as f:
    f.write(pub_key.public_bytes(
        encoding=serial.Encoding.PEM,
        format=serial.PublicFormat.SubjectPublicKeyInfo
    ).decode())

signature = key.sign_ecdsa(b"Hello world!")
print(f">> Signature starts with: {signature.decode('latin-1')[:20]}.")

session.close()
hsm.close()
