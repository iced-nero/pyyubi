# Basic tests with the YubiHSM on amd64

Currently no other architectures are supported.
There is a darwin-universal package for Mac, but exploration is needed.

## Prerequisites

- a non-ARM PC
- Ubuntu 22.04
- a physical YubiHSM2 device
- YubiHSM2 SDK ([install it first][getsdk])
- Python 3.8 or higher (for the [Python wrappers][pyhsm2])

## Procedure

These steps are adapted from the [quickstart guide][getsdk]. Run them on the machine to which the
YubiHSM2 will be connected.

1. [Download][sdkrel] an appropriate version of the SDK. For this case we will be using
   the latest available version at time of writing, [2024.09][202409].

        ```bash
        wget https://developers.yubico.com/YubiHSM2/Releases/yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        ```

2. [Check][signed] that the package is signed by an official developer. If we run `gpg --verify`
   we will see the ID of the key that was used to sign the package. Download that key using `gpg
    --recv-keys`, then re-run the verify step to get the fingerprint of the key. Confirm that it
   is in the list of [developer keys][devkey].

        ```bash
        gpg --verify yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz.sig
        gpg --recv-keys <KEY_ID>
        gpg --verify yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz.sig
        ```

3. Untar the package and install all the libraries. Since we are installing them manually, check
   that they do not clash. Currently, both `libyubihsm-dev` and `libykhsmauth-dev` try to put in
   `ykhsmauth.h` into the same place, which will cause `dpkg` to complain. One workaround for us
   is to [`dpkg-divert`][divert] it first:

        ```bash
        tar xf yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
        cd yubihsm2
	sudo dpkg-divert --package libyubihsm-dev --divert /usr/include/ykhsmauth.h1 --rename /usr/include/ykhsmauth.h
        sudo dpkg -i *.deb
        ```

4. Reset the YubiHSM to factory settings by pressing down on its metal rim for 10 seconds while
   inserting it into a USB port. If correctly inserted, the LED should start blinking.

5. Start the connector daemon in debug mode on the one terminal window.

        ```bash
        yubihsm-connector -d
        ```

6. In another window, try to connect to the YubiHSM. In the second line, the `yubihsm>` is part
   of the shell prompt and doesn't need to be typed in. If no URL is specified, the system will
   try to reach `http://localhost:12345` by default, the locally-connected HSM2 module.

   The `open` line will only work if the HSM2 was reset to factory mode, since it creates a new
   session using the default password `password`. If this works, congratulations! We've reached
   the HSM2 module that is plugged into the PC.

        ```bash
        yubihsm-shell
        yubihsm> connect
        yubihsm> session open 1 password
        ```

7. Create and activate the virtual environment for the Python wrapper.

        ```bash
        python -m venv yubi
        source yubi/bin/activate
        ```

8. Install the `yubihsm` library using Pip.

        ```bash
        pip install -U pip		# just upgrade pip to be safe
        pip install yubihsm[http,usb]	# remove http or usb if it is not needed
        ```

8. Run `basic_test.py` to do some simple tests on the device.

## Troubleshooting

1. `gpg` command not found

   If this message appears, install the `gpg` package on the Ubuntu machine:

   ```bash
   sudo apt-get install gpg
   ```

2. USB access fails when running `yubihsm-connector -d`

   If a message like `libusb: bad access [code -3]` appears when running `yubihsm-connector`, it
   is probably a udev permission issue preventing the use of the USB drive on the machine. Check
   that a rule exists for everyone to use the USB system:

   ```bash
   grep -Rw '^SUBSYSTEM=="usb"' /etc/udev/rules.d/
   ```

   If nothing appears, the rule hasn't been created. The following commands will allow all users
   to read and write the USB drive.

   ```bash
   echo 'SUBSYSTEM=="usb", GROUP="users", MODE="0666"' > 10-usbpermission.rules
   sudo mv 10-usbpermission.rules /etc/udev/rules.d/
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

3. This error may also show up as a failure to connect to..

4. Virtual environment creation fails

   If the system cannot create a virtual environment, a lengthy error message will pop up about
   how some dependencies are missing, as well as the command to fix it. It should probably be:

   ```bash
   sudo apt-get install python3.10-venv
   ```
   This will set up the necessary tools to build virtual environments.

[pyhsm2]:	https://github.com/Yubico/python-yubihsm
[sdkrel]:	https://developers.yubico.com/YubiHSM2/Releases/
[getsdk]:	https://docs.yubico.com/hardware/yubihsm-2/hsm-2-user-guide/hsm2-quick-start.html
[202409]:	https://developers.yubico.com/YubiHSM2/Releases/yubihsm2-sdk-2024-09-ubuntu2204-amd64.tar.gz
[devkey]:	https://developers.yubico.com/Software_Projects/Software_Signing.html
[divert]:	https://linux.die.net/man/8/dpkg-divert
