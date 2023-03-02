# Extras

## Usage

Copy `.py` files to `klipper/klippy/extras`

### pid_calibrate_extra and heaters_extra

Add to beginning of `printer.cfg`

```
[heaters_extra]
[pid_calibrate_extra]
```

### fan_extra

Use `[fan_extra]` instead of `[fan]`

### Applying

Restart klipper service, RESTART command won't activate modules!

## Changes

### heaters_extra

`heater` option:

`control: pid_v`

### pid_calibrate_extra

gcode command

`PID_CALIBRATE_EXTRA`

### fan_extra

Scaling fan value between `off_below` and `max_power`. For example with followong config:

```
[fan_extra]
off_below: 0.2
max_power: 0.8
...
```

Calling `M106 S1` will set output to 0.2, `M106 S255` will set output to 0.8, and all values between would be linear scaled accordingly.

## Credits

### https://github.com/Laker87/klipper:

heaters_extra

pid_calibrate_extra
