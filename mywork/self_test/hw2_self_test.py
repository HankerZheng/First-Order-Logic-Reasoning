import sys, os, random
sys.path.append('../../')
from file_compare import file_compare
# from game_space import gamespace

fname = 'sample'
test_names = ['HongtaiCao']
jump_cases = []
current_path = os.path.dirname(__file__)

def main():
	'''
	001 ~ 005:		samples given with the instructions
	006:			Everything mixed up with query -- Traitor(Sidious) && Bully(x)
	007:			Infinite loop test with query  -- Faster(Pat, x) && Faster(Pat, Pat)
	008:			None test with query -- Bully(x)  while no "Bully" in kb
	009:			Infinite loop test with exchange position for 'Faster(x, y) && Faster(y, z) => Faster(x, z)'
	010 ~020:		Selected long output
	040 ~:			Randomized test case with kb
	'''
	for test_num in xrange(40,100):
		if test_num in jump_cases:
			continue
		# run my code
		os.popen('python ..\\HW2.py -i .\\testcases\\%s%03d.txt' % (fname,test_num))
		my_output_file = '.\\output.txt'
		# run others code
		for name in test_names:
			os.chdir('.\\%s' % name)
			os.popen('python .\\hw2cs561s16.py -i ..\\testcases\\%s%03d.txt'% (fname,test_num))
			os.chdir('..')

		#compare my output with others
		for name in test_names:
			his_output_file = '%s\\output.txt' % name
		file_compare(my_output_file, his_output_file, '(%s%03d.txt) of '% (fname,test_num) + name + ' -- Compare results')

main()
