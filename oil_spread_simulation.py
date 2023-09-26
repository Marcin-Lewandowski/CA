import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.colors import ListedColormap


global macierz

# Funkcja otwiera mapę, tworzy pierwszą macierz i tworzy obraz morza, lądu  i komórek brzegowych
def otworz_mape():
    filepath = filedialog.askopenfilename(title="Otwórz mapę")
    if filepath:

        # Wczytaj plik BMP
        img = Image.open(filepath)

        # Pobierz wymiary obrazu
        szerokosc, wysokosc = img.size

        # Tworzenie macierzy wypełnionej zerami
        
        macierz = np.empty((wysokosc, szerokosc), dtype=object)
        #macierz = np.zeros((wysokosc, szerokosc))


        # Iteruj przez każdy piksel i pobierz jego kolor w formacie RGB, tworzy macierz
        for x in range(szerokosc):
            for y in range(wysokosc):
                pixel_color = img.getpixel((x, y))
                if pixel_color == (0,0,255):
                    
                    macierz[y, x] = ["S", 0]

                if pixel_color == (0,255,0):
                    
                    macierz[y, x] = ["L"]
                    
                elif pixel_color == (250,200,50):
                    
                    macierz[y, x] = ["KB", 0]
                    
                elif pixel_color == (0,0,0):
                    
                    macierz[y, x] = ["S", 1000]
               


        # Zamknij plik BMP
        img.close()

        #Czyszczenie obszaru Canvas
        canvas.delete("all")

        # Tworzenie obrazu morza, lądu i komórek brzegowych
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
    return macierz          

# Funkcja do wydruku macierzy
def wydrukuj_macierz(macierz_gotowa):
    for wiersz in macierz_gotowa:
        print(wiersz)
    print("\n")


# Funkcja wyświetla iterację symulacji

def iteracja(macierz_gotowa):
    nowa_macierz = np.copy(macierz_gotowa)
    wysokosc, szerokosc = macierz_gotowa.shape

    for i in range(wysokosc):
        for j in range(szerokosc):



            ilosc_ropy = 0

            # Obliczanie sumarycznej ilości ropy w 8 sąsiednich komórkach

            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x == 0 and y == 0:
                        continue  # Pomijamy komórkę, którą analizujemy

                    if  i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc:
                        ilosc_ropy = ilosc_ropy + macierz_gotowa[i + x][j + y][1]


            nowa_macierz[i][j][1] = ilosc_ropy / 8


            
            #if macierz[i, j] == ["S", 0]:
                # Symulacja rozprzestrzeniania się ropy
                # Tutaj można dodać logikę rozprzestrzeniania się ropy na podstawie sąsiednich komórek
                
                # Dyfuzja
        
            #elif macierz[i, j] == ["KB", 0]:
                # Symulacja rozprzestrzeniania się brzegów
                # Tutaj można dodać logikę rozprzestrzeniania się brzegów na podstawie sąsiednich komórek
                #pass

    return nowa_macierz


# Funkcja do przypisywania kolorów na podstawie wartości
def get_color(value):
    if value == ["S", 0]:
        return "blue"
    elif  value == ["L"]:
        return "green"
    elif value == ["KB", 0]:
        return "yellow"
    else:
        return "black"


def wyjdz():
    root.quit()


def autor():
    pass



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

# Tworzenie menu "Plik" i "Iteracja" i "Autor"
plik_menu = Menu(menu_bar)
iteracja_menu = Menu(menu_bar)
autor_menu = Menu(menu_bar)

menu_bar.add_cascade(label="Plik", menu=plik_menu)
menu_bar.add_cascade(label="Iteracja", menu=iteracja_menu)
menu_bar.add_cascade(label="Autor", menu=autor_menu)

# Dodawanie opcji do menu "Plik"
plik_menu.add_command(label="Otwórz mape", command=otworz_mape)
plik_menu.add_separator()
plik_menu.add_command(label="Wyjdź", command=wyjdz)


# Dodawanie opcji do menu Iteracja
#iteracja_menu.add_command(label="Iteracja - 1", command=krok_symulacji)
iteracja_menu.add_separator()

# Dodawanie opcji do menu Autor
autor_menu.add_command(label="O autorze", command=autor)
autor_menu.add_separator()




macierz_gotowa = otworz_mape()

# Wykonujemy 2 iteracji automatu komórkowego i drukujemy macierz po każdej iteracji
for k in range(2):
    print(f"Iteracja {k + 1}:\n")
    wydrukuj_macierz(macierz_gotowa)
    macierz_gotowa = iteracja(macierz_gotowa)




root.mainloop()


