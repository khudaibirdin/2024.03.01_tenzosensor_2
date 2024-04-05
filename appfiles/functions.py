
def func(mb, app):
    from datetime import datetime
    """
    Функция, вызываемая appscheduler, 
    которая считывает информацию с modbus
    """
    data_pressure_from_sensor, dwa = mb.process(configuration=app.config["settings"],
                                           slave_parameters={"slave_id": 4, "register": 46, "register_number": 2}, 
                                           sensor_type=app.config["settings"]["pressure_type"], 
                                           shift=0) # датчик давления
    data_tenzo_raw, data_tenzo_raw_unpack = mb.process(configuration=app.config["settings"],
                            slave_parameters={"slave_id": 16, "register": 62, "register_number": 2}, 
                            sensor_type=app.config["settings"]["tenzo_type"],
                            shift=app.config['shift']) # тензодатчик
    data_tenzo = (data_pressure_from_sensor*0.98*10.2+(4.0*data_tenzo_raw)/(3.14*float(app.config["settings"]["diam_upl"])/10.0*float(app.config["settings"]["diam_upl"])/10.0))/10.2
    if app.config["settings"]["pressure_type"] == "0":
        data_tenzo = (float(app.config["settings"]["davl_sredi"])*0.98*10.2+(4.0*data_tenzo_raw)/(3.14*float(app.config["settings"]["diam_upl"])/10.0*float(app.config["settings"]["diam_upl"])/10.0))/10.2
    app.config['data_tenzo_raw_unpack'] = data_tenzo_raw_unpack
    app.config['data_pressure'] = data_pressure_from_sensor
    app.config['data_tenzo'] = data_tenzo
    app.config['data_tenzo_raw'] = data_tenzo_raw
    print(data_tenzo, app.config['max_pressure'])
    if abs(data_tenzo) > abs(app.config['max_pressure']):
        app.config['max_pressure'] = data_tenzo
        print(app.config['max_pressure'])
    if data_tenzo_raw >= float(app.config["settings"]["v1_transformed_exp_begin"]):
        app.config["data_massive"].append(data_tenzo)
        app.config["time_massive"].append(datetime.now())


def make_document(app):
    import matplotlib.pyplot as plt
    from docxtpl import DocxTemplate, InlineImage
    from datetime import date
    import docx
    from docx.shared import Inches
    from os import startfile
    plt.plot(app.config["time_massive"], app.config["data_massive"], label='Давление, МПа')
    plt.grid(True)
    plt.xlabel("Время")
    plt.ylabel("Давление, МПа")
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.legend()
    plt.savefig('user/grafic1.png')
    plt.clf()
    plt.close()
    app.config["data_massive"].clear()
    app.config["time_massive"].clear()
    doc = DocxTemplate("user/shablon.docx")
    doc_graphic1 = InlineImage(doc, image_descriptor='user/grafic1.png', width=docx.shared.Mm(150))
    context = {'doc_date': date.today().strftime('%d.%m.%y'),
               'doc_filial': app.config["settings"]["filial"],
               'doc_naim': app.config["settings"]["naim"],
               'doc_tip': app.config["settings"]["tip"],
               'doc_zavod': app.config["settings"]["zavod"],
               'doc_zav_nomer': app.config["settings"]["zav_nomer"],
               'doc_techn_nom': app.config["settings"]["techn_nom"],
               'doc_god': app.config["settings"]["god"],
               'doc_pruzhina': app.config["settings"]["pruzhina"],
               'doc_diam_upl': app.config["settings"]["diam_upl"],
               'doc_rab_davl': app.config["settings"]["rab_davl"],
               'doc_ust_davl': app.config["settings"]["ust_davl"],
               'doc_davl_sredi': app.config["settings"]["davl_sredi"],
               'doc_mesto_ust': app.config["settings"]["mesto_ust"],
               'doc_graphic1': doc_graphic1,
               'doc_d_srab': round(app.config['max_pressure'], 2),
               'doc_dolzhn': app.config["settings"]["dolzhn"],
               'doc_person': app.config["settings"]["person"]}
    doc.render(context)
    app.config["settings"]["doc_num"] = str(int(app.config["settings"]["doc_num"]) + 1)
    doc.save(f"documents\Протокол№{app.config["settings"]["doc_num"]}.docx")
    try:
        startfile(f"documents\Протокол№{app.config["settings"]["doc_num"]}.docx")
    except:
        startfile(f"documents\Протокол№{app.config["settings"]["doc_num"]}.docx")