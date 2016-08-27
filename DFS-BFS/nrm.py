def checking(graph, starts, pairs):
	print(starts)
	for point in starts:
		record = [point]
		i = 0 # the position in record
		j = 0 # store where should I search for



		while i < len(record): # record is increasing, i is the position
			parent = record[i] # initialize for each start point

			if record[i] not in graph.keys():
				print(record[i], " ----------------------------------> ")

			else:
				# like a 
				for ch in graph[parent]: # b,c,d,e
					if ch not in record:
						record.append(ch)
					else:
						print("Else, i = ", i, "index in record ",record.index(ch), record)
						if i >= record.index(ch):
							i -= 1

						record.remove(ch)
						record.append(ch)
						print(record)

						print("finding num in --->", record[:i], ch)
						for num in record[:i]:
							if [num, ch] in pairs and len(graph[num]) > 1: # need to remove
								pairs.remove([num, ch])
								graph[num].remove(ch)
								print(num, ch)
			i += 1
			print()




	return pairs



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
		pairs = checking(graph, starts, pairs)

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
	
	

	