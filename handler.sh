#!/usr/bin/env bash
#!/bin/bash

#run this script only when a message was received.
if [ "$1" != "RECEIVED" ]; then exit; fi;

cd /opt/advent

/usr/bin/python3 -u /opt/advent/advent.py --incomming --path $2