
def find_paths(graph, start, end, path):
	# update the path and check if start point == end point
	path = path + [start]
	if start == end: return [path]
	if start not in graph.keys(): return []

	# create a new list to store a new path
	# chech all paths with the gieve start point
	paths = []
	for point in graph[start]:
		if point not in path:
			new_paths = find_paths(graph, point, end, path)
			for new_path in new_paths: paths.append(new_path)
	return paths


def main():
	try:
		number = str(input("partial_order_"))
		filename = "partial_order_" + number + ".txt"
		a = datetime.datetime.now()

		#filename = str(input("Which data file do you want to use? "))
		txt = open(filename)

		# read the input file and store the graph into a dictionary
		# also, store all pair of R(a,b) into a list called pairs
		graph = {}; pairs = []
		for line in txt:			
			line = line.replace(" ", ""); pair = line.split(',')
			pair[0], pair[1] = pair[0][2:], pair[1][:-2]
			pairs.append(pair)
			if pair[0] not in graph: graph[pair[0]] = [pair[1]]
			else: graph[pair[0]].append(pair[1])
		
		# check if a path is redundent
		for i in range(len(pairs)-1, -1, -1):
			ways = find_paths(graph, pairs[i][0], pairs[i][1], [])
			if len(ways) > 1: pairs.pop(i)
			elif len(ways) == 1 and len(ways[0]) > 2: pairs.pop(i)

		# print out the non redundant paths stored in pairs
		print("The nonredundant facts are:")
		for p in pairs: print("R({:s},{:s})".format(p[0], p[1]))

		b = datetime.datetime.now()
		print(b-a)
		
	except OSError as err:
		print("OS error: {0}".format(err))


if __name__ == '__main__':
	import datetime
	#
	main()


	