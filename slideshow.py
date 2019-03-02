import random
from tqdm import tqdm

FILENAME = "a"

def get_union(tags1, tags2):
    return list(set(tags1) | set(tags2))

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def get_score(tags_1, tags_2):
	inter = len(list(set(tags_1) & set(tags_2)))
	t1 = len(list(set(tags_1) - set(tags_2)))
	t2 = len(list(set(tags_2) - set(tags_1)))
	return min(t1, inter, t2)

with open(FILENAME + ".txt") as f:
    content = f.readlines()
content = [x.strip() for x in content] 

n = int(content[0])

poze = []

for i in range(1,n-1):
	rand = content[i].split()
	poza = {'id': i-1, 'type': rand[0], 'tags': rand[2:]}
	poze.append(poza)


random.shuffle(poze)

newlist = sorted(poze, key=lambda k: k['type']) 

memory = {}

f = open("result_"+FILENAME+".txt", "w")

output = ''
nr_slides = 0
slides = []
vvert = []

for max in newlist:
	if max['type'] == 'H':
		#output += str(max['id']) + '\n'
		slides.append({'id_1': max['id'], 'id_2': -1, 'tags': max['tags']})
		nr_slides += 1

	else:
		vvert.append(max)
		# if memory == {}:
		# 	memory = max
		# else:
		# 	#output += str(max['id']) + ' ' + str(memory['id']) + '\n'
		# 	slides.append({'id_1': max['id'],
		# 				     'id_2': memory['id'],
		# 				     'tags': list(set(max['tags']) | set(memory['tags'])),
		# 				     'fost': False})
		# 	memory = {}
		# 	nr_slides += 1

vert = sorted(vvert, key=lambda k: len(k['tags']))
vertical = []
nr_vert = len(vert)
decrem = nr_vert - 1

for i in range(nr_vert / 2):
	union = get_union(vert[i]['tags'], vert[decrem]['tags'])
	vertical.append({'id_1': vert[i]['id'], 'id_2': vert[decrem]['id'], 'tags': union})
	decrem -= 1

slides += vertical
nr_slides = len(slides)

#random.shuffle(slides)
slides = sorted(slides, key=lambda k: len(k['tags']))

search_limit = 1000
flag = 0
final_slides = []
final_slides.append(slides[0])
slides.remove(slides[0])

for i in tqdm(range(0, nr_slides-1)):
	slide = final_slides[i]
	interations = 0
	max_comun = -999
	better_one = -1

	for slide2 in slides:
		interations += 1
		if interations > search_limit:
			break
		if better_one == -1:
			better_one = slide2
		comun = get_score(slide['tags'], slide2['tags'])
		if comun > max_comun:
			max_comun = comun
			better_one = slide2

	if better_one != -1:
		slides.remove(better_one)
		final_slides.append(better_one)


f.write(str(len(final_slides)) + '\n')
for slide in final_slides:
	if slide['id_2'] != -1:
		output += str(slide['id_1']) + ' ' + str(slide['id_2']) + '\n'
	else:
		output += str(slide['id_1']) + '\n'

f.write(output)