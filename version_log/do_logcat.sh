NOW=$(date +"%m-%d %H:%M:%S.000");

adb logcat -T "$NOW" -s ActivityManager PackageManager > $1
