import paho.mqtt.client as mqtt
import json
import math
import almath
import time
import argparse
from naoqi import ALProxy
# import main from test2
listAngles = []
shoulderRight= []
elbowRight = []
wristRight = []
t=0

# def sendrobot(anglelist, robotIP = "172.30.248.162", PORT = 9559):
#     try:
#         try:
#             motionProxy = ALProxy("ALMotion", robotIP, PORT)
#         except Exception, e:
#             print "Could not create proxy to AlMotion"
#             print "Error was: ", e
#         try:
#             postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
#         except Exception, e:
#             print "Could not create proxy to ALRobotPosture"
#             print "Error was: ", e
#
#         global t
#
#         if (t == 0):
#             motionProxy.setStiffnesses("Body", 0.0)
#             postureProxy.goToPosture("StandInit", 0.5)
#
#         names      = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
#
#         angleLists  = [[(90-anglelist[0])*almath.TO_RAD],
#                     [(-anglelist[1]/90*75)*almath.TO_RAD],
#                     [(0-anglelist[2])*almath.TO_RAD],
#                     [(anglelist[3]/180*88)*almath.TO_RAD]]
#         timeLists   = [[1.0], [1.0], [1.0], [1.0]]
#         isAbsolute  = True
#         motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)
#         print(angleLists)
#         t +=1
#     except (KeyboardInterrupt, SystemExit):
#         postureProxy.goToPosture("StandInit", 0.5)
#         motionProxy.setStiffnesses("Body", 1.0)
#         raise
#
# def angleRshoulderPitch(x1,y1,z1,x2,y2,z2):
#     print("RShoulderPitch")
#     a1=(x2-x2)**2+(y1-y2)**2 + (z1-z2)**2
#     lineA= a1 ** 0.5
#     # print( "line A: " + str(lineA) +" m")
#     a2=(x2-x2)**2+(y2-y2)**2 + (z1-z2)**2
#     lineB= a2 ** 0.5
#     # print( "line B: " + str(lineB) +" m")
#     a3=(x2-x2)**2+(y1-y2)**2 + (z1-z1)**2
#     lineC= a3 ** 0.5
#     # print( "line C: " + str(lineC) +" m")
#     cosB = (pow(lineA, 2) + pow(lineC,2) - pow(lineB,2))/(2*lineA*lineC)
#     acosB = math.acos(cosB)
#     print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
#     angleB = float(format(math.degrees(acosB), '.2f'))
#     print( "Angle B: " + str(angleB) +" deg")
#     return angleB
#
# def angleRshoulderRoll(x1,y1,z1,x2,y2,z2):
#     print("RShoulderRoll")
#     a1=(x1-x2)**2+(y1-y2)**2 + (z1-z1)**2
#     lineA= a1 ** 0.5
#     # print( "line A: " + str(lineA) +" m")
#     a2=(x2-x1)**2+(y2-y2)**2 + (z1-z1)**2
#     lineB= a2 ** 0.5
#     # print( "line B: " + str(lineB) +" m")
#     a3=(x1-x1)**2+(y1-y2)**2 + (z1-z1)**2
#     lineC= a3 ** 0.5
#     # print( "line C: " + str(lineC) +" m")
#     cosB = (pow(lineA, 2) + pow(lineC,2) - pow(lineB,2))/(2*lineA*lineC)
#     acosB = math.acos(cosB)
#     print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
#     angleB = float(format(math.degrees(acosB), '.2f'))
#     print( "Angle B: " + str(angleB) +" deg")
#     return angleB
#
# def angleRElbowRoll(x1,y1,z1,x2,y2,z2,x3,y3,z3):
#     print("RElbowRoll")
#     a1=(x1-x2)**2+(y1-y2)**2 + (z1-z2)**2
#     lineA= a1 ** 0.5
#     # print( "line A: " + str(lineA) +" m")
#     a2=(x2-x3)**2+(y2-y3)**2 + (z2-z3)**2
#     lineB= a2 ** 0.5
#     # print( "line B: " + str(lineB) +" m")
#     a3=(x1-x3)**2+(y1-y3)**2 + (z1-z3)**2
#     lineC= a3 ** 0.5
#     # print( "line C: " + str(lineC) +" m")
#     cosB = (pow(lineA, 2) + pow(lineB,2) - pow(lineC,2))/(2*lineA*lineB)
#     acosB = math.acos(cosB)
#     print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
#     angleB = float(format(math.degrees(acosB), '.2f'))
#     print( "Angle B: " + str(angleB) +" deg")
#     return angleB
#
# def angleRElbowYaw(x1,y1,z1,x2,y2,z2):
#     print("RElbowYaw")
#     a1=(x1-x2)**2+(y1-y2)**2 + (z1-z2)**2
#     lineA= a1 ** 0.5
#     # print( "line A: " + str(lineA) +" m")
#     a2=(x2-x2)**2+(y2-y1)**2 + (z2-z2)**2
#     lineB= a2 ** 0.5
#     # print( "line B: " + str(lineB) +" m")
#     a3=(x1-x2)**2+(y1-y1)**2 + (z1-z2)**2
#     lineC= a3 ** 0.5
#     # print( "line C: " + str(lineC) +" m")
#     cosB = (pow(lineA, 2) + pow(lineC,2) - pow(lineB,2))/(2*lineA*lineC)
#     acosB = math.acos(cosB)
#     print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
#     angleB = float(format(math.degrees(acosB), '.2f'))
#     print( "Angle B: " + str(angleB) +" deg")
#     return angleB

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/Sandro")

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    payload = json.loads(msg.payload.decode('utf-8'))
    for i in payload:
        print(i['jointname'])
        print(i['coordinates'])
    #     if i['jointname'] == "ShoulderRight":
    #         shoulderRight = i['coordinates']
    #         # print(shoulderRight)
    #         # print(shoulderRight[0])
    #     if i['jointname'] == "ElbowRight":
    #         elbowRight = i['coordinates']
    #     if i['jointname'] == "WristRight":
    #         wristRight = i['coordinates']
    #         listAngles.append(angleRshoulderPitch(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2]))
    #         listAngles.append(angleRshoulderRoll(shoulderRight[0],shoulderRight[1],shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2]))
    #         listAngles.append(angleRElbowYaw(elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0], wristRight[1], wristRight[2]))
    #         listAngles.append(angleRElbowRoll(shoulderRight[0], shoulderRight[1], shoulderRight[2], elbowRight[0], elbowRight[1], elbowRight[2], wristRight[0], wristRight[1], wristRight[2]))
    # sendrobot(listAngles,"172.30.248.162", 9559)
    # print("-----------------------------------")
    
    
    


client = mqtt.Client()
client.on_connect = on_connect

client.on_message = on_message

client.connect("52.174.68.36", 1883,60)
client.loop_forever()


