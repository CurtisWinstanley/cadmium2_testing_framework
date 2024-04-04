
#ifndef top_Vending_Machine_TD
#define top_Vending_Machine_TD

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

#include "atomic_models\Vending_Machine.hpp"

/**
* @class Top_Vending_Machine
* @brief Model used to organize the testing environment of the Vending_Machine DEVS model.
*
* This class is used to connect the generator and oracle model to the model under test. The code that needs to be modified for
* anyone to use it are the port connections, the names of the models, and the test cases.
*/
class top_Vending_Machine : public Coupled {

	public:
		/**
		* Constructor function for a Top model.
		* @param id ID of the model.
		* @param test_set_enumeration Test set number that the set_test_cases() function uses to give the input data to the generator.
		* @param log_file_name name of log file.
		*/
		top_Vending_Machine(const std::string& id, int test_set_enumeration, std::string log_file_name, 
							std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> generator_data,
							std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data,
							std::map<int, std::map<std::string, std::vector<std::string>>> path_data) : Coupled(id) {

            auto gen_i_beverage_selection			= addComponent<Generator<item_selection_t>>("gen_i_beverage_selection", set_test_data<item_selection_t>(test_set_enumeration, "i_beverage_selection", generator_data));
            auto gen_i_money			= addComponent<Generator<float>>("gen_i_money", set_test_data<float>(test_set_enumeration, "i_money", generator_data));

            auto model_Vending_Machine        	= addComponent<Vending_Machine>("Vending_Machine"
              );
            auto comp_o_change			= addComponent<Comparator<float>>("comp_o_change", set_oracle_data<float>(test_set_enumeration, "o_change", comparator_data));
            auto comp_o_dispense_id			= addComponent<Comparator<int>>("comp_o_dispense_id", set_oracle_data<int>(test_set_enumeration, "o_dispense_id", comparator_data));

            auto decider				= addComponent<Decider>("decider", set_path_data(test_set_enumeration, path_data), get_number_of_conditions(comparator_data[test_set_enumeration]), log_file_name);
            addCoupling(gen_i_beverage_selection->output_port, model_Vending_Machine->i_beverage_selection);
            addCoupling(gen_i_money->output_port, model_Vending_Machine->i_money);

            addCoupling(model_Vending_Machine->o_change, comp_o_change->input_port);
            addCoupling(model_Vending_Machine->o_dispense_id, comp_o_dispense_id->input_port);

            addCoupling(comp_o_change->report_port, decider->report_port);
            addCoupling(comp_o_dispense_id->report_port, decider->report_port);


		}

};

#endif //top_Vending_Machine_TD
