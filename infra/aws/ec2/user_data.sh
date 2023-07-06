#!/usr/bin/env sh

yum install git -y
yum install python -y
yum install python-pip -y
pip install --upgrade pip

# # Create a directory for the mount point
# mkdir /mnt/myvolume

# # Mount the volume to the created directory
# mount /dev/xvdf /mnt/myvolume

# chown -R $USER:$USER /mnt/myvolume
# chmod -R 755 /mnt/myvolume
