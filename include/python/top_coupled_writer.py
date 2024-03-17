import os
import re
import ast
import textwrap

# test_driver_dir = "test/drivers"

# model_name = "Mission_Initialization"

# extra_model_constructor_arguments = []

# location_of_model = "atomic_models/Mission_Initialization_c2.hpp"

# num_of_tests = 3


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



def write_top_coupled(input_ports, output_ports, num_of_tests, location_of_model, extra_model_constructor_arguments, model_name, test_driver_dir):

	# Define the initial content of the file
	cpp_code = textwrap.dedent(f"""
	#ifndef top_{model_name}_TD
	#define top_{model_name}_TD

	#include <cadmium/core/modeling/coupled.hpp>


	#include "td_helpers.hpp"
	#include "Generate.hpp"
	#include "Comparator.hpp"
	#include "Decider.hpp"

	#include <tuple>
	#include <map>
	#include <vector>
	#include <variant>
	#include <limits>
	#include <string>
	#include <cassert>
	""")
	cpp_code += f'\n'
	cpp_code += f'#include "{location_of_model}"\n'

	cpp_code += textwrap.dedent(f"""
	/**
	* @class Top_{model_name}
	* @brief Model used to organize the testing environment of the {model_name} DEVS model.
	*
	* This class is used to connect the generator and oracle model to the model under test. The code that needs to be modified for
	* anyone to use it are the port connections, the names of the models, and the test cases.
	*/
	class top_{model_name} : public Coupled {{

		public:
			/**
			* Constructor function for a Top model.
			* @param id ID of the model.
			* @param test_set_enumeration Test set number that the set_test_cases() function uses to give the input data to the generator.
			* @param log_file_name name of log file.
			*/
			top_{model_name}(const std::string& id, int test_set_enumeration, std::string log_file_name, 
								std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> generator_data,
								std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data,
								std::map<int, std::map<std::string, std::vector<std::string>>> path_data) : Coupled(id) {{
				
	""")

	for port_name, port_type in input_ports.items():
		cpp_code += f'            auto gen_{port_name}			= addComponent<Generator<{port_type}>>("gen_{port_name}", set_test_data<{port_type}>(test_set_enumeration, "{port_name}", generator_data));\n'
	cpp_code += f'\n'

	cpp_code += f'            auto model_{model_name}        	= addComponent<{model_name}>("{model_name}"\n'
	for arg in extra_model_constructor_arguments:
		cpp_code += f'          , {arg}\n'

	cpp_code += f'              );\n'

	for port_name, port_type in output_ports.items():
		cpp_code += f'            auto comp_{port_name}			= addComponent<Comparator<{port_type}>>("comp_{port_name}", set_oracle_data<{port_type}>(test_set_enumeration, "{port_name}", comparator_data));\n'
	cpp_code += f'\n'


	cpp_code += f'            auto decider				= addComponent<Decider>("decider", set_path_data(test_set_enumeration, path_data), get_number_of_conditions(comparator_data[test_set_enumeration]), log_file_name);\n'

	#generator couplings
	for port_name, port_type in input_ports.items():
		cpp_code += f'            addCoupling(gen_{port_name}->output_port, model_{model_name}->{port_name});\n'
	cpp_code += f'\n'


	#comparator couplings
	for port_name, port_type in output_ports.items():
		cpp_code += f'            addCoupling(model_{model_name}->{port_name}, comp_{port_name}->input_port);\n'
	cpp_code += f'\n'

	#decider couplings
	for port_name, port_type in output_ports.items():
		cpp_code += f'            addCoupling(comp_{port_name}->report_port, decider->report_port);\n'
	cpp_code += f'\n'

	cpp_code += textwrap.dedent(f"""
			}}

	}};

	#endif //top_{model_name}_TD
	""")

	cpp_file_name = test_driver_dir + "/" +model_name+ "/top_" + model_name + ".hpp"
	print("writing data file to :" + cpp_file_name)

	# Write the C++ code to a new file
	with open(cpp_file_name, 'w') as cpp_file:
		cpp_file.write(cpp_code)

	print(f"C++ file '{cpp_file_name}' has been generated.")