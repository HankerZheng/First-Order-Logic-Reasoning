#coding=utf-8
# 用Python比较两个文件
# 如果相同返回0

def file_compare(file_name1, file_name2, info):
    def cmpstr(str1, str2):
        col = 0
        for c1, c2 in zip(str1, str2):
            if c1 == c2:
                col += 1
                continue
            else :
                break

        if c1 != c2 or len(str1) != len(str2):
            return col+1
        else :
            return 0

    file1 = open(file_name1,'r')
    file2 = open(file_name2,'r')

    fa = file1.readlines()
    fb = file2.readlines()
    file1.close()
    file2.close()

    str1 = ''
    str2 = ''

    #用GBK解码，这样可以处理中文字符
    fa = [ str.decode("gbk") for str in fa]
    fb = [ str.decode("gbk") for str in fb]

    row = 0
    col = 0

    #学习Python上玩蛇网 www.iplaypython.com！
    #开始比较内容
    for str1, str2 in zip(fa, fb):
        col = cmpstr(str1,str2)
        # col=0则说明两行相等
        if col == 0 :
            row += 1
            continue
        else:
            break

    #如果有一行不同，或者文件长度不一样
    print info+':'
    if str1 != str2 or len(fa) != len(fb):
        #打印出不同的行序和列序，并把不同的前一句后本句打印出来
        #最后两个字符是不同的地方
        print "\trow:", row+1, "col:", col
        print "\t%s is:\n\t\t%s\n\t\t%s" % (file_name1 , fa[row-1].strip(),fa[row].strip())
        print "\t%s is:\n\t\t%s\n\t\t%s" % (file_name2, fb[row-1].strip(),fb[row].strip())
        return 0
    else :
        print "\tAll are same!"
        return 1


if __name__ == '__main__':
    my_next_state = "..\\next_state.txt"
    sample_next_state = "..\\Sample\\1\\next_state.txt"

    my_traverse_log = "..\\traverse_log.txt"
    sample_traverse_log = "..\\Sample\\2\\traverse_log.txt"

    my_trace_state = "..\\trace_state.txt"
    sample_trace_state = "..\\Sample\\5\\trace_state.txt"

    file_compare(my_traverse_log, sample_traverse_log, "traverse_log")
    file_compare(my_next_state,sample_next_state,'next_state')
    file_compare(my_trace_state,sample_trace_state,'trace_state')
