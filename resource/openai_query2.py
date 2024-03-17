from openai import OpenAI


client = OpenAI(api_key= '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')

completion = client.chat.completions.create(
  model="gpt-4",  # Specify the model you're using; as of my last update, "gpt-4" is a good choice
  temperature=0.5,  # Low temperature to reduce randomness
  messages=[
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": """{



{
    "model_struct_types": [
        {"name": "message_start_supervisor_t", "elements": "uint8_t autonomy_armed // used to indicate that the autonomy system is ready; uint8_t mission_started //used to indicate that a mission has ALREADY began; uint32_t mission_number;"},
        {"name": "message_aircraft_state_t", "elements": "double gps_time; double lat; double lon; float alt_AGL; float alt_MSL; float hdg_Deg; double vel_Kts;"},
        {"name": "message_update_gcs_t", "elements": "std::string text; int severity;"}
    ],

    "state_variables": [
        {"name": "mission_data", "type": "message_start_supervisor_t"},
        {"name": "perception_healthy", "type": "bool"},
        {"name": "aircraft_height", "type": "double"}
    ],

    "input_ports": [
        {"name": "i_aircraft_state", "type": "message_aircraft_state_t"},
        {"name": "i_perception_status", "type": "bool"},
        {"name": "i_start_supervisor", "type": "message_start_supervisor_t"}
    ],

    "output_ports": [
        {"name": "o_request_perception_status", "type": "bool"},
        {"name": "o_request_aircraft_state", "type": "bool"},
        {"name": "o_set_mission_monitor_status", "type": "uint8_t"},
        {"name": "o_start_mission", "type": "bool"},
        {"name": "o_update_gcs", "type": "message_update_gcs_t"}
    ],

    "transitions": [
    {"currentState": "IDLE",                      "transition type": "wait for input",                "condition": "i_start_supervisor.received",                 "nextState": "MISSION_STATUS",              "state variable update": "mission_data = i_start_supervisor.value", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "MISSION_STATUS",            "transition type": "automatic after 0 seconds",     "condition": "if(mission_data.mission_started == 1)",       "nextState": "RESUME_MISSION",              "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "MISSION_STATUS",            "transition type": "automatic after 0 seconds",     "condition": "if(mission_data.mission_started == 0)",       "nextState": "CHECK_AUTONOMY",              "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "RESUME_MISSION",            "transition type": "automatic after 0 seconds",     "condition": "none",                                        "nextState": "IDLE",                        "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "CHECK_AUTONOMY",            "transition type": "automatic after 0 seconds",     "condition": "if(mission_data.autonomy_armed == 1)",        "nextState": "CHECK_PERCEPTION_SYSTEM",     "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "o_request_perception_status.send(true)"},
    {"currentState": "CHECK_AUTONOMY",            "transition type": "automatic after 0 seconds",     "condition": "if(mission_data.autonomy_armed == 0)",        "nextState": "IDLE",                        "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "CHECK_PERCEPTION_SYSTEM",   "transition type": "wait for input",                "condition": "i_perception_status.received",                "nextState": "OUTPUT_PERCEPTION_STATUS",    "state variable update": "perception_healthy = i_perception_status.value", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "OUTPUT_PERCEPTION_STATUS",  "transition type": "automatic after 0 seconds",     "condition": "none",                                        "nextState": "REQUEST_AIRCRAFT_STATUS",     "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "if(perception_healthy == true){o_update_gcs.send('The perceptions system is ready for operation!', 1)}else{o_update_gcs.send('The perceptions system is not operational!', 6)}"},
    {"currentState": "REQUEST_AIRCRAFT_STATUS",   "transition type": "automatic after 0 seconds",     "condition": "none",                                        "nextState": "CHECK_AIRCRAFT_STATE",        "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "o_request_aircraft_state.send(true)"},
    {"currentState": "CHECK_AIRCRAFT_STATE",      "transition type": "wait for input",                "condition": "i_aircraft_state.received",                   "nextState": "OUTPUT_TAKEOFF_POSITION",     "state variable update": "aircraft_height = i_aircraft_state.value.alt_AGL", "TRANSITION SPECIFIC OUTPUT:": "NO OUTPUT"},
    {"currentState": "OUTPUT_TAKEOFF_POSITION",   "transition type": "automatic after 0 seconds",     "condition": "none",                                        "nextState": "START_MISSION",               "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "o_set_mission_monitor_status.send(1) AND if(aircraft_height > 10){o_update_gcs.send('Starting Mission in air!', 6)}"},
    {"currentState": "START_MISSION",             "transition type": "automatic after 0 seconds",     "condition": "none",                                        "nextState": "IDLE",                        "state variable update": "none", "TRANSITION SPECIFIC OUTPUT:": "o_start_mission.send(true)"}
    ]
}


Above is a description of my state machine in JSON format. Can you please provide me with 3 test cases?
The input data MUST be in the form:
Input Data: {Input Port Name{(input time), [input value]}}

The expected outputs MUST be in the form:
Expected Outputs: {Ouptut Port Name{(output sequence number), [expected output]}}

And finally could you also provide the state transition path in the form of:
State Transition Path: {initial state name,...., final state name}

ALWAYS Assume that the initial state is always IDLE."""
      }
  ]
)

m = completion.choices[0].message.content #MUST BE CONTENT

message = str(m) #NEED EXPLICIT TYPE CAST
print(message)



#**************************************************************************************************#
#* GPT Response Parsing and Populating                    										  *#
#**************************************************************************************************#



# # Adjusted pattern to capture the whole "Input Data" section
# #input_data_pattern = r"Input Data: \n\{(.*?)\}\n"
# input_data_pattern = r"Input Data:[\s\S]*?\{(.*?)\}\n"

# # Adjusted pattern to capture the whole "Expected Outputs" section
# #output_data_pattern = r"Expected Outputs: \n\{(.*?)\}"
# output_data_pattern = r"Expected Outputs:[\s\S]*?\{(.*?)\}\n"

# # Pattern to capture the entire "State Transition Path" section for each test case
# #state_transition_pattern = r"State Transition Path: \n(\{.*?\})"
# state_transition_pattern = r"State Transition Path:\s*\{(.*?)\}"

# # Find all matches of the pattern
# i_matches = re.findall(input_data_pattern, message, re.DOTALL)
# o_matches = re.findall(output_data_pattern, message, re.DOTALL)
# s_matches = re.findall(state_transition_pattern, message, re.DOTALL)
# # print(i_matches)
# # print(o_matches)
# # print(s_matches)

# # Dictionary to hold the input data for each test case
# test_cases = {}
# expected_outputs = {}
# state_transitions = []

# #
# # ----------------Populates State Transitions------------------------
# #
# for i, match in enumerate(s_matches, start=1):
#     # Remove the curly brackets
#     states_str = match.strip("{}")
#     # Split the states and add double quotes to each
#     quoted_states = [f'"{state.strip()}"' for state in states_str.split(',')]
#     # Join the quoted states with commas and enclose in curly brackets
#     formatted_path = "{" + ", ".join(quoted_states) + "}"
#     print(f"Test Case {i} State Transition Path: {formatted_path}")
#     state_transitions.append(formatted_path)




# #
# # ----------------Populates Test Cases------------------------
# #
# # Process each match for the input data
# for i, match in enumerate(i_matches, start=1):
#     # Further processing to split the captured block into individual ports and their data EX: split {i_a{(0, [2])}, i_b{(1, [1, 3, 3.5])}}
#     # to i_a{(0, [2])} and i_b{(1, [1, 3, 3.5])}
#     ports_data = match.split('}, ')
#     ports = {}
#     for port_data in ports_data:
#         # Extract port name and values
#         port_name, values = port_data.split('{(') # This splits the port name and values EX: i_a{(0, [2])} to i_a and 0, [2])}
#         values = values.rstrip(')}')  # Clean up the closing characters EX: 
#         values_tuple = values.strip() # This now keeps the values as a single string

#         # Check if the port name already exists in the dictionary
#         if port_name in ports:
#             ports[port_name].append(values_tuple) # Append new values to existing list
#         else:
#             ports[port_name] = [values_tuple] # Create new entry with values in a list

#     test_cases[f"Test Case {i}"] = ports

# # Print the input data for each test case
# for test_case, ports in test_cases.items():
#     print(f"{test_case}:")
#     for port_name, values_list in ports.items():
#         for values_str in values_list:
#             # Assuming values_str is something like "0, [2]" or "1, [1, 3, 3.5]"
#             first_val, list_str = values_str.split(', ', 1)
#             first_val = first_val.rstrip(')')
#             list_vals = eval(list_str)  # Convert string list to actual list
#             print(f"  {port_name} = {first_val}, {list_vals}")



# #
# # ----------------Populates Expected Outputs------------------------
# #
# # Process each match for the input data
# for i, match in enumerate(o_matches, start=1):
#     # Further processing to split the captured block into individual ports and their data EX: split {i_a{(0, [2])}, i_b{(1, [1, 3, 3.5])}}
#     # to i_a{(0, [2])} and i_b{(1, [1, 3, 3.5])}
#     ports_data = match.split('}, ')
#     ports = {}
#     for port_data in ports_data:
#         # Extract port name and values
#         port_name, values = port_data.split('{(') # This splits the port name and values EX: i_a{(0, [2])} to i_a and 0, [2])}
#         values = values.rstrip(')}')  # Clean up the closing characters EX: 
#         values_tuple = values.strip() # This now keeps the values as a single string

#         # Check if the port name already exists in the dictionary
#         if port_name in ports:
#             ports[port_name].append(values_tuple) # Append new values to existing list
#         else:
#             ports[port_name] = [values_tuple] # Create new entry with values in a list

#     expected_outputs[f"Expected Output {i}"] = ports

# # Print the input data for each test case
# for expected_output, ports in expected_outputs.items():
#     print(f"{expected_output}:")
#     for port_name, values_list in ports.items():
#         for values_str in values_list:
#             # Assuming values_str is something like "0, [2]" or "1, [1, 3, 3.5]"
#             first_val, list_str = values_str.split(', ', 1)
#             first_val = first_val.rstrip(')')
#             list_vals = eval(list_str)  # Convert string list to actual list
#             print(f"  {port_name} = {first_val}, {list_vals}")





#example message to use so testing and developing does not have to use GPT for every run
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: \n{i_a{(0), [3]}, i_b{(1), [2]}}\n\nExpected Outputs: \n{o_x{(1), [5]}, o_y{(2), [6]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: \n{i_a{(0), [5]}, i_b{(1), [4]}}\n\nExpected Outputs: \n{o_x{(1), [9]}, o_y{(2), [20]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO}\n\nTest Case 3:\nInput Data: \n{i_a{(0), [7]}, i_b{(1), [3]}}\n\nExpected Outputs: \n{o_x{(1), [10]}, o_y{(2), [21]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\n\nInput Data:\n{i_a{(1), [2]}, i_b{(2), [3]}}\n\nExpected Outputs:\n{o_x{(1), [5]}, o_y{(2), [6]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\n\nInput Data:\n{i_a{(1), [5]}, i_b{(2), [7]}}\n\nExpected Outputs:\n{o_x{(1), [12]}, o_y{(2), [35]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\n\nInput Data:\n{i_a{(1), [10]}, i_b{(2), [20]}}\n\nExpected Outputs:\n{o_x{(1), [30]}, o_y{(2), [200]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\n\nInput Data:\n{i_a{(0), [3]}, i_b{(1), [4]}}\n\nExpected Outputs:\n{o_x{(1), [7]}, o_y{(2), [12]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\n\nInput Data:\n{i_a{(0), [5]}, i_b{(1), [6]}}\n\nExpected Outputs:\n{o_x{(1), [11]}, o_y{(2), [30]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\n\nInput Data:\n{i_a{(0), [7]}, i_b{(1), [8]}}\n\nExpected Outputs:\n{o_x{(1), [15]}, o_y{(2), [56]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: \n{i_a{(0), [2]}, i_b{(1), [3]}}\nExpected Outputs: \n{o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: \n{i_a{(0), [5]}, i_b{(1), [7]}}\nExpected Outputs: \n{o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: \n{i_a{(0), [10]}, i_b{(1), [20]}}\nExpected Outputs: \n{o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: \n{i_a{(0), [2]}, i_b{(1), [3]}}\nExpected Outputs: \n{o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: \n{i_a{(0), [5]}, i_b{(1), [7]}}\nExpected Outputs: \n{o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: \n{i_a{(0), [10]}, i_b{(1), [20]}}\nExpected Outputs: \n{o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: \n{i_a{(1), [2]}, i_b{(2), [3]}}\n\nExpected Outputs: \n{o_x{(1), [5]}, o_y{(2), [6]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: \n{i_a{(1), [5]}, i_b{(2), [7]}}\n\nExpected Outputs: \n{o_x{(1), [12]}, o_y{(2), [35]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: \n{i_a{(1), [10]}, i_b{(2), [20]}}\n\nExpected Outputs: \n{o_x{(1), [30]}, o_y{(2), [200]}}\n\nState Transition Path: \n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"

#message = "ChatCompletionMessage(content='Test Case 1:\n\nInput Data:\n{i_a{(1), [2]}, i_b{(2), [3]}}\n\nExpected Outputs:\n{o_x{(1), [5]}, o_y{(2), [6]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\n\nInput Data:\n{i_a{(1), [5]}, i_b{(2), [7]}}\n\nExpected Outputs:\n{o_x{(1), [12]}, o_y{(2), [35]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\n\nInput Data:\n{i_a{(1), [10]}, i_b{(2), [20]}}\n\nExpected Outputs:\n{o_x{(1), [30]}, o_y{(2), [200]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\n\nInput Data:\n{i_a{(0), [2]}, i_b{(1), [3]}}\n\nExpected Output:\n{o_x{(1), [5]}, o_y{(2), [6]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\n\nInput Data:\n{i_a{(0), [5]}, i_b{(1), [7]}}\n\nExpected Output:\n{o_x{(1), [12]}, o_y{(2), [35]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\n\nInput Data:\n{i_a{(0), [10]}, i_b{(1), [20]}}\n\nExpected Output:\n{o_x{(1), [30]}, o_y{(2), [200]}}\n\nState Transition Path:\n{WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"

#new change
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"
#message = "ChatCompletionMessage(content='Test Case 1:\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"

#debugging content= 'Test Case 1:\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 2:\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\n\nTest Case 3:\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}'
#debugging message= "ChatCompletionMessage(content='Test Case 1:\\nInput Data: {i_a{(1), [2]}, i_b{(2), [3]}}\\nExpected Outputs: {o_x{(1), [5]}, o_y{(2), [6]}}\\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\\n\\nTest Case 2:\\nInput Data: {i_a{(1), [5]}, i_b{(2), [7]}}\\nExpected Outputs: {o_x{(1), [12]}, o_y{(2), [35]}}\\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}\\n\\nTest Case 3:\\nInput Data: {i_a{(1), [10]}, i_b{(2), [20]}}\\nExpected Outputs: {o_x{(1), [30]}, o_y{(2), [200]}}\\nState Transition Path: {WAIT_A, WAIT_B, DO_BAR, DO_FOO, WAIT_A}', role='assistant', function_call=None, tool_calls=None)"


# **Input Data:**
# - `i_start_supervisor{(0), [autonomy_armed=1, mission_already_started=0, mission_number=789]}`
# - `i_perception_status{(1), [true]}`
# - `i_aircraft_state{(2), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=120.0]}`

# **Input Data:**
# - `i_start_supervisor{(0), [{autonomy_armed: 1, mission_already_started: 0, mission_number: 456}]}`
# - `i_perception_status{(1), [true]}`
# - `i_aircraft_state{(2), [{gps_time: 123456.789, lat: 34.5678, lon: -123.4567, alt_AGL: 15.0, alt_MSL: 1015.0, hdg_Deg: 90.0, vel_Kts: 120.0}]}`

# **Input Data:**
# - `{i_a(0), [4]}`
# - `{i_b(10), [5]}`