#! /bin/bash
ls C2_TrainDev/Dev/*.jpg | sed 's/.*\/Dev\///' | sort > oridev.txt
ls C2_TrainDev/cut3000yolo_dev/*.jpg | sed 's/.*\/cut3000yolo_dev\///' | sort > cutdev.txt
DIFF=$(diff oridev.txt cutdev.txt -y --suppress-common-lines | awk '{print "../Croppedmango/C2_TrainDev/Dev/" $1'\n'}' )
echo "$DIFF" > echofile.txt

