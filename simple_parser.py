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


file = open('log/7.log')
res = parseOneLogFile(file)

all = open('log/pro_log/all', 'a+')
all.write('latency\ttype\n')

for item in res:
	# print item + ': ' + str(res[item])
	nparray = np.array(res[item])
	print item + ': ' + str(nparray.mean())






















