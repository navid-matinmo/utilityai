from utilityai.chat import message
from utilityai.code import InputData, function
from utilityai.model import download

print("************************************************************")
print("Download the model once after installation")
print("************************************************************")
download()

print("************************************************************")
print("Message and ask anything")
print("************************************************************")
message("How do you transpose a PyTorch tensor?")

print("************************************************************")
print("Chat and have a conversation")
print("************************************************************")
r1, c1 = message("What do mutable and immutable mean?")
print()
print("-------------- next message --------------")
print()
message("Give some examples.", c1)

print("************************************************************")
print("Chat about a function")
print("************************************************************")
def list_sum(numbers):
    return sum(numbers)
r1, c1 = message("What does this do?", attachment=list_sum)
print()
print("-------------- next message --------------")
print()
message("Return the minimum and maximum of numbers as well.", c1)

print("************************************************************")
print("Chat about a numpy array")
print("************************************************************")
import numpy as np
array = np.array([[1, 2, 3, 4], 
                  [5, 6, 7, 8], 
                  [9, 10, 11, 12]])
r1, c1 = message("Each row represents the salary of a person. How do I calculate the average salary of each person in an array?", attachment=array)
print()
print("-------------- next message --------------")
print()
message("How do I calculate the average salary of these people for each year in an array?", c1)

print("************************************************************")
print("Chat about a pandas dataframe")
print("************************************************************")
import pandas as pd
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 22, 32, 29],
    'Salary': [50000, 54000, 49000, 62000, 58000],
    'Department': ['HR', 'Engineering', 'Marketing', 'Finance', 'Engineering'],
    'Joining Date': pd.to_datetime(['2020-01-15', '2019-06-23', '2021-03-01', '2018-11-15', '2020-08-30'])
}
df = pd.DataFrame(data)
r1, c1 = message("How to calculate the average salary?", attachment=df)
print()
print("-------------- next message --------------")
print()
message("How to calculate the average salary for each department?", c1)

print("************************************************************")
print("Chat about a pytorch tensor")
print("************************************************************")
import torch
tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
r1, c1 = message("How to transpose this tensor?", attachment=tensor)
print()
print("-------------- next message --------------")
print()
message("How to determine the size of the resulting tensor?", c1)

print("************************************************************")
print("Generate a function interactively by calling data() first, then provide function information")
print("************************************************************")
data = InputData()
data()
function(data)

print("************************************************************")
print("Generate a function by setting data within the code")
print("************************************************************")
data = InputData()
data_dict = {
    'function_name': 'prime_number_checker',
    'input_names': ['num'],
    'input_types': ['int'],
    'output_names': ['is_prime'],
    'output_types': ['bool'],
    'description': "A function to check if a given number is prime.",
    'test_cases': [
        {'inputs': [5], 'outputs': [True]},
        {'inputs': [10], 'outputs': [False]},
        {'inputs': [17], 'outputs': [True]}
    ]
}
data.set_data(data_dict['function_name'], data_dict['input_names'], data_dict['output_names'], data_dict['input_types'], data_dict['output_types'], data_dict['description'], data_dict['test_cases'])
function(data)

print("************************************************************")
print("Generate a function and provide a comment on the result for guided generation")
print("************************************************************")
data = InputData()
data_dict = {
    'function_name': 'vague_function',
    'input_names': ['a', 'b'],
    'input_types': ['int', 'int'],
    'output_names': ['subtract'],
    'output_types': ['int'],
    'description': "A function to subtract two numbers.",
    'test_cases': [
        {'inputs': [1,2], 'outputs': [1]}
    ]
}
data.set_data(data_dict['function_name'], data_dict['input_names'], data_dict['output_names'], data_dict['input_types'], data_dict['output_types'], data_dict['description'], data_dict['test_cases'])
res = function(data, max_tries=1)
print()
print("-------------- comment --------------")
print()
res.comment = "A function that subtracts the smaller number from the larger one."
function(data, res)
