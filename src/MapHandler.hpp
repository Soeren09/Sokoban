#ifndef MAPHANDLER_HPP
#define MAPHANDLER_HPP

#include "State.hpp"

#include <string>

class MapHandler
{
public:
    MapHandler(State * initialState, std::vector<Position*> walls, std::vector<Position*> goals);
    bool finalStateCheck(State * state);
    bool boxDeadLock(State * state);
    std::vector<std::string> actions(State * state);
    bool posVecContains(std::vector<Position*> pos, int row, int col);
    ~MapHandler();
private:
    /* data */
    State * initialState;
    std::vector<Position*> walls;
    std::vector<Position*> goals;
};

MapHandler::MapHandler(State * initialState, std::vector<Position*> walls, std::vector<Position*> goals)
{
    this->initialState = initialState;
    this->walls = walls;
    this->goals = goals;
}

bool MapHandler::finalStateCheck(State * state)
{
    std::vector<Position*> boxes = state->getBoxes();
    for ( unsigned int i = 0; i < boxes.size(); i++ ){
        bool match = false;
        for ( unsigned int j = 0; j < goals.size(); j++ )
            if ( boxes[i]->equal(goals[j]) )
                match = true;
        if (!match)
            return false;
    }
    return true;
}

bool MapHandler::boxDeadLock(State * state)
{

}

std::vector<std::string> MapHandler::actions(State * state)
{

}

bool MapHandler::posVecContains(std::vector<Position*> pos, int row, int col)
{
    
}

MapHandler::~MapHandler()
{
}


#endif // MAPHANDLER_HPP