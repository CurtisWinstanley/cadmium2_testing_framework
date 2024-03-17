#ifndef TEST_ATOMIC_HPP
#define TEST_ATOMIC_HPP
#include <cadmium/core/modeling/atomic.hpp>
#include <iostream>
// C++ Standard Library Headers
#include <limits>
#include <string>
// Utility functions
#include "../enum_string_conversion.hpp"

using namespace cadmium;


DEFINE_ENUM_WITH_STRING_CONVERSIONS(States,
	(WAIT_A)
	(WAIT_B)
    (DO_BAR)
    (DO_FOO)
);

struct Test_Atomic_State {
	int nInternals, nExternals, nInputs;
	double clock, sigma;
    States current_state;
	Test_Atomic_State(): nInternals(), nExternals(), nInputs(), clock(), sigma(std::numeric_limits<double>::infinity()), current_state() {}
};

std::ostream &operator << (std::ostream& os, const Test_Atomic_State& x) {
	os << "," << x.sigma << "," << "state:" << enumToString(x.current_state) << ">";
	return os;
}

class Test_Atomic: public Atomic<Test_Atomic_State> {

    public:
        
        Port<int> i_a;
        Port<int> i_b;
        Port<int> o_x;
        Port<int> o_y;

        explicit Test_Atomic(const std::string& id): Atomic<Test_Atomic_State>(id, Test_Atomic_State()) {
            i_a = addInPort<int>("i_a");
            i_b = addInPort<int>("i_b");
            o_x = addOutPort<int>("o_x");
            o_y = addOutPort<int>("o_y");

            state.current_state = States::WAIT_A; //Initial state is WAIT_A
            a = 0;
        }

        using Atomic<Test_Atomic_State>::internalTransition;
        using Atomic<Test_Atomic_State>::externalTransition;
        using Atomic<Test_Atomic_State>::confluentTransition;
        using Atomic<Test_Atomic_State>::output;
        using Atomic<Test_Atomic_State>::timeAdvance;

        const Test_Atomic_State& getState() {
            return state;
        }

        void internalTransition(Test_Atomic_State& s) const override {
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

        void externalTransition(Test_Atomic_State& s, double e) const override {
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

        void output(const Test_Atomic_State& s) const override {
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


        [[nodiscard]] double timeAdvance(const Test_Atomic_State& s) const override {
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