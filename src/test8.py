import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from Utils import *
import time

rospy.init_node('flight')


z = 2

points = [((0, 0, z), 0),
          ((0, 1, z), 0),
          ((0.7, 1, z), 0),
          ((0.7, 0, z), 0),
          ((1.5, 0, z), 0),
          ((1.5, 1, z), 0),
          ((0.7, 1, z), 0),
          ((0.7, 0, z), 0),
          ((0, 0, z), 1)]

copter = Copter(markers_flipped=False)

copter.takeoff(1.5)

copter.go_to_point((0, 0, z))
time.sleep(3)
for point, dt in points:
    copter.go_to_point(point)
    time.sleep(dt)

copter.land()
