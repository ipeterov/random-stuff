import multiserver

links = ['http://careers.stackoverflow.com/companies?searchTerm=python&location=&range=20&distanceUnits=Miles&pg={}'.format(i) for i in range(1, 252)]
nodes = [('', 9090), ('168.235.86.179', 9090)] #, ('168.235.86.179', 9090)

master = multiserver.Master(links, nodes)
print(master.get_results())
