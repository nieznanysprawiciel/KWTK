from Tkinter import *
import tkFileDialog
import numpy as np
from PIL import ImageTk, Image
import os
import tkMessageBox
import testAllContours2
import cv2


# funkcja wywolywana po nacisnieciu przycisku Otworz...
def openwindows():
    global w1, img, size, t1, t2, child, bt2, bt1

    # deklaracja typu plikow do wyboru [JPG,PNG]
    myfiletypes = [('JPG/JPEG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*')]

    # pobranie sciezki wybranego zdjecia
    open = tkFileDialog.Open(master, filetypes=myfiletypes)
    path = open.show()

    # obsluga bledu - brak wyboru pliku lub niewlasciwy plik
    if path == '':
        return
    try:
        pix_array = Image.open(path)
    except:
        # wyswietlenie okna informacyjnego - blad wyboru pliku
        tkMessageBox.showerror("Blad!", "Blad wyboru pliku!")
        return

    # tworzenie i wyswietlanie nowego okna
    child = Toplevel()
    fullscreen(child)
    child.configure(background='#aaa9ff')
    child.title("Plate recognizer")

    # wczytanie wybranego zdjecia
    colorImage = cv2.imread(path, cv2.cv.CV_LOAD_IMAGE_COLOR)

    img = ImageTk.PhotoImage(pix_array)
    pix_array = np.asarray(pix_array)
    size = pix_array.shape

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # wyswietlanie czesci zwiazanej z analizowanym obrazem

    # tworzenie ramki
    frame = Frame(child, width=child.winfo_screenwidth() / 2,
                  height=child.winfo_screenheight() / 2, borderwidth=4, relief=SUNKEN)

    # tworzenie etykiety
    LF = LabelFrame(frame, text="Oryginalny obraz")
    LF.pack()

    # tworzenie obszaru Canvas do wyswietlenia zdjecia
    w1 = Canvas(LF, width=child.winfo_screenwidth() / 2,
                height=child.winfo_screenheight() / 2, scrollregion=(0, 0, size[1],
                                                                     size[0]))

    # dodanie paskow przewijania
    hbar = Scrollbar(LF, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=w1.xview)
    vbar = Scrollbar(LF, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=w1.yview)
    w1.config(width=child.winfo_screenwidth() / 2,
              height=child.winfo_screenheight() / 2)
    w1.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

    # wyswietlenie wybranego zdjecia
    w1.create_image(0, 0, image=img, anchor='nw')

    # obsluga zdarzen:

    # nacisniecie LPM
    w1.bind("<Button-1>", clicked)

    # zwolnienie LPM
    w1.bind("<ButtonRelease-1>", release)

    # nacisniecie PPM
    child.bind("<Button-3>", right_click)

    w1.pack(expand=True, fill=BOTH)

    frame.pack()

    # pozycjonowanie dodanych elementow - widgetow
    frame.place(x=0, y=0)

    # pobranie rozmiarow widgetow
    wd_frame = frame["width"]
    hg_frame = frame["height"]
    wd_vbar = vbar["width"]
    hg_hbar = hbar["width"]

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # wyswietlanie czesci zwiazanej z wynikami dzialania algorytmu

    # tworzenie ramki
    frame2 = Frame(child, width=child.winfo_screenwidth() / 2 - int(wd_vbar) * 2,
                   height=child.winfo_screenheight() / 2, borderwidth=4, relief=SUNKEN)

    # tworzenie etykiety
    LF2 = LabelFrame(frame2, text="Analizowany fragment obrazu")
    LF2.pack()

    # tworzenie obszaru Canvas do wyswietlenia zdjecia
    w2 = Canvas(LF2, width=child.winfo_screenwidth() / 2 - int(wd_vbar) * 2,
                height=child.winfo_screenheight() / 2, scrollregion=(0, 0, size[1],
                                                                     size[0]))

    # dodanie paskow przewijania
    hbar2 = Scrollbar(LF2, orient=HORIZONTAL)
    hbar2.pack(side=BOTTOM, fill=X)
    hbar2.config(command=w2.xview)
    vbar2 = Scrollbar(LF2, orient=VERTICAL)
    vbar2.pack(side=RIGHT, fill=Y)
    vbar2.config(command=w2.yview)
    w2.config(width=child.winfo_screenwidth() / 2,
              height=child.winfo_screenheight() / 2)
    w2.config(xscrollcommand=hbar2.set, yscrollcommand=vbar2.set)
    w2.pack(expand=True, fill=BOTH)

    frame2.pack()

    # pozycjonowanie widgetow
    frame2.place(x=wd_frame + int(wd_vbar) * 2, y=0)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Parametry
    # parametry sa pobierane po nacisnieciu przycisku Wprowadz przez funkcje insert()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # deklaracja wartosci domyslnych parametrow
    par1 = 0.09
    par2 = 6

    # tworzenie ramki
    frame3 = Frame(child, width=child.winfo_screenwidth() / 2,
                   height=child.winfo_screenheight() / 2, borderwidth=4, relief=SUNKEN)
    frame3.pack()
    frame3.place(x=0, y=hg_frame + int(hg_hbar) * 3)

    # tworzenie etykiety
    LF3 = LabelFrame(frame3)
    LF3.pack()

    # deklaracja wporwadzanych zmiennych
    v1 = StringVar(child, value=par1)
    v2 = StringVar(child, value=par2)

    # tworzenie etykiety Parametr1
    sb1 = statusbar = Label(frame3, text="Parametr 1:", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb1.pack()

    # tworzenie pola wporwadzania Parametru1
    t1 = Entry(frame3, textvariable=v1, font=("Helvetica", 10))
    t1.pack()

    # tworzenie etykiety Parametr2
    sb2 = statusbar = Label(frame3, text="Parametr 2:", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb2.pack()

    # tworzenie pola wporwadzania Parametru2
    t2 = Entry(frame3, textvariable=v2, font=("Helvetica", 10))
    t2.pack()

    # tworzenie przyciskow:

    # tworzenie ramki
    frame4 = Frame(frame3, borderwidth=4, relief=SUNKEN)
    frame4.pack()

    # tworzenie etykiety
    LF4 = LabelFrame(frame4, background='green')
    LF4.pack()

    # Wprowadz - wprowadzenie nowych parametrow - uruchomienie funkcji insert()
    bt1 = Button(LF4, text="Wprowadz \n[opcjonalnie]", command=insert, font=("Helvetica", 10))
    bt1.pack(side=LEFT)

    # Analiza - uruchiomienie algorytmu - wywolanie funckji analizuj()
    bt2 = Button(LF4, text="Analiza", command=lambda: analizuj(pix_array,
                                                               child, click, rel, statusbar, img, path, par1, par2, w2),
                 font=("Helvetica", 10))
    bt2.pack(side=LEFT)

    # Wyjdz
    bt3 = Button(LF4, text="Wyjdz", command=lambda: delete(child), font=("Helvetica", 10))
    bt3.pack(side=RIGHT)


# funckja wywolywana po nacisnieciu przycisku Analizuj
# rozpoczyna dzialanie algorytmu
def analizuj(_colorImage, _child, _click, _rel, _statusbar, _img, _path, _par1, _par2, _w2):
    global rect
    w1.delete(rect)
    rect = None

    # wybor zaznaczonego obszaru
    if _click[0] > _rel[0]:
        temp = _click[0]
        _click[0] = _rel[0]
        _rel[0] = temp

    if _click[1] > _rel[1]:
        temp = _click[1]
        _click[1] = _rel[1]
        _rel[1] = temp

    if (_click[0] != 0) | (_rel[0] != 0):
        if (_click[1] != 0) | (_rel[1] != 0):
            _colorImage = _colorImage[_click[1]:_rel[1], _click[0]:_rel[0], :]

    if (_click[0] == _rel[0] != 0) | (_click[1] == _rel[1] != 0):
        tkMessageBox.showinfo("Zbyt maly obszar!", "Zaznaczono zbyt maly obszar. Prosze zaznaczyc wiekszy obszar")

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # uruchomienie algorytmu

    _results = testAllContours2.plate_recog(_path, _colorImage, _par1, _par2)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # sprawdzenie czy algorytm zwrocil wyniki
    # jesli tak, wykonywany jest algorytm, jesli nie program jest przerywany - error
    if _results[3] == False:

        # sciezka do analizowanego przez algorytm fragmentu obrazu
        path2 = os.path.normpath(os.path.dirname(__file__)).replace('\\', '/') + "/" + _results[2] + ".jpg"

        # wczytanie i wyswietlenie analizowanego przez algorytm fragmentu obrazu
        photo_temp = Image.open(path2)
        photo = ImageTk.PhotoImage(photo_temp)
        photo_temp = np.asarray(photo_temp)
        size2 = photo_temp.shape
        label = Label(_w2, image=photo, borderwidth=1)
        label.image = photo
        label.pack()

        # wyswietlanie zwroconych wynikow
        for i in range(0, len(_results[1])):
            _statusbar = "statusbar" + str(i)

            _statusbar = Label(_w2, text=str(_results[1][i]), bd=1, relief=SUNKEN, anchor=W,
                               font=("Helvetica", 12))
            _statusbar.pack(side=BOTTOM, fill=X)

        # wyswietlanie rozpoznanych numerow rejestracyjnych
        _statusbar.config(text="Rozpoznany numer rejestracyjny: " + str(_results[0]),
                          font=("Helvetica", 14))
        _statusbar.pack(side=TOP, fill=X)

        statusbar2 = Label(_w2, text="Mozliwe znaki i prawdopodobienstwo ich wystapienia:",
                           bd=1, relief=SUNKEN, anchor=W, font=("Helvetica", 13))
        statusbar2.pack(side=BOTTOM, fill=X)

        # blokowanie przyciskow
        bt2.config(state=DISABLED)
        bt1.config(state=DISABLED)
        tkMessageBox.showinfo("Zakonczono!", "Analiza zakonczona pomyslnie", parent=child)
    else:
        tkMessageBox.showerror("Niewlasciwy obszar!",
                               "Zaznaczony obszar zawiera zbyt malo znakow. Prosze ponownie wczytac zdjecie i zaznaczyc obszar obejmujacy tablice rejestracyjna",
                               parent=_child)
        delete(_child)


# zdarzenie - wcisniecie przycisku
def clicked(_event):
    global click
    # zmiana wspolrzednych okna na wspolrzedne Canvas
    x, y = w1.canvasx(_event.x), w1.canvasy(_event.y)
    # pobranie pozycji kursora
    click = [x, y]
    print("Clicked at", x, y)


# event - zwolnienie przycisku [tworzenie zaznaczenia]
def release(_event):
    global rel
    global rect
    global child
    # tworzenie zaznaczenia
    if rect == None:
        # zmiana wspolrzednych okna na wspolrzedne Canvas
        x, y = w1.canvasx(_event.x), w1.canvasy(_event.y)
        # pobranie pozycji kursora
        rel = [x, y]
        print ("Relased at", x, y)
        # tworzenie zaznaczenia
        rect = w1.create_rectangle(click[0], click[1], rel[0], rel[1], width=5)
    else:
        # wyswietlenie okna informacyjnego - error
        tkMessageBox.showinfo("Blad zaznaczenia!", "Usun bierzace zaznaczenie [prawy przycisk myszy]",
                              parent=child)


# usuwanie zaznaczenia
def right_click(_event):
    global rect
    if rect != None:
        w1.delete(rect)
        rect = None


# wprowadzanie parametrow
def insert():
    global par1, par2
    # pobieranie wartosci parametru z pola
    par1 = float(t1.get())
    par2 = float(t2.get())
    # wyswieetlenie okna informacyjnego
    tkMessageBox.showinfo("Wprowadzono nowe parametry", "Wprowadzonie zakonczone pomyslnie", parent=child)


# zamykanie okna
def delete(_child):
    global click
    click = [0, 0]
    global rel
    rel = [0, 0]
    _child.destroy()


# pelny ekran
def fullscreen(_self):
    # pobranie rozdzielczosci ekranu
    w, h = _self.winfo_screenwidth(), _self.winfo_screenheight()
    _self.geometry("%dx%d+0+0" % (w, h))


# deklaracja zmiennych
w = None
rect = None
child = None
par1 = 0.09
par2 = 6
size = np.zeros([2])
click = np.zeros([2])
rel = np.zeros([2])
coord = np.zeros([2])

# tworzenie okna glownego
master = Tk()
master.title("Plate recognizer")
fullscreen(master)
master.configure(background='#aaa9ff')

# tworzenie i pozycjonowanie przyciskow:
# Otworz...
# Wyjdz

b1 = Button(master, text="Otworz...", width=60, height=5, command=openwindows, font=("Helvetica", 10))
b2 = Button(master, text="Wyjdz", width=60, height=5, command=master.destroy, font=("Helvetica", 10))

b1.pack(side=LEFT)
b2.pack(side=RIGHT)

b1.place(x=master.winfo_screenwidth() / 2 - 240, y=master.winfo_screenheight() / 2 - 120)
b2.place(x=master.winfo_screenwidth() / 2 - 240, y=master.winfo_screenheight() / 2)

master.mainloop()