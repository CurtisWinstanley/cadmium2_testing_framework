from openai import OpenAI
import os
import re
import ast
import textwrap


#**************************************************************************************************#
#* Parsing Function Definitions                    												  *#
#**************************************************************************************************#


def split_response(response):
    test_case_pattern = r"(Test Case \d+)"
    test_cases = re.split(test_case_pattern, response)[1:]

    # Since the split will separate the headers from the bodies, recombine them into complete test case strings
    test_cases = [test_cases[i] + test_cases[i + 1] for i in range(0, len(test_cases), 2)]

    #this for loop prevents chatgpt speach that has "Test Case #" from poluting the test cases. This happens if the ai thinks its being
    #clever and wants to explain each test case to you
    k = 0
    for test_case in test_cases:
        if "{" not in test_case:
            test_cases.pop(k)
        k = k + 1

    return test_cases
    
    # Print each test case to verify
    # for i, test_case in enumerate(test_cases, start=1):
    #     print(f"Test Case {i}:\n{test_case}\n")

def split_test_case(test_case):

    i_pattern = r'Input Data.*?(.*?)(?=Expected Outputs)'
    e_pattern = r'Expected Outputs.*?(.*?)(?=State Transition Path)'
    s_pattern = r'State Transition Path.*?(.*?\})'

    i_matches = re.findall(i_pattern, test_case, re.DOTALL)
    e_matches = re.findall(e_pattern, test_case, re.DOTALL)
    s_matches = re.findall(s_pattern, test_case, re.DOTALL)

    input_data_part = i_matches[0]
    expected_outputs_part = e_matches[0]
    state_transition_path_part = s_matches[0]

    # Splitting the string into parts based on the given sections
    # input_data_part = test_case.split("Input Data:")[1].split("Expected Outputs:")[0].strip()
    # expected_outputs_part = test_case.split("Expected Outputs:")[1].split("State Transition Path:")[0].strip()
    # state_transition_path_part = test_case.split("State Transition Path:")[1].strip()
    
    return input_data_part, expected_outputs_part, state_transition_path_part

def extract_data(input_data, ports):
    data_dict = {}
    extracted_data = {}
    for port_name in ports.keys():
        # This pattern matches the port name followed by any characters until it finds the opening '{',
        # then captures everything inside the curly braces. We use re.escape to escape special characters in the port name.
        pattern = re.escape(port_name) + r"\s*\{(.*?)\}"
        # Find all matches in the input data string. re.DOTALL allows '.' to match newlines as well.
        matches = re.findall(pattern, input_data, re.DOTALL)
        if matches:
            # If matches are found, add them to the dictionary under the port name key.
            extracted_data[port_name] = matches
    return extracted_data

#This function will return a dictionary that has all of the data and it will remove any useless characters
def transform_data_format(data_to_org):
    transformed_data = {}
    for port_name, entries in data_to_org.items():
        # Process each entry for the port
        transformed_entries = []
        for entry in entries:
            # Extract numbers, booleans, and strings from the string
            # This pattern matches numbers (including decimals), true/false, and strings enclosed in single quotes
            values = re.findall(r'[\d\.]+|true|false|\'[^\']+\'', entry, re.IGNORECASE)
            # Process extracted values
            formatted_values = []
            for value in values:
                if value.lower() == 'true':
                    formatted_values.append('1')
                elif value.lower() == 'false':
                    formatted_values.append('0')
                elif value.startswith("'") and value.endswith("'"):
                    # Keep the string content and enclose it in double quotes
                    formatted_values.append(f"\"{value[1:-1]}\"")
                else:
                    formatted_values.append(value)
            # Transform into the desired format
            if formatted_values:
                # Assuming the first value is always present and followed by an array of values
                transformed_entry = f"{formatted_values[0]}, [{', '.join(formatted_values[1:])}]"
                transformed_entries.append(transformed_entry)
        # Store the transformed entries
        transformed_data[port_name] = transformed_entries
    return transformed_data


#Used to get the clean the string of a state path
def format_state_path(path):
    # Using regex to extract the content inside the curly braces
    extracted_data = re.search(r'\{(.*?)\}', path)
    if extracted_data:
        # Splitting the extracted data by comma and stripping whitespace
        items = extracted_data.group(1).split(',')
        items = [item.strip() for item in items]
        # Formatting the items into the desired output format
        formatted_output = '{' + ', '.join(f'"{item}"' for item in items) + '}'
        return formatted_output
    else:
        return {}

    return formatted_path


#**************************************************************************************************#
#* GPT Response Parsing and Populating                    										  *#
#**************************************************************************************************#

def write_test_data(gpt_response, input_ports, output_ports, model_name, num_of_test_cases, test_driver_dir):

    input_datas = {} #dictionary to contain all of the input data
    expected_outputs = {} #dictionary to hold all of the expected outputs
    state_transitions = []

    test_cases = split_response(gpt_response) #split the response received from the GPT API into separate test cases

    i = 1 #basic incrementor
    for tc in test_cases:
        #get the string of each test case
        input_data, expected_output, state_transition_path = split_test_case(tc)

        #get Input data
        format_input_data = extract_data(input_data, input_ports)
        cleaned_input_data = transform_data_format(format_input_data)

        #get Output Data
        format_expected_output = extract_data(expected_output, output_ports)
        cleaned_expected_output = transform_data_format(format_expected_output)

        #get State paths
        formatted_state_path = format_state_path(state_transition_path)

        input_datas[f"Test Case {i}"] = cleaned_input_data
        expected_outputs[f"Expected Output {i}"] = cleaned_expected_output
        state_transitions.append(formatted_state_path)

        i = i + 1


    #**************************************************************************************************#
    #* Code Printing                        														  *#
    #**************************************************************************************************#

    # Define the initial content of the 
    cpp_code = textwrap.dedent(f"""
    #ifndef TEST_DATA_{model_name}
    #define TEST_DATA_{model_name}
    #include <iostream>
    #include <vector>
    #include <tuple>
    #include <map>
    #include <string>
    #include <variant>
    \n
    """)

    cpp_code += f'//seek the Variant Goblin to find your variants...\n'  
    cpp_code += f'#include "VariantGoblin.hpp"\n'


    #FIXME: Fix the variant

    cpp_code += f'    //---------------------------------------------------------\n'
    cpp_code += f'    //Test Case Data   ---------------------------------------------------------\n'
    cpp_code += f'    //---------------------------------------------------------\n'

    cpp_code += f'std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> get_test_cases()\n'
    cpp_code += f'{{\n'

    i = 1 # Incrementor for test cases
    # Now you can access and print the input data for each test case i_a and 0, [2])} to i_a and 0, [2]
    for test_case, ports in input_datas.items():
        cpp_code += f'\n'
        cpp_code += f'    //Test Case: {i} Input Data ---------------------------------------------------------\n'
        cpp_code += f'    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc{i};\n'

        for port_name, values_list in ports.items():
            cpp_code += f'    std::vector<std::tuple<double, VariantType>> {port_name}_{i}; \n'

            for values_str in values_list:
                # Remove the outer brackets and split the string into a list
                # Assuming values_str is something like "0, [2]" or "1, [1, 3, 3.5]"
                first_val, list_str = values_str.split(', ', 1)
                first_val = first_val.rstrip(')')
                # Evaluate the list part to convert it into an actual Python list
                # Note: Using eval() can be dangerous if you're not sure about the safety of the input. It's used here for simplicity.
                list_vals = ast.literal_eval(list_str)
                list_vals_str = ', '.join(map(str, list_vals))
                cpp_code += f'    {port_name}_{i}.push_back(std::make_tuple({first_val}, {input_ports[port_name]}({list_vals_str})));\n'
            cpp_code += f'    tc{i}["{port_name}"] = {port_name}_{i};\n'
        i = i + 1


    cpp_code += f'\n'
    cpp_code += f'    std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> test_cases;\n'
    for j in range(num_of_test_cases):
        cpp_code += f'    test_cases[{j+1}] = tc{j+1};\n'

    cpp_code += f'    return test_cases;\n'
    cpp_code += f'}}\n'


    cpp_code += f'\n'
    cpp_code += f'    //---------------------------------------------------------\n'
    cpp_code += f'    //Expected Outputs   ---------------------------------------------------------\n'
    cpp_code += f'    //---------------------------------------------------------\n'


    cpp_code += f'std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> get_comparator_data()\n'
    cpp_code += f'{{\n'

    i = 1 # Incrementor for expected outputs
    # Now you can access and print the input data for each test case i_a and 0, [2])} to i_a and 0, [2]
    for expected_output, ports in expected_outputs.items():
        cpp_code += f'\n'
        cpp_code += f'    //Test Case: {i} Expected Outputs ---------------------------------------------------------\n'
        cpp_code += f'    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo{i};\n'

        for port_name, values_list in ports.items():
            cpp_code += f'    std::vector<std::tuple<int, VariantType>> {port_name}_{i}_eo; \n'

            for values_str in values_list:
                # Remove the outer brackets and split the string into a list
                # Assuming values_str is something like "0, [2]" or "1, [1, 3, 3.5]"
                first_val, list_str = values_str.split(', ', 1)
                first_val = first_val.rstrip(')')
                # Evaluate the list part to convert it into an actual Python list
                # Note: Using eval() can be dangerous if you're not sure about the safety of the input. It's used here for simplicity.
                list_vals = ast.literal_eval(list_str)
                list_vals_str = ', '.join(f'"{item}"' if isinstance(item, str) else str(item) for item in list_vals)
                cpp_code += f'    {port_name}_{i}_eo.push_back(std::make_tuple({first_val}, {output_ports[port_name]}({list_vals_str})));\n'
            cpp_code += f'    eo{i}["{port_name}"] = {port_name}_{i}_eo;\n'
        i = i + 1


    cpp_code += f'\n'
    cpp_code += f'    std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data;\n'
    for k in range(num_of_test_cases):
        cpp_code += f'    comparator_data[{k+1}] = eo{k+1};\n'

    cpp_code += f'    return comparator_data;\n'
    cpp_code += f'}}\n'

    cpp_code += f'\n'
    cpp_code += f'    //---------------------------------------------------------\n'
    cpp_code += f'    //Expected State Transitions   ---------------------------------------------------------\n'
    cpp_code += f'    //---------------------------------------------------------\n'


    cpp_code += f'std::map<int, std::map<std::string, std::vector<std::string>>> get_path_data()\n'
    cpp_code += f'{{\n'

    i = 1 # Incrementor for test cases
    for st in state_transitions:
        cpp_code += f'\n'
        cpp_code += f'    //Test Case: {i} State Transitions ---------------------------------------------------------\n'
        cpp_code += f'    std::vector<std::string> {model_name}_st_{i} = {st};\n'

        cpp_code += f'    std::map<std::string, std::vector<std::string>> test_paths_tc{i};\n'
        cpp_code += f'    test_paths_tc{i}["{model_name}"] = {model_name}_st_{i};\n'
        i = i + 1


    cpp_code += f'\n'
    cpp_code += f'    std::map<int, std::map<std::string, std::vector<std::string>>> path_data;\n'
    for l in range(num_of_test_cases):
        cpp_code += f'    path_data[{l+1}] = test_paths_tc{l+1};\n'

    cpp_code += f'    return path_data;\n'
    cpp_code += f'}}\n'


    cpp_code += f'int get_test_set_size()\n'
    cpp_code += f'{{\n'
    cpp_code += f'    return {num_of_test_cases};\n'
    cpp_code += f'}}\n'


    cpp_code += f'#endif;\n'




    #TODO: Make sure there is a way to check if the directory is there


    # Specify the name of the C++ file to create
    hpp_file_name = test_driver_dir + "/" + model_name + "/test_data.hpp"
    print("writing data file to :" + hpp_file_name)

    # Write the C++ code to a new file
    with open(hpp_file_name, 'w') as hpp_file:
        hpp_file.write(cpp_code)

    print(f"C++ file '{hpp_file_name}' has been generated.")