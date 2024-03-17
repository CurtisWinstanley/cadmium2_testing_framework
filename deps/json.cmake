message(STATUS "Downloading json v3.11.2.")

include(FetchContent)

set(FETCHCONTENT_QUIET FALSE)

FetchContent_Declare(
	json
	URL https://github.com/nlohmann/json/archive/refs/tags/v3.11.2.zip
)

FetchContent_GetProperties(json)
if(NOT json_POPULATED)
  FetchContent_Populate(json)
endif()

set(json_INCLUDE_DIR 
	"${FETCHCONTENT_BASE_DIR}/json-src/include" 
	CACHE STRING "json Include File Location"
)

message(STATUS "json v3.11.2 downloaded.")