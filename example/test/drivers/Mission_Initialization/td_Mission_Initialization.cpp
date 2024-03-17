
// Model Under Test
#include "top_Mission_Initialization.hpp"

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

using hclock = std::chrono::high_resolution_clock;

int main() {
	std::string model_under_test_name = "Mission_Initialization";

	int test_set_size = get_test_set_size(); //From generated tests	

	std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> t = get_test_cases(); //From generated tests

	std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> c = get_comparator_data(); //From generated tests

	std::map<int, std::map<std::string, std::vector<std::string>>> p = get_path_data(); //From generated tests


	for(int test_set_enumeration = 1; test_set_enumeration <= test_set_size; test_set_enumeration++)
	{
		std::string log_file_name = std::to_string(test_set_enumeration) + ".csv";
		std::string log_file_dir = "../simulation_results";
		if(!std::filesystem::is_directory(log_file_dir)) //check if the directory where we put log files exists
		{
			std::filesystem::create_directory(log_file_dir);
		}
		log_file_dir = log_file_dir + std::string("/") + std::string("Mission_Initialization");
		if(!std::filesystem::is_directory(log_file_dir))
		{
			std::filesystem::create_directory(log_file_dir);
		}
		std::string log_file = log_file_dir + "/" + log_file_name;

		auto td = std::make_shared<top_Mission_Initialization>("Top_"+model_under_test_name, test_set_enumeration, log_file, t, c, p);

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

