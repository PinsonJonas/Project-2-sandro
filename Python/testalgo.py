import math




#----------------BEGIN VINCENT-----------------------

#start
# ShoulderRight: 0.03568992,0.5751851,2.444758/ElbowRight: 0.274239,0.6649151,2.406888
# ShoulderRight: 0.06092434,0.5326838,2.438355/ElbowRight: 0.1362722,0.2543808,2.442603
# ElbowRight: 0.1362722,0.2543808,2.442603/WristRight: 0.171876,0.01064131,2.367382



#stop
# ShoulderRight: 0.03568992,0.5751851,2.444758/ElbowRight: 0.274239,0.6649151,2.406888/WristRight: 0.3891994,0.8548476,2.296391

def angleRShoulderPitch(x2,y2,z2,x1,y1,z1):

    angle = math.asin((x2-x1)/(math.sqrt((pow(x2-x1,2))+pow(z2-z1,2))))
    angle = math.degrees(angle)
    print(angle)
    # if(angle < -76):
    #     angle = -76
    #
    # elif(angle > 17):
    #     angle = 17

    print(angle)
    return angle




def angleRShoulderRoll(x2,y2,z2,x1,y1,z1):

    angle = math.asin((z2-z1)/(math.sqrt((pow(z2-z1,2))+pow(y2-y1,2))))
    angle = math.degrees(angle)
    print(angle)
    # if(angle < -119):
    #     angle = -119
    #
    # elif(angle > 119):
    #     angle = 119

    print(angle)
    return angle





def angleRElbowPitch(x2,y2,z2,x1,y1,z1):
    angle = angle = math.asin((x2-x1)/(math.sqrt((pow(x2-x1,2))+pow(z2-z1,2))))
    angle = math.degrees(angle)
    print(angle)
    # if(angle < 2):
    #     angle = 2
    #
    # elif(angle > 88):
    #     angle = 88
    print(angle)
    return angle


def angleRElbowRoll(x2,y2,z2,x1,y1,z1):
    angle = math.asin((z2 - z1) / (math.sqrt((pow(z2 - z1, 2)) + pow(y2 - y1, 2))))
    angle = math.degrees(angle)
    print(angle)



# angleRShoulderPitch(0.03568992,0.5751851,2.444758,0.274239,0.6649151,2.406888 )
# angleRShoulderRoll(0.03568992,0.5751851,2.444758,0.274239,0.6649151,2.406888 )
#
# angleRElbowPitch(0.274239,0.6649151,2.406888, 0.3891994,0.8548476,2.296391)
# angleRElbowRoll(0.274239,0.6649151,2.406888, 0.3891994,0.8548476,2.296391)


angleRShoulderPitch(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603)

angleRShoulderRoll(0.06092434,0.5326838,2.438355, 0.1362722,0.2543808,2.442603)

angleRElbowPitch(0.1362722,0.2543808,2.442603,0.3891994,0.8548476,2.296391)

angleRElbowRoll(0.1362722,0.2543808,2.442603,0.3891994,0.8548476,2.296391)


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