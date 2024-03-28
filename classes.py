import modbus_tk
import serial
import datetime
from struct import *
from modbus_tk import modbus_rtu
import modbus_tk.defines as cst

class GetModbusData:
    def __init__(self):
        pass


    def _get_data(self, configuration, slave_parameters):
        """
        Опрос modbus регистров
        """
        try:
            master = modbus_rtu.RtuMaster(
            serial.Serial(port="COM"+configuration["port"], 
                          baudrate=9600, 
                          bytesize=8, 
                          parity="N",
                          stopbits=1, 
                          xonxoff=0)
            )
            master.set_timeout(5.0)
            master.set_verbose(True)
            value = master.execute(slave_parameters["slave_id"], cst.READ_HOLDING_REGISTERS, slave_parameters["register"], slave_parameters["register_number"])
            data = unpack('>f', pack('>HH', value[0], value[1]))[0]
            return(data)
        except modbus_tk.modbus.ModbusError as exc:
            pass
        except serial.serialutil.SerialException:
            pass
        except modbus_tk.exceptions.ModbusInvalidResponseError:
            pass


    def process(self, configuration, slave_parameters, sensor_type, shift):
        """
        Получение сырых данных modbus, расшифровка, преобразование
        """
        data = self._get_data(configuration, slave_parameters)
        data_reformated = self._data_processing(data, sensor_type, shift)
        time = datetime.datetime.now()  
        return data_reformated, data


    def _data_processing(self, data, sensor_type, shift):
        """
        Преобразования, в зависимости от типа тензодатчика
        """
        try:
            if sensor_type == "200":
                data_reformated = (data - shift - (-0.071)) * (-40)
            if sensor_type == "2000":
                data_reformated = (data - shift - (-0.068)) * (-394.75)
            if sensor_type == "0":
                data_reformated = 0
            if sensor_type == "25":
                data_reformated = data * 0.25
            if sensor_type == "60":
                data_reformated = data * 0.6
            return data_reformated
        except:
            data_reformated = 0
        