import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap

# Rozmiar planszy
wysokosc = 160
szerokosc = 200

# Inicjalizacja planszy jako tablicy numpy (0 - martwa komórka, 1 - żywa komórka)
plansza = np.random.choice([0, 1], size=(wysokosc, szerokosc), p=[0.67, 0.33])

# Zmienna do przechowywania informacji o stanie animacji (pauza/kontynuacja)
animacja_aktywna = True

# Funkcja do wykonywania kroku symulacji
def krok_symulacji(plansza):
    nowa_plansza = np.copy(plansza)
    for i in range(wysokosc):
        for j in range(szerokosc):
            sasiedzi = plansza[max(0, i-1):min(wysokosc, i+2), max(0, j-1):min(szerokosc, j+2)]
            suma_sasiadow = np.sum(sasiedzi) - plansza[i, j]
            if plansza[i, j] == 1:
                if suma_sasiadow < 2 or suma_sasiadow > 3:
                    nowa_plansza[i, j] = 0
            else:
                if suma_sasiadow == 3:
                    nowa_plansza[i, j] = 1
    return nowa_plansza

# Funkcja do obsługi przycisku "Pauza"
def pauza(event):
    global animacja_aktywna
    animacja_aktywna = False

# Funkcja do obsługi przycisku "Kontynuacja"
def kontynuuj(event):
    global animacja_aktywna
    animacja_aktywna = True

# Definicja własnej mapy kolorów RGB (tu używamy kolorów niebieskiego i czerwonego)
colors = [(0.4, 0, 1), (1, 1, 0)]
cmap = ListedColormap(colors)

# Inicjalizacja animacji
fig, ax = plt.subplots()


mat = ax.matshow(plansza, cmap=cmap)  # Użyj własnej mapy kolorów

# Utworzenie przycisków "Pauza" i "Kontynuacja"
ax_pauza = plt.axes([0.7, 0.01, 0.1, 0.04])
ax_kontynuuj = plt.axes([0.81, 0.01, 0.1, 0.04])
przycisk_pauza = Button(ax_pauza, 'Pauza')
przycisk_kontynuuj = Button(ax_kontynuuj, 'Kontynuacja')

# Funkcja do aktualizacji planszy w animacji
def update(frame):
    global plansza, animacja_aktywna
    if animacja_aktywna:
        plansza = krok_symulacji(plansza)
        mat.set_data(plansza)
    return [mat]

# Utworzenie animacji
ani = animation.FuncAnimation(fig, update, frames=100, interval=200, blit=True)

# Przypisanie funkcji do przycisków
przycisk_pauza.on_clicked(pauza)
przycisk_kontynuuj.on_clicked(kontynuuj)

plt.show()