import sys
import copy


class KBRule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs


class Atomic(object):
    def __init__(self, sentence):
        self.operation = sentence.split('(')[0]
        self.args = sentence.split('(')[1].replace(')', '').strip().split(', ')

    def get_sentence(self):
        res = self.operation + '('
        for index in range(len(self.args) - 1):
            res += str(self.args[index]) + ', '
        res += str(self.args[-1])
        res += ')'
        return res


def get_kb_rule(s):
    clauses = s.split(' => ')
    rhs = Atomic(clauses[-1].strip())

    if len(clauses) > 1:
        lhs_atomics = clauses[0].strip().split(' && ')
    else:
        lhs_atomics = []
    lhs = []
    for a in lhs_atomics:
        lhs.append(Atomic(a))
    return KBRule(lhs, rhs)


def subst(theta, s):
    for index in range(len(s.args)):
        while s.args[index] in theta:
            s.args[index] = theta.get(s.args[index])
    return s


def is_variable(args):
    return isinstance(args, str) and args[0].islower()


def is_compound(args):
    return '(' in args


def is_list(args):
    return isinstance(args, list)


def standardize_vars(s):
    global variable_index
    vars_dict = {}
    for index in range(len(s.rhs.args)):
        arg = s.rhs.args[index]
        if is_variable(arg):
            new_arg_index = variable_index + 1
            new_arg = 'a' + str(new_arg_index)
            vars_dict[arg] = new_arg
            s.rhs.args[index] = new_arg
            variable_index = new_arg_index
    for sen in s.lhs:
        for index in range(len(sen.args)):
            arg = sen.args[index]
            if is_variable(arg):
                if arg in vars_dict:
                    sen.args[index] = vars_dict[arg]
                else:
                    new_arg_index = variable_index + 1
                    new_arg = 'a' + str(new_arg_index)
                    vars_dict[arg] = new_arg
                    sen.args[index] = new_arg
                    variable_index = new_arg_index
    return s


def unify(x, y, theta):
    if theta is None:
        return None
    if x == y:
        return theta
    if is_variable(x):
        return unify_var(x, y, theta)
    elif is_variable(y):
        return unify_var(y, x, theta)
    elif is_compound(x) and is_compound(y):
        return unify(Atomic(x).args, Atomic(y).args, unify(Atomic(x).operation, Atomic(y).operation, theta))
    elif is_list(x) and is_list(y):
        if len(x) != len(y):
            return None
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return None


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta.get(var), x, theta)
    elif x in theta:
        return unify(var, theta.get(x), theta)
    elif occur_check(var, x):
        return None
    else:
        return extend(theta, var, x)


def occur_check(var, x):
    if var == x:
        return True
    elif is_compound(x):
        return Atomic(var).operation == Atomic(x).operation or occur_check(var, Atomic(x).args)
    elif not isinstance(x, str) and is_list(x):
        for xi in x:
            if occur_check(var, xi):
                return True
    return False


def extend(theta, var, val):
    theta2 = theta.copy()
    theta2[var] = val
    return theta2


def fetch_rules_for_goal(kb, goal):
    fetch_kb = []
    for s in kb:
        flag_fetch = True
        if s.rhs.operation != goal.operation:
            continue
        rule_args = s.rhs.args
        goal_args = goal.args
        if len(rule_args) != len(goal_args):
            continue
        for index in range(len(rule_args)):
            if not is_variable(goal_args[index]) and not is_variable(rule_args[index]) and goal_args[index] != \
                    rule_args[index]:
                flag_fetch = False
                break
        if flag_fetch:
            fetch_kb.append(s)
    return fetch_kb


def print_rule(s):
    args = s.args
    for index in range(len(args)):
        if is_variable(args[index]):
            args[index] = '_'
    return s


def fol_bc_ask(kb, goal):
    return fol_bc_or(kb, goal, {})


def fol_bc_or(kb, goal, theta):
    fetch_kb = fetch_rules_for_goal(kb, goal)
    ask_query = print_rule(copy.deepcopy(goal)).get_sentence()
    if len(fetch_kb) == 0:
        output_file.write('Ask: ' + ask_query + '\n')
        output_file.write('False: ' + ask_query + '\n')
    else:
        flag_or = False
        global queries_asking
        queries_asking.add(ask_query)
        for s in fetch_kb:
            output_file.write('Ask: ' + ask_query + '\n')
            s = standardize_vars(copy.deepcopy(s))
            for theta_1 in fol_bc_and(kb, s.lhs, unify(s.rhs.get_sentence(), copy.deepcopy(goal.get_sentence()),
                                                       copy.deepcopy(theta))):
                flag_or = True
                queries_asking.discard(ask_query)
                output_file.write('True: ' + print_rule(subst(theta_1, copy.deepcopy(goal))).get_sentence() + '\n')
                yield theta_1
        if flag_or is False:
            queries_asking.discard(ask_query)
            output_file.write('False: ' + ask_query + '\n')


def fol_bc_and(kb, goals, theta):
    if theta is None:
        return
    elif len(goals) == 0:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        subst_first = subst(theta, copy.deepcopy(first))
        for theta_1 in fol_bc_or(kb, subst_first, copy.deepcopy(theta)):
            for theta_2 in fol_bc_and(kb, copy.deepcopy(rest), copy.deepcopy(theta_1)):
                yield theta_2


variable_index = -1
queries_asking = set()
# input_file = open('sample03_3.txt', 'rU')
input_file = open(sys.argv[2], 'rU')
output_file = open('output.txt', 'w')
queries = input_file.readline().strip()
KB_num = int(input_file.readline().strip())
KB = []
for num in range(KB_num):
    rule = input_file.readline().strip()
    KB.append(get_kb_rule(rule))

flag_result = False
for query in queries.split(' && '):
    flag_result = False
    goal = Atomic(query)
    for i in fol_bc_ask(KB, goal):
        flag_result = True
        break
    if flag_result is False:
        output_file.write('False')
        break
if flag_result:
    output_file.write('True')
input_file.close()
output_file.close()
