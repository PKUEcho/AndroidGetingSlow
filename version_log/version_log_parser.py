import os
import numpy as np

def parseLatency(l):
    ll = l.replace('+', '').replace(')', '').replace('ms', '')
    minute = 0
    second = 0
    msec = 0
    if ll.find('m') != -1:
        minute = int(ll[:ll.find('m')])
        ll = ll[ll.find('m') + 1:]
    if ll.find('s') != -1:
        second = int(ll[:ll.find('s')])
        ll = ll[ll.find('s') + 1:]
    msec = int(ll)
    res = (minute * 60 + second) * 1000 + msec
    return res

def read_meta_file():
    meta_file = open('/home/echo/Documents/apks/top_50_apk_meta')
    res = {}
    for line in meta_file:
        if line.find('packageName') != -1:
            continue
        items = line.strip().split('\t')
        res[items[1]] = (items[0], items[2])
    return res

version_map = read_meta_file()
def apk2version(apk):
    if apk.find('apk') != -1:
        apk = apk[:-4]
    return version_map[apk][1]

# perf format:
# {package_name/activity: {apk_version: {android_version1: {[l1, l2, ...]}}}}
perf = {}
raw_logs = os.listdir('raw_log')
for log in raw_logs:
    f = open('raw_log/' + log)
    android_version = log.strip().split('-')[-1]
    apk_version = None
    for line in f:
        if line.find('Continuing with installation') != -1:
            items = line.strip().split(' ')
            apk_name = items[-1].strip().split('/')[-1]
            apk_version = int(apk2version(apk_name))
        if line.find('Displayed') != -1:
            items = line.strip().split(' ')
            if line.find('(total') != -1:
                del items[-2]
                del items[-2]
            package = (items[-2][:-1]).split('/')[0]
            activity = (items[-2][:-1]).split('.')[-1]
            latency =  parseLatency(items[-1])
            # store in perf
            key = package + '/' + activity
            if key not in perf:
                perf[key] = {}
            if apk_version not in perf[key]:
                perf[key][apk_version] = {}
            if android_version not in perf[key][apk_version]:
                perf[key][apk_version][android_version] = []
            perf[key][apk_version][android_version].append(latency)

interested_android_versions = ['5.1.1', '6.0.0']
for activity in perf:
    outFile = open('parse_result/' + activity.replace('/', '-'), 'w+')
    outFile.write('version\t5.1.1\t6.0.0\t7.0.0\n')
    cur_perf = perf[activity]
    keys = cur_perf.keys()
    keys.sort()
    sort_perf = [(key, cur_perf[key]) for key in keys]
    for item in sort_perf:
        outFile.write(str(item[0]))

activity_name = {
    'com.kugou.android': ['MediaActivity', 'SplashActivity'],
    'com.youdao.dict': ['DictSplashActivity', 'MainActivity'],
    'com.halfbrick.fruitninja': ['MortarGameActivity'],
    'com.baidu.video': ['VideoActivity', 'WelcomActivity'],
    'com.estrongs.android.pop': ['FileExplorerActivity'],
}

acts = activity_name[package_name]
outFile = open('parse_result/' + package_name, 'w+')
outFile.write('version\t%s\n' % ('\t'.join(acts)))

for item in sort_perf:
    outFile.write(str(item[0]))
    for act in acts:
        if act in item[1]:
            narray = np.array(item[1][act])
            outFile.write('\t' + str(np.median(narray)))
        else:
            outFile.write('\t0')
    outFile.write('\n')

outFile.close()














