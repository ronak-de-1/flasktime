#!/bin/bash

echo "Well done, you cracked the final round. Your token is:" > /tmp/.gkJarCdxhy1rM7ymo36yHzrJtax
echo -n ${ATTEMPT_ID}ShuT1tD0wn! | md5sum | cut -c 1-6 >> /tmp/.gkJarCdxhy1rM7ymo36yHzrJtax
steghide embed -cf /home/kali/Desktop/key.jpeg -ef /tmp/.gkJarCdxhy1rM7ymo36yHzrJtax -p "Our fears do make us traitors." -f
rm /tmp/.gkJarCdxhy1rM7ymo36yHzrJtax
exiftool -comment="My favourite play is what you need, folger.edu is the best place to read." /home/kali/Desktop/key.jpeg
rm /home/kali/Desktop/key.jpeg_original