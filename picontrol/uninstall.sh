#!/bin/bash

# RetroPi Control Uninstall
SCRIPTS='/home/pi/scripts'

# Start uninstall
echo "**************************************"
echo "Uninstalling Pi Control"
echo "**************************************"

read -rp "Warning: This will uninstall Pi Control. Do you want to proceed? (y/n): " REPLY

if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    echo "**************************************"
    echo "Removing NFC Libraries"
    echo "**************************************"

    pip uninstall Adafruit_Python_PN532 -y

    echo "**************************************"
    echo "Uninstalling picontrol Requirements"
    echo "**************************************"

    pip uninstall -r requirements.txt -y

    # Remove files
    echo "**************************************"
    echo "Removing PiControl Script Files"
    echo "**************************************"
    rm -rf "$SCRIPTS/picontrol"

    echo "**************************************"
    echo "Reverting Serial Interface Settings"
    echo "**************************************"

    cp /boot/old-config.txt /boot/config.txt

    # Restore startup
    echo "**************************************"
    echo "Restoring RetroPie Startup Commands"
    echo "**************************************"

    cp "/opt/retropie/configs/all/old-autostart.sh" "/opt/retropie/configs/all/autostart.sh"
    cp "/opt/retropie/configs/all/old-runcommand-onend.sh" "/opt/retropie/configs/all/runcommand-onend.sh"
    cp "/opt/retropie/configs/all/old-runcommand-onstart.sh" "/opt/retropie/configs/all/runcommand-onstart.sh"

    echo "======================================"
    echo "Uninstallation Complete!!!"
    echo "======================================"
fi

# End
