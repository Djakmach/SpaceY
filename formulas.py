from math import *

MU = 398600.44
g = 9.8


def Tsialkovskys_formula(I, m1, m2):
    """
    :param m1: начальная масса
    :param m2: конечная масса
    :param I: удельный импульс (сек)
    """
    dV = I * g * log(m1 / m2)
    return dV


def finished_mass_KA(I, m2, dV):
    return m2 * exp(dV / (g * I))


def change_apogee_altitude(ra1, rp1, dra):
    """ Поиск минимальной величины управляющего импульса скорости, обеспечивающего изменение апогейного расстояния
    :param ra1: апогейное расстояние
    :param rp1: перигейное расстояние
    :param dra: величина на которую необходимо изменить апогейное расстояние
    :return dV: величина управляющего импульса скорости
    """
    dV = sqrt(2 * MU / rp1) * (sqrt((ra1 + dra) / (ra1 + rp1 + dra)) - sqrt(ra1 / (ra1 + rp1)))
    return dV


def change_perigee_altitude(ra1, rp1, drp):
    """ Поиск минимальной величины управляющего импульса скорости, обеспечивающего изменение перигейного расстояния
    :param ra1: апогейное расстояние
    :param rp1: перигейное расстояние
    :param drp: величина на которую необходимо изменить апогейное расстояние
    :return dV: величина управляющего импульса скорости
    """
    dV = sqrt(2 * MU / ra1) * (sqrt((rp1 + drp) / (ra1 + rp1 + drp)) - sqrt(rp1 / (ra1 + rp1)))
    return dV


def change_right_ascension_ascending_node(dOmega, ra1, rp1):
    """ Поиск минимальной величины управляющего импульса скорости, обеспечивающего изменение прямого восхождения восходящего узла
    :param dOmega:  величина на которую необходимо изменить прямое восхождение восходящего узла (градусы)
    :param ra1:
    :param rp1:
    :return dV: величина управляющего импульса скорости
    """
    dOmega = dOmega * pi / 180  # перевод в радианы
    a = (ra1 + rp1) / 2  # большая полуось
    e1 = (ra1 - rp1) / (ra1 + rp1)
    p1 = a * (1 - e1)
    dV = 2 * sqrt(MU / p1) * (1 + e1 * cos(dOmega / 2)) * sin(dOmega / 2)
    return dV
