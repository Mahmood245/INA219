import machine
import utime
from ina219 import INA219

# Initialize I2C
i2c = machine.I2C(1, scl=machine.Pin(20), sda=machine.Pin(19))

# Create an INA219 instance
sensor = INA219(i2c)

# Function to calculate actual voltage considering the voltage divider
def actual_voltage(measured_voltage):
    divider_ratio = (4.67 + 5.6) / 5.6  # (R1 + R2) / R2
    return measured_voltage * divider_ratio

while True:
    try:
        # Measure voltage and current
        measured_voltage = sensor.voltage()
        voltage = actual_voltage(measured_voltage)
        adjusted_voltage = voltage / ((4.67 + 5.6) / 5.6)
        current = sensor.current()

        # Print results
        print(f"Adjusted Voltage: {adjusted_voltage:.2f} V, Current: {current:.2f} mA")

        # Check for over-voltage
        if adjusted_voltage > 14:
            print("Warning! Voltage exceeds 14V!")

        utime.sleep(2)
    except Exception as e:
        print(f"Error: {e}")