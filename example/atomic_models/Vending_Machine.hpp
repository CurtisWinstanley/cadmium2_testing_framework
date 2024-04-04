#ifndef VENDING_MACHINE_HPP
#define VENDING_MACHINE_HPP
#include <cadmium/core/modeling/atomic.hpp>
#include <iostream>
// C++ Standard Library Headers
#include <limits>
#include <string>
// Utility functions
#include "../enum_string_conversion.hpp"

using namespace cadmium;

#include "../message_structures/message_item_selection_t.hpp"

DEFINE_ENUM_WITH_STRING_CONVERSIONS(States,
	(WAIT_FOR_SELECTION)
	(COLLECT_CURRENCY)
    (CHECK_AMOUNT)
    (OUTPUT_CHANGE)
    (DISPENSE_BEVERAGE)
);

struct Vending_Machine_State {
	int nInternals, nExternals, nInputs;
	double clock, sigma;
    States current_state;
	Vending_Machine_State(): nInternals(), nExternals(), nInputs(), clock(), sigma(std::numeric_limits<double>::infinity()), current_state() {}
};

std::ostream &operator << (std::ostream& os, const Vending_Machine_State& x) {
	os << "," << x.sigma << "," << "state:" << enumToString(x.current_state) << ">";
	return os;
}

class Vending_Machine: public Atomic<Vending_Machine_State> {

    public:
        
        Port<float> i_money;
        Port<item_selection_t> i_beverage_selection;
        Port<float> o_change;
        Port<int> o_dispense_id;

        explicit Vending_Machine(const std::string& id): Atomic<Vending_Machine_State>(id, Vending_Machine_State()) {
            i_money              = addInPort<float>("i_money");
            i_beverage_selection = addInPort<item_selection_t>("i_beverage_selection");
            o_change             = addOutPort<float>("o_change");
            o_dispense_id        = addOutPort<int>("o_dispense_id");

            state.current_state = States::WAIT_FOR_SELECTION; //Initial state is WAIT_A
            a = 0;
        }

        using Atomic<Vending_Machine_State>::internalTransition;
        using Atomic<Vending_Machine_State>::externalTransition;
        using Atomic<Vending_Machine_State>::confluentTransition;
        using Atomic<Vending_Machine_State>::output;
        using Atomic<Vending_Machine_State>::timeAdvance;

        const Vending_Machine_State& getState() {
            return state;
        }

        void internalTransition(Vending_Machine_State& s) const override {
            s.clock += s.sigma;
            //s.sigma = ++s.nInternals;

            switch (state.current_state) {
                case States::DO_BAR:
                    s.current_state = States::DO_FOO;
                    break;
                case States::DO_FOO:
                    s.current_state = States::WAIT_A;
                    break;
                default:
                    return;
            }
        }

        void externalTransition(Vending_Machine_State& s, double e) const override {
            s.clock += e;
            s.nInputs += (int) i_a->size();

            switch (state.current_state) {
                case States::WAIT_A:{
                    bool received_A = !i_a->empty();
                    if(received_A)
                    {
                        a = i_a->getBag().back();

                        s.current_state = States::WAIT_B;
                    }
                    break;
                }
                case States::WAIT_B:{
                    bool received_B = !i_b->empty();
                    if(received_B)
                    {
                        b = i_b->getBag().back();

                        s.current_state = States::DO_BAR;
                    }
                    break;
                }
                default:
                    break;
            }
            return;
        }

        void output(const Vending_Machine_State& s) const override {
            switch(state.current_state){
                case States::DO_BAR:
                {
                    added_sum = a+b;
                    std::cout<< "DO_BAR to output: "<< added_sum <<std::endl;
                    o_x->addMessage(added_sum);
                    break;
                }
                case States::DO_FOO:
                {
                    product = a*b;
                    std::cout<< "product to output: "<< product <<std::endl;
                    o_y->addMessage(product);
                    break;
                }
                default:
                    break;
            }
            return;
        }


        [[nodiscard]] double timeAdvance(const Vending_Machine_State& s) const override {
                switch (s.current_state) {
                case States::WAIT_A:
                    return std::numeric_limits<double>::infinity();
                    break;
                case States::WAIT_B:
                    return std::numeric_limits<double>::infinity();
                    break;
                case States::DO_BAR:
                    return 10;
                    break;
                case States::DO_FOO:
                    return 0;
                    break;
                default:
                    break;
            }
            return s.sigma;
        }


    //
    private:
        mutable int added_sum;
        mutable int product;
        mutable int a; //first number to add
        mutable int b; //second number to add
};
#endif //TEST_ATOMIC_HPP