add_executable(td_test_atomic									"test_atomic/td_test_atomic.cpp")

target_include_directories(td_test_atomic                       PUBLIC ${includes_list})
target_link_libraries(td_test_atomic               				${Boost_LIBRARIES})

add_executable(td_Mission_Initialization						"Mission_Initialization/td_Mission_Initialization.cpp")

target_include_directories(td_Mission_Initialization                       PUBLIC ${includes_list})
target_link_libraries(td_Mission_Initialization               				${Boost_LIBRARIES})


