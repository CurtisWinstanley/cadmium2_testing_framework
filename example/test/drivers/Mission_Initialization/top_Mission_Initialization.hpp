
#ifndef top_Mission_Initialization_TD
#define top_Mission_Initialization_TD

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

#include "atomic_models\Mission_Initialization_c2.hpp"

/**
* @class Top_Mission_Initialization
* @brief Model used to organize the testing environment of the Mission_Initialization DEVS model.
*
* This class is used to connect the generator and oracle model to the model under test. The code that needs to be modified for
* anyone to use it are the port connections, the names of the models, and the test cases.
*/
class top_Mission_Initialization : public Coupled {

	public:
		/**
		* Constructor function for a Top model.
		* @param id ID of the model.
		* @param test_set_enumeration Test set number that the set_test_cases() function uses to give the input data to the generator.
		* @param log_file_name name of log file.
		*/
		top_Mission_Initialization(const std::string& id, int test_set_enumeration, std::string log_file_name, 
							std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> generator_data,
							std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data,
							std::map<int, std::map<std::string, std::vector<std::string>>> path_data) : Coupled(id) {

            auto gen_i_aircraft_state			= addComponent<Generator<message_aircraft_state_t>>("gen_i_aircraft_state", set_test_data<message_aircraft_state_t>(test_set_enumeration, "i_aircraft_state", generator_data));
            auto gen_i_perception_status			= addComponent<Generator<bool>>("gen_i_perception_status", set_test_data<bool>(test_set_enumeration, "i_perception_status", generator_data));
            auto gen_i_start_supervisor			= addComponent<Generator<message_start_supervisor_t>>("gen_i_start_supervisor", set_test_data<message_start_supervisor_t>(test_set_enumeration, "i_start_supervisor", generator_data));

            auto model_Mission_Initialization        	= addComponent<Mission_Initialization>("Mission_Initialization"
              );
            auto comp_o_request_perception_status			= addComponent<Comparator<bool>>("comp_o_request_perception_status", set_oracle_data<bool>(test_set_enumeration, "o_request_perception_status", comparator_data));
            auto comp_o_request_aircraft_state			= addComponent<Comparator<bool>>("comp_o_request_aircraft_state", set_oracle_data<bool>(test_set_enumeration, "o_request_aircraft_state", comparator_data));
            auto comp_o_set_mission_monitor_status			= addComponent<Comparator<uint8_t>>("comp_o_set_mission_monitor_status", set_oracle_data<uint8_t>(test_set_enumeration, "o_set_mission_monitor_status", comparator_data));
            auto comp_o_start_mission			= addComponent<Comparator<int>>("comp_o_start_mission", set_oracle_data<int>(test_set_enumeration, "o_start_mission", comparator_data));
            auto comp_o_update_gcs			= addComponent<Comparator<message_update_gcs_t>>("comp_o_update_gcs", set_oracle_data<message_update_gcs_t>(test_set_enumeration, "o_update_gcs", comparator_data));

            auto decider				= addComponent<Decider>("decider", set_path_data(test_set_enumeration, path_data), get_number_of_conditions(comparator_data[test_set_enumeration]), log_file_name);
            addCoupling(gen_i_aircraft_state->output_port, model_Mission_Initialization->i_aircraft_state);
            addCoupling(gen_i_perception_status->output_port, model_Mission_Initialization->i_perception_status);
            addCoupling(gen_i_start_supervisor->output_port, model_Mission_Initialization->i_start_supervisor);

            addCoupling(model_Mission_Initialization->o_request_perception_status, comp_o_request_perception_status->input_port);
            addCoupling(model_Mission_Initialization->o_request_aircraft_state, comp_o_request_aircraft_state->input_port);
            addCoupling(model_Mission_Initialization->o_set_mission_monitor_status, comp_o_set_mission_monitor_status->input_port);
            addCoupling(model_Mission_Initialization->o_start_mission, comp_o_start_mission->input_port);
            addCoupling(model_Mission_Initialization->o_update_gcs, comp_o_update_gcs->input_port);

            addCoupling(comp_o_request_perception_status->report_port, decider->report_port);
            addCoupling(comp_o_request_aircraft_state->report_port, decider->report_port);
            addCoupling(comp_o_set_mission_monitor_status->report_port, decider->report_port);
            addCoupling(comp_o_start_mission->report_port, decider->report_port);
            addCoupling(comp_o_update_gcs->report_port, decider->report_port);

            addCoupling(gen_i_start_supervisor->finished_generating, decider->finished_executing_notification);
            addCoupling(gen_i_aircraft_state->finished_generating, decider->finished_executing_notification);
            addCoupling(gen_i_perception_status->finished_generating, decider->finished_executing_notification);

            ptr = decider;
		}

    void callback()
    {
      ptr->execute_test_decision();
    }
  private:
    std::shared_ptr<Decider> ptr;
};

#endif //top_Mission_Initialization_TD
