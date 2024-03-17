import os
import re
import ast
import textwrap



# test_driver_dir = "test/drivers"

# model_name = "Mission_Initialization"

# num_of_tests = 3


def write_test_driver(test_driver_dir, model_name, num_of_tests):

	# Define the initial content of the 
	cpp_code = textwrap.dedent(f"""
	// Model Under Test
	#include "top_{model_name}.hpp"
	""")

	cpp_code += textwrap.dedent(f"""
	//cadmium headers
	#include <cadmium/core/logger/csv.hpp>
	#include <cadmium/core/simulation/root_coordinator.hpp>

	//c++ headers
	#include <limits>
	#include <filesystem>

	//helpers
	#include "td_helpers.hpp"

	//Test data header
	#include "test_data.hpp"
	""")

	cpp_code += textwrap.dedent(f"""
	using hclock = std::chrono::high_resolution_clock;

	int main() {{
		std::string model_under_test_name = "{model_name}";

		int test_set_size = get_test_set_size(); //From generated tests	

		std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> t = get_test_cases(); //From generated tests

		std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> c = get_comparator_data(); //From generated tests

		std::map<int, std::map<std::string, std::vector<std::string>>> p = get_path_data(); //From generated tests


		for(int test_set_enumeration = 1; test_set_enumeration <= test_set_size; test_set_enumeration++)
		{{
			std::string log_file_name = std::to_string(test_set_enumeration) + ".csv";
			std::string log_file_dir = "../simulation_results";
			if(!std::filesystem::is_directory(log_file_dir)) //check if the directory where we put log files exists
			{{
				std::filesystem::create_directory(log_file_dir);
			}}
			log_file_dir = log_file_dir + std::string("/") + std::string("{model_name}");
			if(!std::filesystem::is_directory(log_file_dir))
			{{
				std::filesystem::create_directory(log_file_dir);
			}}
			std::string log_file = log_file_dir + "/" + log_file_name;

			auto td = std::make_shared<top_{model_name}>("Top_"+model_under_test_name, test_set_enumeration, log_file, t, c, p);
			
			auto rootCoordinator = cadmium::RootCoordinator(td);
			auto logger = std::make_shared<cadmium::CSVLogger>(log_file_dir+ std::string("/") +log_file_name, ";"); //initialize logger
			rootCoordinator.setLogger(logger);

			auto start = hclock::now(); //to measure simulation execution time

			rootCoordinator.start(); //start the coordinator to begin simulation
			rootCoordinator.simulate(std::numeric_limits<double>::infinity());
			rootCoordinator.stop();

			auto elapsed = std::chrono::duration_cast<std::chrono::duration<double, std::ratio<1>>>(hclock::now() - start).count();
			std::cout<< "Simulation test case " + std::to_string(test_set_enumeration) + " took: " + std::to_string(elapsed) + " seconds"<< std::endl;
			std::cout<<  "TD: " << model_under_test_name <<std::endl;
			std::cout<<"-------------------------------"<<std::endl;
		}}
		return 0;
	}}

	""")



	#TODO: Make sure there is a way to check if the directory is there
	#TODO: add the variant type to the generated files

	# Specify the name of the C++ file to create

	cpp_file_name = test_driver_dir + "/" +model_name+ "/td_" + model_name + ".cpp"
	print("writing data file to :" + cpp_file_name)

	# Write the C++ code to a new file
	with open(cpp_file_name, 'w') as cpp_file:
		cpp_file.write(cpp_code)

	print(f"C++ file '{cpp_file_name}' has been generated.")

