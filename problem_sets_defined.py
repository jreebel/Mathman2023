""" Define the available problem sets """
cur_problem_set = None
problem_sets = []

easy_add_set = {'name': 'Easy Addition', 'ix':0, 'descrs': ['1+1', '2+2', '2+1'],
                'answers': ['2', '4', '3']}
problem_sets.append(easy_add_set)

medium_add_set = {'name': 'Medium Addition', 'ix':1, 'descrs': ['5+6', '8+2', '4+9'],
                  'answers': ['13', '10', '13']}
problem_sets.append(medium_add_set)
