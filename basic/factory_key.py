#! /usr/bin/env python

from yubihsm import YubiHsm

def main():
    hsm = YubiHsm.connect("http://localhost:12345")
    session = hsm.create_session_derived(auth_key_id=1, password="password")
    factory_key = session.list_objects()[0]
    print(f"The factory settings key is {factory_key.get_info()}.")
    session.close()

if __name__ == "__main__":
    main()
