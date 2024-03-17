#ifndef MESSAGE_START_SUPERVISOR_T_HPP
#define MESSAGE_START_SUPERVISOR_T_HPP

// C++ Standard Library Headers
#include <cstdint>
#include <iostream>

// Mavlink Headers
//#include <mavlink/v2.0/peregrine_4_2/mavlink.h>

struct message_start_supervisor_t{
	/****************************************************/
	/* Constructors										*/
	/****************************************************/

    uint8_t autonomy_armed;
    uint8_t mission_started;
    uint32_t mission_number;

    message_start_supervisor_t(
        uint8_t autonomy_armed,
        uint8_t mission_started,
        uint32_t mission_number
	)
		: autonomy_armed(autonomy_armed),
		mission_started(mission_started),
		mission_number(mission_number)
        {}

    message_start_supervisor_t()
		: autonomy_armed(0),
		mission_started(0),
		mission_number(0)
        {}

};
#pragma pack(pop)


/// Output stream operator.
std::ostream &operator<<(std::ostream &os, const message_start_supervisor_t &msg) {
	os << (int)msg.autonomy_armed << " "
	   << (int)msg.mission_started << " "
       << (int)msg.mission_number << " ";
	return os;
}
#endif // MESSAGE_START_SUPERVISOR_T_HPP
