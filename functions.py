
def func(mb, app):
    """Функция, в которой необходимо прописать опрос датчиков"""
    data = mb.process({"slave_id": 4,
                       "register": 46,
                       "register_number": 1})
    app.config['data'] = data
