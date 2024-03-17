import re





#WORK IN PROGRESS... MAYBE COMING SOON... I DONT REALLY KNOW FIGURING THIS OUT SUCKS.







# Path to your CMakeLists.txt file
cmake_lists_path = "test/drivers/CMakeLists.txt"

add_executable_pattern = r"add_executable\(td_test_atomic\s*\"test_atomic/td_test_atomic.cpp\"\)\s*"
target_include_directories_pattern = r"target_include_directories\(td_test_atomic\s+PUBLIC\s+\$\{includes_list\}\)\s*"
target_link_libraries_pattern = r"target_link_libraries\(td_test_atomic\s+\$\{Boost_LIBRARIES\}\)"

# The code block to search for, with a regular expression that handles variable spacing
code_block_pattern = re.compile(
    r"add_executable\(td_test_atomic\s*\"test_atomic/td_test_atomic.cpp\"\)\s*"
    r"target_include_directories\(td_test_atomic\s+PUBLIC\s+\$\{includes_list\}\)\s*"
    r"target_link_libraries\(td_test_atomic\s+\$\{Boost_LIBRARIES\}\)",
    re.DOTALL
)

# Open the CMakeLists.txt file and search for the code block
with open(cmake_lists_path, 'r') as file:
    content = file.read()
    match = code_block_pattern.search(content)
    if match:
        print("The specified code block exists in the file.")
    else:
        print("The specified code block was not found in the file.")