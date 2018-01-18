import paho.mqtt.client as mqtt
import json
import math
import almath
import time
import argparse
from naoqi import ALProxy

listAngles = []
shoulderLeft = []
elbowLeft = []
shoulderRight = []
elbowRight = []
wristRight = []
t = 0

def sendrobot(anglelist, robotIP="172.30.248.73", PORT=9559):
    try:
        try:
            motionProxy = ALProxy("ALMotion", robotIP, PORT)
        except Exception, e:
            print "Could not create proxy to AlMotion"
            print "Error was: ", e
        try:
            postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e

        global t

        if (t == 0):
            motionProxy.setStiffnesses("Body", 0.0)
            postureProxy.goToPosture("StandInit", 0.5)        

        names = ["RShoulderPitch", "RShoulderRoll", "LShoulderPitch", "LShoulderRoll"]

        angleLists = [[(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 3]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 2]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 1]) * almath.TO_RAD]]
        timeLists = [[0.4], [0.4], [0.4], [0.4]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        t += 1   
    # except Exception, e:
    #     print "Error was: ", e:
    except (KeyboardInterrupt, SystemExit):
        postureProxy.goToPosture("StandInit", 0.5)
        motionProxy.setStiffnesses("Body", 1.0)
        raise


#BEGIN VINCENT

def angleRShoulderPitch(x2, y2, z2, x1, y1, z1):
    if(y2<y1):
        angle = math.atan(abs(y2 - y1) / abs(z2 - z1))
        angle = math.degrees(angle)
        angle = -(angle)
        if(angle<-118):
            angle = -117
        print("ik zit hier in en mijn hoek is {0}").format(angle)
        return angle
    else:
        angle = math.atan((z2-z1)/(y2-y1))
        angle = math.degrees(angle)
        angle = 90-angle
        return angle

def angleRShoulderRoll(x2, y2, z2, x1, y1, z1):
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
    # print("x-waarde Shouder: {0}------x-waarde elleboog: {1}").format(x2,x1)
    # print("Z-waarde Shouder: {0}----- z-waarde elleboog: {1}").format(z2,z1)
    # print("RshoulderRoll: {0}").format(angle)
    return angle

def angleLShoulderPitch(x2, y2, z2, x1, y1, z1):
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

def angleLShouderRoll(x2, y2, z2, x1, y1, z1):
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

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/Sandro")

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload.decode('utf-8'))
    for i in payload:
        # print(i['jointname'])
        if i['jointname'] == "ShoulderLeft":
            shoulderLeft = i['coordinates']
            # print(i['coordinates'])
        if i['jointname'] == "ElbowLeft":
            elbowLeft = i['coordinates']
            # print(i['coordinates'])
        if i['jointname'] == "ShoulderRight":
            shoulderRight = i['coordinates']
            # print(i['coordinates'])
        if i['jointname'] == "ElbowRight":
            elbowRight = i['coordinates']
            # print(i['coordinates'])
        if i['jointname'] == "WristRight":
            wristRight = i['coordinates']
            # print(i['coordinates'])
            # print(shoulderRight)

            listAngles.append(
                angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                    elbowRight[2]))
            listAngles.append(
                angleRShoulderRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                   elbowRight[2]))
            
            listAngles.append(
                angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                    elbowLeft[2]))
            listAngles.append(
                angleLShouderRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                   elbowLeft[2]))
    sendrobot(listAngles, "172.30.248.56", 9559)
    # print("-----------------------------------")


client = mqtt.Client()
client.on_connect = on_connect

client.on_message = on_message

# client.connect("169.254.10.11", 1883, 60)
client.connect("52.174.68.36", 1883, 60)
client.loop_forever()