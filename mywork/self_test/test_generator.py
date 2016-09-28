import sys, random
sys.path.append('../../')
from mywork import HW2

class KnowledgeBase(list):
	def __init__(self, input_list):
		self._name = input_list
		self.len = len(input_list)
		func_set, const_set = set(), set()
		for sentence in input_list:
			for clause in sentence.clauses:
				func_set.add((clause.func, len(clause.args)))
				for const in clause.args:
					if isinstance(const, HW2.Constant):
						const_set.add(const)
			if sentence.is_imply:
				func_set.add((sentence.imply[0].func, len(sentence.imply[0].args)))
				for const in sentence.imply[0].args:
					if isinstance(const, HW2.Constant):
						const_set.add(const)
		self._funcs = func_set
		const_set.add('x')
		self._consts = const_set

	@property
	def funcs(self):
		if hasattr(self, '_funcs'):
			return self._funcs
		return set()
	@property 
	def args(self):
		if hasattr(self, '_consts'):
			return self._consts
		return set()
	@property 
	def name(self):
		if hasattr(self, '_name'):
			return self._name
		return self
	def __str__(self):
		if hasattr(self, '_name'):
			return '%s' % self._name
		return self
	__repr__ = __str__

def query_generator(kb):
	func, argc = random.sample(kb.funcs,1)[0]
	args = random.sample(kb.args, argc)
	return '%s(%s)' % (func, ', '.join(args))

test_num = 20 #num of tests generated for each kb
kbs = []
sample_num = 40
# read all kbs
with open('testcases/all_kb.txt') as all_kb:
	kb_tmp = []
	for line in all_kb:
		if line.strip() == '--':
			kbs.append(KnowledgeBase(kb_tmp))
			kb_tmp = []
		else:
			kb_tmp.append(HW2.Sentence(line))

for kb in kbs:
	print kb
	for i in xrange(test_num):
		query = query_generator(kb)
		with open('testcases/sample%03d.txt'%sample_num, 'w') as sample_file:
			sample_file.write('%s\n'%query)
			sample_file.write('%d'%kb.len)
			for sentence in kb.name:				
				sample_file.write('\n%s'%sentence.strip())
		sample_num +=1



