import paho.mqtt.client as mqtt
import json
import math
import almath
import time
import argparse
from naoqi import ALProxy

# Global variables
listAngles = []
shoulderLeft = []
elbowLeft = []
wristLeft = []
shoulderRight = []
elbowRight = []
wristRight = []
t = 0
RobotIP = raw_input("Geef robot IP: ")
RobotPort = int(raw_input("Geef robot Port (standaard 9559): "))
MQTTIP = raw_input("Geef mqtt IP: ")
MQTTTOPIC = raw_input("Geef mqtt topic: ")

def sendrobot(anglelist, robotIP="172.30.248.120", PORT=9559):
    try:
        try:
            motionProxy = ALProxy("ALMotion", robotIP, PORT) #creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to AlMotion"
            print "Error was: ", e
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, PORT) #creates proxy to call specific functions
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        global t # uses global variable t

        if (t == 0): # if it is the first time the robot is called upon
            motionProxy.setStiffnesses("Body", 0.0) # unstiffens the joints
            postureProxy.goToPosture("StandInit", 0.5) # gets the robot into his initial standing position

        names = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw",  "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw"]
        #list of joints that will get changed

        angleLists = [[(anglelist[len(anglelist) - 8]) * almath.TO_RAD], # all the coordinates are saved in one big list
                      [(anglelist[len(anglelist) - 7]) * almath.TO_RAD], # and in a specific order (see list of joints)
                      [(anglelist[len(anglelist) - 6]) * almath.TO_RAD], # this gets them out of that list and sent to the right joint
                      [(anglelist[len(anglelist) - 5]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 3]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 2]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 1]) * almath.TO_RAD]]
        timeLists = [[0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4]] # sets the time the robot has to get to the joint location (when you give more than one coordinate for a joint, you have to give more than one timestamp for that same joint!)
        isAbsolute = True # kindoff is deprecated, but makes the joint positions absolute and not relative
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute) #the function talks with the robot
        t += 1 # global t gets added by 1 so the joints dont get unstiffened again and the robot does not get put in its initial position
    except Exception: # checks for any and all errors
        pass # ignores every single one of them, except keyboardInterupt and SystemExit
    except (KeyboardInterrupt, SystemExit): # when the program gets terminated
        postureProxy.goToPosture("StandInit", 0.5) # set the robot in its initial position
        motionProxy.setStiffnesses("Body", 1.0) # stiffen the joints
        raise #actually quit

def angleRShoulderPitch(x2, y2, z2, x1, y1, z1): #calulates the Shoulderpitch value for the Right shoulder by using geometry
    if(y2<y1):
        angle = math.atan(abs(y2 - y1) / abs(z2 - z1)) 
        angle = math.degrees(angle)
        angle = -(angle)
        if(angle<-118):
            angle = -117
        return angle
    else:
        angle = math.atan((z2-z1)/(y2-y1))
        angle = math.degrees(angle)
        angle = 90-angle
        return angle

def angleRShoulderRoll(x2, y2, z2, x1, y1, z1): #calulates the ShoulderRoll value for the Right shoulder by using geometry
    if(z2<z1):
        test = z2
        anderetest = z1
        z2=anderetest
        z1=test
    if (z2 - z1 < 0.1):
        z2 = 1.0
        z1 = 0.8
    angle = math.atan((x2 - x1) / (z2 - z1))
    angle = math.degrees(angle)
    return angle

def angleLShoulderPitch(x2, y2, z2, x1, y1, z1): #calulates the Shoulderpitch value for the Left shoulder by using geometry
    if (y2 < y1):
        angle = math.atan(abs(y2 - y1) / abs(z2 - z1))
        angle = math.degrees(angle)
        angle = -(angle)
        if (angle < -118):
            angle = -117
        return angle
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = 90 - angle
        return angle

def angleLShouderRoll(x2, y2, z2, x1, y1, z1): #calulates the ShoulderRoll value for the Left shoulder by using geometry
    if (z2 < z1):
        test = z2
        anderetest = z1
        z2 = anderetest
        z1 = test
    if(z2-z1< 0.1):
        z2=1.0
        z1=0.8
    angle = math.atan((x2-x1)/(z2-z1))
    angle = math.degrees(angle)
    return angle

def angleRElbowYaw(x2, y2, z2, x1, y1, z1,shoulderpitch): #calulates the ElbowYaw value for the Right elbow by using geometry
    if(abs(y2-y1)<0.2 and abs(z2-z1) < 0.2 and (x1<x2) ):
        return 0
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (y1>y2)):
        return 90
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        return 90
    elif(abs(y2-y1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch < 50)):
        return 0
    elif(abs(x2-x1)<0.1 and abs(y2-y1)<0.1 and (shoulderpitch > 50)):
        return 90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        return angle


def angleRElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1, z1): #calulates the ElbowRoll value for the Right elbow by using geometry
    a1=(x3-x2)**2+(y3-y2)**2 + (z3-z2)**2 
    lineA= a1 ** 0.5                        # calculates length of line between 2 3D coordinates
    b1=(x2-x1)**2+(y2-y1)**2 + (z2-z1)**2
    lineB= b1 ** 0.5                        # calculates length of line between 2 3D coordinates
    c1=(x1-x3)**2+(y1-y3)**2 + (z1-z3)**2
    lineC= c1 ** 0.5                        # calculates length of line between 2 3D coordinates

    cosB = (pow(lineA, 2) + pow(lineB,2) - pow(lineC,2))/(2*lineA*lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = 180 - angle
    return angle


def angleLElbowYaw(x2, y2, z2, x1, y1, z1, shoulderpitch): #calulates the ElbowYaw value for the Left elbow by using geometry
    if(abs(y2-y1)<0.2 and abs(z2-z1) < 0.2 and (x1>x2) ):
        return 0
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (y1>y2)):
        return -90
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        return -90
    elif(abs(y2-y1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        return 0
    elif(abs(x2-x1)<0.1 and abs(y2-y1)<0.1 and (shoulderpitch > 50)):
        return -90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        return angle

def angleLElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1, z1): #calulates the ElbowRoll value for the Left elbow by using geometry

    a1=(x3-x2)**2+(y3-y2)**2 + (z3-z2)**2
    lineA= a1 ** 0.5                        # calculates length of line between 2 3D coordinates
    b1=(x2-x1)**2+(y2-y1)**2 + (z2-z1)**2
    lineB= b1 ** 0.5                        # calculates length of line between 2 3D coordinates
    c1=(x1-x3)**2+(y1-y3)**2 + (z1-z3)**2
    lineC= c1 ** 0.5                        # calculates length of line between 2 3D coordinates

    cosB = (pow(lineA, 2) + pow(lineB,2) - pow(lineC,2))/(2*lineA*lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = -180+ angle
    return angle

def on_connect(client, userdata, flags, rc): # connects with mqtt and subscribes to /Sandro
    print("Connected with result code " + str(rc))
    client.subscribe(MQTTTOPIC)
    client.subscribe(MQTTTOPIC+str(2))

def on_message(client, userdata, msg): # Checks the mqtt message it receives and processes the json
    payload = json.loads(msg.payload.decode('utf-8'))
    if(msg.topic == "/Sandro"):
        for i in payload:
            if i['jointname'] == "ShoulderLeft":
                shoulderLeft = i['coordinates']
            if i['jointname'] == "ElbowLeft":
                elbowLeft = i['coordinates']
            if i['jointname'] == "WristLeft":
                wristLeft = i['coordinates']
            if i['jointname'] == "ShoulderRight":
                shoulderRight = i['coordinates']
            if i['jointname'] == "ElbowRight":
                elbowRight = i['coordinates']
            if i['jointname'] == "WristRight":
                wristRight = i['coordinates']

                listAngles.append(
                    angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                        elbowRight[2]))
                listAngles.append(
                    angleRShoulderRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                    elbowRight[2]))
                listAngles.append(
                    angleRElbowRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                    elbowRight[2], wristRight[0], wristRight[1], wristRight[2]))
                listAngles.append(
                    angleRElbowYaw(elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0], wristRight[1],
                                wristRight[2], angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                        elbowRight[2])))
                listAngles.append(
                    angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                        elbowLeft[2]))
                listAngles.append(
                    angleLShouderRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                    elbowLeft[2]))
                listAngles.append(
                    angleLElbowRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                    elbowLeft[2], wristLeft[0], wristLeft[1], wristLeft[2]))
                listAngles.append(
                    angleLElbowYaw(elbowLeft[0], elbowLeft[1], elbowLeft[2], wristLeft[0], wristLeft[1],
                                wristLeft[2], angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                        elbowLeft[2])))
        sendrobot(listAngles, RobotIP, RobotPort) # takes userinput
    if(msg.topic == "/Sandro2"):
        x=1
        while x <= len(payload)-1:
            for key,value in payload.iteritems():
                numcoord = "coord" + str(x)
                if(key == numcoord ):
                    for i in value:
                        if i['jointname'] == "ShoulderLeft": # checks jointname in json
                            shoulderLeft = i['coordinates'] # puts the corresponding coordinates in the global list
                        if i['jointname'] == "ElbowLeft": # checks jointname in json
                            elbowLeft = i['coordinates'] # puts the corresponding coordinates in the global list
                        if i['jointname'] == "WristLeft": # checks jointname in json
                            wristLeft = i['coordinates'] # puts the corresponding coordinates in the global list
                        if i['jointname'] == "ShoulderRight": # checks jointname in json
                            shoulderRight = i['coordinates'] # puts the corresponding coordinates in the global list
                        if i['jointname'] == "ElbowRight": # checks jointname in json
                            elbowRight = i['coordinates'] # puts the corresponding coordinates in the global list
                        if i['jointname'] == "WristRight": # checks jointname in json
                            wristRight = i['coordinates'] # puts the corresponding coordinates in the global list

                    listAngles.append(angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],elbowRight[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleRShoulderRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleRElbowRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0], wristRight[1], wristRight[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleRElbowYaw(elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0], wristRight[1], wristRight[2], angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2]))) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1], elbowLeft[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleLShouderRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1], elbowLeft[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleLElbowRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1], elbowLeft[2], wristLeft[0], wristLeft[1], wristLeft[2])) # calculates the angles via the Function with given coordinates and appends them to the masterlist
                    listAngles.append(angleLElbowYaw(elbowLeft[0], elbowLeft[1], elbowLeft[2], wristLeft[0], wristLeft[1], wristLeft[2], angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1], elbowLeft[2]))) # calculates the angles via the Function with given coordinates and appends them to the masterlist
            sendrobot(listAngles, RobotIP, RobotPort) # Takes userinput


            x+=1



client = mqtt.Client() # mqtt stuff
client.on_connect = on_connect # mqtt stuff

client.on_message = on_message # mqtt stuff

client.connect(MQTTIP, 1883, 60) # takes userinput
client.loop_forever() # listen forever