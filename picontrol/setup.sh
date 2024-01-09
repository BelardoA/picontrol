#!/bin/bash

# RetroPi Control Install
CURRENT=$(pwd)
PARENT=$(dirname "$CURRENT")
SCRIPTS='/home/pi/scripts'

# Create a function to output the current section
section () {
    echo ""
    echo "**************************************"
    echo "$1"
    echo "**************************************"
    echo ""
}

# Start install
    echo "======================================"
    echo "PiControl Installation Script"
    echo "======================================"

echo "**************************************"
echo "Warning!!! Installing the Pi Control Board on the incorrect pins on the Pi can damage your Pi!"
echo "Please use Pi Control Hardware and Software at your own risk. We do not take responsibility for any damages to your Raspberry Pi that may occur."
echo "By downloading and installing our hardware and software, you are agreeing to these terms."
echo "**************************************"
read -rp "Would you like to continue with the installation? (y/n): " REPLY

if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    section "Updating System"
    apt-get update -y && apt-get upgrade

    section "Installing Pre-Requisites"
    apt-get install -y python3-dev python3-pip git libssl-dev
    python3 -m pip install --upgrade pip setuptools wheel
    
    section "Installing NFC Libraries and Webserver"

    git clone https://github.com/adafruit/Adafruit_Python_PN532.git
    # Make sure the Adafruit_Python_PN532 folder exists
    if [ ! -d "Adafruit_Python_PN532" ]; then
        echo "Adafruit_Python_PN532 folder not found. Please check the installation and try again."
        exit 1
    else
      cd Adafruit_Python_PN532 || exit 1
      python setup.py install
      cd ..
      rm -R Adafruit_Python_PN532
    fi

    section "Determining Raspberry Pi Model"

    # Determine Raspberry Pi Model
    RPI_MODEL=$(cat /proc/device-tree/model)
    echo "$RPI_MODEL"
    MODEL_NUMBER=$(echo $RPI_MODEL | grep -o -E '[0-9]+' | head -n 1)

    case $MODEL_NUMBER in
        3)
            echo "Raspberry Pi Model 3 Detected"
            section "Installing PiControl for Raspberry PI 3"
            ;;
        4)
            echo "Raspberry Pi Model 4 Detected"
            section "Installing PiControl for Raspberry PI 4"
            ;;
        5)
            echo "Raspberry Pi 5 Detected"
            section "Installing PiControl for Raspberry PI 5"
            ;;
        *)
            echo "Raspberry Pi Model Not Detected or not supported. Please use a raspberry pi 3, 4, or 5."
            exit 1
            ;;
    esac
    REQS=pi$MODEL_NUMBER-requirements.txt
    pip install -r "$REQS"

    section "Verifying Dependencies Were Installed"

    # shellcheck disable=SC2013
    for i in $(cat "$REQS"); do
      i=${i%==*}  # Remove version numbers
        if python -c "import $i" &> /dev/null; then
            echo "$i is installed"
        else
            echo "$i is not installed"
            echo "Retrying install for $i..."
            pip install "$i"
        fi
    done

    section "Installing Script Files"
    mkdir -p "$SCRIPTS/picontrol"
    cp -r "$PARENT/picontrol" "$SCRIPTS"
    chmod -R 777 "$SCRIPTS"

    section "Enabling Serial Interface"

    cp /boot/config.txt /boot/old-config.txt
    sed -i '/enable_uart=0/d' /boot/config.txt
    sed -i '/enable_uart=1/d' /boot/config.txt
    echo 'enable_uart=1' >> /boot/config.txt

    # Update startup
    section "Updating RetroPie Startup Commands"

    cp "/opt/retropie/configs/all/autostart.sh" "/opt/retropie/configs/all/old-autostart.sh"
    sed -i '/emulationstation #auto/d' "/opt/retropie/configs/all/autostart.sh"
    sed -i '/emulationstation/d' "/opt/retropie/configs/all/autostart.sh"
    sed -i '/python3 \/home\/pi\/scripts\/picontrol\/picontrol.py&/d' "/opt/retropie/configs/all/autostart.sh"
    echo 'python3 /home/pi/scripts/picontrol/picontrol.py&' >> "/opt/retropie/configs/all/autostart.sh"
    echo 'emulationstation' >> "/opt/retropie/configs/all/autostart.sh"

    if [ -e "/opt/retropie/configs/all/old-runcommand-onstart.sh" ]; then
      cp "/opt/retropie/configs/all/old-runcommand-onstart.sh" "/opt/retropie/configs/all/runcommand-onstart.sh"
    else
      touch "/opt/retropie/configs/all/runcommand-onstart.sh"
    fi

    if [ -e "/opt/retropie/configs/all/old-runcommand-onend.sh" ]; then
      cp "/opt/retropie/configs/all/old-runcommand-onend.sh" "/opt/retropie/configs/all/runcommand-onend.sh"
    else
      touch "/opt/retropie/configs/all/runcommand-onend.sh"
    fi

    mv "/opt/retropie/configs/all/runcommand-onend.sh" "/opt/retropie/configs/all/old-runcommand-onend.sh"
    echo 'python3 /home/pi/scripts/picontrol/picontrol_gameend.py&' > "/opt/retropie/configs/all/runcommand-onend.sh"

    mv "/opt/retropie/configs/all/runcommand-onstart.sh" "/opt/retropie/configs/all/old-runcommand-onstart.sh"
    echo 'python3 /home/pi/scripts/picontrol/picontrol_gamestart.py&' > "/opt/retropie/configs/all/runcommand-onstart.sh"

    echo "======================================"
    echo "Installation Complete!!!"
    echo "======================================"

    read -rp "You must reboot for changes to take effect, reboot now? (y/n): " REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        sudo reboot
    fi
fi

# End
