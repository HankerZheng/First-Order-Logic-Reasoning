import HW2

empty_sub = HW2.Substitution()

print '========================'
print 'TEST FOR OBJECT PARSING:'
sentences = []
with open('../samples/sample05.txt') as f:
	#test for imply find
	for line in f:
		sentences.append(HW2.Sentence(line))
print sentences
inspect = sentences[2]
print isinstance(inspect,str)
print inspect
print inspect.clauses
print inspect.clauses[0].func
print inspect.clauses[0].args
print isinstance(inspect.clauses[0].args[0], HW2.Variable)
if inspect.is_imply:
	print inspect.imply[0]
	print inspect.imply[0].func
	print inspect.imply[0].args
print '========================'

'''
print 'TEST FOR VAR_CHANGE:'
test02 = HW2.Clause('A(x)')
print "HW2.Clause('A(x)').args ==", test02.args
test02.change_arg('x','z')
print "test02.change_arg('x','z'), test02.args ==",test02.args
print "test02.args ==",test02
test02.update_name()
print "test02.update_name(), test02 ==",test02
print '========================'

print 'TEST FOR STANDARD_VARIABLES:'
print "test03 = HW2.Sentence('A(x) && B(y) && C(x, z) => D(x, z)')"
test03 = HW2.Sentence('A(x) && B(y) && C(x, z) => D(x, z)')
print 'After STANDARD_VARIABLES(test03.clauses, test03.imply):'
print '  ',HW2.STANDARD_VARIABLES(test03.clauses, test03.imply)
print '========================'

print 'TEST FOR UNIFY:'
print "test04 = HW2.Clause('B(HT, y)')"
test04 = HW2.Clause('B(HT, y)')
print "test05 = HW2.Clause('C(x)')"
test05 = HW2.Clause('C(x)')
print 'After HW2.UNIFY(test03, test04, empty_sub):'
print '  ', HW2.UNIFY(test04, test05, empty_sub)
print "test04 = HW2.Clause('B(HT, y)')"
test04 = HW2.Clause('B(HT, y)')
print "test05 = HW2.Clause('B(x, You)')"
test05 = HW2.Clause('B(x, You)')
print 'After HW2.UNIFY(test04, test05, empty_sub):'
sub = HW2.UNIFY(test04, test05, empty_sub)
print '  ', sub
print '========================'

print 'TEST FOR SUBST:'
print 'HW2.SUBST(sub, test04) ==',HW2.SUBST(sub, test04)
print 'HW2.SUBST(sub, test04) ==',HW2.SUBST(sub, test05)
test06 = HW2.Clause('A(x, z)')
print "test06 = HW2.Clause('A(x, z)')"
print 'HW2.SUBST(sub, test06) ==',HW2.SUBST(sub, test06)
print '========================'

print 'TEST FOR SUBSTITUTION:'
sub = HW2.Substitution(x='A',y='B')
print sub
sub.add_subst('z','C')
print sub
'''

print '========================'
print 'FINAL TEST1:'
kb = [HW2.Sentence('F(x) && G(x) => A(x)'), HW2.Sentence('F(B)'), HW2.Sentence('G(B)')]
query = 'A(B)'
print HW2.FOL_BC_ASK(kb,query)
print '========================'


print 'FINAL TEST2:'
kb = sentences[2:]
query = sentences[0]
print HW2.FOL_BC_ASK(kb, query)


