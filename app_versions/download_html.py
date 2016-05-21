import urllib
import os
import socket

meta_file = open('top_50_apk_meta')
socket.setdefaulttimeout(15)

for line in meta_file:
	if line.find('versionCode') != -1:
		continue
	items = line.strip().split('\t')
	html_file = 'htmls/' + items[0] + '-' + items[2] + '.html'
	if os.path.exists(html_file):
		# print html_file + ' already exists'	
		continue
	url = 'http://apk.hiapk.com/appinfo/' + items[0] + '/' + items[2]
	print 'Download ' + url + '...'
	try:
		urllib.urlretrieve(url, html_file)
	except Exception:
		continue