import sys, os, random
sys.path.append('../../')
from file_compare import file_compare
# from game_space import gamespace

fname = 'sample'
test_names = ['JinfengPan']
current_path = os.path.dirname(__file__)

def main():
	for test_num in xrange(6,8):
		# run my code
		os.popen('python ..\\HW2.py -i .\\testcases\\%s%02d.txt' % (fname,test_num))
		my_output_file = '.\\output.txt'
		# run others code
		for name in test_names:
			os.chdir('.\\%s' % name)
			os.popen('python .\\hw2cs561s16.py -i ..\\testcases\\%s%02d.txt'% (fname,test_num))
			os.chdir('..')

		#compare my output with others
		for name in test_names:
			his_output_file = '%s\\output.txt' % name
		file_compare(my_output_file, his_output_file, '(%s%02d.txt) of '% (fname,test_num) + name + ' -- Compare results')

main()
