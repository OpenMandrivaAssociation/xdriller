#!/bin/bash
#
# Wrapper script for xdriller.
#
# Copies the default configuration files to the current user's home.
#

CONFIG_DIR="$HOME/.config/xdriller/"

if ! test -x "$CONFIG_DIR/"
then
	mkdir -p "$CONFIG_DIR/"
	cp -R /usr/share/xdriller/default_config/*.cfg "$CONFIG_DIR"
fi

/usr/bin/xdriller-bin $*
