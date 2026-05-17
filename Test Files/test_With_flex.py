# Team Fantastic 4

from machine import ADC, Pin
import time


# Define the pin connected to the flex sensor
# The Raspberry Pi Pico pin GP26 (ADC0) connected to the flex sensor
#flex_sensor_pin_thumb =
flex_sensor_pin_pointer = 26
#flex_sensor_pin_middle =


# Initialize ADC on the specified pin
#flex_sensor_thumb = ADC(Pin(flex_sensor_pin_thumb))
#no_flex_thumb = 104  # Calibrate this based on reading at resting position
flex_sensor_pointer = ADC(Pin(flex_sensor_pin_pointer))
no_flex_pointer = 104  # Calibrate this based on reading at resting position
#flex_sensor_middle = ADC(Pin(flex_sensor_pin_middle))
#no_flex_middle = 104  # Calibrate this based on reading at resting position


# Calibration
cal = 0
cal_vals = []
while cal < 100:
    analog_reading = flex_sensor_pointer.read_u16()  # Read the raw analog value (0-65535)
    analog_reading = int(analog_reading/200)  # Divide to stabilize reading
    cal_vals.append(analog_reading)
    
    # Print the raw analog reading
    print("Flex sensor reading = ", analog_reading)
    
    cal_max = max(cal_vals)
    cal_min = min(cal_vals)

    time.sleep(.05)
    
    print("cal:", cal)
    cal += 1
    

print("min:", cal_min, "max:", cal_max)
time.sleep(5)



# Main loop
while True:
    analog_reading = flex_sensor_pointer.read_u16()  # Read the raw analog value (0-65535)
    analog_reading = int(analog_reading/200)  # Divide to stabilize reading

    # Print the raw analog reading
    print("Flex sensor reading = ", analog_reading)

    # Print flex direction
    if analog_reading < cal_min:
        print("flexed backward")
    elif analog_reading > cal_max:
        print("flexed forward")
    else:
        print("no flex")

    time.sleep(1)  # Delay for 1000 milliseconds