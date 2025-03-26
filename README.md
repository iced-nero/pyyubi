# Basic tests with the YubiHSM on amd64

Currently no other architectures are supported.
There is a darwin-universal package for Mac, but exploration is needed.

## Prerequisites

- a non-ARM PC (the one we have runs Ubuntu 22.04)
- a physical YubiHSM2 device
- YubiHSM2 SDK ([install it first][getsdk])
- Python 3.8 or higher (for the [Python wrappers][pyhsm2])

## Procedure

This is adapted from the [quickstart guide][getsdk].

1. [Download][sdkrel] an appropriate version of the SDK. For this case we will be using
   the latest available version at time of writing, [2024.09][202409].

        ```bash
        wget https://developers.yubico.com/YubiHSM2/Releases/yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        ```

2. [Check][signed] that the package is signed by an official developer. When we run `gpg --verify`
   we will see the key used to make the signature. Download that key using `gpg --recv-keys`, then
   re-run the verify step to confirm the fingerprint is in the list of [developer keys][devkey].

        ```bash
        gpg --verify yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        gpg --recv-keys <KEY_ID>
        gpg --verify yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        ```

3. Untar the package and install all the libraries. Since we are installing them manually, check
   that they do not clash. Currently, both `libyubihsm-dev` and `libykhsmauth-dev` try to put in
   `ykhsmauth.h` into the same place, which will cause `dpkg` to complain. One workaround for us
   is to `dpkg-divert` it first:

        ```bash
        tar xf yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        cd yubihsm2
	sudo dpkg-divert --package libyubihsm-dev --divert /usr/include/ykhsmauth.h1 --rename /usr/include/ykhsmauth.h
        sudo dpkg -i *.deb
        ```


Reset the YubiHSM by holding down the touch sensor for 10 seconds while inserting it.
3. Start the connector daemon.

        ```bash
        $ yubihsm-connector -d
        ```
[pyhsm2]:	https://github.com/Yubico/python-yubihsm
[sdkrel]:	https://developers.yubico.com/YubiHSM2/Releases/
[getsdk]:	https://docs.yubico.com/hardware/yubihsm-2/hsm-2-user-guide/hsm2-quick-start.html
[202409]:	https://developers.yubico.com/YubiHSM2/Releases/yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
[devkey]:	https://developers.yubico.com/Software_Projects/Software_Signing.html
