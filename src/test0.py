import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from Utils import *

z = 2

points = [((0, 0, z), 0),
          ((1, 0, z), 0),
          ((1, 1, z), 0),
          ((0, 1, z), 0),
          ((0, 0, z), 0.5)]

copter = Copter(markers_flipped=False)

copter.takeoff()

for point in points:
    copter.go_to_point(point)

copter.land()
