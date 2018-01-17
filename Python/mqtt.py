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

        names = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw",  "LShoulderPitch", "LShoulderRoll"]

        #"RElbowYaw", "RElbowRoll",
        #[(anglelist[len(anglelist) - 5]) * almath.TO_RAD],
        #[(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
        #, [0.4], [0.4]
        # [(anglelist[len(anglelist) - 6]) * almath.TO_RAD]
        angleLists = [[(anglelist[len(anglelist) - 6]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 5]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 4]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 3]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 2]) * almath.TO_RAD],
                      [(anglelist[len(anglelist) - 1]) * almath.TO_RAD]]
        timeLists = [[0.4], [0.4], [0.4], [0.4],[0.4],[0.4]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        # print(angleLists)
        t += 1
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
            angle = -118
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
            angle = -118
        print("ik zit hier in en mijn hoek is {0}").format(angle)
        return angle
    else:
        angle = math.atan((z2 - z1) / (y2 - y1))
        angle = math.degrees(angle)
        angle = 90 - angle
        return angle

def angleLShouderRoll(x2, y2, z2, x1, y1, z1):
    # angle = math.asin((z2 - z1) / (math.sqrt((pow(z2 - z1, 2)) + pow(y2 - y1, 2))))
    # angle = math.degrees(angle)
    # # angle = angle
    # # print(angle)
    # return angle

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
        # print("x-waarde Shouder: {0}------x-waarde elleboog: {1}").format(x2,x1)
        # print("Z-waarde Shouder: {0}----- z-waarde elleboog: {1}").format(z2, z1)
        # print("LshoulderRoll: {0}").format(angle)
        return angle



def angleRElbowYaw(x2, y2, z2, x1, y1, z1,shoulderpitch):
    angle = math.atan((z2 - z1) / (y2 - y1))
    angle = math.degrees(angle)
    angle= angle + abs(shoulderpitch)
    print("RElbowYaw: {0} ").format(angle)
    return angle


def angleRElbowRoll(x2, y2, z2, x1, y1, z1):


     angle = math.atan((x2 - x1) / (z2 - z1))
     angle = math.degrees(angle)
     angle = angle
     print("x-elbow: {0} - x-wrist: {1}").format(x2,x1)
     print("")
     print("RElbowRoll: {0}").format(angle)

     return angle


#EINDE VINCENT

def angleRshoulderPitch(x1, y1, z1, x2, y2, z2):
    # print("RShoulderPitch")
    a1 = (x2 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x2) ** 2 + (y2 - y2) ** 2 + (z1 - z2) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x2 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineC, 2) - pow(lineB, 2)) / (2 * lineA * lineC)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = 90 - angleB
    # print( "Angle B: " + str(angleB) +" deg")
    return angleB


def angleRshoulderRoll(x1, y1, z1, x2, y2, z2):
    # print("RShoulderRoll")
    a1 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x1) ** 2 + (y2 - y2) ** 2 + (z1 - z1) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x1 - x1) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineC, 2) - pow(lineB, 2)) / (2 * lineA * lineC)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = - angleB
    # print( "Angle B: " + str(angleB) +" deg")
    print("RShoulderRoll: {0}").format(angleB)
    return angleB


def angleRelbowRoll(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    # print("RElbowRoll")
    a1 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x3) ** 2 + (y2 - y3) ** 2 + (z2 - z3) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x1 - x3) ** 2 + (y1 - y3) ** 2 + (z1 - z3) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineB, 2) - pow(lineC, 2)) / (2 * lineA * lineB)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = angleB + 90
    # print( "Angle B: " + str(angleB) +" deg")
    return angleB


def angleRelbowYaw(x1, y1, z1, x2, y2, z2):
    # print("RElbowYaw")
    a1 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x2) ** 2 + (y2 - y1) ** 2 + (z2 - z2) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x1 - x2) ** 2 + (y1 - y1) ** 2 + (z1 - z2) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineC, 2) - pow(lineB, 2)) / (2 * lineA * lineC)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = angleB + 90
    # print( "Angle B: " + str(angleB) +" deg")
    return angleB


def angleLshoulderPitch(x1, y1, z1, x2, y2, z2):
    # print("RShoulderPitch")
    a1 = (x2 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x2) ** 2 + (y2 - y2) ** 2 + (z1 - z2) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x2 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineC, 2) - pow(lineB, 2)) / (2 * lineA * lineC)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = 90 - angleB
    # print( "Angle B: " + str(angleB) +" deg")
    return angleB


def angleLshoulderRoll(x1, y1, z1, x2, y2, z2):
    # print("RShoulderRoll")
    a1 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineA = a1 ** 0.5
    # print( "line A: " + str(lineA) +" m")
    a2 = (x2 - x1) ** 2 + (y2 - y2) ** 2 + (z1 - z1) ** 2
    lineB = a2 ** 0.5
    # print( "line B: " + str(lineB) +" m")
    a3 = (x1 - x1) ** 2 + (y1 - y2) ** 2 + (z1 - z1) ** 2
    lineC = a3 ** 0.5
    # print( "line C: " + str(lineC) +" m")
    cosB = (pow(lineA, 2) + pow(lineC, 2) - pow(lineB, 2)) / (2 * lineA * lineC)
    acosB = math.acos(cosB)
    # print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
    angleB = float(format(math.degrees(acosB), '.2f'))
    angleB = -angleB
    # print( "Angle B: " + str(angleB) +" deg")
    return angleB


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
                angleRElbowRoll(elbowRight[0], elbowRight[1],
                                elbowRight[2], wristRight[0], wristRight[1], wristRight[2]))
            listAngles.append(
            angleRElbowYaw(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                               elbowRight[2],angleRShoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1],
                                    elbowRight[2])))
            listAngles.append(
                angleLShoulderPitch(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                    elbowLeft[2]))
            listAngles.append(
                angleLShouderRoll(shoulderLeft[0], shoulderLeft[1], shoulderLeft[2], elbowLeft[0], elbowLeft[1],
                                   elbowLeft[2]))
    sendrobot(listAngles, "172.30.248.73", 9559)
    # print("-----------------------------------")


client = mqtt.Client()
client.on_connect = on_connect

client.on_message = on_message

client.connect("172.30.252.101", 1883, 60)
client.loop_forever()