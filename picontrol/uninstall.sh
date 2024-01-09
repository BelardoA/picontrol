#!/bin/bash

# RetroPi Control Uninstall
SCRIPTS='/home/pi/scripts'
# RetroPie configs
CONFIGS='/opt/retropie/configs/all'

section () {
    echo ""
    echo "**************************************"
    echo "$1"
    echo "**************************************"
    echo ""
}

# Start uninstall
echo "**************************************"
echo "Uninstalling Pi Control"
echo "**************************************"

read -rp "Warning: This will uninstall Pi Control. Do you want to proceed? (y/n): " REPLY

if [ "$REPLY" = "y" ] || [ "$REPLY" = "Y" ]; then
    section "Removing NFC Libraries"

    pip uninstall Adafruit-PN532 Adafruit-GPIO -y
    echo "Done."

    section "Uninstalling PiControl libraries"

    # Determine Raspberry Pi Model
    RPI_MODEL=$(cat /proc/device-tree/model)
    echo "$RPI_MODEL"
    MODEL_NUMBER=$(echo $RPI_MODEL | grep -o -E '[0-9]+' | head -n 1)

    case $MODEL_NUMBER in
        3)
            echo "Raspberry Pi 3 PiControl Detected"
            ;;
        4)
            echo "Raspberry Pi 4 PiControl Detected"
            ;;
        5)
            echo "Raspberry Pi 5 PiControl Detected"
            ;;
        *)
            echo "Raspberry Pi Model Not Detected or not supported. Please use a raspberry pi 3, 4, or 5."
            exit 1
            ;;
    esac
    REQS=pi$MODEL_NUMBER-requirements.txt
    pip uninstall -r "$REQS" -y

    # Remove files
    section "Removing PiControl Script Files"
    rm -rf "$SCRIPTS"
    # make sure the folder is gone
    if [ -d "$SCRIPTS" ]; then
        echo "PiControl folder not removed. Please check the installation and try again."
        exit 1
    else
        echo "Done."
    fi

    section "Reverting Serial Interface Settings"

    cp /boot/old-config.txt /boot/config.txt
    echo "Done."

    # Restore startup
    section "Restoring RetroPie Startup Commands"
    cp "$CONFIGS/old-autostart.sh" "$CONFIGS/autostart.sh"
    echo "Done."
    section "Restoring RetroPie Runcommand Commands"
    cp "$CONFIGS/old-runcommand-onend.sh" "$CONFIGS/runcommand-onend.sh"
    cp "$CONFIGS/old-runcommand-onstart.sh" "$CONFIGS/runcommand-onstart.sh"
    echo "Done."

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
