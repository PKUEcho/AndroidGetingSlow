import numpy as np
import os

def getLatencyFromChar(l):
	ll = l.replace('+', '').replace(')', '').replace('ms', '')
	minute = 0
	second = 0
	mesc = 0
	if ll.find('m') != -1:
		minute = int(ll[:ll.find('m')])
		ll = ll[ll.find('m') + 1:]
	if ll.find('s') != -1:
		second = int(ll[:ll.find('s')])
		ll = ll[ll.find('s') + 1:]
	mesc = int(ll)
	res = (minute * 60 + second) * 1000 + mesc
	return res

def parseOneLogFile(file):
	res = {}
	for line in file:
		if line.find('Displayed') == -1:
			continue
		items = line.strip().split(':')
		activity = items[1][11:]
		latency = items[2].split(' ')[-1]
		if activity in res:
			res[activity].append(getLatencyFromChar(latency))
		else:
			res[activity] = [getLatencyFromChar(latency)]
	return res


os.system('rm log/pro_log/*')

file1 = open('log/AM1.log')
res1 = parseOneLogFile(file1)
file2 = open('log/AM2.log')
res2 = parseOneLogFile(file2)

all = open('log/pro_log/all', 'a+')
all.write('latency\ttype\n')

for item in res1:
	if len(res1[item]) < 10:
		continue
	pro_file = 'log/pro_log/' + item.replace('/', '-')
	if not os.path.exists(pro_file):
		f = open(pro_file, 'a+')
		f.write('latency\ttype\n')
	else:
		f = open(pro_file, 'a')
	for l in res1[item]:
		if l > 15 * 1000:
			continue
		f.write(str(l) + '\tT1\n')
		all.write(str(l) + '\tT1\n')
	# print item + ': ' + str(res[item])
	nparray = np.array(res1[item])
	print item + ': ' + str(nparray.mean())

for item in res2:
	if len(res2[item]) < 10:
		continue
	pro_file = 'log/pro_log/' + item.replace('/', '-')
	if not os.path.exists(pro_file):
		f = open(pro_file, 'a+')
		f.write('latency\ttype\n')
	else:
		f = open(pro_file, 'a')
	for l in res2[item]:
		if l > 15 * 1000:
			continue
		f.write(str(l) + '\tT2\n')
		all.write(str(l) + '\tT2\n')
	# print item + ': ' + str(res[item])
	nparray = np.array(res2[item])
	print item + ': ' + str(nparray.mean())

























