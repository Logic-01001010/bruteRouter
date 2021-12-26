import requests

proxies = {
    'http':'socks5://127.0.0.1:9050',
    'https':'socks5://127.0.0.1:9050'
}
url = 'https://ipinfo.io/ip'
res = requests.get(url, proxies=proxies)

print(res.text)
