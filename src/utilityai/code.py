from utilityai.core import infer
import ast
import traceback
import time
import keyword
from typing import Optional

class InputData:
    def __init__(self, function_name="", input_names=None, output_names=None, input_types=None, output_types=None, description="", test_cases=None):
        self.function_name = function_name
        self.input_names = input_names if input_names is not None else []
        self.output_names = output_names if output_names is not None else []
        self.input_types = input_types if input_types is not None else []
        self.output_types = output_types if output_types is not None else []
        self.description = description
        self.test_cases = test_cases if test_cases is not None else []

    @staticmethod
    def get_input(prompt, type_fn):
        while True:
            try:
                return type_fn(input(prompt))
            except ValueError:
                print(f"Invalid input. Please enter a valid {type_fn.__name__}")

    @staticmethod
    def get_value(prompt, var_type):
        while True:
            value = input(prompt)
            try:
                if var_type == "int":
                    return int(value)
                elif var_type == "float":
                    return float(value)
                elif var_type == "str":
                    return value
                elif var_type == "bool":
                    return ast.literal_eval(value.capitalize())
                elif var_type == "list":
                    return ast.literal_eval(value)
                elif var_type == "dict":
                    return ast.literal_eval(value)
                elif var_type == "tuple":
                    return ast.literal_eval(value)
                else:
                    print(f"Unsupported type {var_type}")
            except (ValueError, SyntaxError):
                print(f"Invalid value for type {var_type}")

    def __call__(self):
        while True:
            function_name = input('Enter the function name: ')
            if function_name.isidentifier() and not keyword.iskeyword(function_name):
                self.function_name = function_name
                break
            else:
                print("Invalid function name")

        num_input = self.get_input('Number of input variables: ', int)
        for i in range(num_input):
            while True:
                if num_input == 1:
                    input_name = input(f'Name of input: ')
                else:
                    input_name = input(f'Name of input {i+1}: ')
                if input_name.isidentifier() and not keyword.iskeyword(input_name):
                    self.input_names.append(input_name)
                    break
                else:
                    print("Invalid input name")
            while True:
                input_type = input(f'Type of input {input_name} (int, float, str, bool, list, dict, tuple): ')
                if input_type in ["int", "float", "str", "bool", "list", "dict", "tuple"]:
                    self.input_types.append(input_type)
                    break
                else:
                    print("Invalid input type, please enter one of: int, float, str, bool, list, dict, tuple")
        
        num_output = self.get_input('Number of output variables: ', int)
        for i in range(num_output):
            while True:
                if num_output == 1:
                    output_name = input(f'Name of output: ')
                else:
                    output_name = input(f'Name of output {i+1}: ')
                if output_name.isidentifier() and not keyword.iskeyword(output_name):
                    self.output_names.append(output_name)
                    break
                else:
                    print("Invalid output name")
            while True:
                output_type = input(f'Type of output {output_name} (int, float, str, bool, list, dict, tuple): ')
                if output_type in ["int", "float", "str", "bool", "list", "dict", "tuple"]:
                    self.output_types.append(output_type)
                    break
                else:
                    print("Invalid output type, please enter one of: int, float, str, bool, list, dict, tuple")

        self.description = input('Describe the function: ')
        
        num_cases = self.get_input('Number of test cases: ', int)
        for i in range(num_cases):
            case_current = {'inputs': [], 'outputs': []}
            inputs = []
            outputs = []
            for j, input_name in enumerate(self.input_names):
                inputs.append(self.get_value(f'Value of input {input_name} ({self.input_types[j]}): ', self.input_types[j]))
            for j, output_name in enumerate(self.output_names):
                outputs.append(self.get_value(f'Value of output {output_name} ({self.output_types[j]}): ', self.output_types[j]))
            case_current['inputs'] = inputs
            case_current['outputs'] = outputs
            self.test_cases.append(case_current)

    def set_data(self, function_name, input_names, output_names, input_types, output_types, description, test_cases):
        self.function_name = function_name
        self.input_names = input_names
        self.output_names = output_names
        self.input_types = input_types
        self.output_types = output_types
        self.description = description
        self.test_cases = test_cases
        if not self.validate_data():
            raise ValueError("Invalid data provided")

    def validate_data(self):
        if not self.function_name:
            print("Function name is missing")
            return False
        
        if not self.function_name.isidentifier() or keyword.iskeyword(self.function_name):
            print(f"Invalid function name: {self.function_name}")
            return False

        if not self.description:
            print("Description is missing")
            return False
        
        for input_name in self.input_names:
            if not input_name.isidentifier() or keyword.iskeyword(input_name):
                print(f"Invalid input name: {input_name}")
                return False
            
        for output_name in self.output_names:
            if not output_name.isidentifier() or keyword.iskeyword(output_name):
                print(f"Invalid output name: {output_name}")
                return False

        valid_types = {"int", "float", "str", "bool", "list", "dict", "tuple"}
        for input_type in self.input_types:
            if input_type not in valid_types:
                print(f"Invalid input type: {input_type}")
                return False
            
        for output_type in self.output_types:
            if output_type not in valid_types:
                print(f"Invalid output type: {output_type}")
                return False

        for case in self.test_cases:
            if 'inputs' not in case or 'outputs' not in case:
                print(f"Test case missing 'inputs' or 'outputs' key: {case}")
                return False
            if not isinstance(case['inputs'], list) or not isinstance(case['outputs'], list):
                print(f"Invalid format for test case inputs/outputs: {case}")
                return False
            if len(case['inputs']) != len(self.input_names):
                print(f"Mismatch in number of inputs for case: {case}")
                return False
            if len(case['outputs']) != len(self.output_names):
                print(f"Mismatch in number of outputs for case: {case}")
                return False
            for input_value, input_type in zip(case['inputs'], self.input_types):
                if not self.is_valid_type(input_value, input_type):
                    print(f"Invalid input value: {input_value} for expected type {input_type}")
                    return False
            for output_value, output_type in zip(case['outputs'], self.output_types):
                if not self.is_valid_type(output_value, output_type):
                    print(f"Invalid output value: {output_value} for expected type {output_type}")
                    return False
        return True

    @staticmethod
    def is_valid_type(value, var_type):
        try:
            return isinstance(value, eval(var_type))
        except (ValueError, SyntaxError):
            return False

class CodeGenerationResult:
    def __init__(self):
        self.num_iterations = 0
        self.success = False
        self.final_function_code = None
        self.responses = []
        self.results = []
        self.comment = None
    
    def add_response(self, response, result):
        self.responses.append(response)
        self.results.append(result)
    
    def set_final_result(self, final_function_code):
        self.final_function_code = final_function_code
        self.success = True
    
    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        return (f'Code Generation Result:\n'
                f'Number of tries: {self.num_iterations}\n'
                f'Status: {status}\n'
                f'Final Function Code:\n{self.final_function_code}')

def function(data: InputData, result: Optional[CodeGenerationResult] = None, max_tries: int = 5, verbose: int = 1, option: Optional[int] = None) -> CodeGenerationResult:
    if not isinstance(max_tries, int):
        raise TypeError("max_tries must be an integer")
    if not isinstance(verbose, int) or verbose not in {0, 1, 2}:
        raise ValueError("verbose must be an integer either 0, 1, or 2")
    if not isinstance(data, InputData):
        raise TypeError("data must be an instance of InputData class")
    if not data.validate_data():
        raise ValueError("Invalid data provided")
    if result:
        if not isinstance(result, CodeGenerationResult):
            raise TypeError("result must be an instance of CodeGenerationResult class")
        else:
            result.num_iterations = 0
            result.success = False
            result.final_function_code = None

    def extract_python_code(input_string):
        start_index = input_string.rfind("```python")
        end_index = input_string.find("```", start_index + 1)
        if start_index != -1 and end_index != -1:
            return input_string[start_index + 9:end_index].strip()
        return input_string.strip()

    if not result:
        result = CodeGenerationResult()

    inputs_str = ', '.join([f'{data.input_names[i]}: {data.input_types[i]}' for i in range(len(data.input_names))])
    outputs_def_str = ', '.join([data.output_types[i] for i in range(len(data.output_names))])
    if len(data.output_names) > 1:
        outputs_def_str = f'tuple[{outputs_def_str}]'
    outputs_ret_str = ', '.join([data.output_names[i] for i in range(len(data.output_names))])

    while not result.success and result.num_iterations < max_tries:

        result.num_iterations += 1
        if verbose == 1:
            print()
            print(f'Try {result.num_iterations}: ', end='', flush=True)
        elif verbose == 2:
            print()
            print(f'Try {result.num_iterations}: ', flush=True)

        introduction = f"""
Write a python function named {data.function_name}
input(s): {inputs_str}
output(s): {outputs_ret_str}: {outputs_def_str}

Explanation: {data.description}
"""
        introduction += "\nExamples: \n"
        for c in data.test_cases:
                introduction += ', '.join([f'{data.input_names[i]} = {c["inputs"][i]}' for i in range(len(data.input_names))]) + ' --> ' + ', '.join([f'{data.output_names[i]} = {c["outputs"][i]}' for i in range(len(data.output_names))]) + '\n'
        
        instructions = f"""
Your reponse MUST be the FINAL CORRECT function and not a comment or other code.
Do NOT give any print or example in your response.
{time.time()}
Your FINAL CORRECT function definition MUST look like this (use the same function, input(s), and output(s) names as given in the following format):
```python
import ... # if needed
def {data.function_name}({inputs_str}) -> {outputs_def_str}:
    # your code here
    return {outputs_ret_str}
```
"""
        
        conv = []
        memory = 1
        if result.responses and result.results:
            current = [introduction, None]
            for i in range(max(0, len(result.responses)-memory), len(result.responses)):
                n_chars = int(1000*4/(memory+1))
                if len(result.responses[i]) > n_chars:
                    shortened = result.responses[i][:int(n_chars/2)] + result.responses[i][-int(n_chars/2):]
                    current[1] = "```python\n" + shortened + '\n```\n'
                else:
                    current[1] = "```python\n" + result.responses[i] + '\n```\n'
                conv.append(tuple(current))
                s = """
With this result(s): 
                """
                for j in range(len(data.test_cases)):
                    s += result.results[i][j] + '\n'
                current = [s, None]
            s = """
With this result(s):
            """
            for j in range(len(data.test_cases)):
                s += result.results[-1][j] + '\n'
            s += "Fix it and Give ONE FINAL CORRECT function definition.\n"
            if result.comment:
                s += result.comment + "\n"
                result.comment = None
            s += instructions
            current = (s, None)
            conv.append(current)
        else:
            conv.append((introduction + instructions,None))

        raw_response = infer(conv, verbose=1 if verbose==2 else 0, option=option)
        code_response = extract_python_code(raw_response)

        try:
            exec_response = code_response.replace(data.function_name,'func')
            exec(exec_response, globals())
            
            if verbose == 2:
                print()
                print('Evaluating test cases')
            all_passed = True
            num_passed = 0
            cases_results = []
            for ind, c in enumerate(data.test_cases):
                try:
                    func_args = [c['inputs'][i] for i in range(len(data.input_names))]
                    if len(data.output_names) == 1:
                        run_r = [func(*func_args)]
                    else:
                        run_r = list(func(*func_args))

                except KeyError as ke:
                    run_r = [traceback.format_exception_only(type(ke), ke)[-1]] * len(data.output_names)
                except Exception as e:
                    run_r = [traceback.format_exception_only(type(e), e)[-1]] * len(data.output_names)

                outcome = 'Passed'

                for i in range(len(data.output_names)):
                    if c['outputs'][i] != run_r[i]:
                        outcome = 'Not passed'
                        all_passed = False
                        break
                    num_passed += 1
                if verbose == 2:
                    print(f'Test case {ind+1}: {outcome}')

                cases_results.append(', '.join([f'{data.input_names[i]} = {c["inputs"][i]}' for i in range(len(data.input_names))]) +
                            ' --> ' + ', '.join([f'{data.output_names[i]} = {run_r[i]} (desired: {c["outputs"][i]})' if c['outputs'][i] != run_r[i] else f'{data.output_names[i]} = {run_r[i]}' for i in range(len(data.output_names))]) +
                            f': {outcome}') 
            
            if verbose == 1:
                print(f'{num_passed} / {len(data.test_cases)} test cases passed')
            result.add_response([], cases_results)
            result.responses[-1] = code_response

            if all_passed:
                result.set_final_result(code_response)
                if verbose != 0:
                    print('\nSuccess!')
                    print(f'Your function:\n{code_response}')

        except KeyError as ke:
            if verbose == 2:
                print()
                print('Function is not valid')
            result.add_response([], [traceback.format_exception_only(type(ke), ke)[-1]] + [""]*(len(data.test_cases)-1))
            result.responses[-1] = code_response
        except Exception as e:
            if verbose == 2:
                print()
                print('Function is not valid')
            result.add_response([], [traceback.format_exception_only(type(e), e)[-1]] + [""]*(len(data.test_cases)-1))
            result.responses[-1] = code_response

    return result
