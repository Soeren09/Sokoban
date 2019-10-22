#pragma once

class Position
{

public:
    Position(int row, int col);
    int hashCode();
    bool equal(Position* pos);
    ~Position();

private:
    /* data */
    int row;
    int col;
    int MAX_COL = 1000;
};

Position::Position(int row, int col)
{
    this->row = row;
    this->col = col;
}

int Position::hashCode()
{
    return MAX_COL*this->row + this->col;
}

bool Position::equal(Position *pos)
{
    if ( pos == nullptr )
        return false;
    if ( pos->hashCode() == this->hashCode() )
        if ( pos->row == this->row && pos->col == this->col )
            return true;
    return false;
}

Position::~Position()
{
}
