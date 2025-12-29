#!/bin/bash
set -e

IMAGE_NAME=ke5haav/claude-desktop-builder:latest
DEB_FILE=claude-desktop_0.12.55_amd64.deb

echo "Pulling Claude Desktop Docker image…"
docker pull $IMAGE_NAME

echo "Extracting .deb package…"
docker create --name claude-temp $IMAGE_NAME
docker cp claude-temp:/home/appuser/claude-desktop-debian/$DEB_FILE .
docker rm claude-temp

echo "Installing Claude Desktop…"
sudo dpkg -i $DEB_FILE
sudo apt-get -f install -y

echo "Claude Desktop installed successfully!"
echo "You can now run: claude-desktop"

# Cleanup
rm $DEB_FILE