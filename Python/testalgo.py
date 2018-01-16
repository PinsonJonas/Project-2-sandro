import math




#----------------BEGIN VINCENT-----------------------

#start
# ShoulderRight: 0.03568992,0.5751851,2.444758/ElbowRight: 0.274239,0.6649151,2.406888
# ShoulderRight: 0.06092434,0.5326838,2.438355/ElbowRight: 0.1362722,0.2543808,2.442603
# ElbowRight: 0.1362722,0.2543808,2.442603/WristRight: 0.171876,0.01064131,2.367382



#stop
# ShoulderRight: 0.03568992,0.5751851,2.444758/ElbowRight: 0.274239,0.6649151,2.406888/WristRight: 0.3891994,0.8548476,2.296391

def angleRShoulderRoll(x2,y2,z2,x1,y1,z1):

    angle = math.asin((x2-x1)/(math.sqrt((pow(x2-x1,2))+pow(z2-z1,2))))
    angle = math.degrees(angle)

    print(angle)
    return angle

def angleRShoulderPitch(x2,y2,z2,x1,y1,z1):

    angle = math.asin((z2-z1)/(math.sqrt((pow(z2-z1,2))+pow(y2-y1,2))))
    angle = math.degrees(angle)
    angle = 90-angle

    print(angle)
    return angle


def angleRElbowRoll(x2,y2,z2,x1,y1,z1):
    angle = angle = math.asin((x2-x1)/(math.sqrt((pow(x2-x1,2))+pow(z2-z1,2))))
    angle = math.degrees(angle)
    angle = angle + 90
    print(angle)
    return angle


def angleRElbowYaw(x2,y2,z2,x1,y1,z1):
    angle = math.asin((z2 - z1) / (math.sqrt((pow(z2 - z1, 2)) + pow(y2 - y1, 2))))
    angle = math.degrees(angle)
    angle = angle + 90
    print(angle)




#--------------HITLER---------------

# angleRShoulderPitch(0.223395169, 0.576230049, 2.46206927, 0.35252142, 0.574617, 2.20622349)
#
# angleRShoulderRoll(0.223395169, 0.576230049, 2.46206927, 0.35252142, 0.574617, 2.20622349)
#
# angleRElbowPitch(0.35252142, 0.574617, 2.20622349,0.389017761, 0.61063695, 1.95986521)
#
# angleRElbowRoll(0.35252142, 0.574617, 2.20622349,0.389017761, 0.61063695, 1.95986521)



# print("arm naar voor")
# angleRShoulderRoll(0.02199679, 0.5273222, 2.80220771, 0.146205723, 0.723523259, 2.71396375)
# angleRShoulderPitch(0.02199679, 0.5273222, 2.80220771, 0.146205723, 0.723523259, 2.71396375)
# angleRElbowRoll( 0.146205723, 0.723523259, 2.71396375,0.1647887, 0.9566303, 2.64511585)
# angleRElbowYaw(0.146205723, 0.723523259, 2.71396375,0.1647887, 0.9566303, 2.64511585)

# angleRShoulderRoll(0.11797893, 0.570831537, 2.50675845, 0.202992275, 0.277180821, 2.48302412)
print("arm volledig naar buiten")
angleRShoulderRoll(-0.0391769968, 0.463029563, 2.55212164,0.08141533, 0.206684858, 2.60391641)
# angleRShoulderPitch(-0.040135894, 0.4721547, 2.7137568,0.169201538, 0.443810672, 2.68723679)
# angleRElbowRoll(0.169201538, 0.443810672, 2.68723679,0.215785459, 0.6406293, 2.651608)
# angleRElbowYaw(0.169201538, 0.443810672, 2.68723679,0.215785459, 0.6406293, 2.651608)



# angleRElbowPitch(0.535722554, 0.5728591, 2.38850212,0.75688386, 0.5706984, 2.35852218)
#
# angleRElbowRoll(0.535722554, 0.5728591, 2.38850212,0.75688386, 0.5706984, 2.35852218)





#--------------------EINDE VINCENT--------------------------------




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
#
# #
# #
# #
# #
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
#
# angleRshoulderRoll(0.03568992,0.5751851,2.444758,0.274239,0.6649151,2.406888 )
#
#
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
#
# def angleRElbowYaw(x1,y1,z1,x2,y2,z2):
#     print("RElbowYaw")
#     a1=(x1-x2)**2+(y1-y2)**2 + (z1-z2)**2
#     lineA= a1 ** 0.5
#     # print( "line A: " + str(lineA) +" m")
#     a2=(x2-x2)**2+(y2-y1)**2 + (z2-z1)**2
#     lineB= a2 ** 0.5
#     # print( "line B: " + str(lineB) +" m")
#     a3=(x1-x2)**2+(y1-y1)**2 + (z1-z1)**2
#     lineC= a3 ** 0.5
#     # print( "line C: " + str(lineC) +" m")
#     cosB = (pow(lineA, 2) + pow(lineC,2) - pow(lineB,2))/(2*lineA*lineC)
#     acosB = math.acos(cosB)
#     print( "Radian B: " + str(float(format(acosB, '.3f'))) +" rad")
#     angleB = float(format(math.degrees(acosB), '.2f'))
#     print( "Angle B: " + str(angleB) +" deg")
#
# angleRshoulderPitch(0.06092434, 0.5326838, 2.438355, 0.1362722, 0.2543808, 2.442603)
# angleRshoulderRoll(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603)
#
# angleRElbowRoll(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603, 0.171876,0.01064131,2.367382)
# angleRElbowYaw(0.1362722,0.2543808,2.442603, 0.171876,0.01064131,2.367382)




# list_of_joints = []

# text_file = open("BoneOrientationsTest.txt", "r")
# lines = text_file.read().split(',')
# text_file.close()

# i=0
# while i<=77:
#     angleRshoulderPitch(float(lines[i]),float(lines[i+1]),float(lines[i+2]),float(lines[i+3]),float(lines[i+4]),float(lines[i+5]))
#     angleRshoulderRoll(float(lines[i]),float(lines[i+1]),float(lines[i+2]),float(lines[i+3]),float(lines[i+4]),float(lines[i+5]))
#     i+=6

# angleRshoulderRoll(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603)
# angleRElbowRoll(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603, 0.171876,0.01064131,2.367382)
# angleRElbowYaw(0.1362722,0.2543808,2.442603, 0.171876,0.01064131,2.367382)
# print("------------------")
# angleRshoulderPitch(0.03568992,0.5751851,2.444758, 0.274239,0.6649151,2.406888)
# angleRshoulderRoll(0.03568992,0.5751851,2.444758, 0.274239,0.6649151,2.406888)
# angleRElbowRoll(0.03568992,0.5751851,2.444758, 0.274239,0.6649151,2.406888, 0.3891994,0.8548476,2.296391)
# angleRElbowYaw(0.274239,0.6649151,2.406888, 0.3891994,0.8548476,2.296391)