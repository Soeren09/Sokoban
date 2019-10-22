#pragma once

#include "State.hpp"

#include <string>

class Node
{
public:
    Node(State * state, Node * parent, std::string action);
    bool equal(Node * node);
    ~Node();

private:
    State * state;
    Node * parent;
    std::string action; // Skal muligivs ændes til (int) som afgør action type?
};

Node::Node(State * state, Node * parent, std::string action)
{
    this->state = state;
    this->parent = parent;
    this->action = action;
}

bool Node::equal(Node * node)
{
    return this->state->equal(node->state);
}

Node::~Node()
{
}
