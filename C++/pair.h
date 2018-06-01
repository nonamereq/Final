#ifndef PAIR_H_
#define PAIR_H_

class Pair{
    public:
        int first;
        int second;

        Pair() = default;
        Pair(int, int);
        Pair(Pair&);
        Pair& operator=(Pair&);

        int getFirst();
        int getSecond();

        void setFirst(int);
        void setSecond(int);
};

#endif
