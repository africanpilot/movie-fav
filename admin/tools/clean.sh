#!/bin/bash

# Copyright © 2022 by Richard Maku.
# All Rights Reserved. Proprietary and confidential.
set -e

sudo docker system prune
sudo rm -rf ~/.local/share/Trash/*
sudo apt-get clean
sudo apt-get autoclean
sudo apt-get autoremove --purge

$SHELL