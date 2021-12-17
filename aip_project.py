from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import random

from PIL import Image as Imagepil
from PIL import ImageTk

import data_var


# ФУНКЦИИ ДЛЯ ОТОБРАЖЕНИЯ ОСНОВНОЙ ИНФОРМАЦИИ
def drawmainwindow():
    """
    Данная функция прорисовывает главный экран, который показывается при запуске программы.
    Прорисовываются кнопки выбора вариантов, показа определенного варианта, меню и вспомогательные надписи.
    """
    main_window.config(bg=colorbackground)
    Label(main_window, text='ЕГЭ профильная математика', font='Times 30', bg=colorbackground).place(x=width // 3, y=10)
    Label(main_window, text='Выбирите вариант(Отсчет времени пойдет сразу после выбора варианта):', font='Times 16',
          bg=colorbackground).place(x=225, y=150)
    kolvo_stolbcev = kolvariantov // 5  # количесвто кнопок вариантов в столбце
    # расставляем кнопки вариантов
    for i in range(1, kolvariantov // kolvo_stolbcev + 1):
        for j in range(kolvo_stolbcev):
            bt = Button(main_window, text=str(i + j * kolvariantov // kolvo_stolbcev) + " вариант", font='Times 14',
                        bg=color_button_variant, command=partial(openvariant, i + j * kolvariantov // kolvo_stolbcev))
            bt.place(x=300 + 180 * j, y=150 + i * 50, width=100, height=35)
            massiv_delete.append(bt)
    # добавляем случайный вариант
    bt = Button(main_window, text="Случайный вариант", font='Times 14', bg=color_button_variant,
                command=partial(openvariant, random.randint(1, kolvariantov)))
    bt.place(x=1000, y=200)
    massiv_delete.append(bt)
    # создаю просмотр варианта
    strv = Label(main_window,
                 text='Чтобы посмотреть задания варианта с ответами к первой части и решениями ко второй введите',
                 font='Times 16', bg=colorbackground)
    strv.place(x=220, y=500)
    massiv_delete.append(strv)
    massiv_show = []
    strv = Label(main_window, text='номер варианта:',
                 font='Times 16', bg=colorbackground)
    strv.place(x=320, y=540)
    massiv_delete.append(strv)
    strv = Entry(main_window, textvariable=StringVar(), bg=color_str_vvoda, font='Times 16')
    strv.place(x=470, y=540, width=50)
    massiv_delete.append(strv)
    massiv_show.append(strv)
    strv = Label(main_window, text='пароль:',
                 font='Times 16', bg=colorbackground)
    strv.place(x=320, y=585)
    massiv_delete.append(strv)
    strv = Entry(main_window, textvariable=StringVar(), bg=color_str_vvoda, font='Times 16')
    strv.place(x=400, y=588, width=150)
    massiv_delete.append(strv)
    massiv_show.append(strv)
    bt = Button(main_window, text='Посмотреть вариант', font='Times 16', bg=background_button_check,
                command=partial(show_variant, massiv_show))
    bt.place(x=600, y=620)
    massiv_delete.append(bt)
    # запускаю инициализацию меню
    initmenu()


def openvariant(number):
    """
    Прорисовка варианта после его выбора в главном меню. Удаляются все прошлые объкты. Также запусается таймер.
    :param number: передается номер выбранного пользователем варианта для дальнейшего
    испоьзование в выборе нужных изображений.
    """
    global second_frame, massiv_delete
    # очистим экран
    vrem_perem = alldelete(massiv_delete)
    massiv_delete = vrem_perem
    create_scrollbar()  # Присоедени скроллбар
    main_window.title(str(number) + " вариант")  # установим в загаловке номер варианта
    rashir_window(second_frame).pack()  # расширим окно под размер пользователя
    # вставка заданий
    for i in range(1, 18 + 1):
        # номер задания
        Label(second_frame, text=str(i) + " задание", font='Times 20', bg=colorbackground_number_zadaniy).pack()
        # вставка задания
        im = Imagepil.open("images/" + str(number) + "_" + str(i) + ".png")
        (shirina, visota) = im.size
        # подгонка изображения под размер экрана пользователя
        if shirina > screen_width - 10:
            im = im.resize((screen_width - 50, visota))
        photo = ImageTk.PhotoImage(im)
        label = Label(second_frame, image=photo)
        label.image = photo
        label.pack()
        # строка ввода ответа и отступы
        doindent_second_frame(0, second_frame).pack()
        if i <= 11:
            frame = Frame(second_frame)
            Label(frame, text='Ваш ответ:', font='Times 16', bg=colorbackground).grid(row=0, column=0)
            strv = Entry(frame, textvariable=StringVar(), bg=color_str_vvoda, font='Times 16')
            strvvoda.append(strv)
            strv.grid(row=0, column=1)
            frame.pack()
            doindent_second_frame(1, second_frame).pack()
    # Кнопка для окончания решения и проверки второй части
    vrem_perem = Button(main_window, text='Проверить', bg=background_button_check, command=partial(docheck, number))
    vrem_perem.pack(side=RIGHT)
    massiv_delete.append(vrem_perem)
    # запуск таймера
    start_time(number)


def docheck2(number, vern):
    """
    Показ решений второй части, радиокнопки для оценки пользователя своих заданий.
    После оценки запускается функция финального экрана, этот удаляется
    :param number: номер решаемого варианта
    :param vern: количество верных заданий в первой части
    """
    global massiv_delete
    massivradiobutton = []
    vrem_perem = alldelete(massiv_delete)
    massiv_delete = vrem_perem
    create_scrollbar()
    rashir_window(second_frame).pack()
    # вставка решений и радиокнопок
    for i in range(12, 18 + 1):
        Label(second_frame, text=str(i) + " задание", font='Times 20', bg=colorbackground_number_zadaniy).pack()
        # вставка решения
        im = Imagepil.open("images/resh_" + str(number) + "_" + str(i) + ".png")
        photo = ImageTk.PhotoImage(im)
        label = Label(second_frame, image=photo)
        label.image = photo
        label.pack()
        rediobuttonslabel, labelradiobutton = doradiobutton(i)
        rediobuttonslabel.pack()
        massivradiobutton.append(labelradiobutton)
        doindent_second_frame(1, second_frame).pack()
    # кнопка для окончания проверки
    btcheck = Button(main_window, text='Закончить', bg=background_button_check,
                     command=partial(endprogramm, massivradiobutton, vern))
    btcheck.pack(side=RIGHT)
    massiv_delete.append(btcheck)


def endprogramm(massivradiobutton, vern):
    """
    Финальная функция, удаляются все прошлые объекты, окончательный подсчет
    правильно решенных заданий и вывод информации на экран
    :param massivradiobutton: массив радиокнопок с оценкой второй части
    :param vern: количество верно решенных заданий в первой части
    :return: None
    """
    global massiv_delete
    summa_second_chast = srballvtoroichasti(massivradiobutton)
    procent = raschitprocenti(summa_second_chast + vern)
    end_frame = Frame(main_window)
    vrem_perem = alldelete(massiv_delete)
    massiv_delete = vrem_perem
    data_file = open('rezults.txt', 'a')  # записывем результат в файл
    d1 = str(datetime.datetime.now())
    data_file.write(d1[:d1.rfind(':')] + ' ' + str(vern + summa_second_chast) + ' ' + str(procent) + '\n')
    data_file.close()  # закрываем файл
    Label(end_frame, text=nadpis(procent), font='Times 30').pack()
    Label(end_frame, text='Ваш результат:', font='Times 30').pack()
    Label(end_frame, text=str(procent) + '%   или ' + str(summa_second_chast + vern) + ' ' + nadpis_ball(
        summa_second_chast + vern),
          font='Times 30').pack()
    end_frame.pack(fill=BOTH, expand=1)
    return None


# ФУНКЦИИ ДЛЯ ОТОБРАЖЕНИЯ ПОБОЧНОЙ ИНФОРМАЦИИ
def show_variant(write_password):
    """
    Показывается вариант выбранный пользователем при вводе правильного пароля. В варинате представлены условия и решения
    :param write_password:  введенный пароль
    """
    if write_password[1].get() == password:
        window_show_variant = Toplevel()  # создание второго экрана
        window_show_variant.title(write_password[0].get() + ' вариант')
        window_show_variant.state("zoomed")
        # создаю фрейм и растягиваю на весь экран
        main_frame = Frame(window_show_variant)
        main_frame.pack(fill=BOTH, expand=1)
        # создаю холст и растягиваю на фрейм
        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        canvas.config(width=width, height=height)
        # создаю полосу прокрутки и прикрепляю справа
        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        # прикрепляю полосу прокрутки к холсту и присоединяю к прокрутке
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>", partial(on_mouse_wheel, canvas))
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # новый фрейм и прикрепление к холсту
        second_frame = Frame(canvas)
        second_frame.config(bg=colorbackground)
        canvas.create_window((0, 0), window=second_frame, anchor="nw")
        # выводим номера и ответы к ним
        rashir_window(second_frame).pack()
        for i in range(1, 18 + 1):
            # номер задания
            Label(second_frame, text=str(i) + " задание", font='Times 20', bg=colorbackground_number_zadaniy).pack()
            # вставка задания
            im = Imagepil.open("images/" + str(write_password[0].get()) + "_" + str(i) + ".png")
            (shirina, visota) = im.size
            # подгонка изображения под размер экрана пользователя
            if shirina > screen_width - 20:
                im = im.resize((screen_width - 50, visota))
            photo = ImageTk.PhotoImage(im)
            label = Label(second_frame, image=photo)
            label.image = photo
            label.pack()
            # строка ввода ответа и отступы
            doindent_second_frame(0, second_frame).pack()
            if i <= 11:
                Label(second_frame, text='Ответ:' + str(data_var.otvet[int(write_password[0].get())][i]),
                      font='Times 16', bg='White').pack()
            else:
                Label(second_frame, text='Решение', font='Times 16', bg='White').pack()
                im = Imagepil.open("images/resh_" + write_password[0].get() + "_" + str(i) + ".png")
                photo = ImageTk.PhotoImage(im)
                label = Label(second_frame, image=photo)
                label.image = photo
                label.pack()
            doindent_second_frame(1, second_frame).pack()
        window_show_variant.mainloop()


def initmenu():
    """
    Происходит прорисовка верхнего меню с необходимыми вкладками.
    """
    menuitem = Menu(main_window)
    main_window.config(menu=menuitem)
    filemenu = Menu(menuitem, tearoff=0)
    # вкладка результаты
    menuitem.add_cascade(label='Результаты', menu=filemenu)
    filemenu.add_command(label='Посмотреть результаты', command=show_results)
    # вкладка о программе
    helpmenu = Menu(menuitem, tearoff=0)
    menuitem.add_cascade(label="Справка", menu=helpmenu)
    helpmenu.add_command(label="О программе", command=partial(massage, 0))
    helpmenu.add_command(label='Помощь разработчику', command=partial(massage, 1))
    # вкладка справочные материалы
    spr_data = Menu(menuitem, tearoff=0)
    menuitem.add_cascade(label="Справочные данные", menu=spr_data)
    spr_data.add_command(label='Инструкция по выполнению', command=partial(sprav_data, 0))
    spr_data.add_command(label="Справочные материалы", command=partial(sprav_data, 1))


def show_results():
    """
    Выводит в отдельном окне результаты ранее решаемых вариантов и время окончания решения"""
    window_show_result = Toplevel()  # создается второе окно
    Label(window_show_result, text='Таблица результатов', font='Times 14 bold').grid(row=0, column=1)
    Label(window_show_result, text='Дата решения', font='Times 14').grid(row=2, column=0)
    Label(window_show_result, text='Результат в первичных баллах   ', font='Times 14').grid(row=2, column=1)
    Label(window_show_result, text='Результат в процентах', font='Times 14').grid(row=2, column=2)
    # считываем из файла результаты и записываем их в строки
    data_file = open('rezults.txt', 'r')
    lines = data_file.readlines()
    for line in range(len(lines) - 1, -1, -1):
        stroka = lines[line]
        Label(window_show_result, text=stroka[stroka.rfind(' '):], font='Times 14').grid(row=len(lines) - line + 2,
                                                                                         column=2)
        stroka = stroka[:stroka.rfind(' ')]
        Label(window_show_result, text=stroka[stroka.rfind(' '):], font='Times 14').grid(row=len(lines) - line + 2,
                                                                                         column=1)
        Label(window_show_result, text=stroka[:stroka.rfind(' ')], font='Times 14').grid(row=len(lines) - line + 2,
                                                                                         column=0)
    data_file.close()  # закрываем файл
    window_show_result.mainloop()


def rashir_window(gde):
    """
    Функция расширяет frame до ширины экрана пользователя с целью чтобы изображения условия и
    решений через pack были по середине
    :param gde: место куда необходимо вставить изображение
    :return: изображение в 1 пиксель в ввысоту и ширину экрана пользователя
    """
    im = Imagepil.open('images/raschir.png')
    im = im.resize((screen_width - 25, 1), Imagepil.ANTIALIAS)
    photo = ImageTk.PhotoImage(im)
    label = Label(gde, image=photo, bg=colorbackground)
    label.image = photo
    return label


def sprav_data(what_show):
    """
    Функция отображает выбранные справочные данные в отдельном окне
    :param what_show: номер необходимого справочного  материала
    """
    window_info = Toplevel()  # создаем отдельное окно
    if what_show == 0:
        im = ImageTk.PhotoImage(Imagepil.open("images/instr.png"))
        Label(window_info, image=im).pack()
    elif what_show == 1:
        im = ImageTk.PhotoImage(Imagepil.open("images/spravochnie_data.png"))
        Label(window_info, image=im).pack()
    window_info.mainloop()


def massage(what_do):
    """
    Показывает необходимые справочные сообщения
    :param what_do: номер необходимого сообщения
    """
    if what_do == 0:
        messagebox.showinfo("О программе",
                            "Данная программа создана с целью помочь в подготовке к ЕГЭ по профильной математике. "
                            "\n Выбирите номер варианта и начните решение. По окончанию выполните самопроверку "
                            "второй части.\n В конце вы увидете свой результат.")
    elif what_do == 1:
        messagebox.showinfo("Связь с разработчиком",
                            'если вы желаете помочь разработчику или у вас есть вопросы, можете обращаться по почте: '
                            '\n banil11@yandex.ru')


def doindent_second_frame(size, gde):
    """
    Делает отступ выбранного размера в необходимом месте
    :param size: размер отступа
    :param gde: frame, окно и т.д. где нужно сделать отступ
    :return: строка с нужным отступом
    """
    ots = Label(gde, bg=colorbackground)
    if size == 0:
        ots.config(font='Times 7')
    else:
        ots.config(font='Times 20')
    return ots


def doradiobutton(kolvo):
    """
    Создает необходимой заданию количество радиокнопок, привязанных к одной группе
    :param kolvo: номер задания
    :return:  frame с радиокнопками и группу в которой находятся радиокнопки одного задания
    """
    value_frame = Frame(second_frame, bg=colorbackground, width=screen_width, height=50)
    var = IntVar()
    # 2 балловая система
    Label(value_frame, text='Ваша оценка:', font='Times 14 bold', bg=colorbackground_number_zadaniy).place(
        x=screen_width // 10, y=0, width=150, height=30)
    Radiobutton(value_frame, text='0 баллов', font='Times 14 bold', bg=colorbackground, variable=var, value=0).place(
        x=screen_width // 5,
        y=0, width=100,
        height=30)
    Radiobutton(value_frame, text='1 балл', font='Times 14 bold', bg=colorbackground_number_zadaniy, variable=var,
                value=1).place(
        x=screen_width // 3, y=0, width=100, height=30)
    Radiobutton(value_frame, text='2 балла', font='Times 14 bold', bg=colorbackground_number_zadaniy, variable=var,
                value=2).place(
        x=screen_width // 2, y=0, width=100, height=30)
    # 3 балловая система
    if kolvo == 13 or kolvo == 16:
        Radiobutton(value_frame, text='3 балла', font='Times 14 bold', bg=colorbackground_number_zadaniy, variable=var,
                    value=3).place(
            x=screen_width - (screen_width // 3), y=0, width=100, height=30)
    # 4 балловая сстема
    elif kolvo == 17 or kolvo == 18:
        Radiobutton(value_frame, text='3 балла', font='Times 14 bold', bg=colorbackground_number_zadaniy, variable=var,
                    value=3).place(
            x=screen_width - (screen_width // 3), y=0, width=100, height=30)
        Radiobutton(value_frame, text='4 балла', font='Times 14 bold', bg=colorbackground_number_zadaniy, variable=var,
                    value=4).place(
            x=screen_width - (screen_width // 10), y=0, width=100, height=30)
    return value_frame, var


# ФУНКЦИИ-ПОМОЩНИКИ
def alldelete(what_delete):
    """
    Удаляет все объекты находящиеся в массиве
    :param what_delete: массив объектов
    :return: пустой массив
    """
    for i in what_delete:
        i.destroy()
    return []


def on_mouse_wheel(chto, event):
    """
    Привязка движения скроллбара к прокручиванию мышки
    :param chto: объект к которому привязывается прокрутка
    :param event: событие прокрутки
    """
    chto.yview_scroll(-1 * int((event.delta / 120)), "units")


def create_scrollbar():
    """
    Создается frame с привязанным к нему скроллбаром. Основная особенность в том, что скроллбар
    привязывается лишь к канвас, поэтому создается несколько и frame canvas
    """
    global second_frame
    # создаю фрейм и растягиваю на весь экран
    main_frame = Frame(main_window)
    main_frame.pack(fill=BOTH, expand=1)
    # создаю холст и растягиваю на фрейм
    canvas = Canvas(main_frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    canvas.config(width=width, height=height)
    # создаю полосу прокрутки и прикрепляю справа
    scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    # прикрепляю полосу прокрутки к холсту и присоединяю к прокрутке
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind_all("<MouseWheel>", partial(on_mouse_wheel, canvas))
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # новый фрейм и прикрепление к холсту
    second_frame = Frame(canvas)
    second_frame.config(bg=colorbackground)
    canvas.create_window((0, 0), window=second_frame, anchor="nw")
    # добавляем в массив для удаления фреймы
    massiv_delete.append(main_frame)


def docheck(number):
    """
    Функция обрабатывает введенные ответы, после чего запускает их проверку,
    после получения результата запускается проверка второй части
    :param number: номер варианта
    """
    global strvvoda, reshenie_go, label_time
    # останавливаю и прячу таймер
    reshenie_go = False
    label_time.pack_forget()
    # проверка ответов в первой части
    massiv_otvetov = [0]
    for i in range(1, 11 + 1):
        insertanswer = strvvoda[i].get()
        insertanswer.replace(',', '.')
        ischislo = True
        for k in insertanswer:
            if not ('0' <= k <= '9' or k == '.'):
                ischislo = False
        if ischislo and insertanswer != '':
            insertanswer = float(insertanswer)
        massiv_otvetov.append(insertanswer)
    vern = sravnenie_otvetov(massiv_otvetov, number)
    docheck2(number, vern)


# ФУНКЦИИ ВРЕМЕНИ
def start_time(number):
    """
        Функция запускают таймер, считывая с системы время и задает время окончания.
        После этого запускает функцию проверки и обновления времени.
        :param number: передает номер варианта для следующей функции
        """
    d1 = datetime.datetime.now()  # время сейчас
    d2 = d1 + datetime.timedelta(hours=3, minutes=55)  # время окончания
    label_time.config(text=d2 - d1)
    label_time.pack(side=LEFT)
    main_window.after(1000, partial(check_time, d2, number))
    return 'start'


def check_time(konec, number):
    """
        Функция обновляет время на экране решения, считывая настоящее время из системы,
        и в случае наступление конца экзамена запускает проверку
        global reshenie_go служит флагом о том, идет решение или нет. Без нее при проврке может случится ошибка,
        когда пользователь выйдет раньше, а потом кончится время
        :param konec: передает время окончания решения, после которого автоматически перейдет на страницу проверки
        :param number: передает номер выбранного пользователем варианта
        """
    global reshenie_go
    d1 = datetime.datetime.now()  # время в данный момент
    d_show = konec - d1  # время до конца экзамена
    d_show = str(d_show)
    label_time.config(text=d_show[:d_show.rfind('.')])  # отображение только часов, минут и секунд
    if d1 <= konec and reshenie_go:  # если время не вышло то обновить таймер
        main_window.after(1000, partial(check_time, konec, number))
    elif reshenie_go:  # сли время вышло и пользователь решает, то идти на проверку
        docheck(number)
        reshenie_go = False


# ФУНКЦИИ ДЛЯ РАСЧЕТА
def sravnenie_otvetov(otveti, number):
    """
    Функция сравнивает ответы пользователя с ответами на задания и подсчитывает количество набранных баллов
    :param otveti: массив с введенными ответами пользователя
    :param number: номер варианта
    :return: количество набранных баллов в первой части
    """
    k = 0
    for i in range(1, 11 + 1):
        if otveti[i] == data_var.otvet[number][i]:
            k += 1
    return k


def srballvtoroichasti(massivradiobutton):
    """
        Функция подсчитывает количество баллов, набранных при самооценке пользователем во второй части
        :param massivradiobutton: массив радиокнопок с оценками пользователя
        :return: сумма набранных баллов во второй части
        """
    summa = 0
    for i in range(len(massivradiobutton)):
        summa += massivradiobutton[i].get()
    return summa


def raschitprocenti(ball):
    """
        Происходит перевод первичных баллов во вторичные по шкале ЕГЭ
        :param ball: первичный балл набранный участником
        :return: вторичный балл взятый из файла с данными
        """
    for i in range(0, 64, 2):
        if ball == data_var.grade_translate[i]:
            return data_var.grade_translate[i + 1]


def nadpis(procent):
    """
        Функция подбирает авторский комментарий под количество набранных процентов участником
        :param procent: количество набранных вторичных баллов
        :return: строка-комментарий автора
        """
    stroka = ''
    if procent <= 23:
        stroka += 'К сожалению вы не сдали экзамен. Готовьтесь усерднее!'
    elif 23 < procent < 50:
        stroka += 'Вы сдали экзамен, но результат не высокий. Возможно стоит подготовиться еще.'
    elif 50 <= procent <= 68:
        stroka += 'Вы сдали экзамен, результат примерно такой же как у большинства по стране. ' \
                  'Еще немного и ты будешь лучше остальных!'
    elif 69 <= procent < 90:
        stroka += 'Вы сдали экзамен, результат очень хороший. Осталось выучить самое сложное!'
    elif 90 <= procent < 100:
        stroka += 'Вы сдали экзамен, результат впечатляет. Сможешь написать на 100? Я в тебя верю!'
    else:
        stroka += 'Ура! Ура! Ура! Это 100% за профильную матеатику на ЕГЭ!!! Поздравляю тебя!!!'
    return stroka


def nadpis_ball(chislo):
    """
        Происходит подбор нужного падежа под количество набранных баллов
        :param chislo: число набранных баллов
        :return: строка-надпись о баллах
        """
    if chislo % 10 == 0 or 5 <= chislo <= 20 or 25 <= chislo <= 30:
        stroka = 'баллов'
    elif chislo % 10 == 1:
        stroka = 'балл'
    else:
        stroka = 'балла'
    return stroka


kolvariantov = 10  # количество вариантов в программе
# ширина и высота при выходе из полноэкранного режима
width = 1200
height = 700
password = '159753'  # пароль для вариантов
strvvoda = []  # массив для строк ввода
radiobutton = []  # массив для радиокнопок
strvvoda.append(0)
# цвета
colorbackground = '#FEFFF3'
colorbackground_number_zadaniy = '#35F621'
background_button_check = '#F62421'
color_button_variant = '#AEFC77'
color_str_vvoda = '#F0F2EF'
massiv_delete = []  # массив для хранения удаляемых объктов
reshenie_go = True  # идет ли экзамен или нет

main_window = Tk()
screen_width = main_window.winfo_screenwidth()  # ширина экрана пользователя
screen_height = main_window.winfo_screenheight()  # высота экрана пользователя
main_window.title("Подготовка к ЕГЭ по математике")
main_window.config(width=width, height=height)
main_window.state("zoomed")  # открываем полноэкранный режим
label_time = Label(main_window, text='', font='Times 16 bold', bg=colorbackground)

drawmainwindow()

main_window.mainloop()
