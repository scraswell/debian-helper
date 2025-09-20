#!/bin/bash

if [[ ! -f /home/github/_work/.permissions_fixed ]]; then
    sudo chown -R github:github /home/github/_work
    touch /home/github/_work/.permissions_fixed
fi
