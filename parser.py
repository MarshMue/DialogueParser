#!/usr/bin/env python

import os
import nltk
import json
import speech_recognition as sr
import xml.etree.ElementTree as ET
import rospy
from std_msgs.msg import String


if __name__ == "__main__":

    # ROS init
    pub = rospy.Publisher('mav_task', String, queue_size=10)
    rospy.init_node('control_node', anonymous=True)
    rospy.sleep(1)

    # set up speech recognition
    r = sr.Recognizer()
    m = sr.Microphone()
    
    #data 
    objects = []

    dr = "../models/"
    # load in data
    for directory in os.listdir(dr):
        if directory[0] != ".": 
            tree = ET.parse(dr + directory + "/model.config")
            root = tree.getroot()
            mname = root[0].text
            print type(mname)
            objects.append(mname)

    #with open("json/objects.json") as objectFile:
     #   objects = json.load(objectFile)

    with open("json/actions.json") as actionFile:
        actions = json.load(actionFile)

    q = True
    print actions
    print objects
    action = None
    object = None

    while(q):
        # take in user string

        print("Say something!")
        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))
                if format(value).encode("utf-8") == "quit":
                    q = False
            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
            continue
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
        tokens = nltk.word_tokenize(format(value).encode("utf-8"))

        # find the action and object
        for token in tokens:
            for key in actions:
                if token.lower() == key.lower():
                    action = actions[key]
            for item in objects:
                if item.lower() == token.lower():
                    object = item


        # tags = nltk.pos_tag(tokens)
        print "action: " + str(action) + " object: " + str(object)

        # publish ros data
        if action is not None and object is not None:
            ros.publish(object)

        # reset data
        action = None
        object = None

