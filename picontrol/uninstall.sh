#!/bin/bash

# RetroPi Control Uninstall
SCRIPTS='/home/pi/scripts'
# RetroPie configs
CONFIGS='/opt/retropie/configs/all'

# Start uninstall
echo "**************************************"
echo "Uninstalling Pi Control"
echo "**************************************"

read -rp "Warning: This will uninstall Pi Control. Do you want to proceed? (y/n): " REPLY

if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    echo "**************************************"
    echo "Removing NFC Libraries"
    echo "**************************************"

    pip uninstall Adafruit-Python Adafruit-GPIO -y

    echo "**************************************"
    echo "Uninstalling picontrol Requirements"
    echo "**************************************"

    pip uninstall -r requirements.txt -y

    # Remove files
    echo "**************************************"
    echo "Removing PiControl Script Files"
    echo "**************************************"
    rm -rf "$SCRIPTS"

    echo "**************************************"
    echo "Reverting Serial Interface Settings"
    echo "**************************************"

    cp /boot/old-config.txt /boot/config.txt

    # Restore startup
    echo "**************************************"
    echo "Restoring RetroPie Startup Commands"
    echo "**************************************"
    echo "Restoring RetroPie Startup Commands"
    cp "$CONFIGS/old-autostart.sh" "$CONFIGS/all/autostart.sh"
    echo "Restoring RetroPie Runcommand Commands"
    cp "$CONFIGS/old-runcommand-onend.sh" "$CONFIGS/runcommand-onend.sh"
    cp "$CONFIGS/old-runcommand-onstart.sh" "$CONFIGS/runcommand-onstart.sh"

    echo "======================================"
    echo "Uninstallation Complete!!!"
    echo "======================================"
    echo "You will need to remove the PiControl Hardware from your Raspberry Pi while it is powered off."
    read -rp "You must shutdown for changes to take effect, shutdown now? (y/n):" REPLY
    if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
        echo "Shutting Down in 5 seconds..."
        sleep 5 && sudo shutdown -h 0
    fi
fi

# End
