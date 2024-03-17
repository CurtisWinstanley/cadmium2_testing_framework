#ifndef COUPLE_ATOMIC_TEST_TD
#define COUPLE_ATOMIC_TEST_TD

#include <cadmium/core/modeling/coupled.hpp>
#include "atomic_models/test_atomic.hpp"


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

/**
 * @class Top_Test_Atomic
 * @brief Model used to organize the testing environment of a DEVS model.
 *
 * This class is used to connect the generator and oracle model to the model under test. The code that needs to be modified for
 * anyone to use it are the port connections, the names of the models, and the test cases.
 */
class Couple_Test_Atomic_TD : public Coupled {

	public:
		/**
		* Constructor function for a Top model.
		* @param id ID of the gpt model.
		* @param test_set_enumeration Test set number that the set_test_cases() function uses to give the input data to the generator.
		* @param log_file_name name of log file.
		*/
		Couple_Test_Atomic_TD(const std::string& id, int test_set_enumeration, std::string log_file_name, 
							std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> generator_data,
							std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data,
							std::map<int, std::map<std::string, std::vector<std::string>>> path_data) : Coupled(id) {
			

			auto gen_inPort_A			= addComponent<Generator<int>>("gen_inPort_A", set_test_data<int>(test_set_enumeration, "i_a", generator_data));
			auto gen_inPort_B			= addComponent<Generator<int>>("gen_inPort_B", set_test_data<int>(test_set_enumeration, "i_b", generator_data));

			auto test_atomic        	= addComponent<Test_Atomic>("test_atomic");

			auto comp_outPort_Sum		= addComponent<Comparator<int>>("comp_outPort_Sum", set_oracle_data<int>(test_set_enumeration, "o_x", comparator_data));
			auto comp_outPort_Product	= addComponent<Comparator<int>>("comp_outPort_Product", set_oracle_data<int>(test_set_enumeration, "o_y", comparator_data));

			auto decider				= addComponent<Decider>("decider", set_path_data(test_set_enumeration, path_data), get_number_of_conditions(comparator_data[test_set_enumeration]), log_file_name);


			addCoupling(gen_inPort_A->output_port, test_atomic->i_a);
			addCoupling(gen_inPort_B->output_port, test_atomic->i_b);
			addCoupling(test_atomic->o_x, comp_outPort_Sum->input_port);
			addCoupling(test_atomic->o_y, comp_outPort_Product->input_port);

			addCoupling(comp_outPort_Sum->report_port, decider->report_port);
			addCoupling(comp_outPort_Product->report_port, decider->report_port);
		}

};

#endif //COUPLE_ATOMIC_TEST_TD