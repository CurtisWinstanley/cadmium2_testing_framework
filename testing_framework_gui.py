import os
import re
import ast
import sys
import tkinter as tk
import json

sys.path.append('include/python')
#python files in include/python
import cadmium2_driver_writer
import top_coupled_writer
import variant_goblin_writer
import test_data_writer
import openai_query



test_str = """### Test Case 1: Mission Already Started

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=1, mission_number=123]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, RESUME_MISSION, IDLE}`

---

### Test Case 2: Mission Not Started, Autonomy Not Armed

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=0, mission_already_started=0, mission_number=123]}`

#### Expected Outputs:
- No outputs as per the transitions specified.

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, IDLE}`

---

### Test Case 3: Mission Not Started, Autonomy Armed, Perception System Healthy, Aircraft State Received

#### Input Data:
- `i_start_supervisor{(1), [autonomy_armed=1, mission_already_started=0, mission_number=123]}`
- `i_perception_status{(2), [true]}`
- `i_aircraft_state{(3), [gps_time=123456.789, lat=34.5678, lon=-123.4567, alt_AGL=15.0, alt_MSL=1015.0, hdg_Deg=90.0, vel_Kts=100.0]}`

#### Expected Outputs:
- `o_request_perception_status{(1), [true]}`
- `o_update_gcs{(2), ['The perceptions system is ready for operation!', 1]}`
- `o_request_aircraft_state{(3), [true]}`
- `o_set_mission_monitor_status{(4), [1]}`
- `o_update_gcs{(5), ['Starting Mission in air!', 6]}`
- `o_start_mission{(6), [true]}`

#### State Transition Path:
- `{IDLE, MISSION_STATUS, CHECK_AUTONOMY, CHECK_PERCEPTION_SYSTEM, OUTPUT_PERCEPTION_STATUS, REQUEST_AIRCRAFT_STATE, CHECK_AIRCRAFT_STATE, OUTPUT_TAKEOFF_POSITION, START_MISSION, IDLE}`"""





# #**************************************************************************************************#
# #* Model Information                    														  *#
# #**************************************************************************************************#


# test_driver_dir = "test/drivers"

# model_name = "Mission_Initialization"

# num_of_tests = 3




# extra_model_constructor_arguments = []

# location_of_model = "atomic_models/Mission_Initialization_c2.hpp"

# input_ports = {} # Contains the names and types of the input ports

# input_ports['i_start_supervisor'] = 'message_start_supervisor_t'
# input_ports['i_perception_status'] = 'bool'
# input_ports['i_aircraft_state'] = 'message_aircraft_state_t'

# output_ports = {} # Contains the names and types of the output ports

# output_ports['o_request_perception_status'] = 'bool'
# output_ports['o_request_aircraft_state'] = 'bool'
# output_ports['o_start_mission'] = 'int'
# output_ports['o_set_mission_monitor_status'] = 'uint8_t'
# output_ports['o_update_gcs'] = 'message_update_gcs_t'




# extra_port_types = []
# extra_port_types.append("message_start_supervisor_t")
# extra_port_types.append("message_aircraft_state_t")
# extra_port_types.append("message_update_gcs_t")

# extra_port_type_definition_locations = []
# extra_port_type_definition_locations.append("message_structures/message_start_supervisor_t.hpp")
# extra_port_type_definition_locations.append("message_structures/message_aircraft_state_t.hpp")
# extra_port_type_definition_locations.append("message_structures/message_update_gcs_t.hpp")


# input_ports = {} # Contains the names and types of the input ports
# # input_ports['i_a'] = 'int'
# # input_ports['i_b'] = 'int'
# input_ports['i_start_supervisor'] = 'message_start_supervisor_t'
# input_ports['i_perception_status'] = 'bool'
# input_ports['i_aircraft_state'] = 'message_aircraft_state_t'

# output_ports = {} # Contains the names and types of the output ports
# # output_ports['o_x'] = 'int'
# # output_ports['o_y'] = 'int'
# output_ports['o_request_perception_status'] = 'bool'
# output_ports['o_request_aircraft_state'] = 'bool'
# output_ports['o_start_mission'] = 'int'
# output_ports['o_set_mission_monitor_status'] = 'uint8_t'
# output_ports['o_update_gcs'] = 'message_update_gcs_t'

# extra_port_types = []
# extra_port_types.append("message_start_supervisor_t")
# extra_port_types.append("message_aircraft_state_t")
# extra_port_types.append("message_update_gcs_t")




#cadmium2_driver_writer.write_test_driver(test_driver_dir, model_name, num_of_tests)
#top_coupled_writer.write_top_coupled(input_ports, output_ports, num_of_tests, location_of_model, extra_model_constructor_arguments, model_name, test_driver_dir)
#variant_goblin_writer.write_variant_goblin(extra_port_types, extra_port_type_definition_locations)
#test_data_writer.write_test_data(test_str, input_ports, output_ports, model_name, num_of_tests, test_driver_dir)
#openai_query.query_gpt()


#**************************************************************************************************#
#* GUI Functions                        														  *#
#**************************************************************************************************#



##For Testing GUI: C:\Users\curti\repositories\_Fall2023\cadmium2_testing_framework\example\test\drivers
##For Testing GUI: C:\Users\curti\repositories\_Fall2023\cadmium2_testing_framework\example\atomic_models\Vending_Machine.hpp
##For Testing GUI: atomic_models\Vending_Machine.hpp
##For Testing GUI: Vending_Machine
##For Testing GUI: *No Constructor args*
##For Testing GUI: 3
##For Testing GUI: C:\Users\curti\repositories\_Fall2023\cadmium2_testing_framework\example\json\vending_machine.json

#
#
#TODO: Make it fix model args, make it so we can custom includes to the top coupled incase model arguments come from external sources
def generate_tests():
    #Gather all of the necessary variables from the GUI

    test_driver_directory = str(test_driver_directory_entry.get()) #absolute path to the directory

    location_of_model = str(location_of_model_entry.get()) #relative path (based off of how you configured directory management)

    model_relative_directory = str(relative_directory_model_start_entry.get())

    model_name = str(model_name_entry.get())

    model_args_str = str(extra_model_constructor_arguments_entry.get())

    num_of_tests = int(num_of_tests_entry.get())

    model_json = str(model_json_location_entry.get())

    gpt_flag = checkbox_var.get()

    #first validate any directorys we will be writing to OR we check for valitidty.
    if os.path.isdir(test_driver_directory):
        print("The test driver directory exists!")
    else:
        print("ERROR: The test driver directory you entered does not exist.")
        return

    if os.path.isfile(model_json):
        print("The model JSON exists!")
    else:
        print("ERROR: The JSON file you provided does not exist, you may need to provide its absolute path.")
        return

    if os.path.isfile(location_of_model):
        print("The model location exists!")
    else:
        print("WARNING: Your Model does not exist, your tests may not compile")

    #now lets parse our JSON and get the input_ports and output_ports
    input_ports, output_ports = parse_model_json(model_json)

    with open(model_json, 'r') as file:
        model_description = file.read()

    #now get any extra constructor arguments that may be important
    model_args = model_args_str.split(';') #FIXME:
    #print("SIZE--------------------------------------" + str(len(model_args)))

    #START GENERATING

    cadmium2_driver_writer.write_test_driver(test_driver_directory, model_name, num_of_tests)

    if(model_args_str == ''):
        top_coupled_writer.write_top_coupled(input_ports, output_ports, num_of_tests, model_relative_directory, [], model_name, test_driver_directory)
    else:
        top_coupled_writer.write_top_coupled(input_ports, output_ports, num_of_tests, model_relative_directory, model_args, model_name, test_driver_directory)

    #Now we must check if the user wants chatgpt to generate some test cases or not
    if(gpt_flag ==1):
        gpt_response = openai_query.query_gpt(model_description) #get the response from chat gpt
        test_data_writer.write_test_data(gpt_response, input_ports, output_ports, model_name, num_of_tests, test_driver_directory) #create the test cases
    else:
        test_data_writer.write_test_data("", input_ports, output_ports, model_name, num_of_tests, test_driver_directory)

#
#
#
def parse_model_json(model_file):
    with open(model_file, 'r') as file:
        data = json.load(file)

    # Initialize an empty dictionary for input_ports
    input_ports = {}

    # Iterate through each item in the output_ports list and populate the dictionary
    for port in data['input_ports']:
        input_ports[port['name']] = port['type']

    

    # Initialize an empty dictionary for output_ports
    output_ports = {}

    # Iterate through each item in the output_ports list and populate the dictionary
    for port in data['output_ports']:
        output_ports[port['name']] = port['type']


    # Print the result to verify
    print(input_ports)
    print(output_ports)

    return input_ports, output_ports




##For testing GUI: C:\Users\curti\repositories\_Fall2023\cadmium_v2_test\example\message_structures
##For testing GUI: message_update_gcs_t.hpp;message_aircraft_state_t.hpp;message_start_supervisor_t.hpp
##For testing GUI: message_update_gcs_t;message_aircraft_state_t;essage_start_supervisor_t
##For testing GUI: message_structures
#
#
#
def variant_goblin_button_handler():
    #gets the folder location containing all data types. It is an absolute path to check that the files exist
    extra_port_type_definition_location_str = str(location_entry_box.get()) #gets the folder location containing all data types

    data_struture_file_names_str = str(data_struture_file_names_entry.get())

    extra_port_types_str = str(structure_names.get()) #gets the struct names

    relative_directory_start_str = str(relative_directory_start_entry.get())

    #tell the user incase they forgot to add their data types
    if(len(extra_port_type_definition_location_str) == 0 or len(extra_port_types_str) == 0):
        print("WARNING: One or more of the entry boxes are empty.")

    if(len(extra_port_type_definition_location_str) == 0 and len(extra_port_types_str) != 0):
        print("ERROR: Your model uses custom data structure but you did not specify the location of said data types")
        return
    
    if(len(extra_port_type_definition_location_str) == 0 and len(data_struture_file_names_str) != 0):
        print("ERROR: You have the files names for your data types but no folder directory where they exist")
        return

    extra_port_types = extra_port_types_str.split(';')
    data_struture_file_names = data_struture_file_names_str.split(';') #has the name for each file
    data_structure_files = [] #will have the absolute path for each data structure file

    for file in data_struture_file_names:
        data_structure_files.append(extra_port_type_definition_location_str + "/" +file)

    for file_path in data_structure_files:
        if os.path.isfile(file_path):
            print(f"The file '{file_path}' exists.")
        else:
            print(f"ERROR: The file '{file_path}' does not exist.")
            return
    
    relative_dirs_to_include = []
    for file in data_struture_file_names:
        relative_dirs_to_include.append(relative_directory_start_str + "/" + file)

    print(relative_dirs_to_include)
    #create the variant goblin file to store all possiable data types for the cadmium project
    variant_goblin_writer.write_variant_goblin(extra_port_types, relative_dirs_to_include)




#**************************************************************************************************#
#* GUI Config                              														  *#
#**************************************************************************************************#

# Create the main window
root = tk.Tk()
root.title("Cadmium 2 Testing Framework")

# Configure the grid layout (each column will have the same weight)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

#----------------------------------VARIANT GOBLIN PART
variant_goblin_label = tk.Label(root, text="----------Variant Goblin Information:----------")
variant_goblin_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

##### Location Label
data_location = tk.Label(root, text="Location of Port Data Structures:")
data_location.grid(row=1, column=0, sticky="w")  # Align to the west (left)

# Entry Box
location_entry_box = tk.Entry(root)
location_entry_box.grid(row=1, column=1)

# Button
variant_write_button = tk.Button(root, text="Generate Variant Goblin", command=variant_goblin_button_handler)
variant_write_button.grid(row=1, column=2, sticky="e")  # Align to the east (right)


##### Data Structure File Names
data_struture_file_names = tk.Label(root, text="Data Structure File Names:\n(use ';' to separate names)")
data_struture_file_names.grid(row=2, column=0, sticky="w")  # Align to the west (left)

# Entry Box
data_struture_file_names_entry = tk.Entry(root)
data_struture_file_names_entry.grid(row=2, column=1)


##### Data Structure Name label
data_struture_names = tk.Label(root, text="Data Structure Names:\n(use ';' to separate names)")
data_struture_names.grid(row=3, column=0, sticky="w")  # Align to the west (left)

# Entry Box
structure_names = tk.Entry(root)
structure_names.grid(row=3, column=1)

##### Relative Directory Start label
relative_directory_start = tk.Label(root, text="Data Structures Relative Include Directory")
relative_directory_start.grid(row=4, column=0, sticky="w")  # Align to the west (left)

# Entry Box
relative_directory_start_entry = tk.Entry(root)
relative_directory_start_entry.grid(row=4, column=1)
#----------------------------------END
#----------------------------------TEST DRIVER PART
test_driver_label = tk.Label(root, text="----------Test Drivers Information:----------")
test_driver_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))

##### Test Driver Directory Label
test_driver_directory = tk.Label(root, text="Directory to Store Test Files:\n(Test Driver Dir)")
test_driver_directory.grid(row=6, column=0, sticky="w")  # Align to the west (left)

# Entry Box
test_driver_directory_entry = tk.Entry(root)
test_driver_directory_entry.grid(row=6, column=1)

# Button
test_write_button = tk.Button(root, text="Generate Test Driver", command=generate_tests)
test_write_button.grid(row=6, column=2, sticky="e")  # Align to the east (right)


##### Location of Model Label
location_of_model = tk.Label(root, text="Model Full Directory:")
location_of_model.grid(row=7, column=0, sticky="w")  # Align to the west (left)

# Entry Box
location_of_model_entry = tk.Entry(root)
location_of_model_entry.grid(row=7, column=1)


##### Relative Directory Model Start label
relative_directory_model_start = tk.Label(root, text="Model Relative Include Directory:")
relative_directory_model_start.grid(row=8, column=0, sticky="w")  # Align to the west (left)

# Entry Box
relative_directory_model_start_entry = tk.Entry(root)
relative_directory_model_start_entry.grid(row=8, column=1)


##### Model Name Label
model_name = tk.Label(root, text="Model Name:")
model_name.grid(row=9, column=0, sticky="w")  # Align to the west (left)

# Entry Box
model_name_entry = tk.Entry(root)
model_name_entry.grid(row=9, column=1)



##### Extra Model Arguments Label
extra_model_constructor_arguments = tk.Label(root, text="Model Constructor Arguments:\n(use ';' to separate args)")
extra_model_constructor_arguments.grid(row=10, column=0, sticky="w")  # Align to the west (left)

# Entry Box
extra_model_constructor_arguments_entry = tk.Entry(root)
extra_model_constructor_arguments_entry.grid(row=10, column=1)


##### Num of Tests Label
num_of_tests = tk.Label(root, text="Number of Tests:")
num_of_tests.grid(row=11, column=0, sticky="w")  # Align to the west (left)

# Entry Box
num_of_tests_entry = tk.Entry(root)
num_of_tests_entry.grid(row=11, column=1)


##### Model JSON Location Label
model_json_location = tk.Label(root, text="Model JSON:")
model_json_location.grid(row=12, column=0, sticky="w")  # Align to the west (left)

# Entry Box
model_json_location_entry = tk.Entry(root)
model_json_location_entry.grid(row=12, column=1)


##### Checkbox Variable
checkbox_var = tk.IntVar()

# Checkbox
generate_tests_checkbox = tk.Checkbutton(root, variable=checkbox_var)
generate_tests_checkbox.grid(row=13, column=1)

# Greeting Label
generate_tests_checkbox_label = tk.Label(root, text="Use ChatGPT to Generate Tests Data:")
generate_tests_checkbox_label.grid(row=13, column=0)


# Start the GUI event loop
root.mainloop()