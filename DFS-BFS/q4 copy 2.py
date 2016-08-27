def dfs_rec(graph, start, path, n, deep):
    path = list(path) + [start]
    print(start, n)

    if start not in deep:
    	deep[start] = n
    
    if start not in graph.keys():
    	pass

    else:
    	for node in graph[start]:
    		print("node",node, "start = ", start)
    		if node not in path:
    			path = dfs_rec(graph, node, path, n+1, deep)
    		else:
    			print("start -> end = ", start, node)
    			if node in graph[start]:
    				if deep[start] >= deep[node]:
    					deep[node] = deep[start] + 1
    					path = dfs_rec(graph, node, path, n+1, deep)
    return deep
    



def main():
	try:
		number = str(input("partial_order_"))
		filename = "partial_order_" + number + ".txt"

		a = datetime.datetime.now()
		#filename = str(input("Which data file do you want to use? "))
		txt = open(filename)

		# read the input file and store the graph into a dictionary
		# also, store all pair of R(a,b) into a list called pairs
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
			deep = dfs_rec(graph, starts[i], [], 0, {})
			print(deep)
			for k in range(len(pairs)-1,-1,-1):
				try:
					#print(deep[pairs[k][1]])
					current = []
					for vertex in graph[pairs[k][0]]:
						current.append( deep[vertex] - deep[pairs[k][0]] )

					current_min = min(current)
					if abs(deep[pairs[k][1]] - deep[pairs[k][0]]) > current_min:
						pairs.pop(k)
				except:
					pass
		
					
		#print(pairs)


		# print out the non redundant paths stored in pairs
		print()
		print("The nonredundant facts are:")
		for p in pairs: print("R({:s},{:s})".format(p[0], p[1]))

		b = datetime.datetime.now()
		print(b-a)
		
	except OSError as err:
		print("OS error: {0}".format(err))


if __name__ == '__main__':
	import datetime
	
	main()
	
	

	