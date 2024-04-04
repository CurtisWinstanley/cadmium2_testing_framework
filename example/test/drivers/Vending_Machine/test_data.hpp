
#ifndef TEST_DATA_Vending_Machine
#define TEST_DATA_Vending_Machine
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
    std::vector<std::tuple<double, VariantType>> i_beverage_selection_1; 
    i_beverage_selection_1.push_back(std::make_tuple(0, item_selection_t(2.5, 1)));
    tc1["i_beverage_selection"] = i_beverage_selection_1;
    std::vector<std::tuple<double, VariantType>> i_money_1; 
    i_money_1.push_back(std::make_tuple(1, float(3.0)));
    tc1["i_money"] = i_money_1;

    //Test Case: 2 Input Data ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc2;
    std::vector<std::tuple<double, VariantType>> i_beverage_selection_2; 
    i_beverage_selection_2.push_back(std::make_tuple(0, item_selection_t(3.5, 2)));
    tc2["i_beverage_selection"] = i_beverage_selection_2;
    std::vector<std::tuple<double, VariantType>> i_money_2; 
    i_money_2.push_back(std::make_tuple(1, float(2.0)));
    i_money_2.push_back(std::make_tuple(2, float(1.0)));
    tc2["i_money"] = i_money_2;

    //Test Case: 3 Input Data ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<double, VariantType>>> tc3;
    std::vector<std::tuple<double, VariantType>> i_beverage_selection_3; 
    i_beverage_selection_3.push_back(std::make_tuple(0, item_selection_t(1.0, 3)));
    tc3["i_beverage_selection"] = i_beverage_selection_3;
    std::vector<std::tuple<double, VariantType>> i_money_3; 
    i_money_3.push_back(std::make_tuple(1, float(1.0)));
    tc3["i_money"] = i_money_3;

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
    std::vector<std::tuple<int, VariantType>> o_change_1_eo; 
    o_change_1_eo.push_back(std::make_tuple(11, float(0.5)));
    eo1["o_change"] = o_change_1_eo;
    std::vector<std::tuple<int, VariantType>> o_dispense_id_1_eo; 
    o_dispense_id_1_eo.push_back(std::make_tuple(16, int(1)));
    eo1["o_dispense_id"] = o_dispense_id_1_eo;

    //Test Case: 2 Expected Outputs ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo2;
    std::vector<std::tuple<int, VariantType>> o_change_2_eo; 
    o_change_2_eo.push_back(std::make_tuple(12, float(0.5)));
    eo2["o_change"] = o_change_2_eo;
    std::vector<std::tuple<int, VariantType>> o_dispense_id_2_eo; 
    o_dispense_id_2_eo.push_back(std::make_tuple(17, int(2)));
    eo2["o_dispense_id"] = o_dispense_id_2_eo;

    //Test Case: 3 Expected Outputs ---------------------------------------------------------
    std::map<std::string, std::vector<std::tuple<int, VariantType>>> eo3;
    std::vector<std::tuple<int, VariantType>> o_change_3_eo; 
    o_change_3_eo.push_back(std::make_tuple(11, float(0.0)));
    eo3["o_change"] = o_change_3_eo;
    std::vector<std::tuple<int, VariantType>> o_dispense_id_3_eo; 
    o_dispense_id_3_eo.push_back(std::make_tuple(16, int(3)));
    eo3["o_dispense_id"] = o_dispense_id_3_eo;

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
    std::vector<std::string> Vending_Machine_st_1 = {"WAIT_FOR_SELECTION", "COLLECT_CURRENCY", "CHECK_AMOUNT", "OUTPUT_CHANGE", "DISPENSE_BEVERAGE", "WAIT_FOR_SELECTION"};
    std::map<std::string, std::vector<std::string>> test_paths_tc1;
    test_paths_tc1["Vending_Machine"] = Vending_Machine_st_1;

    //Test Case: 2 State Transitions ---------------------------------------------------------
    std::vector<std::string> Vending_Machine_st_2 = {"WAIT_FOR_SELECTION", "COLLECT_CURRENCY", "CHECK_AMOUNT", "COLLECT_CURRENCY", "CHECK_AMOUNT", "OUTPUT_CHANGE", "DISPENSE_BEVERAGE", "WAIT_FOR_SELECTION"};
    std::map<std::string, std::vector<std::string>> test_paths_tc2;
    test_paths_tc2["Vending_Machine"] = Vending_Machine_st_2;

    //Test Case: 3 State Transitions ---------------------------------------------------------
    std::vector<std::string> Vending_Machine_st_3 = {"WAIT_FOR_SELECTION", "COLLECT_CURRENCY", "CHECK_AMOUNT", "OUTPUT_CHANGE", "DISPENSE_BEVERAGE", "WAIT_FOR_SELECTION"};
    std::map<std::string, std::vector<std::string>> test_paths_tc3;
    test_paths_tc3["Vending_Machine"] = Vending_Machine_st_3;

    std::map<int, std::map<std::string, std::vector<std::string>>> path_data;
    path_data[1] = test_paths_tc1;
    path_data[2] = test_paths_tc2;
    path_data[3] = test_paths_tc3;
    return path_data;
}
int get_test_set_size()
{
    return 3;
}
#endif;
