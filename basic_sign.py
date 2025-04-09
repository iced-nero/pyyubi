from yubihsm import YubiHsm
from yubihsm.objects import AsymmetricKey
from yubihsm.defs import ALGORITHM, CAPABILITY

hsm = YubiHsm.connect("http://localhost:12345")
session = hsm.create_session_derived(1, "password")

key = AsymmetricKey.generate(session, 0, "EC Key", 1, CAPABILITY.SIGN_ECDSA, ALGORITHM.EC_P256)

data = b'Hello world!'
print(f">> Data: {data.decode()}")
signature = key.sign_ecdsa(data)
print(f">> Signed the above data with {key}.")
print(f">> Signature begins with {signature.decode('latin-1')[:20]} :: done!")

key.delete()

session.close()
hsm.close()
