# Pi Control
-----------------
## Pi Control Install 
(Requires RetroPie, please see instructions to install RetroPie at https://retropie.org.uk)

## Warning!!! Installing the Pi Control Board on the incorrect pins on the Pi can damage your Pi!

1. Configure keyboard or controller if not already done
  * up, down, left, right, start, select, a, and b are enough for now
2. Connect your raspberry pi to the network if using wireless, use RetroPies built in wifi setup tool
3. In RetroPie settings, choose “SHOW IP” and make a note of the IP address given to your Pi.
4. Press F4 on the keyboard to exit to the terminal or connect to your raspberry pi via SSH
```bash
ssh pi@<your raspberry pis IP address>
password: raspberry
```
5. Download and extract Pi Control archive
  ```bash
 sudo apt-get update
 wget https://github.com/BelardoA/picontrol/raw/master/picontrol.tgz
 tar -xzf picontrol.tgz
 ```
5. Run installer

  ```bash
 cd picontrol
 sudo sh ./setup.sh
 ``` 
6. When prompted to reboot type “y” and hit enter.
7. After reboot, you may now access Pi Control web app from any browser connected to same local network by typing in the IP address of the Pi.
  * Example: 192.168.1.25
  * Default Username: picontrol
  * Default Password: password

(The NFC reader has set of switches that must be configured for SPI communication)

## Pi Control Uninstall
1. Connect to your raspberry pi via SSH
```bash
ssh pi@<your raspberry pis IP address>
password: raspberry
```
2. Run uninstaller
```bash
cd picontrol
sudo sh ./uninstall.sh
```
3. Follow the prompts
4. Once the raspberry pi shuts down, you may remove the Pi Control hardware and restore your Pi to its original state