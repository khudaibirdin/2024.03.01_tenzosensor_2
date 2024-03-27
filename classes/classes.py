import modbus_tk
import serial
import datetime
from struct import *
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst

class GetModbusData:
    def __init__(self, config):
        self.config = config


    def _get_data(self, param):
        try:
            time = datetime.datetime.now()
            master = modbus_rtu.RtuMaster(
            serial.Serial(port=self.config["port"], 
                          baudrate=9600, 
                          bytesize=8, 
                          parity="N",
                          stopbits=1, 
                          xonxoff=0)
            )
            master.set_timeout(5.0)
            master.set_verbose(True)
            # value1 = master.execute(16, cst.READ_HOLDING_REGISTERS, 62, 2)
            value = master.execute(param["slave_id"], cst.READ_HOLDING_REGISTERS, param["register"], param["register_number"])
            return(value)
        except modbus_tk.modbus.ModbusError as exc:
            pass
        except serial.serialutil.SerialException:
            pass
        except modbus_tk.exceptions.ModbusInvalidResponseError:
            pass
        


    def process(self, param):
        #modbus_master = self.connect()
        data = self._get_data(param)
        import random
        # return unpack('>f', pack('>HH', data[0], data[1]))[0]
        return random.random()
        # data_reformated = self.reformat_data(data, tenzo_sensor_type)
        # time = datetime.datetime.now()  
        # .replace(microsecond=0)

    def data_processing(self, value1):
        pass
            # if tenzo_sensor_type.get() == 0:
                # v1_transformed = (v1 - v1_shift - (-0.071)) * (-40)
            # if tenzo_sensor_type.get() == 1:
                # v1_transformed = (v1 - v1_shift - (-0.068)) * (-394.75)