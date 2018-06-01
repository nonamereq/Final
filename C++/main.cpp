#include <iostream>
#include "pair.h"

int main(){
    Pair p1;
    std::cout << "Value-initialized: "
              << p1.first << ", " << p1.second << '\n';
 
    Pair p2(42, 0.123);
    std::cout << "Initialized with two values: "
              << p2.first << ", " << p2.second << '\n';
 
    Pair p4(p2);
    std::cout << "copy  constructer: "
              << p4.first << ", " << p4.second << '\n';

    p1.setFirst(5);
    p1.setSecond(5);
    std::cout << "Set values: "
              << p1.first << ", " << p1.second << '\n';
    std::cout << "Get values: "
              << p1.getFirst() << ", " << p1.getSecond() << '\n';

    p4 = p1;
    std::cout << "Operator =: "
              << p1.first << ", " << p1.second << '\n';
}
