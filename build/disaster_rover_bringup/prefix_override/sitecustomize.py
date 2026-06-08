import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sai-abhinay/disaster_ws/src/install/disaster_rover_bringup'
