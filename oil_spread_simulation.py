import tkinter as tk
from tkinter import Menu
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np




filepath = 'C:\\kodilla\\CA\\grafiki\\tescik1.bmp'
#Dyfuzja jako stan początkowy rozpływu ropy: kierunek = 0
kierunek = 0

# Funkcja otwiera mapę, tworzy pierwszą macierz i tworzy obraz morza, lądu  i komórek brzegowych
def otworz_mape():

    global macierz  # Dostęp do zmiennej globalnej
    filepath = filedialog.askopenfilename(title="Otwórz mapę")
    if filepath:

        # Wczytaj plik BMP
        img = Image.open(filepath)

        # Pobierz wymiary obrazu
        szerokosc, wysokosc = img.size

        # Inicjowanie początkowej macierzy
        macierz = tworzenie_macierzy(filepath)

        
        #Czyszczenie obszaru Canvas
        canvas.delete("all")

        # Tworzenie obrazu morza, lądu i komórek brzegowych
        for i in range(wysokosc):
            for j in range(szerokosc):
                pixel_color = img.getpixel((j, i))
                if pixel_color == (0, 0, 255):
                    color = "blue"  # Kolor morza
                elif pixel_color == (0, 255, 0):
                    color = "green"  # Kolor lądu
                elif pixel_color == (250, 200, 50):
                    color = "yellow"  # Kolor komórek brzegowych
                elif pixel_color == (0, 0, 0):
                    color = "black"  # Kolor inny
                



                canvas.create_rectangle(
                    j * cell_width,
                    i * cell_height,
                    (j + 1) * cell_width,
                    (i + 1) * cell_height,
                    fill=color,
                    outline=""
                )
               
    
        # Zamknij plik BMP - tu może być powód problemu !!! ??????
        img.close()





def tworzenie_macierzy(filepath):
    img = Image.open(filepath)
    szerokosc, wysokosc = img.size
    macierz = np.empty((wysokosc, szerokosc), dtype=object)

    for x in range(szerokosc):
        for y in range(wysokosc):
            pixel_color = img.getpixel((x, y))
            if pixel_color == (0, 0, 255):
                macierz[y, x] = ["S", 0]
            elif pixel_color == (0, 255, 0):
                macierz[y, x] = ["L"]
            elif pixel_color == (250, 200, 50):
                macierz[y, x] = ["KB", 0]
            elif pixel_color == (0, 0, 0):
                macierz[y, x] = ["S", 2000]

    img.close()
    return macierz



# Funkcja tworzy iterację symulacji
def iteracja(macierz):
    nowa_macierz = np.copy(macierz)
    wysokosc, szerokosc = macierz.shape

    for i in range(wysokosc):
        for j in range(szerokosc):

            ilosc_ropy = 0

            # Obliczanie sumarycznej ilości ropy w 8 sąsiednich komórkach

            for x in range(-1, 2):
                for y in range(-1, 2):


                    # 0 - Dyfuzja

                    if  i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 0:

                        ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]

                    # 1 - kierunek na Północ

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 1:

                        if x == -1 and y == 0:
                            continue

                        elif x == 1 and y == 0:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]

                    # 2 - kierunek na Południe

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 2:

                        if x == 1 and y == 0:
                            continue

                        elif x == -1 and y == 0:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]

                    # 3 - kierunek na Wschód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 3:

                        if x == 0 and y == 1:
                            continue

                        elif x == 0 and y == -1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]


                    # 4 - kierunek na Zachód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 4:

                        if x == 0 and y == -1:
                            continue

                        elif x == 0 and y == 1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]


                    # 5 - kierunek na północny wschód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 5:

                        if x == -1 and y == 1:
                            continue

                        elif x == 1 and y == -1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]


                    # 6 - kierunek na południowy wschód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 6:

                        if x == 1 and y == 1:
                            continue

                        elif x == -1 and y == -1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]


                    # 7 - kierunek na południowy zachód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 7:

                        if x == 1 and y == -1:
                            continue

                        elif x == -1 and y == 1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]



                    # 8 - kierunek na północny zachód

                    elif i + x >= 0 and i + x < wysokosc and  j + y >= 0  and j + 1 < szerokosc and kierunek == 8:

                        if x == -1 and y == -1:
                            continue

                        elif x == 1 and y == 1:
                            ilosc_ropy = ilosc_ropy + (2 * macierz[i + x][j + y][1])

                        else: 
                            ilosc_ropy = ilosc_ropy + macierz[i + x][j + y][1]


                        


            
            # Wzór na ilość ropy dla komórki morza
            nowa_macierz[i][j][1] = ilosc_ropy / 9



    return nowa_macierz

def rysowanie_mapy(liczba_iteracji):

    global macierz  # Dostęp do zmiennej globalnej


    licznik = 0


    # Wykonujemy n  iteracji [liczba iteracji wpisywana w oknie dialogowym] automatu komórkowego i drukujemy macierz 
    while licznik < liczba_iteracji:
       

        macierz = iteracja(macierz)
        licznik = licznik + 1

        if licznik == liczba_iteracji:

            # Rysuje obraz iteracji symulacji dla powierzchnii morza
            for i in range(len(macierz)):
                    for j in range(len(macierz[0])):
                        value = macierz[i][j]
                        color = get_sim_sea_color(value)
                        canvas.create_rectangle(
                            j * cell_width,
                            i * cell_height,
                            (j + 1) * cell_width,
                            (i + 1) * cell_height,
                            fill=color,
                            outline=""
                        )
        
    




# Funkcja do przypisywania kolorów do początkowej macierzy na podstawie wartości
def get_color(value):
    if value == ["S", 0]:
        return "blue"
    elif  value == ["L"]:
        return "green"
    elif value == ["KB", 0]:
        return "yellow"
    else:
        return "black"
    
# Kolorystyka dla komórek morza
def get_sim_sea_color(value):

    if value[1] >= 100:
        return "black"
    elif value[1] >= 75 and value[1] < 100:
        return "brown"
    elif value[1] >= 50 and value[1] < 75:
        return "purple"
    elif value[1] >= 25 and value[1] < 50:
        return "red"
    elif value[1] >= 15 and value[1] < 25:
        return "orange"
    elif value[1] >= 7 and value[1] < 15:
        return "yellow"
    elif value[1] >= 3 and value[1] < 7:
        return "cyan"
    elif value[1] >= 1 and value[1] < 3:
        return "white"
    elif value[1] < 1:
        return "blue"
    

# Kolorystyka dla komórek brzegowych z zawartością ropy
def get_sim_border_color(value):

    if value[1] > 0 and value[1] <= 5:
        return "red"
    elif value[1] > 5 and value[1] <= 10:
        return "brown"
    else:
        return "black"





def autor():
    pass

def dyfuzja():
    global kierunek
    kierunek = 0

def polnoc():
    global kierunek
    kierunek = 1

def poludnie():
    global kierunek
    kierunek = 2

def wschod():
    global kierunek
    kierunek = 3
    
def zachod():
    global kierunek
    kierunek = 4

def polnocny_wschod():
    global kierunek
    kierunek = 5

def poludniowy_wschod():
    global kierunek
    kierunek = 6

def poludniowy_zachod():
    global kierunek
    kierunek = 7

def polnocny_zachod():
    global kierunek
    kierunek = 8
    






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

# Tworzenie menu "Plik" i "Iteracja" i "Autor"
plik_menu = Menu(menu_bar)
iteracja_menu = Menu(menu_bar)
autor_menu = Menu(menu_bar)
kierunek_menu = Menu(menu_bar)

menu_bar.add_cascade(label="Plik", menu=plik_menu)
menu_bar.add_cascade(label="Iteracja", menu=iteracja_menu)
menu_bar.add_cascade(label="Kierunek wiatru", menu=kierunek_menu)
menu_bar.add_cascade(label="Autor", menu=autor_menu)

# Dodawanie opcji do menu "Plik"
plik_menu.add_command(label="Otwórz mape", command = otworz_mape)
plik_menu.add_separator()
plik_menu.add_command(label="Stwórz macierz", command = tworzenie_macierzy(filepath))
plik_menu.add_separator()
plik_menu.add_command(label="Wyjdź", command=wyjdz)


# Dodawanie opcji do menu Iteracja
iteracja_menu.add_command(label="Iteracja x 2", command=lambda: rysowanie_mapy(2))  # Podaj odpowiednią liczbę iteracji
iteracja_menu.add_separator()

kierunek_menu.add_command(label="Dyfuzja", command=dyfuzja)
kierunek_menu.add_command(label="Północ", command=polnoc)
kierunek_menu.add_command(label="Południe", command=poludnie)
kierunek_menu.add_command(label="Wschód", command=wschod)
kierunek_menu.add_command(label="Zachód", command=zachod)

kierunek_menu.add_command(label="Północny wschód", command=polnocny_wschod)
kierunek_menu.add_command(label="Południowy wschód", command=poludniowy_wschod)
kierunek_menu.add_command(label="Południowy zachód", command=poludniowy_zachod)
kierunek_menu.add_command(label="Północny zachód", command=polnocny_zachod)


# Dodawanie opcji do menu Autor
autor_menu.add_command(label="O autorze", command=autor)
autor_menu.add_separator()


# Dodaj pole tekstowe do wprowadzenia liczby iteracji
iteracje_entry = tk.Entry(root)
iteracje_entry.pack()

# Utwórz funkcję, która będzie wywoływana po kliknięciu przycisku "Start"
def rozpocznij_symulacje():
    # Pobierz wartość wprowadzoną przez użytkownika
    liczba_iteracji = int(iteracje_entry.get())
    
    # Wywołaj funkcję rysowanie_mapy z wprowadzoną liczbą iteracji
    rysowanie_mapy(liczba_iteracji)

# Dodaj przycisk "Start" do rozpoczęcia symulacji
start_button = tk.Button(root, text="Start", command=rozpocznij_symulacje)
start_button.pack()

root.mainloop()