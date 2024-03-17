import os
import re
import ast
import textwrap


# extra_port_types = []
# extra_port_types.append("message_start_supervisor_t")
# extra_port_types.append("message_aircraft_state_t")
# extra_port_types.append("message_update_gcs_t")

# extra_port_type_definition_locations = []
# extra_port_type_definition_locations.append("message_structures/message_start_supervisor_t.hpp")
# extra_port_type_definition_locations.append("message_structures/message_aircraft_state_t.hpp")
# extra_port_type_definition_locations.append("message_structures/message_update_gcs_t.hpp")

def write_variant_goblin(extra_port_types, extra_port_type_definition_locations):

    # Define the initial content of the 
    cpp_code = textwrap.dedent("""
    #ifndef VARIANT_GOBLIN_HPP
    #define VARIANT_GOBLIN_HPP

    #include <iostream>
    #include <vector>
    #include <tuple>
    #include <map>
    #include <string>
    #include <variant>
    \n
    """)
    cpp_code += f'//locations of structure or class definitions that the model ports use.\n'
    cpp_code += f'//IMPORTANT: Make sure to add all of the port locations that your project uses.\n'
    for location in extra_port_type_definition_locations:
        cpp_code += f'#include "{location}"\n'

    cpp_code += f'\n'
    cpp_code += f'//This variant holds every type that the ports can output\n'   

    cpp_code += f'using VariantType = std::variant<int, double, bool, float, std::string, uint8_t, uint16_t, uint32_t\n'
    for struct in extra_port_types:
        cpp_code += f', {struct}\n'

    cpp_code += f'      >;\n' #end the variant

    cpp_code += f'#endif;'

    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    cpp_file_name = current_file_directory+"/../VariantGoblin.hpp"
    print("writing data file to :" + cpp_file_name)

    # Write the C++ code to a new file
    with open(cpp_file_name, 'w') as cpp_file:
        cpp_file.write(cpp_code)

    print(f"C++ file '{cpp_file_name}' has been generated.")