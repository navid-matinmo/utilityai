# utilityai

This package brings language model capabilities into the coding environment, providing a variety of functionalities such as:

- Message and ask anything
- Chat and have a conversation
- Chat about a function
- Chat about a numpy array
- Chat about a pandas dataframe
- Chat about a pytorch tensor
- Generate a function interactively
- Generate a function by setting data within the code
- Generate a function and provide a comment on the result for guided generation

Function generation feature iteratively builds and refines functions by evaluating them against predefined test cases.

## install

```
pip install utilityai
```

## quick start

Download the model once after installation
```
from utilityai.model import download
download()
```

Message and ask anything
```
from utilityai.chat import message
message("How do you transpose a PyTorch tensor?");
```
![Message and ask anything](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/1.gif)

Chat and have a conversation
```
from utilityai.chat import message
r1, c1 = message("What do mutable and immutable mean?")
message("Give more examples.", c1);
```
![Chat and have a conversation](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/2.gif)

Chat about a function
```
from utilityai.chat import message
def list_sum(numbers):
    return sum(numbers)
r1, c1 = message("What does this do?", attachment=list_sum)
message("Return the minimum and maximum values of the numbers instead.", c1);
```
![Chat about a function](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/3.gif)


Chat about a numpy array
```
from utilityai.chat import message
import numpy as np
array = np.array([[1, 2, 3, 4], 
                  [5, 6, 7, 8], 
                  [9, 10, 11, 12]])
r1, c1 = message("Each row represents the salary of a person. How do I calculate the average salary of each person in another array?", attachment=array)
message("How do I calculate the average salary of these people for each year in an array?", c1);
```
![Chat about a numpy array](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/4.gif)

Chat about a pandas dataframe
```
from utilityai.chat import message
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
message("How to calculate the average salary for each department?", c1);
```
![Chat about a pandas dataframe](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/5.gif)

Chat about a pytorch tensor
```
from utilityai.chat import message
import torch
tensor = torch.tensor([[1, 2, 3], [4, 5, 6]])
r1, c1 = message("How to transpose this tensor?", attachment=tensor)
message("How to determine the size of the resulting tensor?", c1);
```
![Chat about a pytorch tensor](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/6.gif)

Generate a function interactively by calling data() first, then provide function information
```
from utilityai.code import InputData, function
data = InputData()
data()
function(data);
```
![Generate a function interactively by calling data() first, then provide function information](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/7.gif)

Generate a function by setting data within the code
```
from utilityai.code import InputData, function
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
function(data);
```
![Generate a function by setting data within the code](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/8.gif)

Generate a function and provide a comment on the result for guided generation
```
from utilityai.code import InputData, function
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
res.comment = "A function that subtracts the smaller number from the larger one."
function(data, res);
```
![Generate a function and provide a comment on the result for guided generation](https://raw.githubusercontent.com/navid-matinmo/utilityai/main/assets/9.gif)