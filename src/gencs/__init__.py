
import genmsg.msgs

try:
    from cStringIO import StringIO #Python 2.x
except ImportError:
    from io import StringIO #Python 3.x

# If enabled, many base message types (e.g. vector3, point) will
# be replaced with Unity types (e.g. UnityEngine.Vector3)
USE_UNITY_TYPES = True

MSG_TYPE_TO_CS = {    'byte' : 'sbyte',
                      'char' : 'byte',
                      'bool' : 'bool',
                     'uint8' : 'byte',
                      'int8' : 'sbyte',
                    'uint16' : 'System.UInt16',
                     'int16' : 'System.Int16',
                    'uint32' : 'System.UInt32',
                     'int32' : 'System.Int32',
                    'uint64' : 'System.UInt64',
                     'int64' : 'System.Int64',
                   'float32' : 'float',
                   'float64' : 'double',
                    'string' : 'string',
                      'time' : 'ROSBridgeLib.msg_helpers.Time',
                  'duration' : 'ROSBridgeLib.msg_helpers.Duration'}

# These substitutions are purely for convenience when working with data on the
# Unity side so we we don't have to martial everything all the time. The Unity
# types here are safe to use because they serialize to the same JSON as the msg
# types they replace.
MSG_TO_UNITY = {      'geometry_msgs.Point' : 'UnityEngine.Vector3',
                    'geometry_msgs.Vector3' : 'UnityEngine.Vector3',
                 'geometry_msgs.Quaternion' : 'UnityEngine.Quaternion'}

def base_type_to_base_cs(base_type):
    cs_type = None
    if (genmsg.msgs.is_builtin(base_type)):
        cs_type = MSG_TYPE_TO_CS[base_type]
    elif (len(base_type.split('/')) == 1):
        if (genmsg.msgs.is_header_type(base_type)):
            cs_type = 'ROSBridgeLib.std_msgs.Header'
        else:
            cs_type = base_type
    else:
        pkg = base_type.split('/')[0]
        msg = base_type.split('/')[1]
        cs_type = '%s.%s'%(pkg, msg)
        if USE_UNITY_TYPES and cs_type in MSG_TO_UNITY:
            cs_type = MSG_TO_UNITY[cs_type]
    return cs_type

def msg_type_to_cs(type):
    """
    Converts a message type (uint32, std_msgs/String, etc.) into the C#
    declaration for that type (int, System.String, etc.)

    @param type: The message type
    @type type: str
    @return: The C# declaration
    @rtype: str
    """
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(type)
    cs_type = base_type_to_base_cs(base_type)

    if (is_array):
        if (array_len is None):
            return 'System.Collections.Generic.List<%s> '%(cs_type)
        else:
            return '%s[] '%(cs_type)
    else:
        return cs_type

def _escape_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    return s

def escape_message_definition(definition):
    lines = definition.splitlines()
    if not lines:
        lines.append('')
    s = StringIO()
    for line in lines:
        line = _escape_string(line)
        s.write('%s\\n\\\n'%(line))

    val = s.getvalue()
    s.close()
    return val

def default_value(type):
    """
    Returns the value to initialize a message member with. 0 for integer types, 0.0 for floats,
    false for bool, empty string for others.

    @param type: The type
    @type type: str
    """
    if type in ['byte', 'int8', 'int16', 'int32', 'int64', 'char', 'uint8', 'uint16', 'uint32', 'uint64']:
        return '0'
    elif type == 'float32':
        return '0.0f'
    elif type == 'float64':
        return '0.0'
    elif type == 'bool':
        return 'false'

    return ""

def array_initializer(type):
    (base_type, is_array, array_len) = genmsg.msgs.parse_type(type)
    cs_type = base_type_to_base_cs(base_type)
        
    if not is_array:
        return ""
    
    if array_len is None:
        return "new System.Collections.Generic.List<%s>()"%(cs_type)
    else:
        return "new %s[%s]"%(cs_type, array_len)

