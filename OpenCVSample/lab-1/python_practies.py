import random

list = []
while len(list)<50:
	x = random.randrange(0,100)
	list.append(x)
	
list2 = []
list3 = []
list4 = []

for i in list:
	if i<50:
		list2.append(i)
	elif (i>50 and i<75):
		list3.append(i)
	else:
		list4.append(i)
		
print list2
print list3
print list4