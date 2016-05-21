for i in {1..102}
do
    adb shell dd if=/dev/zero of=/sdcard/FIOTEST/files/zero$i bs=13*1024 count=1024*10
done
