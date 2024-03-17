#ifndef MULTIPLIER_STRUCT_T_HPP
#define MULTIPLIER_STRUCT_T_HPP

#include <iostream>

struct multiplier_struct_t{
    int first_number;
    int second_number;

    bool operator==(const multiplier_struct_t& msg){
        return (first_number = msg.first_number, second_number = msg.second_number);
    }
    
    explicit multiplier_struct_t(int _first, int _second): first_number(_first), second_number(_second){};
};

#ifndef NO_LOGGING
	/**
	 * Insertion operator for dll_frame objects.
	 * @param out output stream.
	 * @param b bid to be represented in the output stream.
	 * @return output stream with the value of the bid already inserted.
	 */
	std::ostream& operator<<(std::ostream& out, const multiplier_struct_t& msg) {
		out << "{ multiplier_struct_t: ";
        out << (int) msg.first_number << ", " << (int) msg.second_number;
        out << " }";
		
		return out;
	}
#endif

#endif //MULTIPLIER_STRUCT_T_HPP