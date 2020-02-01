
## ROS message source code generation for C#
##
## Converts ROS .msg and .srv files in a package into C# implementation

import sys
import os
import genmsg.template_tools

msg_template_map = { 'msg.cs.template':'@NAME@.cs' }
srv_template_map = { 'srv.cs.template':'@NAME@.cs' }

if __name__ == "__main__":
    genmsg.template_tools.generate_from_command_line_options(sys.argv, msg_template_map, srv_template_map)

