
def func(mb, app):
    """
    Функция, вызываемая appscheduler, 
    которая считывает информацию с modbus
    """
    data = mb.process({"slave_id": 4,
                       "register": 46,
                       "register_number": 1})
    app.config['data'] = data
