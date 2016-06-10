import re
import numpy as np

package_name = 'com.halfbrick.fruitninja'
log_file = 'raw_log/ninja_5.1.1.log'

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
        if not items[0] in res:
            res[items[0]] = {}
        res[items[0]][items[1]] = items[2]
    return res

version_map = read_meta_file()

def apk2version(apk):
    if apk.find('apk') != -1:
        apk = apk[:-4]
    return version_map[package_name][apk]


f = open(log_file)

perf = {}
cur_version = None
for line in f:
    # Sample line:
    # I/PackageManager( 1843 ): Verification timed out for file:///data/local/tmp/fdf8c517ce82db7a684f64d31ee7c329.apk
    if line.find('Continuing with installation') != -1:
        print line
        items = line.strip().split(' ')
        apk_name = items[-1].strip().split('/')[-1]
        cur_version = int(apk2version(apk_name))
        perf[cur_version] = {}
    # Sample line:
    # I/ActivityManager( 1843 ): Displayed com.kugou.android/.app.splash.SplashActivity: +667ms
    if line.find('Displayed') != -1:
        value = perf[cur_version]
        items = re.split(' |\t', line.strip())
        print items
        activity = (items[4][:-1]).split('.')[-1]
        if activity not in value:
            value[activity] = []
        latency =  parseLatency(items[-1])
        value[activity].append(latency)



# perf format:
# {v1: {act1: [l1, l2...], act2: [...]},
#  v2: {...}}
for version in perf:
    print version
    for activity in perf[version]:
        print '\t' + activity + ': '+ str(len(perf[version][activity]))

# Sort via version number
keys = perf.keys()
keys.sort()
sort_perf = [(key, perf[key]) for key in keys]

activity_name = {
    'com.kugou.android': ['MediaActivity', 'SplashActivity'],
    'com.youdao.dict': ['DictSplashActivity', 'MainActivity']
}

act = activity_name[package_name]
outFile = open('parse_result/' + package_name, 'w+')
outFile.write('version\t%s\t%s\n' % (act[0], act[1]))

for item in sort_perf:
    outFile.write(str(item[0]) + '\t')
    if act[0] in item[1]:
        narray = np.array(item[1][act[0]])
        outFile.write(str(np.median(narray)) + '\t')
    else:
        outFile.write('0\t')
    if act[1] in item[1]:
        narray = np.array(item[1][act[1]])
        outFile.write(str(np.median(narray)) + '\n')
    else:
        outFile.write('0\n')



outFile.close()














