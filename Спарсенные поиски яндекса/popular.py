requests = open('resultp.txt', 'r', encoding = 'utf8')
unique_requests = {}
bad_strings = ['http', 'www', '&quot', '/', '.', 'вконтакт', 'одноклассник', 'vk', 'google']

for request in requests:
    request = request.strip('\n').lower()
    if request not in unique_requests:
        unique_requests[request] = 1
    else:
        unique_requests[request] += 1
for key in unique_requests.copy():
    todelete = 0
    #for string in bad_strings:
        #if string in key:
            #todelete = 1
    if unique_requests[key] < 20:
        todelete = 1
    if todelete:
        del unique_requests[key]

output = open('output.txt', 'w', encoding = 'utf8')

kv = list(zip(unique_requests.keys(), unique_requests.values()))
kv.sort(key=lambda x: x[1])
kv.reverse()

for pair in kv:
    output.write(str(pair[0]) + ' ' + str(pair[1]) + '\n')
