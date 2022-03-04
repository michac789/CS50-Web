from itertools import permutations

def lexicographical_permutation(str):
	perm = sorted(''.join(chars) for chars in permutations(str))
	return perm

def check1(str):
    for i in range(len(str) - 1):
        if str[i] == 'a' and str[i + 1] == 'a':
            return False
    return True
		
str ='aaabbcc'
strings = lexicographical_permutation(str)
count = 0
results = set()
for string in strings:
    if check1(string):
    	results.add(string)
for result in results:
    print(result)
print(len(results))
