#!/usr/bin/env python

import nltk
import json




if __name__ == "__main__":
    # load in data
    with open("json/objects.json") as objectFile:
        objects = json.load(objectFile)

    with open("json/actions.json") as actionFile:
        actions = json.load(actionFile)

    q = True
    print actions
    print objects
    action = None
    object = None

    while(q):
        # take in user string
        text = raw_input("enter a task: ")
        if text == "q":
            q = False
        tokens = nltk.word_tokenize(text)

        # find the action and object
        for token in tokens:
            for key in actions:
                if token.lower() == key:
                    action = actions[key]
            for item in objects:
                if item == token.lower():
                    object = item

        # assume move if no action specified
        action = "move"

        # tags = nltk.pos_tag(tokens)
        print "action: " + str(action) + " object: " + str(object)

        # reset data
        action = None
        object = None

