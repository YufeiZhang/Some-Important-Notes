def dfs_rec(graph, start, deep):
    if start not in graph.keys():
    	pass
    
    else:
    	for node in graph[start]:
    		if node not in deep:
    			deep[node] = [[start], deep[start][0] + deep[start][1]]

    		else:
    			for ch in deep[node][0]:
    				if ch in deep[start][1]:
    					deep[node][0].remove(ch)

    			if start not in deep[node][1]:
    				deep[node][0].append(start)
    				deep[node][1] = deep[node][1] + deep[start][0] + deep[start][1]
    			
    		deep = dfs_rec(graph, node, deep)

    return deep
    

def main():
	try:
		number = str(input("partial_order_"))
		filename = "partial_order_" + number + ".txt"

		a = datetime.datetime.now()
		#filename = str(input("Which data file do you want to use? "))
		txt = open(filename)
	

		graph = {}; pairs = []; starts, ends = [], []
		deep = {}
		for line in txt:			
			line = line.replace(" ", ""); pair = line.split(',')
			pair[0], pair[1] = pair[0][2:], pair[1][:-2]
			pairs.append(pair)

			if pair[0] not in starts:
				if pair[0] not in ends:
					starts.append(pair[0])

			if pair[1] not in ends:
				if pair[1] in starts: 
					starts.remove(pair[1])
				ends.append(pair[1])

			if pair[0] not in graph: graph[pair[0]] = [pair[1]]
			else: 
				if pair[1] not in graph[pair[0]]:
					graph[pair[0]].append(pair[1])

		# check which to print
		for i in range(len(starts)):
			deep[starts[i]] = [[],[]]
			deep = dfs_rec(graph, starts[i], deep)
			
			#print(deep)
			for k in range(len(pairs)-1,-1,-1):
				try:
					if pairs[k][0] in deep[pairs[k][1]][1]:
						pairs.pop(k)
				except:
					pass


		# print out the non redundant paths stored in pairs
		print("The nonredundant facts are:")
		for p in pairs: print("R({:s},{:s})".format(p[0], p[1]))

		b = datetime.datetime.now()
		print(b-a)
		
	except OSError as err:
		print("OS error: {0}".format(err))


if __name__ == '__main__':
	import datetime
	
	main()
	
	

	