import pygeoip

ip = input('Input IP: ')
gip = pygeoip.GeoIP('GeoLiteCity.dat')

for key, value in gip.record_by_addr('64.233.161.99').items():
    print('{}: {}'.format(key, value))
