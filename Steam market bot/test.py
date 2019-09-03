import requests, simplejson, matplotlib, time

cookies = {'steamLogin': '76561198077297097%7C%7C7228218AB5621A0DC1704556D4737F5162965836'}
params = {'country': 'US', 'currency': 1, 'appid': 570, 'market_hash_name': 'Dragonclaw Hook'}
data = requests.get('http://steamcommunity.com/market/pricehistory', params=params, cookies=cookies)
#print(data.text)
a = simplejson.loads(data.text)

date = ' '.join(a['prices'][0][0].split()[0:3])

print(date)

t = time.strptime("30 Nov 00", "%d %b %y") #date, '%b %d %y'
#t = datetime.datetime(2005, 7, 14, 12, 30)

print(t.tm_year)
