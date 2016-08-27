def checking(graph, starts, pairs, deep):
	for start in starts:
		record = [start]; i = 0; j = 0
		if start not in deep: deep[start] = [[],[]]

		while i < len(record): 
			parent = record[i] 

			if record[i] not in graph.keys(): pass

			else:
				for node in graph[parent]: # b,c,d,e
					if node not in record:
						record.append(node)
						if node not in deep:
							deep[node] = [[parent], deep[parent][0] + deep[parent][1]]
						else:
							for ch in deep[node][0]:
								if ch in deep[parent][1]:
									deep[node][0].remove(ch)
							if parent not in deep[node][1]:
								deep[node][0].append(parent)
								deep[node][1] = deep[node][1] + deep[parent][0] + deep[parent][1]

					else:
						if i >= record.index(node): i -= 1
						record.remove(node); record.append(node)

						for ch in deep[node][0]:
							if ch in deep[parent][1] or ch in deep[parent][0]:
								deep[node][0].remove(ch)

						if parent not in deep[node][1]:
							deep[node][0].append(parent)
							deep[node][1] = deep[node][1] + deep[parent][0] + deep[parent][1]
			i += 1
	return deep



def main():
	try:
		number = str(input("partial_order_"))
		filename = "partial_order_" + number + ".txt"
		#a = datetime.datetime.now()
		#filename = str(input("Which data file do you want to use? "))
		txt = open(filename)
		
		graph = {}; pairs = []; deep = {}; starts, ends = [], []
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
		deep = checking(graph, starts, pairs, deep)
		for k in range(len(pairs)-1,-1,-1):
			try:
				if pairs[k][0] in deep[pairs[k][1]][1]:
					pairs.pop(k)
			except:
				pass

		# print out the non redundant paths stored in pairs
		print("The nonredundant facts are:")
		for p in pairs: print("R({:s},{:s})".format(p[0], p[1]))

		#b = datetime.datetime.now()
		#print(b-a)
		
	except OSError as err:
		print("OS error: {0}".format(err))


if __name__ == '__main__':
	import datetime	
	main()
	

	