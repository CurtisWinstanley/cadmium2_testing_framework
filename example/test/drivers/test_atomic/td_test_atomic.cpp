// Model Under Test
#include "couple_test_atomic_td.hpp"

//cadmium headers
#include <cadmium/core/logger/csv.hpp>
#include <cadmium/core/simulation/root_coordinator.hpp>

#include <limits>
#include <filesystem>
#include <boost/filesystem.hpp>

#include "message_structures/message_start_supervisor_t.hpp"
#include "message_structures/message_aircraft_state_t"
#include "message_structures/message_update_gcs_t"

#include "Config.hpp"

//helpers
#include "td_helpers.hpp"

//Test data header
#include "test_data.hpp"

using hclock = std::chrono::high_resolution_clock;

int main() {
	std::string model_under_test_name = "test_atomic";

	int test_set_size = get_test_set_size(); //From generated tests	

	std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> t = get_test_cases(); //From generated tests

	std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> c = get_comparator_data(); //From generated tests

	std::map<int, std::map<std::string, std::vector<std::string>>> p = get_path_data(); //From generated tests


	for(int test_set_enumeration = 1; test_set_enumeration <= test_set_size; test_set_enumeration++)
	{
		std::string log_file_name = std::to_string(test_set_enumeration) + ".csv";
		std::string log_file_dir = std::string(PROJECT_DIRECTORY) + std::string("/test/simulation_results/") + model_under_test_name;										//###
		if(!std::filesystem::is_directory(log_file_dir)) //check if the directory where we put log files exists
		{
			if(!std::filesystem::is_directory(std::string(PROJECT_DIRECTORY) + std::string("/test/simulation_results")))
			{
				std::filesystem::create_directory(std::string(PROJECT_DIRECTORY) + std::string("/test/simulation_results"));
			}
			std::filesystem::create_directory(log_file_dir);
		}

		std::string log_file = log_file_dir + "/" + log_file_name;

		auto td = std::make_shared<Couple_Test_Atomic_TD>("Top_"+model_under_test_name, test_set_enumeration, log_file, t, c, p); //Instantiate the model 	//###
		
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
	}
    return 0;
}
