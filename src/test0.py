import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
from Utils import *
import time
z = 1.45

rospy.init_node('flight')

points = [((-0.2, -0.2, z), 1),
          ((0.5, -0.2, z), 1),
          ((0.5, 0.7, z), 1),
          ((-0.2, 0.7, z), 1),
          ((0, 0, z), 1)]

copter = Copter(markers_flipped=False)

copter.takeoff(z)

for point, dt in points:
    copter.go_to_point(point)
    time.sleep(dt)

copter.land()
