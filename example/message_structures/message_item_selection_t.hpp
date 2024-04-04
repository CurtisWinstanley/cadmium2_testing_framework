#ifndef MESSAGE_ITEM_SELECTION_T_HPP
#define MESSAGE_ITEM_SELECTION_T_HPP

#include <cstdint>
#include <string>
#include <iostream>


struct item_selection_t {
	float price; //represents price of an item
	int item_id; //represents the id of an item

	item_selection_t(): price(0), item_id(0) {}
	item_selection_t(float price, int item_id): price(price), item_id(item_id) {}


	// Define the equality operator
    bool operator==(const item_selection_t& other) const {
        return price == other.price && item_id == other.item_id;
    }
};

/***************************************************/
/************* Output stream ***********************/
/***************************************************/

std::ostream& operator<<(std::ostream& os, const item_selection_t& msg) {
	os << msg.price << " "
	   << msg.item_id << " ";
	return os;
}

#endif