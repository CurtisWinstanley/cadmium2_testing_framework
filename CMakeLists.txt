cmake_minimum_required(VERSION 3.20 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

project(cadmium_v2_test)

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/include/Config.hpp.in" "${CMAKE_CURRENT_SOURCE_DIR}/include/Config.hpp")
set(CMAKE_TOOLCHAIN_FILE C:/Program Files/vcpkg/scripts/buildsystems/vcpkg.cmake CACHE STRING "")
# Boost
# Enables thread pools
add_compile_definitions(BOOST_THREAD_PROVIDES_FUTURE_CONTINUATION)
add_compile_definitions(BOOST_THREAD_PROVIDES_EXECUTORS)
add_compile_definitions(BOOST_THREAD_USES_MOVE)

# Ignore min/max macros
add_compile_definitions(NOMINMAX)

##########################
###  Dependency Setup  ###
##########################
include(deps/cadmium2.cmake) 					# Downloads cadmium2 and sets up variables for includes
include(deps/boost.cmake) 						# Downloads boost and sets up variables for includes+
include(deps/json.cmake)
include(deps/logging-tools.cmake)	

##########################
###  Global Variables  ###
##########################
set(includes_list 
	"${CADMIUM2_INCLUDE_DIR}"
	"${json_INCLUDE_DIR}"
	"${CMAKE_CURRENT_SOURCE_DIR}/include"
	"${CMAKE_CURRENT_SOURCE_DIR}/example"
	"${CMAKE_SOURCE_DIR}"
	"${logging_tools_INCLUDE_DIR}"
)

# Include Boost directories
include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(example/test/drivers)

