# -*- coding: utf-8 -*-

import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import time
import math

def get_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

rospy.init_node('flight')
arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)



z = 1 # высота
tolerance = 0.4  # точность проверки высоты (м)

# Запоминаем изначальную точку
start = get_telemetry()

# Взлетаем на 2 м
print navigate(z=z, yaw=float('nan'), speed=0.5, frame_id='body', auto_arm=True)
print("sl")
time.sleep(1.3)
print("sl2")
tolerance = 0.3  # точность проверки прилета (м)
frame_id='aruco_map'

# Летим в точку 1:2:3 в поле ArUco-маркеров
print navigate(frame_id=frame_id, yaw=float('nan'), x=0.2, y=0.2, z=1.45, speed=0.5)
print("ar1")
time.sleep(10)
print("ar2")

print navigate(frame_id=frame_id, yaw=float('nan'), x=0.6, y=0.6, z=1.45, speed=0.5)
print("ar2")
time.sleep(10)
print("ar3")


land()
time.sleep(7)

arming(False)  # дизарм
