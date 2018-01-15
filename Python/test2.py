import time
import argparse
from naoqi import ALProxy

import math




def main(robotIP = "172.30.248.162", PORT = 9559):
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

    

    

    motionProxy.setStiffnesses("Body", 0.0)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Example showing multiple trajectories
    # Interpolates the head yaw to 1.0 radian and back to zero in 2.0 seconds
    # while interpolating HeadPitch up and down over a longer period.
    names      = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"]
    # Each joint can have lists of different lengths, but the number of
    # angles and the number of times must be the same for each joint.
    # Here, the second joint ("HeadPitch") has three angles, and
    # three corresponding times.
    angleLists  = [[(80-0.89)*almath.TO_RAD, (80-22.88)*almath.TO_RAD],
                   [(-0.5-15.15)*almath.TO_RAD, (-0.5-69.56)*almath.TO_RAD],
                   [(119.5-82.05)*almath.TO_RAD, (119.5-139.59)*almath.TO_RAD],
                   [(-180+160.94)*almath.TO_RAD, (-180+62.38)*almath.TO_RAD]]
    timeLists   = [[1.0, 3.0], [ 1.0, 3.0], [1.0, 3.0], [1.0, 3.0]]
    isAbsolute  = True
    motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    motionProxy.setStiffnesses("Body", 1.0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="172.30.248.162",
                        help="Robot ip address")
    parser.add_argument("--port", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.ip, args.port)