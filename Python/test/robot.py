import paho.mqtt.client as mqtt
import json
import math
import almath
import time
import argparse
from naoqi import ALProxy

# import main from test2
listAngles = []
shoulderLeft = []
elbowLeft = []
wristLeft = []
shoulderRight = []
elbowRight = []
wristRight = []
t = 0


def sendrobot(anglelist, robotIP="172.30.248.56", PORT=9559):
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

        names = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw",  "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw"]

        angleLists = [[(anglelist[len(anglelist) - 8]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 7]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 6]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 5]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 3]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 2]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 1]) * almath.TO_RAD]]
        timeLists = [[0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4], [0.4]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        t += 1  
    except Exception:
        pass
    except (KeyboardInterrupt, SystemExit):
        postureProxy.goToPosture("StandInit", 0.5)
        motionProxy.setStiffnesses("Body", 1.0)
        raise

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

def angleRElbowYaw(x2, y2, z2, x1, y1, z1,shoulderpitch):
    if(abs(y2-y1)<0.2 and abs(z2-z1) < 0.2 and (x1<x2) ):
        print ("Ra")
        return 0
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (y1>y2)):
        print("Rb")
        return 90
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        print("Rc")
        return 90
    elif(abs(y2-y1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch < 50)):
        print("Rd")
        return 0
    elif(abs(x2-x1)<0.1 and abs(y2-y1)<0.1 and (shoulderpitch > 50)):
        print("Re")
        return 90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        print("Rf: " + str(angle))
        return angle


def angleRElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1, z1):
    a1=(x3-x2)**2+(y3-y2)**2 + (z3-z2)**2
    lineA= a1 ** 0.5
    b1=(x2-x1)**2+(y2-y1)**2 + (z2-z1)**2
    lineB= b1 ** 0.5
    c1=(x1-x3)**2+(y1-y3)**2 + (z1-z3)**2
    lineC= c1 ** 0.5

    cosB = (pow(lineA, 2) + pow(lineB,2) - pow(lineC,2))/(2*lineA*lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = 180 - angle
    print("RElbowRoll", angle)
    return angle


def angleLElbowYaw(x2, y2, z2, x1, y1, z1, shoulderpitch):
    if(abs(y2-y1)<0.2 and abs(z2-z1) < 0.2 and (x1>x2) ):
        print ("La")
        return 0
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (y1>y2)):
        print("Lb")
        return -90
    elif(abs(x2-x1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        print("Lc")
        return -90
    elif(abs(y2-y1)<0.1 and abs(z2-z1)<0.1 and (shoulderpitch > 50)):
        print("Ld")
        return 0
    elif(abs(x2-x1)<0.1 and abs(y2-y1)<0.1 and (shoulderpitch > 50)):
        print("LE")
        return -90
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = - angle + (shoulderpitch)
        angle = - angle
        print("Lf: " + str(angle))
        return angle

def angleLElbowRoll(x3, y3, z3, x2, y2, z2, x1, y1, z1):

    a1=(x3-x2)**2+(y3-y2)**2 + (z3-z2)**2
    lineA= a1 ** 0.5
    b1=(x2-x1)**2+(y2-y1)**2 + (z2-z1)**2
    lineB= b1 ** 0.5
    c1=(x1-x3)**2+(y1-y3)**2 + (z1-z3)**2
    lineC= c1 ** 0.5

    cosB = (pow(lineA, 2) + pow(lineB,2) - pow(lineC,2))/(2*lineA*lineB)
    acosB = math.acos(cosB)
    angle = math.degrees(acosB)
    angle = -180+ angle
    print("LElbowRoll", angle)
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
        if i['jointname'] == "WristLeft":
            wristLeft = i['coordinates']
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
    sendrobot(listAngles, "172.30.248.175", 9559)
    # print("-----------------------------------")


client = mqtt.Client()
client.on_connect = on_connect

client.on_message = on_message

# client.connect("169.254.10.11", 1883, 60)
client.connect(raw_input("Mqtt ip addres: "), 1883, 60)
client.loop_forever()