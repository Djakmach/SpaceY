from tkinter import Tk, Label, Button, Entry

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


def calculation():
    pass
    # res = f'Привет {value.get()}'
    # lbl.configure(text=res)


def create_block_with_data(window, cur_row, name_block, name_labels):
    lbl = Label(window, text=name_block, font=("Arial Bold", 20))
    lbl.grid(column=1, row=cur_row)
    cur_row += 1
    for idx, name_lbl in enumerate(name_labels):
        lbl = Label(window, text=name_lbl[0], font=FONT, )
        lbl.grid(column=0, row=idx + cur_row)
        value = Entry(window, width=10)
        value.grid(column=1, row=idx + cur_row)
        lbl = Label(window, text=name_lbl[1], font=FONT, )
        lbl.grid(column=2, row=idx + cur_row)
    cur_row += len(parameters_satellite)
    return cur_row

def create_interface():
    window = Tk()
    window.geometry('1000x500')
    window.title("Расчет параметров орбитального маневра")

    cur_row = 0

    cur_row = create_block_with_data(window, cur_row, 'Параметры КА', parameters_satellite)
    cur_row = create_block_with_data(window, cur_row, 'Параметры начальной орбиты', initial_orbit_parameters)
    cur_row = create_block_with_data(window, cur_row, 'Параметры конечной орбиты', final_orbit_parameters)

    window.mainloop()


def main():
    # pass
    create_interface()


if __name__ == '__main__':
    main()
