#pragma once
#include "Position.hpp"

#include <vector>

class State
{

public:
    State(Position *player, std::vector<Position*> boxes);
    int hashCode();
    bool equal(State * s);
    ~State();

private:
    /* data */
    Position *player;
    std::vector<Position*> boxes;
};

State::State(Position *player, std::vector<Position*> boxes)
{
    this->player = player;
    this->boxes = boxes;
}

int State::hashCode()
{
    int hash = 17; // Arbitrary prime number
    for ( unsigned int i = 0; i < boxes.size(); i++ )
        hash = 37 * hash + this->boxes[i]->hashCode(); // Multiply with arbitrary prime
    hash = 37 * hash + this->player->hashCode();
    return hash;
}

bool State::equal(State * s)
{
    if ( s == nullptr )
        return false;
    if ( s->hashCode() == this->hashCode() )
        if ( this->player->equal(s->player) ){
            for ( unsigned int i = 0; i < s->boxes.size(); i++ )
                if ( ! this->boxes[i]->equal( s->boxes[i] ) )
                    return false;
            return true;
        }
    return false;
}

State::~State()
{
}
