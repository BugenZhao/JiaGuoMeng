#!/bin/bash

# 1920x1080 (default):
# Line1arr=("300 600" "560 400" "800 320") # 第一行建筑坐标
# Line2arr=("300 850" "560 700" "820 600") # 第二行建筑坐标
# Line3arr=("320 1130" "560 1000" "820 850") # 第三行建筑坐标
# Train=("670 1640" "840 1590" "950 1500") # 火车三个货物坐标

Line1arr=("300 600" "560 400" "800 320") # 第一行建筑坐标
Line2arr=("300 850" "560 700" "820 600") # 第二行建筑坐标
Line3arr=("320 1130" "560 1000" "820 850") # 第三行建筑坐标
Train=("670 1640" "840 1590" "950 1500") # 火车三个货物坐标
AllBuilding=("${Line1arr[@]}"  "${Line2arr[@]}" "${Line3arr[@]}")
COUNTER1=0
while [ $COUNTER1 -lt 1000000 ]
do
  echo "火车上货 开始"
  for tra in "${Train[@]}"
  do
    # 处理异常弹框 点击一下关闭弹框先
    ~/Library/Android/sdk/platform-tools/adb shell input tap $tra
    for building in "${AllBuilding[@]}"
    do
      for count in 1 2 3
      do 
        ~/Library/Android/sdk/platform-tools/adb shell input swipe $tra  $building 150
        # echo $tra  $building
        sleep 0.02
      done
    done
  done
  echo "火车上货 结束"
  sleep 0.01
done
