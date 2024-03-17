/**
 * 	\file		Mission_Initialization.hpp
 *	\brief		Definition of the Mission Initialization atomic model.
 *	\details	This header file defines the Mission Initialization atomic model for use in the Cadmium DEVS
				simulation software. The model represents the behaviour of the Supervisor at the beginning
				of the mission when the autonomy system is being initialized.
 *	\image		html atomic_models/mission_initialization.png
 *	\author		Tanner Trautrim
 *	\author		James Horner
 */
#ifndef MISSION_INITIALIZATION_C2_HPP
#define MISSION_INITIALIZATION_C2_HPP
#include <cadmium/core/modeling/atomic.hpp>
#include <iostream>
// C++ Standard Library Headers
#include <limits>
#include <string>

// Logging Headers
#include <LogConsole.hpp>

// Messages structures
#include "../message_structures/message_aircraft_state_t.hpp"
#include "../message_structures/message_start_supervisor_t.hpp"
#include "../message_structures/message_update_gcs_t.hpp"

// Utility functions
#include "enum_string_conversion.hpp"
//#include "constants.hpp"

using namespace cadmium;

/**
 *	\par	States
 * 	Declaration of the states of the atomic model.
 */
namespace mission_initialization{
    DEFINE_ENUM_WITH_STRING_CONVERSIONS(States,
        (IDLE)
        (MISSION_STATUS)
        (RESUME_MISSION)
        (CHECK_AUTONOMY)
        (CHECK_PERCEPTION_SYSTEM)
        (OUTPUT_PERCEPTION_STATUS)
        (REQUEST_AIRCRAFT_STATE)
        (CHECK_AIRCRAFT_STATE)
        (OUTPUT_TAKEOFF_POSITION)
        (REQUIRE_MONITORING)
        (START_MISSION)
    );
}

struct Mission_Initialization_State {
	int nInternals, nExternals, nInputs;
	double clock, sigma;
    mission_initialization::States current_state;
	Mission_Initialization_State(): nInternals(), nExternals(), nInputs(), clock(), sigma(std::numeric_limits<double>::infinity()), current_state() {}
};

std::ostream &operator << (std::ostream& os, const Mission_Initialization_State& x) {
	os << "," << x.sigma << "," << "state:" << enumToString(x.current_state) << ">";
	return os;
}


/**
 * 	\class		Mission_Initialization
 *	\brief		Definition of the Mission Initialization atomic model.
 *	\details	This class defines the Mission Initialization atomic model for use in the Cadmium DEVS
				simulation software. The model represents the behaviour of the Supervisor at the beginning
				of the mission when the autonomy system is being initialized.
 *	\image		html atomic_models/mission_initialization.png
 */
class Mission_Initialization: public Atomic<Mission_Initialization_State> {

    public:

        /// @name Input Ports
        ///@{
        Port<message_aircraft_state_t> i_aircraft_state;        /**< Port for receiving the current state of the aircraft. */
        Port<bool> i_perception_status;                         /**< Port for receiving the status of the perception system. */
        Port<message_start_supervisor_t> i_start_supervisor;    /**< Port for receiving signal to start the supervisor. */
        ///@}

        /// @name Output Ports
        ///@{
        Port<bool> o_request_perception_status;      /**< Port for requesting the current state of the perception system. */
        Port<bool> o_request_aircraft_state;         /**< Port for requesting the current aircraft state. */
        Port<uint8_t> o_set_mission_monitor_status;  /**< Port for telling the mission monitor to stop monitoring mission progress. */
        Port<int> o_start_mission;                   /**< Port for sending a notification that the mission has started. */
        Port<message_update_gcs_t> o_update_gcs;     /**< Port for sending updates to the GCS. */
        ///@}


        /**
         * @brief Constructor for Mission Initialization.
         *
         * @param id The identifier for the instance.
         */
        explicit Mission_Initialization(const std::string& id): Atomic<Mission_Initialization_State>(id, Mission_Initialization_State()) {

            i_aircraft_state =                  addInPort<message_aircraft_state_t>("i_aircraft_state");
            i_perception_status =               addInPort<bool>("i_perception_status");
            i_start_supervisor =                addInPort<message_start_supervisor_t>("i_start_supervisor");

            o_request_perception_status =       addOutPort<bool>("o_request_perception_status");
            o_request_aircraft_state =          addOutPort<bool>("o_request_aircraft_state");
            o_set_mission_monitor_status =      addOutPort<uint8_t>("o_set_mission_monitor_status");
            o_start_mission =                   addOutPort<int>("o_start_mission");
            o_update_gcs =                      addOutPort<message_update_gcs_t>("o_update_gcs");
            
            state.current_state = mission_initialization::States::IDLE; //Initial state is IDLE
        }

        using Atomic<Mission_Initialization_State>::internalTransition;
        using Atomic<Mission_Initialization_State>::externalTransition;
        using Atomic<Mission_Initialization_State>::confluentTransition;
        using Atomic<Mission_Initialization_State>::output;
        using Atomic<Mission_Initialization_State>::timeAdvance;

        const Mission_Initialization_State& getState() {
            return state;
        }

        void internalTransition(Mission_Initialization_State& s) const override {
            s.clock += s.sigma;
            switch (s.current_state) {
                case mission_initialization::States::MISSION_STATUS:
                    s.current_state = mission_data.mission_started ? mission_initialization::States::RESUME_MISSION: mission_initialization::States::CHECK_AUTONOMY;
                    break;
                case mission_initialization::States::RESUME_MISSION:
                    s.current_state = mission_initialization::States::IDLE;
                    break;
                case mission_initialization::States::CHECK_AUTONOMY:
                    s.current_state = mission_data.autonomy_armed ? mission_initialization::States::CHECK_PERCEPTION_SYSTEM: mission_initialization::States::IDLE;
                    break;
                case mission_initialization::States::OUTPUT_PERCEPTION_STATUS:
                    s.current_state = mission_initialization::States::REQUEST_AIRCRAFT_STATE;
                    break;
                case mission_initialization::States::REQUEST_AIRCRAFT_STATE:
                    s.current_state = mission_initialization::States::CHECK_AIRCRAFT_STATE;
                    break;
                case mission_initialization::States::OUTPUT_TAKEOFF_POSITION:
                    s.current_state = mission_initialization::States::START_MISSION;
                    break;
                case mission_initialization::States::START_MISSION:
                    s.current_state = mission_initialization::States::IDLE;
                    break;
                default:
                    return;
            }
        }

        void externalTransition(Mission_Initialization_State& s, double e) const override {
            s.clock += e;

            switch (s.current_state) {
                case mission_initialization::States::IDLE: {
                    //bool received_start_supervisor = !cadmium::get_messages<typename defs::i_start_supervisor>(mbs).empty();
                    bool received_start_supervisor =  !i_start_supervisor->empty();
                    if (received_start_supervisor) {
                        // Get the most recent start supervisor input (found at the back of the vector of inputs)
                        //mission_data = cadmium::get_messages<typename defs::i_start_supervisor>(mbs).back();
                        mission_data = i_start_supervisor->getBag().back();
                        s.current_state = mission_initialization::States::MISSION_STATUS;
                    }
                    break;
                }
                case mission_initialization::States::CHECK_PERCEPTION_SYSTEM: {
                    //bool received_perception_status = !cadmium::get_messages<typename defs::i_perception_status>(mbs).empty();
                    bool received_perception_status = !i_perception_status->empty();
                    if (received_perception_status) {
                        //std::vector<bool> perception_status = cadmium::get_messages<typename defs::i_perception_status>(mbs);
                        std::vector<bool> perception_status = i_perception_status->getBag();
                        perception_healthy = perception_status[0];
                        s.current_state = mission_initialization::States::OUTPUT_PERCEPTION_STATUS;
                    }
                    break;
                }
                case mission_initialization::States::CHECK_AIRCRAFT_STATE: {
                    //bool received_aircraft_state = !cadmium::get_messages<typename defs::i_aircraft_state>(mbs).empty();
                    bool received_aircraft_state = !i_aircraft_state->empty();
                    if (received_aircraft_state) {
                        //std::vector<message_aircraft_state_t> new_aircraft_state = cadmium::get_messages<typename defs::i_aircraft_state>(mbs);
                        std::vector<message_aircraft_state_t> new_aircraft_state = i_aircraft_state->getBag();
                        aircraft_height = new_aircraft_state[0].alt_AGL;
                        s.current_state = mission_initialization::States::OUTPUT_TAKEOFF_POSITION;
                    }
                    break;
                }
                default:
                    break;
            }
            return;
        }

        void output(const Mission_Initialization_State& s) const override {
            switch (s.current_state) {
                case mission_initialization::States::CHECK_AUTONOMY: {
                    if (mission_data.autonomy_armed) {
                        //cadmium::get_messages<typename defs::o_request_perception_status>(bags).emplace_back(true);
                        o_request_perception_status->addMessage(true);
                    }
                    break;
                }
                case mission_initialization::States::OUTPUT_PERCEPTION_STATUS: {
                    std::string update_text;
                    //MAV_SEVERITY MESSAGE_SEVERITY;
                    if (perception_healthy) {
                        update_text = "The perceptions system is ready for operation!";
                        //MESSAGE_SEVERITY = MAV_SEVERITY_INFO;
                        t = 1;
                    } else {
                        update_text = "The perception system is not operational!";
                        //MESSAGE_SEVERITY = MAV_SEVERITY_ALERT;
                        t = 6;
                        
                    }
                    // cadmium::get_messages<typename defs::o_update_gcs>(bags).emplace_back(
                    //         update_text,
                    //     MESSAGE_SEVERITY
                    // );
                    o_update_gcs->addMessage(message_update_gcs_t(update_text, t));
                    break;
                }
                case mission_initialization::States::REQUEST_AIRCRAFT_STATE: {
                    //cadmium::get_messages<typename defs::o_request_aircraft_state>(bags).emplace_back(true);
                    o_request_aircraft_state->addMessage(true);
                    break;
                }
                case mission_initialization::States::OUTPUT_TAKEOFF_POSITION: {
                    //cadmium::get_messages<typename defs::o_set_mission_monitor_status>(bags).emplace_back(1);
                    o_set_mission_monitor_status->addMessage(1);
                    bool in_air = aircraft_height > 10.0;

                    // Print a message to the console with a summary of the state of the mission.
                    // logging::console::get_instance().print_parallel(
                    //     std::string("Starting Supervisor with following state:") +
                    //     "\nMission Number:    " + std::to_string(mission_data.mission_number) +
                    //     "\nMission Started:   " + (mission_data.mission_started ? "True" : "False") +
                    //     "\nAutonomy:          " + (mission_data.autonomy_armed ? "Armed" : "Not armed") +
                    //     "\nPerception System: " + (perception_healthy ? "Operational" : "Not operational") +
                    //     "\nIn Air:            " + (in_air ? "True" : "On Ground"),
                    //     MODEL_PRINT_NAME,
                    //     logging::severity::info
                    // );

                    if (in_air) {
                        // cadmium::get_messages<typename defs::o_update_gcs>(bags).emplace_back(
                        //         "Starting Mission in air!",
                        //         MAV_SEVERITY_ALERT
                        // );
                        o_update_gcs->addMessage(message_update_gcs_t("Starting Mission in air!", t));
                    }
                    break;
                }
                case mission_initialization::States::START_MISSION: {
                    //cadmium::get_messages<typename defs::o_start_mission>(bags).push_back(mission_data.mission_number);
                    o_start_mission->addMessage(mission_data.mission_number);
                    break;
                }
                default:
                    break;
            }
            return;
        }


        [[nodiscard]] double timeAdvance(const Mission_Initialization_State& s) const override {
            switch (s.current_state) {
                case mission_initialization::States::IDLE:
                case mission_initialization::States::CHECK_PERCEPTION_SYSTEM:
                case mission_initialization::States::CHECK_AIRCRAFT_STATE:
                    return std::numeric_limits<double>::infinity();
                    break;
                case mission_initialization::States::MISSION_STATUS:
                case mission_initialization::States::RESUME_MISSION:
                case mission_initialization::States::CHECK_AUTONOMY:
                case mission_initialization::States::OUTPUT_PERCEPTION_STATUS:
                case mission_initialization::States::REQUEST_AIRCRAFT_STATE:
                case mission_initialization::States::OUTPUT_TAKEOFF_POSITION:
                case mission_initialization::States::START_MISSION:
                    return 0;
                    break;
                default:
                    //assert(false && "Unhandled time advance");
                    break;
            }
            return s.sigma;
        }


    //
    private:
        /// Constant name of the model to use in printing to the console.
        const static inline std::string MODEL_PRINT_NAME = "Mission Initialization";
        /// Variable for storing the startup data about the mission.
        mutable message_start_supervisor_t mission_data;
        /// Variable for storing whether the perception system is healthy or not.
        mutable bool perception_healthy;
        /// Variable for storing the height of the aircraft in ft AGL to determine if the aircraft is starting on the ground.
        mutable double aircraft_height;

        mutable int t = 1; //TEMPORARY
};
#endif //MISSION_INITIALIZATION_HPP