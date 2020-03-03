# -*- coding:utf-8 -*-

import os
import sys

p_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scan_rule_dir = p_dir + os.path.sep + "conf" + os.path.sep + "scan_rule.ini"
payload_dir = p_dir + os.path.sep + "payload"
lib_dir = p_dir + os.path.sep + "lib"



sys.path.append(p_dir)
sys.path.append(lib_dir)
sys.path.append(payload_dir)
sys.path.append(scan_rule_dir)
