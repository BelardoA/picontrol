#!/bin/bash

# RetroPi Control Install
CURRENT=$(pwd)
PARENT=$(dirname "$CURRENT")
SCRIPTS='/home/pi/scripts'

# Start install
echo "**************************************"
echo "Installing Pi Control"
echo "**************************************"

echo "**************************************"
echo "Warning!!! Installing the Pi Control Board on the incorrect pins on the Pi can damage your Pi!"
echo "Please use Pi Control Hardware and Software at your own risk. We do not take responsibility for any damages to your Raspberry Pi that may occur."
echo "By downloading and installing our hardware and software, you are agreeing to these terms."
echo "**************************************"
read -rp "Would you like to continue with the installation? (y/n): " REPLY

if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    echo "**************************************"
    echo "Installing NFC Libraries and Webserver"
    echo "**************************************"

    apt-get install -y python-dev python-pip git
    git clone https://github.com/adafruit/Adafruit_Python_PN532.git
    cd Adafruit_Python_PN532
    python setup.py install
    cd ..
    rm -R Adafruit_Python_PN532

    echo "**************************************"
    echo "Installing picontrol Requirements"
    echo "**************************************"

    pip install -r requirements.txt

    # Copy files
    echo "**************************************"
    echo "Installing Script Files"
    echo "**************************************"
    mkdir -p "$SCRIPTS/picontrol"
    cp -r "$PARENT/picontrol" "$SCRIPTS"
    chmod -R 777 "$SCRIPTS"

    echo "**************************************"
    echo "Enabling Serial Interface"
    echo "**************************************"

    cp /boot/config.txt /boot/old-config.txt
    sed -i '/enable_uart=0/d' /boot/config.txt
    sed -i '/enable_uart=1/d' /boot/config.txt
    echo 'enable_uart=1' >> /boot/config.txt

    # Update startup
    echo "**************************************"
    echo "Updating RetroPie Startup Commands"
    echo "**************************************"

    cp "/opt/retropie/configs/all/autostart.sh" "/opt/retropie/configs/all/old-autostart.sh"
    sed -i '/emulationstation #auto/d' "/opt/retropie/configs/all/autostart.sh"
    sed -i '/emulationstation/d' "/opt/retropie/configs/all/autostart.sh"
    sed -i '/python \/home\/pi\/scripts\/picontrol\/picontrol.py&/d' "/opt/retropie/configs/all/autostart.sh"
    echo 'python /home/pi/scripts/picontrol/picontrol.py&' >> "/opt/retropie/configs/all/autostart.sh"
    echo 'emulationstation' >> "/opt/retropie/configs/all/autostart.sh"

    mv "/opt/retropie/configs/all/runcommand-onend.sh" "/opt/retropie/configs/all/old-runcommand-onend.sh"
    echo 'python /home/pi/scripts/picontrol/picontrol_gameend.py&' > "/opt/retropie/configs/all/runcommand-onend.sh"

    mv "/opt/retropie/configs/all/runcommand-onstart.sh" "/opt/retropie/configs/all/old-runcommand-onstart.sh"
    echo 'python /home/pi/scripts/picontrol/picontrol_gamestart.py&' > "/opt/retropie/configs/all/runcommand-onstart.sh"

    echo "======================================"
    echo "Installation Complete!!!"
    echo "======================================"

    read -rp "You must reboot for changes to take effect, reboot now? (y/n): " REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        sudo reboot
    fi
fi

# End
