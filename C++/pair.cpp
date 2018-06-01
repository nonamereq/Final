#include "pair.h"

Pair::Pair(int first, int second){
    this->first = first;
    this->second = second;
}

Pair::Pair(Pair& pair){
    first = pair.first;
    second = pair.second;
}

Pair& Pair::operator=(Pair& pair){
    first = pair.first;
    second = pair.second;
    return *this;
}

int Pair::getFirst(){
    return first;
}

int Pair::getSecond(){
    return second;
}

void Pair::setFirst(int first){
    this->first = first;
}

void Pair::setSecond(int second){
    this->second = second;
}
