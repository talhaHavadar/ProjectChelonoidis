from datetime import datetime

COMMAND_TYPE_JOYSTICK = 0
COMMAND_TYPE_MOVEMENT_CONTROL = 0
COMMAND_TYPE_ULTRASONIC_SENSOR = 1
<<<<<<< HEAD
COMMAND_TYPE_AUTOPILOT = 2
=======
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367

def parseCommandString(command_string):
    start_index = command_string.find("#CMD#")
    end_index = command_string.find("#END#")
    command_body = command_string[(start_index+len("#CMD#")):end_index]
    command_type, arguments = command_body.split("|")
    action_time = None
    if arguments.find("@") != -1:
        arguments, action_time = arguments.split("@")
    arguments = arguments.split(";")
    if command_type == "JS" or command_type == "MC":
        command_type = COMMAND_TYPE_JOYSTICK
    elif command_type == "US":
        command_type = COMMAND_TYPE_ULTRASONIC_SENSOR
<<<<<<< HEAD
    elif command_type == "AP":
        command_type = COMMAND_TYPE_AUTOPILOT

=======
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367
    return (command_type, arguments, datetime.fromtimestamp(float(action_time)/1000.0) if action_time is not None else None)

class Command(object):

    def __init__(self, command_string):
        # command_string will be like : #CMD#MC|38;39@1491654579794#END#
        self.type, self.arguments, self.time = parseCommandString(command_string)

    def __str__(self):
        return "Type: %s, Arguments: %s, Time: %s" % (self.type, self.arguments, self.time)

class CommandsHandler():

<<<<<<< HEAD
    def __init__(self, pool_size = 20):
        self.movement_commands = list()
        self.sensor_commands = list()
        self.autopilot_commands = list()
=======
    def __init__(self, pool_size = 10):
        self.movement_commands = list()
        self.sensor_commands = list()
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367
        self.pool_size = pool_size

    def addCommand(self, command):
        if command.type == COMMAND_TYPE_JOYSTICK:
            self.__addMovementCommand(command)
        elif command.type == COMMAND_TYPE_ULTRASONIC_SENSOR:
            self.__addSensorCommand(command)
<<<<<<< HEAD
        elif command.type == COMMAND_TYPE_AUTOPILOT:
            self.__addAutopilotCommand(command)
=======
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367

    def lastCommand(self, command_type):
        if command_type == COMMAND_TYPE_JOYSTICK:
            return self.movement_commands[-1] if len(self.movement_commands) > 0 else None
        elif command_type == COMMAND_TYPE_ULTRASONIC_SENSOR:
            return self.sensor_commands[-1] if len(self.sensor_commands) > 0 else None
<<<<<<< HEAD
        elif command_type == COMMAND_TYPE_AUTOPILOT:
            if len(self.autopilot_commands) == 0:
                return None

            cmd_dict = dict()
            max_command = [None, 0]
            for i in range(len(self.autopilot_commands)):
                command = self.autopilot_commands[i]
                if str(command.arguments[-1]) in cmd_dict:
                    cmd_dict[str(command.arguments[-1])] += 1
                    if max_command[1] < cmd_dict[str(command.arguments[-1])]:
                        max_command[0] = command
                        max_command[1] = cmd_dict[str(command.arguments[-1])]
                else:
                    cmd_dict[str(command.arguments[-1])] = 1
                    if max_command[0] is None:
                        max_command[0] = command
                        max_command[1] = 1
                    elif max_command[0] is not None and max_command[1] == 1:
                        max_command[0] = command
            # print("cmd_dict", cmd_dict)
            return max_command[0]
=======

>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367
    def __addMovementCommand(self, command):
        if len(self.movement_commands) == 0:
            self.movement_commands.append(command)
        else:
            if self.movement_commands[-1].time < command.time:
                if len(self.movement_commands) >= self.pool_size:
                    del self.movement_commands[0]
                self.movement_commands.append(command)
<<<<<<< HEAD
    def __addAutopilotCommand(self, command):
        if len(self.autopilot_commands) == 0:
            self.autopilot_commands.append(command)
        else:
            if self.autopilot_commands[-1].time < command.time:
                if len(self.autopilot_commands) >= self.pool_size:
                    del self.autopilot_commands[0]
                self.autopilot_commands.append(command)
=======
>>>>>>> 853bfb8c9094baee2b673d2613ffe77a82c1e367

    def __addSensorCommand(self, command):
        if len(self.sensor_commands) == 0:
            self.sensor_commands.append(command)
        else:
            if self.sensor_commands[-1].time < command.time:
                if len(self.sensor_commands) >= self.pool_size:
                    del self.sensor_commands[0]
                self.sensor_commands.append(command)
