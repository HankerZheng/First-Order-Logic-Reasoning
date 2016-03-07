import re

_RE_IMPLY = re.compile('^.+=> (.+)$')
_RE_CLAUSE = re.compile(r'([A-Z]\w*?\(.+?\))')

_RE_FUNC = re.compile(r'([A-Z]\w*?)\(.+?\)')
_RE_ARGS = re.compile(r'[\( ](\w+?)[,\)]')

name_count = 0
_APP_NAME = 'deadbeef'

class BasicClassHW2(str):
	'''
	The basic class for HW2 which inherents from str
	'''
	def __init__(self, name):
		self.name = name.strip(' \n')
		#super(BasicClassHW2,self).__init__(self.name)


class Substitution(dict):
	'''
	Substitution class, a['x']='y' means x/y
	'''
	def __init__(self, *args, **kw):
		for sub in args:
			for key in sub.keys():
				self[key] = sub[key]
		super(Substitution, self).__init__(**kw)

	def add_subst(self, key, val):
		self[key] = val
		# if sub={a/b,b/A}, then the sub should be {a/A, b/A}
		if key in self.values():
			for a in self.keys():
				if self[a] == key: self[a] = val
		return self

	def __str__(self):
		return '(%s, %s)' % (self.keys(), self.values())
	__repr__ = __str__


class Sentence(BasicClassHW2):
	def __init__(self, content):
		self._imply = [Clause(a) for a in _RE_IMPLY.findall(content)]
		self._is_imply = True if self._imply else False

		find_clause = _RE_CLAUSE.findall(content)
		clause = find_clause[:-1] if self._imply else find_clause
		self._clauses = [Clause(a) for a in clause]

		super(Sentence, self).__init__(content)

	@property
	def is_imply(self):
		if hasattr(self, '_is_imply'):
			return self._is_imply
		return False

	@property
	def imply(self):
		if hasattr(self, '_imply'):
			return self._imply
		return []

	@property 
	def clauses(self):
		if hasattr(self,'_clauses'):
			return self._clauses
		return[]

	def __str__(self):
		return self.name
	__repr__ = __str__


class Clause(BasicClassHW2):
	def __init__(self, content):
		self._func = Function(_RE_FUNC.findall(content)[0])
		args = _RE_ARGS.findall(content)
		self._args = []
		for arg in args:
			if arg[0].upper() == arg[0]:
				self._args.append(Constant(arg))
			else:
				self._args.append(Variable(arg))

		super(Clause, self).__init__(content)

	@property
	def func(self):
		if hasattr(self, '_func'):
			return self._func
		return None

	@property 
	def args(self):
		if hasattr(self, '_args'):
			return self._args
		return []

	def update_name(self):
		self.name = '%s(%s)' % (self.func, ', '.join(self.args))

	def change_arg(self, arg, value):
		if arg in self.args:
			if value[0].upper() == value[0]:
				self._args[self.args.index(arg)] = Constant(value)
			else:
				self._args[self.args.index(arg)] = Variable(value)
		else:
			raise ValueError('no such arg found')

	def __str__(self):
		return self.name
	__repr__ = __str__


class Function(BasicClassHW2):
	def __str__(self):
		return self.name
	__repr__ = __str__
class Constant(BasicClassHW2):
	def __str__(self):
		return self.name
	__repr__ = __str__
class Variable(BasicClassHW2):
	def __str__(self):
		return self.name
	__repr__ = __str__


def log_func(func):
	def wrapper(*arg, **kw):
		print "ENTERING %s with " %func.__name__,arg, kw
		result = func(*arg, **kw)
		print "LEAVING %s with" % func.__name__, result
		return result
	return wrapper

#@log_func
def UNIFY(x, y, sub):
	'''
	From the outside of this func, x and y should only be one Clause
	returns a substitution to make x and y identical or 'Failure'

	x,y should at most be one Clause with several args
	if list, the list of all its args
	if var,  the var name
	'''	
	if sub == 'Failure':
		return 'Failure'
	elif x == y:
		return sub
	elif isinstance(x, Variable):
		return UNIFY_VAR(x,y,sub)
	elif isinstance(y, Variable):
		return UNIFY_VAR(y,x,sub)
	elif isinstance(x,Clause) and isinstance(y,Clause):
		return UNIFY(x.args,y.args, UNIFY(x.func,y.func,sub))
	elif isinstance(x,list) and isinstance(y,list):
		return UNIFY(x[1:],y[1:],UNIFY(x[0],y[0],sub))
	else:
		return 'Failure'

def UNIFY_VAR(var,x,sub):
	def OCCUR_CHECK(var,x):
		if isinstance(x, Clause) and var in x.args:
			return True

	if var in sub.keys() and sub[var]==x:
		return sub
	elif var in sub.keys():
		return UNIFY(var, sub[var], sub)
	elif OCCUR_CHECK(var,x):
		return 'Failure'
	else:		
		return sub.add_subst(var,x)

def STANDARD_VARIABLES(clauses, imply):
	'''
	Rename the var in the clauses, and return the new renamed clauses
	The new name is a global unique name
	'''	
	def name_gen(var):
		global name_count
		name_count+=1
		if _APP_NAME in var.name:
			return var[:var.find(_APP_NAME)+len(_APP_NAME)]+str(name_count)
		else:
			return var+_APP_NAME+str(name_count)

	def change_var_name(clause, var_pool):
		tmp = Clause(clause.name)
		for arg in tmp.args:
			if isinstance(arg, Variable):
				if not arg in var_pool:
					var_pool[arg] = name_gen(arg)
					tmp.change_arg(arg, Variable(var_pool[arg])) 
				else:
					tmp.change_arg(arg, Variable(var_pool[arg]))
		tmp.update_name()
		return tmp

	var_pool, lhs, rhs = {}, [], []
	for clause in clauses:
		lhs.append(change_var_name(clause, var_pool))
	for clause in imply:
		rhs.append(change_var_name(clause, var_pool))
	return (lhs,rhs)

def SUBST(sub, clause_in):
	clause = Clause(clause_in.name)
	for arg in clause.args:
		if isinstance(arg, Variable) and arg in sub:
			clause.change_arg(arg, sub[arg])
			clause.update_name()
	return clause


def FATCH_RULE_FOR_GOAL(kb, goal):
	flag = 0
	for sentence in kb:
		if sentence.is_imply:
			if sentence.imply[0].func == goal.func:
				flag = 1
				yield (sentence.clauses, sentence.imply, 0)
		else:
		# find such cases:	1. ASK: A(B),  KB: A(B),  True: A(B)
		#				  	2. ASK: A(x),  KB: A(B),  True: A(B)
			for clause in sentence.clauses:
				if clause.func == goal.func and clause.args == goal.args:
				# case 1
					flag = 1
					yield (sentence.clauses, [goal], 1)
				elif clause.func == goal.func:
					check = 0
					for i in xrange(len(goal.args)):
						if isinstance(goal.args[i], Constant) and isinstance(clause.args[i], Constant) and goal.args[i].name != clause.args[i].name:
							check = 1
							break
					if check == 0:
					# case 2
						flag = 1
						yield ([clause], [goal], 2)
					else: continue
	# goal is false
	if flag == 0:	yield (None,None,-1)

def FOL_BC_OR(kb, goal, substs):
	'''
	this is a generator which will yield a Substitution
	kb:		a list of sentences from input file
	goal:	a single clause
	substs:	a dict of substitutions

	the relationships between substitutions are OR
	Yield a substitution to match the goal, there may be several different substitution
		Print 'True' when there exists a substitution
		Print 'False' when there is no substitution
	'''
	def arg_match(cargs, gargs, sub_in):
		sub = Substitution(sub_in)
		for i in xrange(len(cargs)):
			if isinstance(gargs[i], Constant) and gargs[i] != cargs[i]:
				return "Failure"
			elif isinstance(gargs[i], Variable) and not gargs[i] in sub:
				sub.add_subst(gargs[i], cargs[i])
		return sub

	old_sub, flag = substs, 0
	args = [arg if isinstance(arg, Constant) else '_' for arg in goal.args]
	for (lhs,rhs,code) in FATCH_RULE_FOR_GOAL(kb, goal):
		#undo last sub
		substs = old_sub
		print 'Ask%d: %s(%s)' % (code,goal.func, ', '.join(args))
		if code == -1:
			break
		if code == 0:
			lhs, rhs = STANDARD_VARIABLES(lhs,rhs)
			for sub_and in FOL_BC_AND(kb, lhs, UNIFY(rhs[0], goal, substs)):
				print 'True: %s0' % SUBST(sub_and, rhs[0])
				old_sub, flag = substs, 1
				yield sub_and
		elif code == 1:
			print 'True: %s1' % rhs[0]
			flag = 1
			yield substs
		elif code == 2:
		#no need for STANDARD_VARIABLES, variable already standardized
			old_sub = substs
			res = arg_match(lhs[0].args, rhs[0].args, substs)
			if res != 'Failure':
				print 'True: %s2' % SUBST(res, rhs[0])
				flag = 1
				yield res
	if flag == 0:
		print 'False: %s(%s)' % (goal.func, ', '.join(args))

def FOL_BC_AND(kb, goals, substs):
	'''
	this is a generator which will yield a Substitution
	Yield a substitution if there is a way to satisfy the goals at the same time
	Return when there is no way to satisfy the goals at the same time 

	the relationships between substitutions are AND
	'''
	if isinstance(substs,str) and substs == 'Failure':
		return
	elif len(goals) == 0:
		yield substs
	else:
		first, rest = goals[0], goals[1:]		
		this_query = SUBST(substs,first)
		for sub_or in FOL_BC_OR(kb, this_query, substs):
			for sub_and in FOL_BC_AND(kb,rest,sub_or):
				yield sub_and

def FOL_BC_ASK(kb, query):
	'''
	for each clause in query, call FOL_BC_OR()
	'''
	flag = 0
	this_query = query if isinstance(query, Sentence) else Sentence(query)
	for goal in this_query.clauses:
		for sub in FOL_BC_OR(kb,goal,Substitution()):
			flag +=1
			break
	return True if flag==len(this_query.clauses) else False


if __name__ == '__main__':
	pass