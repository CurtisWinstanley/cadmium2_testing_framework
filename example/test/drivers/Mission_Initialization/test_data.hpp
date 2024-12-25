
#ifndef TEST_DATA_Mission_Initialization
#define TEST_DATA_Mission_Initialization
#include <iostream>
#include <vector>
#include <tuple>
#include <map>
#include <string>
#include <variant>


//seek the Variant Goblin to find your variants...
#include "VariantGoblin.hpp"
    //---------------------------------------------------------
    //Test Case Data   ---------------------------------------------------------
    //---------------------------------------------------------
std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> get_test_cases()
{

    //Test Case: 1 Input Data ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc1;
    std::vector<std::tuple<double, VariantType>> i_start_supervisor_1; 
    i_start_supervisor_1.push_back(std::make_tuple(1, message_start_supervisor_t(0, 1, 123)));
    tc1["i_start_supervisor"] = i_start_supervisor_1;

    //Test Case: 2 Input Data ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc2;
    std::vector<std::tuple<double, VariantType>> i_start_supervisor_2; 
    i_start_supervisor_2.push_back(std::make_tuple(1, message_start_supervisor_t(0, 0, 123)));
    tc2["i_start_supervisor"] = i_start_supervisor_2;

    //Test Case: 3 Input Data ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc3;
    std::vector<std::tuple<double, VariantType>> i_aircraft_state_3; 
    i_aircraft_state_3.push_back(std::make_tuple(3, message_aircraft_state_t(123456.789, 34.5678, 123.4567, 15.0, 1015.0, 90.0, 100.0)));
    tc3["i_aircraft_state"] = i_aircraft_state_3;
    std::vector<std::tuple<double, VariantType>> i_perception_status_3; 
    i_perception_status_3.push_back(std::make_tuple(2, bool(1)));
    tc3["i_perception_status"] = i_perception_status_3;
    std::vector<std::tuple<double, VariantType>> i_start_supervisor_3; 
    i_start_supervisor_3.push_back(std::make_tuple(1, message_start_supervisor_t(1, 0, 123)));
    tc3["i_start_supervisor"] = i_start_supervisor_3;

    std::map<int, std::map<std::string, std::vector<std::tuple<double, VariantType>>>> test_cases;
    test_cases[1] = tc1;
    test_cases[2] = tc2;
    test_cases[3] = tc3;
    return test_cases;
}

    //---------------------------------------------------------
    //Expected Outputs   ---------------------------------------------------------
    //---------------------------------------------------------
std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> get_comparator_data()
{

    //Test Case: 1 Expected Outputs ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo1;

    //Test Case: 2 Expected Outputs ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo2;

    //Test Case: 3 Expected Outputs ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo3;
    std::vector<std::tuple<int, VariantType>> o_request_perception_status_3_eo; 
    o_request_perception_status_3_eo.push_back(std::make_tuple(1, bool(1)));
    eo3["o_request_perception_status"] = o_request_perception_status_3_eo;
    std::vector<std::tuple<int, VariantType>> o_request_aircraft_state_3_eo; 
    o_request_aircraft_state_3_eo.push_back(std::make_tuple(3, bool(1)));
    eo3["o_request_aircraft_state"] = o_request_aircraft_state_3_eo;
    std::vector<std::tuple<int, VariantType>> o_set_mission_monitor_status_3_eo; 
    o_set_mission_monitor_status_3_eo.push_back(std::make_tuple(4, uint8_t(1)));
    eo3["o_set_mission_monitor_status"] = o_set_mission_monitor_status_3_eo;
    std::vector<std::tuple<int, VariantType>> o_start_mission_3_eo; 
    o_start_mission_3_eo.push_back(std::make_tuple(6, int(1)));
    eo3["o_start_mission"] = o_start_mission_3_eo;
    std::vector<std::tuple<int, VariantType>> o_update_gcs_3_eo; 
    o_update_gcs_3_eo.push_back(std::make_tuple(2, message_update_gcs_t("The perceptions system is ready for operation!", 1)));
    o_update_gcs_3_eo.push_back(std::make_tuple(5, message_update_gcs_t("Starting Mission in air!", 6)));
    eo3["o_update_gcs"] = o_update_gcs_3_eo;

    std::map<int, std::map<std::string, std::vector<std::tuple<int, VariantType>>>> comparator_data;
    comparator_data[1] = eo1;
    comparator_data[2] = eo2;
    comparator_data[3] = eo3;
    return comparator_data;
}

    //---------------------------------------------------------
    //Expected State Transitions   ---------------------------------------------------------
    //---------------------------------------------------------
std::map<int, std::map<std::string, std::vector<std::string>>> get_path_data()
{

    //Test Case: 1 State Transitions ---------------------------------------------------------
    std::vector<std::string> Mission_Initialization_st_1 = {"IDLE", "MISSION_STATUS", "RESUME_MISSION", "IDLE"};
    std::map<std::string, std::vector<std::string>> test_paths_tc1;
    test_paths_tc1["Mission_Initialization"] = Mission_Initialization_st_1;

    //Test Case: 2 State Transitions ---------------------------------------------------------
    std::vector<std::string> Mission_Initialization_st_2 = {"IDLE", "MISSION_STATUS", "CHECK_AUTONOMY", "IDLE"};
    std::map<std::string, std::vector<std::string>> test_paths_tc2;
    test_paths_tc2["Mission_Initialization"] = Mission_Initialization_st_2;

    //Test Case: 3 State Transitions ---------------------------------------------------------
    std::vector<std::string> Mission_Initialization_st_3 = {"IDLE", "MISSION_STATUS", "CHECK_AUTONOMY", "CHECK_PERCEPTION_SYSTEM", "OUTPUT_PERCEPTION_STATUS", "REQUEST_AIRCRAFT_STATE", "CHECK_AIRCRAFT_STATE", "OUTPUT_TAKEOFF_POSITION", "START_MISSION", "IDLE"};
    std::map<std::string, std::vector<std::string>> test_paths_tc3;
    test_paths_tc3["Mission_Initialization"] = Mission_Initialization_st_3;

    std::map<int, std::map<std::string, std::vector<std::string>>> path_data;
    path_data[1] = test_paths_tc1;
    path_data[2] = test_paths_tc2;
    path_data[3] = test_paths_tc3;
    return path_data;
}



    //---------------------------------------------------------
    //Constructor Args   ---------------------------------------------------------
    //---------------------------------------------------------
std::map<int, std::vector<VariantType>> get_constructor_data()
{
    std::vector<VariantType> Vending_Machine_ca_1 = {"stuff", 99};
    std::map<int, std::vector<VariantType>> con_args_data;
    con_args_data[1] = Vending_Machine_ca_1;
    return con_args_data;

}


int get_test_set_size()
{
    return 3;
}
#endif;
