import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from matplotlib.lines import Line2D

id_device = "1"

with open('data/Sensors_Data.json', 'r', encoding='utf-8') as file:
    sensors_data = json.load(file)
    device = sensors_data[id_device]

for data in device:
    times = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in device[data]['time']]
    temps = [float(temp) for temp in device[data]['temp']]
    pres = [float(p) for p in device[data]['pres']]

    # Установка значений для красной зоны
    threshold_low = 3
    threshold_high = 8

    # Построение графика
    plt.figure(figsize=(10, 6))

    # График температуры
    for i in range(len(temps) - 1):
        print(temps[i])
        if (temps[i] < 21 and temps[i + 1] < 21) or (temps[i] > 29 and temps[i + 1] > 29):
            plt.plot([times[i], times[i + 1]], [temps[i], temps[i + 1]], linewidth=2, color='#BC3A1D')
        elif temps[i] > 21 and temps[i + 1] > 21 and temps[i] < 29 and temps[i + 1] < 29:
            plt.plot([times[i], times[i + 1]], [temps[i], temps[i + 1]], linewidth=2, color='#43C5E2')
        elif temps[i] < 21 and temps[i + 1] > 21 and temps[i + 1] < 29:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [temps[i], 21], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [21, temps[i + 1]], linewidth=2, color='#43C5E2')
        elif temps[i] > 21 and temps[i + 1] < 21 and temps[i] < 29:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [temps[i], 21], linewidth=2, color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [21, temps[i + 1]], linewidth=2, color='#BC3A1D')
        elif temps[i] > 29 and temps[i + 1] < 29 and temps[i + 1] > 21:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [temps[i], 29], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [29, temps[i + 1]], linewidth=2, color='#43C5E2')
        elif temps[i] < 29 and temps[i + 1] > 29 and temps[i] > 21:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [temps[i], 29], linewidth=2, color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [29, temps[i + 1]], linewidth=2, color='#BC3A1D')
        elif temps[i] < 21 and temps[i + 1] > 29:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=600)], [temps[i], 21], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=600), times[i + 1] - timedelta(milliseconds=300)], [21, 29],
                     color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=300), times[i + 1]], [29, temps[i + 1]], linewidth=2, color='#BC3A1D')
        elif temps[i] > 29 and temps[i + 1] < 21:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=600)], [temps[i], 21], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=600), times[i + 1] - timedelta(milliseconds=300)], [21, 29],
                     color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=300), times[i + 1]], [29, temps[i + 1]], linewidth=2, color='#BC3A1D')

    # Границы для температуры
    plt.axhline(y=21, linewidth=1.5, color='black', linestyle='dashed')
    plt.axhline(y=29, linewidth=1.5, color='black', linestyle='dashed')

    # График давления
    for i in range(len(pres) - 1):
        if (pres[i] < 3 and pres[i + 1] < 3) or (pres[i] > 9 and pres[i + 1] > 9):
            plt.plot([times[i], times[i + 1]], [pres[i], pres[i + 1]], linewidth=2, color='#BC3A1D')
        elif pres[i] > 3 and pres[i + 1] > 3 and pres[i] < 9 and pres[i + 1] < 9:
            plt.plot([times[i], times[i + 1]], [pres[i], pres[i + 1]], linewidth=2, color='#5A5CA8')
        elif pres[i] < 3 and pres[i + 1] > 3 and pres[i + 1] < 9:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [pres[i], 3], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [3, pres[i + 1]], linewidth=2, color='#5A5CA8')
        elif pres[i] > 3 and pres[i + 1] < 3 and pres[i] < 9:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [pres[i], 3], linewidth=2, color='#5A5CA8')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [3, pres[i + 1]], linewidth=2, color='#BC3A1D')
        elif pres[i] > 9 and pres[i + 1] < 9 and pres[i + 1] > 3:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [pres[i], 9], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [9, pres[i + 1]], linewidth=2, color='#5A5CA8')
        elif pres[i] < 9 and pres[i + 1] > 9 and pres[i] > 3:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=500)], [pres[i], 9], linewidth=2, color='#5A5CA8')
            plt.plot([times[i + 1] - timedelta(milliseconds=500), times[i + 1]], [9, pres[i + 1]], linewidth=2, color='#BC3A1D')
        elif pres[i] < 3 and pres[i + 1] > 9:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=600)], [pres[i], 3], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=600), times[i + 1] - timedelta(milliseconds=300)], [3, 9],
                     color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=300), times[i + 1]], [9, pres[i + 1]], linewidth=2, color='#BC3A1D')
        elif pres[i] > 9 and pres[i + 1] < 3:
            plt.plot([times[i], times[i + 1] - timedelta(milliseconds=600)], [pres[i], 3], linewidth=2, color='#BC3A1D')
            plt.plot([times[i + 1] - timedelta(milliseconds=600), times[i + 1] - timedelta(milliseconds=300)], [3, 9],
                     color='#43C5E2')
            plt.plot([times[i + 1] - timedelta(milliseconds=300), times[i + 1]], [9, pres[i + 1]], linewidth=2, color='#BC3A1D')

    # Границы для давления
    plt.axhline(y=3, linewidth=1.5, color='black', linestyle='dashed')
    plt.axhline(y=9, linewidth=1.5, color='black', linestyle='dashed')

    custom_lines = [Line2D([0], [0], linewidth=2, color='#43C5E2', lw=2),
                    Line2D([0], [0], linewidth=2, color='#5A5CA8', lw=2),
                    Line2D([0], [0], linewidth=2, color='#BC3A1D', lw=2),
                    Line2D([0], [0], linewidth=2, color='black', linestyle='dashed')]
    plt.legend(custom_lines, ['Температура', 'Давление', 'Выход за предел', 'Пороги'])

    # Настройка графика
    plt.xlabel('Время')
    plt.ylabel('Значение')
    plt.title('График температуры и давления')
    plt.grid(True)

    # Отображение графика
    plt.show()
