# ECEopenHouse
Raspberry pi based camera for open house presentation
#
Camera based on the Rasperry Pi 4 B+, the Pimoroni Hyperpixel 4" Touch screen Display, and the HQ Camera Module. The use of [this tripod](https://www.pishop.ca/product/tripod-for-raspberry-pi-hq-camera/) is also required to supply parts for the mount.
⚠️The project requires the use of Raspberry Pi OS Bookworm (or later) to allow for proper Kernel drivers used in the display.

To Build the project from a fresh install, follow the steps listed:
  1. After installing Rasperry Pi OS onto and SD card using [the raspberry pi imager](https://www.raspberrypi.com/software/), insert it into the Pi.
  2. Plug the camera cable into the Pi's camera port and run it along the surface of the Pi under where the screen will sit.
  3. Mount the display to the Pi using the GPIO extender and standoffs, ensure to not press on the middle of the screen.
  4. Power on the Pi
  5. After boot, add the cam_preview.py file to a directory (used was /home/*user*/Documents/DemoCam/cam_preview.py), take note of this path.
  6. Open the config.txt file in boot/firmware with the command ```sudo nano /boot/firmware/config.txt```
  7. At the end of the file under ```[all]``` add the 2 lines:
     ```
     [all]
     dtoverlay=vc4-kms--dpi-hyperpixel4,rotate=270
     dtparam=rotate=90
     ```
     You can now save and close config.txt
  8. Edit the autostart file to include the cam_preview.py file by
     ```
     sudo nano ~/.config/autostart/cam_preview.desktop
     ```
     and appending
     ```
     Type=Application
     Name=Camera Preview
     Exec=python3 /home/*user*/Documents/DemoCam/cam_preview.py > /home/pi/camera_log.txt 2>&1
     StartupNotify=false
     Terminal=false
     ```
     after ```[Desktop entry]```
  10.  Make sure the script is executable by running the bash command ```chmod +x /home/*user*/Documents/DemoCam/cam_preview.py```
  11.  Reboot
