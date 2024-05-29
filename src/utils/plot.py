import matplotlib.pyplot as plt


def plot_traffic(x, y):
    # Проверяем количество данных
    if len(x) > 1 and len(y) > 1:
        # Если есть достаточно данных, строим линейный график
        plt.plot(x, y)
    elif len(x) == 1 and len(y) == 1:
        # Если данных меньше двух значений, строим точечный график
        plt.scatter(x, y)

    # Настройка осей и отображение графика
    plt.xlabel("Дата")
    plt.ylabel("Трафик")
    plt.title("График трафика")
