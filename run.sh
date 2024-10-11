#!/bin/bash

if [ "$1" == "pub" ]; then
    python sd/launch.py --autolaunch --xformers --share --listen --no-half-vae
else
    python sd/launch.py --autolaunch --xformers --listen
fi
