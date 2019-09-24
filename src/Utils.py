import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time
import pigpio
from rpi_ws281x import Color
from std_msgs.msg import String

led_colors = {
    "takeoff":Color(200,0,200), 
    "wait":Color(0,90,140), 
    "rec":Color(225,50,5), 
    "land":Color(225,90,0),
    "none":Color(0, 0, 0),
    "red":Color(200, 20, 0),
    "green":Color(0, 200, 20),
    "blue":Color(0, 20, 200),
    "yellow":Color(160, 120, 0)
}

class Magnet:
    def __init__(self, pin=22):
        self.pi = pigpio.pi()
        self._pin = pin
        self.pi.set_mode(self._pin, pigpio.OUTPUT)
        # pi.write(self._pin, 0)
    def on(self):
        self.pi.write(self._pin, 1)
    def off(self):
        self.pi.write(self._pin, 0)

class IR:
    def __init__(self, topic="/ir_reciv"):
        self.sub = rospy.Subscriber(topic, String, self._callback)
        self.data = "none"
    def _callback(self, msg):
        self.data = msg.data
    def waitData(self, l):
        print("wait")
        d = "none"
        while True:
            a = self.data
            if a != "none" and a in l:
                d = a
                break
        return d
            
        
# class RosTools:
#     def __init__(self, node_name="flight"):
#         rospy.init_node(node_name)
#         self.node_name = node_name

class ColorReg:
    def __init__(self, topic="/color_reg"):
        self.sub = rospy.Subscriber(topic, String, self._callback)
        self.color = "none"
    def _callback(self, msg):
        self.color = msg.data

class Copter:
    def __init__(self, markers_flipped=False):
        self.get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy('navigate', srv.Navigate)
        self.navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
        self.set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
        self.set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
        self.set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
        self.set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
        self.land_serv = rospy.ServiceProxy('land', Trigger)
        self.arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
        self.zero_z = 0
        self.markers_flipped = markers_flipped
        self.start_coord = (0, 0, 1.5)
        # self.tolerance = 0.2
    def get_distance(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    def callib_zero_z(self):
        """
        Zero floor level
        """
        count = 20
        zz = 0
        for i in range(count):
            telem = self.get_telemetry(frame_id="aruco_map")
            zz += telem.z
            rospy.sleep(0.15)
        self.zero_z = zz/count
        print("zero_z", self.zero_z)
        

    def get_telemetry_aruco(self, floor=False):
        telem =  self.get_telemetry(frame_id="aruco_map")
        return telem

    def navigate_aruco(self, x=0, y=0, z=0, yaw=float('nan'), speed=0.35,  floor=False):
        return self.navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id='aruco_map')

    def takeoff(self, z):
        telem = self.get_telemetry()
        print(telem)
        self.navigate(z=2, speed=1.5, frame_id="body", auto_arm=True)
        print("Sleeping")
        rospy.sleep(7)
        self.navigate_aruco(x=0.5, y=0.5, z=z, speed=0.5)
        print("aruco")

    def go_to_point(self, point, yaw=float('nan'), speed=0.4, tolerance=0.218, floor=False): #0.185
        self.navigate_aruco(x=point[0], y=point[1], z=point[2], yaw=yaw, speed=speed,  floor=floor)
        while True:
            telem = self.get_telemetry_aruco(floor=floor)
            print(self.get_distance(point[0], point[1], point[2], telem.x, telem.y, telem.z))
            if self.get_distance(point[0], point[1], point[2], telem.x, telem.y, telem.z) < tolerance:
                break
            rospy.sleep(0.15)
    def land(self):
        self.land_serv()
        rospy.sleep(5)
        self.arming(False)

