from tkinter import Tk, Label, Button, Entry, Checkbutton, BooleanVar
from tkinter.messagebox import showinfo
from formulas import *
from math import *


Hz = 6371  # TODO keijgfhsjgeoije
FONT = ("Arial Bold", 14)
parameters_satellite = (('Масса КА', 'кг'), ('Масса РТ', 'кг'), ('Тяга ДУ', 'Н'), ('Удельный импульс ДУ', 'сек'))

initial_orbit_parameters = [
    ('Высота орбиты', 'км'),
    ('Наклонение', 'град'),
    ('Прямое восхождение восходящего узла', 'град'),
    ('Аргумент широты перигея', 'град')
]

final_orbit_parameters = [
    ('Высота орбиты', 'км'),
    ('Прямое восхождение восходящего узла', 'град'),
    ('Аргумент широты перигея', 'град')
]

indicators_satellite = (
    ('Конечная масса КА', 'кг'),
    ('Затраты РТ', 'кг'),
    ('Остаток РТ', 'кг'),
    ('Начальный запас dV', 'м/с'),
    ('Остаток dV', 'м/с')
)


def create_block_with_data(cur_row, name_block, name_labels):
    lbl = Label(window, text=name_block, font=("Arial Bold", 20))
    lbl.grid(column=0, row=cur_row, )
    cur_row += 1
    for idx, name_lbl in enumerate(name_labels):
        Label(window, text=name_lbl[0], font=FONT, ).grid(column=0, row=idx + cur_row, sticky="w")
        Label(window, text=name_lbl[1], font=FONT).grid(column=2, row=idx + cur_row, sticky="w")

    cur_row += len(parameters_satellite)
    return cur_row


def get_values_from_fields():
    data = dict()
    try:
        data.update({'m_KA': float(m_KA.get())})
        data.update({'m_RT': float(m_RT.get())})
        data.update({'P': float(P.get())})
        data.update({'I': float(I.get())})

        data.update({'m_RT': float(m_RT.get())})
        data.update({'h_1': float(h_1.get())})
        data.update({'longitude_ascending_node_1': float(longitude_ascending_node_1.get())})
        data.update({'argument_periapsis_1': float(argument_periapsis_1.get())})

        data.update({'h_2': float(h_2.get())})
        data.update({'longitude_ascending_node_2': float(longitude_ascending_node_2.get())})
        data.update({'argument_periapsis_2': float(argument_periapsis_2.get())})

    except ValueError:
        print('Ошибка ввода данных!!!')
        exit()
    return data


def create_interface():
    cur_row = 0

    cur_row = create_block_with_data(cur_row, 'Параметры КА', parameters_satellite)
    cur_row = create_block_with_data(cur_row, 'Параметры начальной орбиты', initial_orbit_parameters)
    create_block_with_data(cur_row, 'Параметры конечной орбиты', final_orbit_parameters)


def enter_result(*args):
    create_block_with_data(cur_row=18, name_block='Показатели КА', name_labels=indicators_satellite)
    for idx, row in enumerate(range(19, 24)):
        Label(window, text=round(args[idx], 3), font=FONT).grid(column=1, row=row, )

    create_block_with_data(cur_row=24, name_block='Затраты Характеристической скорости', name_labels=(('dV', 'м/с'),))
    Label(window, text=round(args[-1], 3), font=FONT).grid(column=1, row=25, )


def calculate():
    data = get_values_from_fields()
    I = data.get('I')
    print(I)
    m_1 = data.get('m_KA')
    m_2 = data.get('m_KA') - data.get('m_RT')
    max_dV = Tsialkovskys_formula(I, m_1, m_2)

    h_1 = data.get('h_1')
    h_2 = data.get('h_2')
    ra_1 = Hz + h_1
    rp_1 = Hz + h_1

    if value_change_altitude.get():
        dh = abs(h_2 - h_1)
        min_dV_change_apogee = change_apogee_altitude(ra_1, rp_1, dh)
        ra_1 += dh
        min_dV_change_perigee = change_perigee_altitude(ra_1, rp_1, dh)
        min_dV = min_dV_change_perigee + min_dV_change_apogee


    elif value_longitude_ascending_node.get():
        longitude_ascending_node_1 = data.get('longitude_ascending_node_1')
        longitude_ascending_node_2 = data.get('longitude_ascending_node_2')
        dOmega = abs(longitude_ascending_node_1 - longitude_ascending_node_2)
        min_dV = change_right_ascension_ascending_node(dOmega, ra_1, rp_1)

    # elif value_argument_periapsis.get():
    #     pass

    else:
        showinfo(title="Info", message='Выберите маневр')
        return

    dV_remaining = max_dV - min_dV
    if dV_remaining < 0:
        showinfo(title="Info", message='Запасов ракетного топлива не достаточно для маневра')

    value_finished_mass_KA = finished_mass_KA(I, m_2, dV_remaining)
    mass_remaining_rocket_fuel = value_finished_mass_KA - m_2
    expenses_rocket_fuel = data.get('m_RT') - mass_remaining_rocket_fuel

    enter_result(
        value_finished_mass_KA,
        mass_remaining_rocket_fuel,
        expenses_rocket_fuel,
        max_dV,
        dV_remaining,
        min_dV
    )


window = Tk()
window.geometry('1000x1000')
window.title("Расчет параметров орбитального маневра")

create_interface()

m_KA = Entry(window, width=10)
m_KA.grid(column=1, row=1)
m_RT = Entry(window, width=10)
m_RT.grid(column=1, row=2)
P = Entry(window, width=10)
P.grid(column=1, row=3)
I = Entry(window, width=10)
I.grid(column=1, row=4)

h_1 = Entry(window, width=10)
h_1.grid(column=1, row=6)
i_1 = Entry(window, width=10)
i_1.grid(column=1, row=7)
longitude_ascending_node_1 = Entry(window, width=10)
longitude_ascending_node_1.grid(column=1, row=8)
argument_periapsis_1 = Entry(window, width=10)
argument_periapsis_1.grid(column=1, row=9)

h_2 = Entry(window, width=10)
h_2.grid(column=1, row=11)
longitude_ascending_node_2 = Entry(window, width=10)
longitude_ascending_node_2.grid(column=1, row=12)
argument_periapsis_2 = Entry(window, width=10)
argument_periapsis_2.grid(column=1, row=13)

value_change_altitude = BooleanVar()
value_longitude_ascending_node = BooleanVar()
# value_argument_periapsis = BooleanVar()

def insert_value():
    m_KA.insert(0, '250')
    m_RT.insert(0, '200')
    P.insert(0, '1')
    I.insert(0, '100')
    h_1.insert(0, '800')
    i_1.insert(0, '63')
    longitude_ascending_node_1.insert(0, '90')
    argument_periapsis_1.insert(0, '90')
    h_2.insert(0, '900')
    longitude_ascending_node_2.insert(0, '90')
    argument_periapsis_2.insert(0, '90')


insert_value()


change_altitude = Checkbutton(
    window,
    text='Изменение высоты орбиты без изменения долготы восходящего узла и аргумента широты',
    variable=value_change_altitude,
    offvalue=False,
    onvalue=True
)
change_altitude.grid(column=0, row=14)

select_2 = Checkbutton(
    window,
    text='Изменение долготы восходящего узла без изменения высоты орбиты и аргумента широты.',
    variable=value_longitude_ascending_node,
    offvalue=False,
    onvalue=True
)
select_2.grid(column=0, row=15)

# select_3 = Checkbutton(
#     window,
#     text='Изменение аргумента широты без изменения высоты орбиты и долготы восходящего узла.',
#     variable=value_argument_periapsis,
#     offvalue=False,
#     onvalue=True
# )
# select_3.grid(column=0, row=16)

Button(text='Рассчитать', command=calculate).grid(column=2, row=17)

window.mainloop()
