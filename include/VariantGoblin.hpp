
#ifndef VARIANT_GOBLIN_HPP
#define VARIANT_GOBLIN_HPP

#include <iostream>
#include <vector>
#include <tuple>
#include <map>
#include <string>
#include <variant>


//locations of structure or class definitions that the model ports use.
//IMPORTANT: Make sure to add all of the port locations that your project uses.
#include "message_structures/message_update_gcs_t.hpp"
#include "message_structures/message_aircraft_state_t.hpp"
#include "message_structures/message_start_supervisor_t.hpp"

//This variant holds every type that the ports can output
using VariantType = std::variant<int, double, bool, float, std::string, uint8_t, uint16_t, uint32_t
, message_update_gcs_t
, message_aircraft_state_t
, message_start_supervisor_t
      >;
#endif;