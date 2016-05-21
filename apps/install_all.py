from subprocess import call
import time
import os

def run(cmd):
    ret = call(cmd, shell=True)
    if ret != 0:
        sys.exit('Exec cmd %s error, return value: %s' %(cmd, str(ret)))

apk_dir = './installed/'
apks = os.listdir(apk_dir)

for apk in apks:
	print 'Installing apk: ' + apk + '......'
	run('adb install ' + apk_dir + apk)