from utilityai_2.chat import message
from utilityai_2.code import InputData, function

# # message and ask anything
# message("how to transpose a pytorch tensor?")

# # chat and have a conversation
# r1, c1 = message("why does mutable and immutable mean")
# print()
# print("-------------- next message --------------")
# print()
# message("give some examples", c1)

# # chat about a function
# def list_sum(numbers):
#     return sum(numbers)
# r1, c1 = message("what does this do?", attachment=list_sum)
# print()
# print("-------------- next message --------------")
# print()
# message("return min and max of numbers too", c1)

# # chat about a numpy array
# import numpy as np
# array = np.array([[1, 2, 3, 4], 
#                   [5, 6, 7, 8], 
#                   [9, 10, 11, 12]])
# r1, c1 = message("each row is salaries of a person. how to get average salary of each person in an array", attachment=array)
# print()
# print("-------------- next message --------------")
# print()
# message("what about age?", c1)

# # chat about a pandas dataframe
# import pandas as pd
# data = {
#     'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
#     'Age': [24, 27, 22, 32, 29],
#     'Salary': [50000, 54000, 49000, 62000, 58000],
#     'Department': ['HR', 'Engineering', 'Marketing', 'Finance', 'Engineering'],
#     'Joining Date': pd.to_datetime(['2020-01-15', '2019-06-23', '2021-03-01', '2018-11-15', '2020-08-30'])
# }
# df = pd.DataFrame(data)
# r1, c1 = message("write code to get average of salary", attachment=df)
# print()
# print("-------------- next message --------------")
# print()
# message("how to get average salary of each department?", c1)

# # chat about a pytorch tensor
# import torch
# tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
# r1, c1 = message("how to transpose this tensor", attachment=tensor)
# print()
# print("-------------- next message --------------")
# print()
# message("how to get the size of the resulting tensor", c1)

# # function generation in an interactive way. Calling data() and then give function info.
# data = InputData()
# data()
# function(data)

# # function generation by setting data in the code
# data = InputData()
# data_dict = {
#     'function_name': 'prime_number_checker',
#     'input_names': ['num'],
#     'input_types': ['int'],
#     'output_names': ['is_prime'],
#     'output_types': ['bool'],
#     'description': "function that checks if a given number is a prime number",
#     'test_cases': [
#         {'inputs': [5], 'outputs': [True]},
#         {'inputs': [10], 'outputs': [False]},
#         {'inputs': [17], 'outputs': [True]}
#     ]
# }
# data.set_data(data_dict['function_name'], data_dict['input_names'], data_dict['output_names'], data_dict['input_types'], data_dict['output_types'], data_dict['description'], data_dict['test_cases'])
# function(data)

# # function generation by giving comment on the result
# data = InputData()
# data_dict = {
#     'function_name': 'vague_function',
#     'input_names': ['a', 'b'],
#     'input_types': ['int', 'int'],
#     'output_names': ['subtract'],
#     'output_types': ['int'],
#     'description': "function that subtracts two numbers",
#     'test_cases': [
#         {'inputs': [1,2], 'outputs': [1]}
#     ]
# }
# data.set_data(data_dict['function_name'], data_dict['input_names'], data_dict['output_names'], data_dict['input_types'], data_dict['output_types'], data_dict['description'], data_dict['test_cases'])
# res = function(data, max_tries=1)
# print()
# print("-------------- comment --------------")
# print()
# res.comment = "actually the smaller number must be subtracted from the larger one"
# function(data, res)