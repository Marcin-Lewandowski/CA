import tkinter as tk
from tkinter import Menu, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np


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
                elif pixel_color == (200,200,200):
                    color = "grey"
                


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
            elif pixel_color == (200,200,200):
                macierz[y,x] = ["U"]

    img.close()
    return macierz



# Funkcja tworzy iterację symulacji
def iteracja(macierz):
    nowa_macierz = np.copy(macierz)
    wysokosc, szerokosc = macierz.shape
    

    for i in range(wysokosc):
        for j in range(szerokosc):


            # Logika dla komórki morza
            if macierz[i][j][0] == "S":
                
                
                ilosc_ropy = 0
                ikm = 0        # ilosc sąsiednich komórek morza + komórka analizowana
                ikb = 0         # ilosc sąsiednich komórek brzegowych - potrzebne do operacji odejmowania ilości ropy z komórki gdy jest ona w sąsiedztwie komórek brzegowych


                for x in range(-1, 2):
                    for y in range(-1, 2):

                        # sprawdza czy komórki dookoła są komórkami morza, jeśli tak to zmienna ikm zwiększa się o 1    
                        

                        if (0 <= i + x < wysokosc) and (0 <= j + y < szerokosc):

                            # Jeżeli sąsiednia komórka jest komórką morza to ikm zwiększa się o 1 oraz ilość ropy sumuje się
                            if macierz[i + x][j + y][0] == "S":

                                ikm = ikm + 1
                                ilosc_ropy = round(ilosc_ropy + macierz[i + x][j + y][1], 2)
                                #print(" Ilosc komorek morza: ", ikm)

                            else:
                                ikm = ikm + 0



                if ikm == 9:
                    if kierunek == 0:
                            
                        # Wzór na ilość ropy dla komórki morza
                        # 0 - Dyfuzja
                        nowa_macierz[i][j][1] = round(ilosc_ropy / 9, 2)

                    elif kierunek == 1:

                        # 1 - kierunek na Północ
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i - 1][j][1] + macierz[i + 1][j][1]) / 9, 2)

                    elif kierunek == 2:

                        # 2 - kierunek na południe
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i + 1][j][1] + macierz[i - 1][j][1]) / 9, 2)


                    elif kierunek == 3:

                        # 3 - kierunek na wschód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i][j + 1][1] + macierz[i][j - 1][1]) / 9, 2)

                    elif kierunek == 4:

                        # 4 - kierunek na zachód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i][j - 1][1] + macierz[i][j + 1][1]) / 9, 2)

                    elif kierunek == 5:

                        # 5 - kierunek północny wschód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i - 1][j + 1][1] + macierz[i + 1][j - 1][1]) / 9, 2)


                    elif kierunek == 6:

                        # 6 - kierunek południowy wschód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i + 1][j + 1][1] + macierz[i - 1][j - 1][1]) / 9, 2)


                    elif kierunek == 7:

                        # 7 - kierunek południowy zachód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i + 1][j - 1][1] + macierz[i - 1][j + 1][1]) / 9, 2)


                    elif kierunek == 8:

                        # 8 - kierunek północny zachód
                        nowa_macierz[i][j][1] = round((ilosc_ropy  - macierz[i - 1][j - 1][1] + macierz[i + 1][j + 1][1]) / 9, 2)



                        
                else:
                    nowa_macierz[i][j][1] = round(ilosc_ropy / ikm, 2)



            # Logika dla komórki brzegowej
            elif macierz[i][j][0] == "KB":

                ilosc_ropy_w_komorce_brzegowej = 0
                ikm_obok_komórki_brzegowej = 0

                for x in range(-1, 2):
                    for y in range(-1, 2):

                        # sprawdza czy komórki dookoła są komórkami morza, jeśli tak to zmienna ikm zwiększa się o 1    
                        

                        if (0 <= i + x < wysokosc) and (0 <= j + y < szerokosc):

                            # Jeżeli sąsiednia komórka jest komórką morza to ikm zwiększa się o 1 oraz ilość ropy sumuje się
                            if macierz[i + x][j + y][0] == "S":

                                ikm_obok_komórki_brzegowej = ikm_obok_komórki_brzegowej + 1
                                ilosc_ropy_w_komorce_brzegowej = ilosc_ropy_w_komorce_brzegowej + round(macierz[i + x][j + y][1], 2)
                                

                            else:
                                ikm_obok_komórki_brzegowej = ikm_obok_komórki_brzegowej + 0

                if ikm_obok_komórki_brzegowej == 0:
                    ikm_obok_komórki_brzegowej = 1
                    print("Współrzędne felernej komorki brzegowej:  ", i, j)
                nowa_macierz[i][j][1] = round(macierz[i][j][1] + (ilosc_ropy_w_komorce_brzegowej / ikm_obok_komórki_brzegowej), 2)


            
            elif macierz[i][j][0] == "L" or macierz[i][j][0] == "U":
                pass
                
                        


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
                        if value[0] == 'S':
                            
                            color = get_sim_sea_color(value)  # Pobierz kolor jako krotkę RGB
                            color_hex = "#{:02x}{:02x}{:02x}".format(*color)  # Przekształć kolor na heksadecymalny format
                            canvas.create_rectangle(
                                j * cell_width,
                                i * cell_height,
                                (j + 1) * cell_width,
                                (i + 1) * cell_height,
                                fill = color_hex,
                                outline=""
                                
                            )

                           
                        elif value[0] == "KB":
                            color = get_sim_border_color(value)
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
    elif value == ["U"]:
        return "grey"
    else:
        return "black"
    
# Kolorystyka dla komórek morza
def get_sim_sea_color(value):
    color_mapping = {
        "black": (0, 0, 0),
        "brown": (255, 0, 0),
        "purple": (255, 0, 85),
        "red": (255, 0, 170),
        "orange": (255, 0, 255),
        "yellow": (195, 0, 255),
        "cyan": (130, 0, 255),
        "white": (85, 0, 255),
        "blue": (0, 0, 255)
    }

    if value[1] >= 100:
        return color_mapping["black"]
    elif value[1] >= 75 and value[1] < 100:
        return color_mapping["brown"]
    elif value[1] >= 50 and value[1] < 75:
        return color_mapping["purple"]
    elif value[1] >= 25 and value[1] < 50:
        return color_mapping["red"]
    elif value[1] >= 15 and value[1] < 25:
        return color_mapping["orange"]
    elif value[1] >= 7 and value[1] < 15:
        return color_mapping["yellow"]
    elif value[1] >= 3 and value[1] < 7:
        return color_mapping["cyan"]
    elif value[1] >= 0.2 and value[1] < 3:
        return color_mapping["white"]
    elif value[1] < 0.2:
        return color_mapping["blue"]
    

# Kolorystyka dla komórek brzegowych z zawartością ropy
def get_sim_border_color(value):

    if value[1] <= 0.5:
        return "yellow"
    elif value[1] > 0.5 and value[1] <= 5:
        return "orange"
    elif value[1] > 5 and value[1] <= 10:
        return "red"
    elif value[1] > 10 and value[1] <= 20:
        return "brown"
    else:
        return "black"


def get_pixel_xy(event):
    x = int(canvas.canvasx(event.x))
    y = int(canvas.canvasy(event.y))
    
    print(f"Współrzędne na Canvasie: x={x}, y={y}")
    wsp_x_komorki = round(x / 4)
    wsp_y_komorki = round(y / 4)
    print("Jest to komórka o współrzędnych: ", wsp_x_komorki, wsp_y_komorki)

    print()
    print(macierz[wsp_x_komorki][wsp_y_komorki])


def autor():
    messagebox.showinfo("Autor programu", "Cześć. Mam na imię Marcin. Ten program stworzyłem na bazie mojej pracy dyplomowej z 2006 roku. Wtedy pisałem program w oprogramowaniu Delphi 7. Stworzenie aplikacji trwało wtedy baaaardzo długo - kilka miesięcy. Po przeglądzie kodu który wówczas wysmarzyłem, postanowiłem napisać kod w Pythonie. Zajęło mi to tydzień. Bazując na wiedzy którą nabyłem wykonując proste programy w Pythonie i z pomocą biliotek udało mi się stworzyć program który symuluje rozprzestrzenianie się ropy naftowej na powierzchni morza oraz jej kumulację w komórkach brzegowych lądu.")

def dzialanie_programu():
    messagebox.showinfo("Działanie programu", " Działanie . . . ")

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
plik_menu.add_command(label="Działanie programu", command=dzialanie_programu)
plik_menu.add_separator()
plik_menu.add_command(label="Wyjdź", command=wyjdz)


# Dodawanie opcji do menu Iteracja
iteracja_menu.add_command(label="Iteracja x 2", command=lambda: rysowanie_mapy(2))  # Podaj odpowiednią liczbę iteracji
iteracja_menu.add_command(label="Iteracja x 5", command=lambda: rysowanie_mapy(5)) 
iteracja_menu.add_command(label="Iteracja x 10", command=lambda: rysowanie_mapy(10)) 



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



# Dodaj pole tekstowe do wprowadzenia liczby iteracji
iteracje_entry = tk.Entry(root)
iteracje_entry.pack()



# Utwórz funkcję, która będzie wywoływana po kliknięciu przycisku "Start"
def rozpocznij_symulacje():
    # Pobierz wartość wprowadzoną przez użytkownika
    liczba_iteracji_str = iteracje_entry.get()

    try:
        liczba_iteracji = int(liczba_iteracji_str)
        # Pobierz wartość wprowadzoną przez użytkownika
        if liczba_iteracji <= 0:
            messagebox.showerror("Błąd", "Wpisz liczbę całkowitą większą od zera, np. 5, 20, itp.")
        else:
            # Wywołaj funkcję rysowanie_mapy z wprowadzoną liczbą iteracji
            rysowanie_mapy(liczba_iteracji)
    except ValueError:
        messagebox.showerror("Błąd", "Wpisz liczbę całkowitą większą od zera, np. 5, 20, itp.")




# Dodaj przycisk "Start" do rozpoczęcia symulacji
start_button = tk.Button(root, text="Start", command=rozpocznij_symulacje)
start_button.pack()


canvas.bind("<Button-1>", get_pixel_xy)


root.mainloop()