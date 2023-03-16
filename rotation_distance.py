import logging


class StepperRotationDistance:
    def __init__(self, config):
        self.printer = config.get_printer()

        gcode = self.printer.lookup_object('gcode')
        gcode.register_command("ROTATION_DISTANCE_CALC",
                               self.cmd_ROTATION_DISTANCE_CALC,
                               desc=self.cmd_ROTATION_DISTANCE_CALC_help)
        gcode.register_command("ROTATION_DISTANCE_SAVE",
                               self.cmd_ROTATION_DISTANCE_SAVE,
                               desc=self.cmd_ROTATION_DISTANCE_SAVE_help)


    cmd_ROTATION_DISTANCE_CALC_help = "Adjust rotation distance value based on calibration"
    def cmd_ROTATION_DISTANCE_CALC(self, gcmd):
        stepper_name = gcmd.get('EXTRUDER', None)
        if stepper_name is None:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Missing EXTRUDER value')
            return
        if stepper_name == 'extruder':
            extruder = self.printer.lookup_object('extruder')
            stepper = extruder.extruder_stepper.stepper
        else:
            object_name = f'extruder_stepper {stepper_name}'
            if object_name in self.printer.objects:
                extruder_stepper = self.printer.lookup_object(object_name)
                stepper = extruder_stepper.extruder_stepper.stepper
        if stepper is None:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Invalid EXTRUDER value "%s"'
                              % (stepper_name,))
            return
        extruded = gcmd.get_float('EXTRUDED', None)
        if extruded is None:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Missing EXTRUDED value')
            return
        if extruded < 0:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Invalid EXTRUDED value "%f"'
                              % (extruded,))
            return
        requested = gcmd.get_float('REQUESTED', None)
        if requested is None:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Missing REQUESTED value')
            return
        if requested < 0:
            gcmd.respond_info('ROTATION_DISTANCE_CALC: Invalid REQUESTED value "%f"'
                              % (requested,))
            return
        distance_current, spr = stepper.get_rotation_distance()
        gcmd.respond_info("Extruder '%s' current rotation distance set to %0.6f"
                          % (stepper_name, distance_current))
        distance_new = distance_current * extruded / requested
        toolhead = self.printer.lookup_object('toolhead')
        toolhead.flush_step_generation()
        stepper.set_rotation_distance(distance_new)
        gcmd.respond_info("Extruder '%s' rotation distance set to %0.6f"
                          % (stepper_name, distance_new))

    cmd_ROTATION_DISTANCE_SAVE_help = "Save rotation distance to config"
    def cmd_ROTATION_DISTANCE_SAVE(self, gcmd):
        stepper_name = gcmd.get('EXTRUDER', None)
        if stepper_name is None:
            gcmd.respond_info('ROTATION_DISTANCE_SAVE: Missing EXTRUDER value')
            return
        if stepper_name == 'extruder':
            extruder = self.printer.lookup_object('extruder')
            stepper = extruder.extruder_stepper.stepper
        else:
            object_name = f'extruder_stepper {stepper_name}'
            if object_name in self.printer.objects:
                extruder_stepper = self.printer.lookup_object(object_name)
                stepper = extruder_stepper.extruder_stepper.stepper
        if stepper is None:
            gcmd.respond_info('ROTATION_DISTANCE_SAVE: Invalid EXTRUDER value "%s"'
                              % (stepper_name,))
            return

        distance_current, spr = stepper.get_rotation_distance()
        configfile = self.printer.lookup_object('configfile')
        configfile.set(object_name, 'rotation_distance', distance_current)

        gcmd.respond_info("Extruder '%s' rotation distance set to %0.6f\n"
                          "The SAVE_CONFIG command will update the printer config file"
                          % (stepper_name, distance_current))

def load_config(config):
    return StepperRotationDistance(config)