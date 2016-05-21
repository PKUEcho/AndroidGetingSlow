from subprocess import call
import time

def run(cmd):
    ret = call(cmd, shell=True)
    if ret != 0:
        sys.exit('Exec cmd %s error, return value: %s' %(cmd, str(ret)))



app_list = {
'com.android.chrome': [('org.chromium.chrome.browser.ChromeTabbedActivity', 10)],
# 'com.android.settings': [('.Settings', 10)],
'com.eg.android.AlipayGphone': [('.AlipayLogin', 15)],
'com.hupu.games': [('.home.activity.HupuHomeActivity', 10)],
'com.tencent.mm': [('.ui.LauncherUI', 20), ('.plugin.sns.ui.SnsTimeLineUI', 10)],
# 'com.sina.weibo': [('.SplashActivity', 15)],
'com.android.gallery3d': [('.app.GalleryActivity', 5)],
'com.android.mms': [('.ui.ConversationList', 5)],
# 'com.android.camera2': [('com.android.camera.CameraLauncher', 8)],
'com.android.contacts': [('.activities.PeopleActivity', 4)]
}

test_time = 10

for package in app_list:
	stop_cmd = 'adb shell am force-stop ' + package
	for i in xrange(test_time):
		run('adb shell "echo 3 > /proc/sys/vm/drop_caches"')
		for activity in app_list[package]:
			start_cmd = 'adb shell am start -n ' + package +  '/' + activity[0]
			run(start_cmd)
			time.sleep(activity[1] + 5)
		run(stop_cmd)
		time.sleep(3)