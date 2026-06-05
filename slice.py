# lists takign slices out of them 

cities =  ["Atlanta", "Baltimore", "Chicago",
"Denver", "Los Angeles", "Seattle"]

smaller_of_list_cities = cities[2:5]
# "Chicago","Denver", "Los Angeles"

print(smaller_of_list_cities)


# removing elements

tasks = ["email Frank", "call Sarah", "meet with Zach"]

del tasks[0]
print(tasks)

#tasks.remove("email Frank")# error
tasks.remove("call Sarah")
print(tasks)


# pop removes and returns a element

tasks.append("email Frank")
tasks.append("meet with Joseph")
tasks.insert(0, "lixo1")

print(tasks)


smaller_tasks = tasks.pop(1)
print(smaller_tasks)


# starts with the last element 
print(tasks.pop())

# tuples is like a list BUT cant change, 
# defined and has this constraint of being immutable


## input and castings to change type

#numMaybe : str = str(input("Digite aqui um NUMERO: "))
#print(type(numMaybe))
#print(numMaybe)

#print(numMaybe + " 5")

#print(numMaybe + 5)# ERROR, CANNOT CONCAT


# geting title -> Title with the title function, and lowering something, and uppering it

dic = {}

dic["abc","cdf"] = "al","hneta"

print(dic)


# to list
print(dic.values())

print(dic.keys())


# a item in a dictionary is a pair (key, value), OBVIOUS!


# can make a list of dictionaries or [KEY - VALUE], struct type maybe

# * -> list ; ** -> dictionary OBVIOS - case is a 2 dimensional structure 



## classes -> abstracting things


class Patient:
	def __init__(self, name, last_name, age, id):
		self.name = name
		self.last_name = last_name
		self.age = age 
		self.id = id 


	def __repr__(self):
		return (f"Name: {self.name.title()}\nLast name: {self.name.title()}\nAge: {self.age}\nID: {self.id}\n")


	def verify_age_adult(self, verifyAge):
		idade_objAtual = self.age 

		if idade_objAtual < 21:
			print("adulto voce nao é")
			if verifyAge > idade_objAtual:
				print("idade menor que a pedida. Favor se retire!\n")
		else:
			print("talvez voce seja adulto ein\n")


patient = Patient("fausto", "silva", 22, 1)
print(patient)

## DATA FILES!



#with open("testes_union_attack.txt", "r") as fp:



# csv files -> 
import csv

with open("contents_csv.csv") as fp:
	contents_of_fp = csv.reader(fp)

	buffer_line = [[] for _ in range(3)]

	print(buffer_line)

	lines = []

	for index, each_line in enumerate(contents_of_fp):
		buffer_line.append(each_line)

		lines += each_line


# closes the fp!

print(buffer_line)
print(lines)


## references, garbage colletion

import weakref 
s1 = {1,2,3}
s2 = s1 # second reference to the list 

def bye():
	print("whatever")

ender = weakref.finalize(s1, bye) # callback no objeto s1
print(ender.alive) 

del s1 
ender.alive
s2 = 'spam'

print(ender.alive)

t1 = (1,2,3)
t2 = t1
if t2 is t1:
	print("True")

t3 = t1[:]



### ALGUNS SAO COMPARTILHADOS!