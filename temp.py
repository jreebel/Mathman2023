""" Define the available problem sets """
cur_problem_set = []

easy_add_set = {'name': 'Easy Addition', 'ix':0, 'descrs': ['1+1', '2+2', '2+1'],
                'answers': ['2', '4', '3']}
cur_problem_set.append(easy_add_set)
medium_add_set = {'name': 'Medium Addition', 'ix':1, 'descrs': ['5+6', '8+2', '4+9'],
                  'answers': ['13', '10', '13']}
cur_problem_set.append(medium_add_set)

for prob_set in cur_problem_set:
    print(prob_set['name'])

print(cur_problem_set)
