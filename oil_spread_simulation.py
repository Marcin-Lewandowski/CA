import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap


# Funkcje obsługujące polecenia z menu
def otworz_mape():
    filepath = filedialog.askopenfilename(title="Otwórz mapę")
    if filepath:

        # Wczytaj plik BMP
        img = Image.open(filepath)

        # Pobierz wymiary obrazu
        szerokosc, wysokosc = img.size

        licznik_komorek_brzegowych = 0
        licznik_komorek_oceanu = 0
        licznik_komorek_ladu = 0
        licznik_komorek_ropy = 0

        # Tworzenie macierzy wypełnionej zerami
        macierz = np.zeros((wysokosc, szerokosc))


        # Iteruj przez każdy piksel i pobierz jego kolor w formacie RGB
        for x in range(szerokosc):
            for y in range(wysokosc):
                pixel_color = img.getpixel((x, y))
                if pixel_color == (0,0,255):
                    licznik_komorek_oceanu += 1
                    macierz[y, x] = 0.1
                    #print("To jest ocean ", licznik)
                if pixel_color == (0,255,0):
                    licznik_komorek_ladu += 1
                    macierz[y, x] = 0
                    #print("To jest ląd ", licznik)
                elif pixel_color == (250,200,50):
                    licznik_komorek_brzegowych += 1
                    macierz[y, x] = 2
                    #print("To jest brzeg ", licznik)
                elif pixel_color == (0,0,0):
                    licznik_komorek_ropy += 1
                    macierz[y, x] = 9
                #print(f"Piksel ({x}, {y}): RGB = {pixel_color}")


        # Zamknij plik BMP
        img.close()
        #Czyszczenie obszaru Canvas
        canvas.delete("all")


        for i in range(len(macierz)):
            for j in range(len(macierz[0])):
                value = macierz[i][j]



                color = get_color(value)



                canvas.create_rectangle(
                    j * cell_width,
                    i * cell_height,
                    (j + 1) * cell_width,
                    (i + 1) * cell_height,
                    fill=color,
                    outline=""
                )
                '''
                # Wyświetla wartość liczbową w komórce macierzy
                canvas.create_text(
                    j * cell_width + cell_width // 2,
                    i * cell_height + cell_height // 2,
                    text=str(value),
                    fill="white" if color == "black" else "black"
                )
                
                
                

        print()
        print("Liczba komórek oceanu: ", licznik_komorek_oceanu)
        print()
        print("Liczba komórek lądu: ", licznik_komorek_ladu)
        print()
        print("Liczba komórek brzegowych: ", licznik_komorek_brzegowych)
        print()
        print("Liczba komórek ropy: ", licznik_komorek_ropy)
        '''

# Funkcja do przypisywania kolorów na podstawie wartości
def get_color(value):
    if value == 0.1:
        return "blue"
    elif  value == 0:
        return "green"
    elif value == 2:
        return "yellow"
    else:
        return "black"


def wyjdz():
    root.quit()

# Tworzenie głównego okna o rozmiarze 800x600 pikseli
root = tk.Tk()
root.title("Oil spreading simulation")
root.geometry("1800x960")

# Tworzenie płótna
canvas = tk.Canvas(root, width=1800, height=960)
canvas.pack()

# Wyświetlanie macierzy w formie graficznej
cell_width = 4
cell_height = 4


# Tworzenie paska menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Tworzenie menu "Plik"
plik_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Plik", menu=plik_menu)

# Dodawanie opcji do menu "Plik"
plik_menu.add_command(label="Otwórz mape", command=otworz_mape)
plik_menu.add_separator()
plik_menu.add_command(label="Wyjdź", command=wyjdz)

# Uruchomienie głównej pętli programu
root.mainloop()












































































'''


# Funkcja wyświetla mapę z przypisanymi kolorami do wartości liczbowych
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
'''

