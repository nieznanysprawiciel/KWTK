import logging
import os
import tkFileDialog
import tkMessageBox
import tkSimpleDialog
from Tkinter import *

import cv2
import numpy as np
from PIL import ImageTk, Image

import testAllContours2

logging.basicConfig(filename='kwtk.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)

# funkcja wywolywana po nacisnieciu przycisku Otworz...
def openwindows():
    global w1, img, size, t3, t4, child, bt2, click_list

    # deklaracja typu plikow do wyboru [JPG,PNG]
    myfiletypes = [('JPG/JPEG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*')]

    # pobranie sciezki wybranego zdjecia
    path = tkFileDialog.askopenfilename(parent=master, filetypes=myfiletypes)

    # obsluga bledu - brak wyboru pliku lub niewlasciwy plik
    if not path:
        logger.info("File: [" + path + "] is not valid")
        return

    try:
        pix_array = Image.open(path)
        logger.info("Opened file: [" + path + "]")
    except Exception as exc:
        # wyswietlenie okna informacyjnego - blad wyboru pliku
        logger.exception(exc)
        tkMessageBox.showerror("Blad!", "Blad wyboru pliku!")
        return

    # tworzenie i wyswietlanie nowego okna
    click_list = []
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
                   height=child.winfo_screenheight() /2, borderwidth=4, relief=SUNKEN)

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
              height=child.winfo_screenheight()/2 )
    w2.config(xscrollcommand=hbar2.set, yscrollcommand=vbar2.set)
    w2.pack(expand=True, fill=BOTH)

    frame2.pack()

    # pozycjonowanie widgetow
    frame2.place(x=wd_frame + int(wd_vbar) * 2, y=0)

    # tworzenie ramki
    frame3 = Frame(child, width=child.winfo_screenwidth() / 2,
                   height=child.winfo_screenheight() / 2, borderwidth=4, relief=SUNKEN)
    frame3.pack()
    frame3.place(x=0, y=hg_frame + int(hg_hbar) * 3)

    # tworzenie etykiety
    LF3 = LabelFrame(frame3)
    LF3.pack()

    # deklaracja wporwadzanych zmiennych
    adaptive_thresholding_block_size_input = IntVar(master=child, value=15)
    adaptive_thresholding_constant_input = DoubleVar(master=child, value=5.0)
    segmentation_threshold_input = DoubleVar(master=child, value=0.09)
    min_dist_between_segments_input = IntVar(master=child, value=6)
    min_character_similarity_input = DoubleVar(master=child, value=0.15)

    # tworzenie etykiet i pol tekstowych dla parametrow
    sb1 = statusbar = Label(frame3, text="adaptive_thresholding_block_size", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb1.pack()
    t1 = Entry(frame3, textvariable=adaptive_thresholding_block_size_input, font=("Helvetica", 10))
    t1.pack()

    sb2 = statusbar = Label(frame3, text="adaptive_thresholding_constant", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb2.pack()
    t2 = Entry(frame3, textvariable=adaptive_thresholding_constant_input, font=("Helvetica", 10))
    t2.pack()

    sb3 = statusbar = Label(frame3, text="segmentation_threshold", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb3.pack()
    t3 = Entry(frame3, textvariable=segmentation_threshold_input, font=("Helvetica", 10))
    t3.pack()

    sb4 = statusbar = Label(frame3, text="min_dist_between_segments", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb4.pack()
    t4 = Entry(frame3, textvariable=min_dist_between_segments_input, font=("Helvetica", 10))
    t4.pack()

    sb5 = statusbar = Label(frame3, text="min_character_similarity", bd=1, relief=SUNKEN,
                            anchor=W, font=("Helvetica", 11))
    sb5.pack()
    t5 = Entry(frame3, textvariable=min_character_similarity_input, font=("Helvetica", 10))
    t5.pack()

    # tworzenie przyciskow:

    # tworzenie ramki
    frame4 = Frame(frame3, borderwidth=4, relief=SUNKEN)
    frame4.pack()

    # tworzenie etykiety
    LF4 = LabelFrame(frame4, background='green')
    LF4.pack()

    def on_analysis_button_click():
        try:
            adaptive_thresholding_block_size = adaptive_thresholding_block_size_input.get()
            adaptive_thresholding_constant = adaptive_thresholding_constant_input.get()
            segmentation_threshold = segmentation_threshold_input.get()
            min_dist_between_segments = min_dist_between_segments_input.get()
            min_character_similarity = min_character_similarity_input.get()
            analizuj(
                pix_array, child, click, rel, statusbar, img, path,
                adaptive_thresholding_block_size, adaptive_thresholding_constant,
                segmentation_threshold, min_dist_between_segments,
                min_character_similarity, w2)
        except Exception:
            tkMessageBox.showerror("Blad!", "Nieprawidlowe wartosci parametrow!", parent=child)

    # Analiza - uruchiomienie algorytmu - wywolanie funckji analizuj()
    bt2 = Button(LF4, text="Analiza", command=on_analysis_button_click, font=("Helvetica", 10))
    bt2.pack(side=LEFT)

    # Wyjdz
    bt3 = Button(LF4, text="Wyjdz", command=lambda: delete(child), font=("Helvetica", 10))
    bt3.pack(side=RIGHT)


# funckja wywolywana po nacisnieciu przycisku Analizuj
# rozpoczyna dzialanie algorytmu
def analizuj(_colorImage, _child, _click, _rel, _statusbar, _img, _path,
             _adaptive_thresholding_block_size, _adaptive_thresholding_constant,
             _segmentation_threshold, _min_dist_between_segments, _min_character_similarity, _w2):
    try:
        global click_list
         #w1.delete(rect)
         #rect = None

        # # wybor zaznaczonego obszaru
        # if _click[0] > _rel[0]:
        #     temp = _click[0]
        #     _click[0] = _rel[0]
        #     _rel[0] = temp
        #
        # if _click[1] > _rel[1]:
        #     temp = _click[1]
        #     _click[1] = _rel[1]
        #     _rel[1] = temp


        only_x = [clk[0] for clk in click_list]
        only_y = [clk[1] for clk in click_list]

        corners = None
        
        if only_x and only_y:
            min_x, max_x = min(only_x), max(only_x)
            min_y, max_y = min(only_y), max(only_y)
                       
            point1 = [ click_list[0][0] - min_x, click_list[0][1] - min_y ]
            point2 = [ click_list[1][0] - min_x, click_list[1][1] - min_y ]
            point3 = [ click_list[2][0] - min_x, click_list[2][1] - min_y ]
            point4 = [ click_list[3][0] - min_x, click_list[3][1] - min_y ]
                       
            _colorImage = _colorImage[min_y:max_y, min_x:max_x, :]
            corners = [np.array( [ [point1],[point2],[point3],[point4] ])]
            
            #print corners

        # if (_click[0] != 0) | (_rel[0] != 0):
        #     if (_click[1] != 0) | (_rel[1] != 0):
        #         _colorImage = _colorImage[_click[1]:_rel[1], _click[0]:_rel[0], :]
        #         print "TEST!!!", type(_colorImage)
        #
        # if (_click[0] == _rel[0] != 0) | (_click[1] == _rel[1] != 0):
        #     tkMessageBox.showinfo("Zbyt maly obszar!", "Zaznaczono zbyt maly obszar. Prosze zaznaczyc wiekszy obszar")



        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # uruchomienie algorytmu

        license_plate, probable_characters, result_file, threshholding_letters_file = testAllContours2.plate_recog(
            _path,
            _colorImage,
            _adaptive_thresholding_block_size,
            _adaptive_thresholding_constant,
            _segmentation_threshold,
            _min_dist_between_segments,
            _min_character_similarity,
            corners )

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # sprawdzenie czy algorytm zwrocil wyniki
        # jesli tak, wykonywany jest algorytm, jesli nie program jest przerywany - error
        if license_plate is not None:

            # obraz tablicy po tresholdingu
            thresholding_letters_path =\
                os.path.normpath(os.path.dirname(__file__)).replace('\\', '/') + "/" + threshholding_letters_file
            thresholding_letters_temp = Image.open(thresholding_letters_path)
            thresholding_letters = ImageTk.PhotoImage(thresholding_letters_temp)
            thresholding_label = Label(_w2, image=thresholding_letters, borderwidth=1)
            thresholding_label.image = thresholding_letters
            thresholding_label.pack()

            # sciezka do analizowanego przez algorytm fragmentu obrazu
            path2 = os.path.normpath(os.path.dirname(__file__)).replace('\\', '/') + "/" + result_file + ".jpg"

            # wczytanie i wyswietlenie analizowanego przez algorytm fragmentu obrazu
            photo_temp = Image.open(path2)
            photo = ImageTk.PhotoImage(photo_temp)
            photo_temp = np.asarray(photo_temp)
            size2 = photo_temp.shape
            label = Label(_w2, image=photo, borderwidth=1)
            label.image = photo
            label.pack()


            statusbar2 = Label(_w2, text="lalala ",
                               bd=1, relief=SUNKEN, anchor=W, font=("Helvetica", 13))
            # statusbar2.pack(side=BOTTOM, fill=X)
            # # wyswietlanie rozpoznanych numerow rejestracyjnych
            statusbar2.config(text="Rozpoznany numer rejestracyjny: " + str(license_plate) + "\n Mozliwe znaki i prawdopodobienstwa stwa ich wystapienia",
                              font=("Helvetica", 14))
            statusbar2.pack(side=TOP, fill=X)

            wyniki = probable_characters
            # wyswietlanie zwroconych wynikow
            for wynik in wyniki:
                tekst = "; ".join("{} = {}".format(litera, str(wartosc)[:5]) for litera, wartosc in wynik)

                _statusbar = Label(_w2, text=str(tekst), bd=1, relief=SUNKEN, anchor=W,
                                   font=("Helvetica", 12))
                _statusbar.pack(side=TOP, fill=X)

            tkMessageBox.showinfo("Zakonczono!", "Analiza zakonczona pomyslnie", parent=child)
        else:
            tkMessageBox.showerror("Niewlasciwy obszar!",
                                   "Zaznaczony obszar zawiera zbyt malo znakow. Prosze ponownie wczytac zdjecie i zaznaczyc obszar obejmujacy tablice rejestracyjna",
                                   parent=_child)
                                   
    except Exception as exc:
        logger.exception(exc)
        tkMessageBox.showerror("Blad programu!", "Analiza zakonczona bledem! Sprawdz logi programu.", parent=_child)


def draw_click_list():
    global click_list, w1

    if len(click_list) < 2:
        return

    flatten = []
    for x, y in click_list:
        flatten += [x, y]

    if len(click_list) == 4:
        flatten += click_list[0]

    w1.create_line(*flatten, width=3, fill="blue", tags="area_line")

# zdarzenie - wcisniecie przycisku
def clicked(_event):
    global click, click_list

    if len(click_list) == 4:
        return

    # zmiana wspolrzednych okna na wspolrzedne Canvas
    x, y = w1.canvasx(_event.x), w1.canvasy(_event.y)
    # pobranie pozycji kursora
    click = [x, y]

    click_list.append((x, y))
    draw_click_list()

    logger.debug("Clicked at %d %d", x, y)


# event - zwolnienie przycisku [tworzenie zaznaczenia]
def release(_event):
    return

    #
    # global rel
    # global rect
    # global child
    # # tworzenie zaznaczenia
    # if rect == None:
    #     # zmiana wspolrzednych okna na wspolrzedne Canvas
    #     x, y = w1.canvasx(_event.x), w1.canvasy(_event.y)
    #     # pobranie pozycji kursora
    #     rel = [x, y]
    #     print ("Relased at", x, y)
    #     # tworzenie zaznaczenia
    #     rect = w1.create_rectangle(click[0], click[1], rel[0], rel[1], width=5)
    # else:
    #     # wyswietlenie okna informacyjnego - error
    #     tkMessageBox.showinfo("Blad zaznaczenia!", "Usun biezace zaznaczenie [prawy przycisk myszy]",
    #                           parent=child)



# usuwanie zaznaczenia
def right_click(_event):
    global click_list, w1
    click_list = []
    w1.delete("area_line")


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


class LogInDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        Label(master, text="Login:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master, show='*')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1

    def apply(self):
        login = str(self.e1.get())
        password = str(self.e2.get())
        self.result = login, password


def show_log_in_window():
    log_in_dialog = LogInDialog(master)
    login, password = log_in_dialog.result

    if login == 'login' and password == 'password':
        delete(log_in_button)
        b1.config(state=ACTIVE)
        b2.config(state=ACTIVE)
        
        logger.info( "Logged as: [" + login + "]" )
    else:
        tkMessageBox.showerror("Logowanie", "Podano bledny login i/lub haslo!", parent=master)
        logger.info( "Login as: [" + login + "] failed" )
        
        b2.config(state=ACTIVE)

# deklaracja zmiennych
w = None
rect = None
child = None
size = np.zeros([2])
click = np.zeros([2])
click_list = []
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

log_in_button = Button(master, text="Zaloguj sie", width=60, height=5, command=show_log_in_window, font=("Helvetica", 10))
b1 = Button(master, text="Otworz...", width=60, height=5, command=openwindows, font=("Helvetica", 10), state=DISABLED)
b2 = Button(master, text="Wyjdz", width=60, height=5, command=master.destroy, font=("Helvetica", 10), state=DISABLED)

log_in_button.pack(side=LEFT)
b1.pack(side=LEFT)
b2.pack(side=RIGHT)

log_in_button.place(x=master.winfo_screenwidth() / 2 - 240, y=master.winfo_screenheight() / 2 - 240)
b1.place(x=master.winfo_screenwidth() / 2 - 240, y=master.winfo_screenheight() / 2 - 120)
b2.place(x=master.winfo_screenwidth() / 2 - 240, y=master.winfo_screenheight() / 2)

master.mainloop()
