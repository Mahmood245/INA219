from machine import I2C, Pin
import time

class INA219:
    def __init__(self, i2c, addr=0x40):
        self.i2c = i2c
        self.addr = addr
        self._cal_value = 4096
        self._current_divider_mA = 10
        self._power_multiplier_mW = 2
        self._init()

    def _init(self):
        # Configure to max range (32V, 2A)
        self.i2c.writeto_mem(self.addr, 0x00, b'\x39\x9F')
        # Calibrate for 12-bit conversion, 32V and 2A
        self.i2c.writeto_mem(self.addr, 0x05, self._cal_value.to_bytes(2, 'big'))

    def _read(self, reg):
        return int.from_bytes(self.i2c.readfrom_mem(self.addr, reg, 2), 'big')

    def voltage(self):
        value = self._read(0x02) >> 3
        return value * 4 * 0.001  # 4mV per LSB

    def current(self):
        value = self._read(0x04)
        return value / self._current_divider_mA
