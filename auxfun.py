import copy
import shutil
import webbrowser

import requests
import pprint
from time import sleep

import numpy as nm
import talib as ta
import locale

import operator
import requests
from datetime import datetime

from bs4 import BeautifulSoup

list_names_main = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'NEARUSDT',
                   'MATICUSDT', 'LTCUSDT']




list_string_Remove = ['futures/usdc/', 'usdt/', ]
class InstrInfo:
    # intType = 1 MA10 > MA70 для лонга или  MA10 < MA70 для шорта
    # intType = 2 цена вчера закрылась выше(лонг) или ниже(шорт) обеих МА
    def __init__(self, symbol, turnover24h, price24Pcnt, priceLast,
                 priceLastDay=0.0, ema_10D=0.0, ema_70D=0.0,
                 intType=0):
        self.symbol = symbol
        self.turnover24h = float(turnover24h)  # то что дается для инструмента в виде объема
        self.price24Pcnt = float(price24Pcnt)
        self.priceLast = float(priceLast)
        self.priceLastDay = float(priceLastDay)
        self.ema_10D = float(ema_10D)
        self.ema_70D = float(ema_70D)
        self.intType = int(intType)

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.turnover24h < other.turnover24h
        return False

    # def __str__(self):
    #     return f'symbol={self.symbol}, turnover24h={self.turnover24h}, price24Pcnt={self.price24Pcnt}'

class InstrData:
    def __init__(self, prc, hyper):
        self.prc = prc
        self.hyper = hyper


def get_listMonets(intQvnt=100):
    bool_repeat = True
    while (bool_repeat):
        try:
            text = input("type Enter for skip(100 монет)\nили количество монет:")
            if text == "":
                bool_repeat = False
            else:
                intQvnt = int(text)
                bool_repeat = False

        except ValueError:
            print('Недопустимый ввод, введите число')

    list_instrum_All = get_list_instrums()
    list_instrum_All.reverse()
    list_instrum = list_instrum_All[:intQvnt]
    sleep(1)

    str_file_save = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_work150.txt"
    write_listelem_to_file(str_file_save, list_instrum)

    list_workEMA = getinstrbybit70D(list_instrum, 'long')

    str_file_save = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workEMA.txt"
    write_listelem_to_file(str_file_save, list_workEMA)

    print('Done list_workEMA.txt')

    return list_workEMA


def write_listelem_to_file(str_file_save, list_elem):
    locale.setlocale(locale.LC_ALL, '')
    try:
        with open(str_file_save, 'w') as fp:
            int_count = 0

            for item in list_elem:
                strMoney = locale.format_string('%d', item.turnover24h, grouping=True)
                if (0 != int(item.intType)):
                    str_write = item.symbol + '   ' + str(int(item.intType)) + '             ' + strMoney
                else:
                    str_write = item.symbol + '             ' + strMoney
                fp.write("%s\n" % str_write)

    except:
        print("Exception : ")
        print(str_file_save)

    return


def fun_get_ListWork70(str_file_in="list_work70.txt"):
    list_class_hyp = []

    if str_file_in == "":
        bool_repeat = True
        while (bool_repeat):
            try:
                text = input("type Enter for ListWork70\nили имя файла:")
                if text == "":
                    str_file_in = ""
                    bool_repeat = False
                else:
                    str_file_in = text
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите имя файла')

    list_instruments = []
    if (str_file_in == ""):
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_work70.txt"
    else:
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\" + str_file_in

    with open(str_file, 'r') as f:
        list_instruments = [line[:-1] for line in f]

    int_count = 0
    intcountelem = len(list_instruments)

    for elem in list_instruments:

        hyper = 'https://www.bybit.com/trade/usdt/' + elem
        print(hyper)  # Вывод: foo
        webbrowser.open(hyper)  # Go to example.com

        int_count = int_count + 1
        str_print = str(int_count) + r'/' + str(intcountelem)
        print(str_print)
        bool_repeat = True

        while (bool_repeat):
            try:
                text = input("type Enter for skip\nor any value to save:")
                if text == "":
                    bool_repeat = False
                else:
                    list_class_hyp.append(hyper)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyp


def moving_average(x, n, type='exp'):
    x = nm.asarray(x)
    if type == 'simple':
        weights = nm.ones(n)
    else:
        weights = nm.exp(nm.linspace(-1., 0., n))

    weights /= weights.sum()

    a = nm.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


# Функция подсчета среднего на основе библиотеки  talib
def CalculateEMA(listallsec, timeperiod=10):
    # Prepare data for numpy and talib

    return_data = []
    for each in listallsec:
        return_data.append(float(each))

    np_array = nm.array(return_data)
    out = ta.EMA(np_array, timeperiod)

    return out[-1]


def CalculateEMA_ATR(listallsec, timeperiod=10):
    # Prepare data for numpy and talib

    return_data = []
    for each in listallsec:
        if (0.0 == float(each)):
            each = 0.000001
        return_data.append(float(each))

    np_array = nm.array(return_data)
    out = ta.EMA(np_array, timeperiod)

    return out[-1]


def getkindle(strinstr, strcategory, strperiod, strlimit, intEMAPER=10):
    list_close = []
    str_in = 'https://api.bybit.com/v5/market/kline?category=' + strcategory + '&symbol=' + \
             strinstr + '&interval=' + strperiod + '&limit=' + strlimit
    klines = requests.get(str_in)
    result = klines.json()
    # pprint.pprint(result)
    result_result = result['result']
    result_result_list = result_result['list']
    if (len(result_result_list) > intEMAPER + 2):
        for elem in result_result_list:
            list_close.append(float(elem[4]))

        list_close.reverse()

    # print( strinstr)
    sleep(1)  # MUST BE!!!
    return list_close


def checkEMA(elem, period='W', strcategory='linear'):
    float_period = 10
    list_close = []
    floatEMA = 0.0
    list_close = getkindle(elem.symbol, strcategory, period, '200')

    intreturn = 999
    floatCloseLastOneBefore = 0
    if (len(list_close) > float_period + 2):
        floatlast_close = list_close[-1]
        floatEMA = CalculateEMA(list_close)
        if (floatlast_close > floatEMA):
            intreturn = 1
        elif (floatlast_close < floatEMA):
            intreturn = -1
        else:
            intreturn = 0

        floatCloseLastOneBefore = list_close[-2]  # Цена Закрытия вчера по времени Bybit

    return intreturn, floatEMA, floatCloseLastOneBefore


def getinstrbybit70D(list_instrum, strdirection='long', strcategory='linear'):
    list_ret = []
    locale.setlocale(locale.LC_ALL, '')
    for elem in list_instrum:
        # if( elem.symbol == 'PARTIUSDT'):
        #     injg = 0
        #
        boollist_ret_append = False
        intType = 0
        # priceLastWeek Не используется
        intxcheck_70, floatEMA_70, priceLastWeek = checkEMA(elem, 'W')
        if (intxcheck_70 == 999):  # инструмент торгуется малый период
            continue
        intxcheck_10, floatEMA_10, priceLastDay = checkEMA(elem, 'D')
        if (intxcheck_10 == 999):  # инструмент торгуется малый период
            continue
        if (strdirection == 'long'):
            if intxcheck_70 in [0, 1]:
                if (floatEMA_10 >= floatEMA_70):
                    # Заносим элемент в список если он сегодня торгуется так, что
                    # МА10Д больше МА70Д
                    boollist_ret_append = True
                    intType = 1
                elif (priceLastDay > floatEMA_10 and
                      priceLastDay > floatEMA_70):
                    # Заносим элемент в список если он вчера торговался выше
                    # обеих своих скользящих средних
                    boollist_ret_append = True
                    intType = 2
        elif (strdirection == 'short'):
            if intxcheck_70 in [-1, 0]:
                if (floatEMA_10 <= floatEMA_70):
                    # Заносим элемент в список если он сегодня торгуется так, что
                    # МА10Д меньше МА70Д
                    boollist_ret_append = True
                    intType = 1
                elif (priceLastDay < floatEMA_10 and
                      priceLastDay < floatEMA_70):
                    # Заносим элемент в список если он вчера торговался ниже
                    # обеих своих скользящих средних
                    boollist_ret_append = True
                    intType = 2

        # Физическое занесение в сисок торгуемых, при удовлетворении условий выше.
        if (boollist_ret_append == True):
            elem_new = elem
            elem_new.ema_70D = floatEMA_70
            elem_new.ema_10D = floatEMA_10
            elem_new.intType = intType
            list_ret.append(elem_new)
            # ========================================================
            strMoney = locale.format_string('%d', elem.turnover24h, grouping=True)
            strprint = elem.symbol + '   ' + str(intType) + '   ' + strMoney
            print(strprint)

    return list_ret


def fun_open_List_Instruments(list_instr, boolSaveList=True):
    intCount = 0
    list_class_hyp1 = []

    for elem in list_instr:

        ppname = elem[:elem.find(':')]
        ppname = fun_convert(ppname)

        strhyper1 = 'https://www.bybit.com/trade/' + ppname
        webbrowser.open(strhyper1)  # Go to example.com

        bool_repeat = True
        print(strhyper1)
        intCount = intCount + 1
        print(elem)
        print(intCount)
        # intNum = data_into_list.__len__() - intCount

        while (bool_repeat):
            try:
                if (boolSaveList == True):
                    text = input("type Enter for skip\nor any value to save:")
                else:
                    text = input("type Enter for skip\n")

                if text == "":
                    bool_repeat = False
                else:
                    float_percent = float(text)
                    aa = InstrData(float_percent, strhyper1)
                    list_class_hyp1.append(aa)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyp1


def fun_createAdrVolAlfa():
    print("fun_createAdrVolAlfa")

    str_fileAdr = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_Adr.txt"
    str_fileVol = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_4Days.txt"
    str_fileAlfa = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_AlfaFactor.txt"

    listAdr = []
    listVol = []
    listAlfa = []

    strProblema = ""
    try:
        strProblema = "str_fileAdr"
        with open(str_fileAdr, 'r') as f:
            listAdr = [line[:-1] for line in f]
        listAdr = fun_clearListInstrs(listAdr)

        strProblema = "str_fileVol"
        with open(str_fileVol, 'r') as f:
            listVol = [line[:-1] for line in f]
        listVol = fun_getVolatile(listVol)
        listVol = fun_clearListInstrs(listVol)

        strProblema = "str_fileAlfa"
        with open(str_fileAlfa, 'r') as f:
            listAlfa = [line[:-1] for line in f]

        listAlfa = fun_getAlfa(listAlfa)
        listAlfa = fun_clearListInstrs(listAlfa)

        new_list = listAdr + listVol + listAlfa
        list_res = []  # создаем список, в котором
        # будут храниться уникальные элементы
        for strelem in new_list:
            if strelem not in list_res:  # проверка на наличие элемента в списке
                strelem = strelem
                list_res.append(strelem)  # добавляем новый элемент

        list_res2 = []
        for strelem in list_res:
            strelem = strelem + ':'
            list_res2.append(strelem)  # добавляем новый элемент
        print(list_res2)

        str_file_combi = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\LastCombi.txt"
        strProblema = str_file_combi
        with open(str_file_combi, 'w') as fp:
            int_count = 0
            for item in list_res2:
                fp.write("%s\n" % item)

            print('Done Last_Combi.txt')
    except ValueError:
        print("Проблема с файлом: ")
        print(strProblema)

    return list_res2


def fun_getVolatile(listVol):
    listVolNew = []

    for strelem in listVol:
        if "-1.0" in strelem:
            listVolNew.append(strelem)

    return listVolNew


def fun_getAlfa(listAlfa):
    listAlfaNew = []

    str_SpecAlfa = "+"
    boolRepeat = True
    while (boolRepeat):
        str_SpecAlfa = str(input('(-) для падения\n(+) для роста: '))
        if "+" == str_SpecAlfa:
            boolRepeat = False
            for strelem in listAlfa:
                if "-" not in strelem:
                    listAlfaNew.append(strelem)
        elif "-" == str_SpecAlfa:
            boolRepeat = False
            for strelem in listAlfa:
                if "-" in strelem:
                    listAlfaNew.append(strelem)

    return listAlfaNew


def fun_get_ListWorkLast(str_file_in="LastCrypto.txt"):
    list_class_hyp3 = []
    if str_file_in == "":
        bool_repeat = True
        while (bool_repeat):
            try:
                text = input("type Enter for LastCrypto\nили имя файла:")
                if text == "":
                    str_file_in = ""
                    bool_repeat = False
                else:
                    str_file_in = text
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите имя файла')

    list_instruments = []
    if (str_file_in == ""):
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\LastCrypto.txt"
    else:
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + str_file_in

    with open(str_file, 'r') as f:
        list_instruments = [line[:-1] for line in f]

    int_count = 0
    intcountelem = len(list_instruments)

    for elem in list_instruments:

        text = elem
        hyper = ""
        try:
            separator_old, hyper = text.split('#', 1)
            if str_file_in == "LastCrypto.txt":
                separator_new, hyper = hyper.split('#', 1)

        except:
            hyper = text

        print(hyper)  # Вывод: foo
        webbrowser.open(hyper)  # Go to example.com

        int_count = int_count + 1
        str_print = str(int_count) + r'/' + str(intcountelem)
        print(str_print)
        bool_repeat = True

        while (bool_repeat):
            try:
                text = input("type Enter for next:")
                if text == "":
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

        #
        # time.sleep(13)

    return list_class_hyp3

def fun_clearListInstrs(listInstrs):
    listInstrlNew = []

    for elem in listInstrs:

        text = elem
        hyper = ""
        try:
            separator_old, hyper = text.split(':', 1)
            listInstrlNew.append(separator_old)

        except:
            print("Exception : ")
            print(elem)  # Вывод: foo

    return listInstrlNew


def get_N_instruments():
    intInstMax = 100
    list_simple = get_list_instrums(intInstMax)

def fun_save_volatileLast(intDays):
    list_instruments = []
    # str_date = datetime.now().strftime('%Y_%m_%d')
    strDays = str(intDays)
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\" + strDays + "Days.txt"

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    del list_instruments[1::2]

    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file_new = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_" + strDays + "Days.txt"
    try:
        with open(str_file_new, 'w') as fp:
            for item in list_instruments:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done Last_N_Days.txt')

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)
    return


def fun_save_AdrLast():
    list_instruments = []
    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\Adr.txt"

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    del list_instruments[1::2]

    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file_new = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_Adr.txt"
    try:
        with open(str_file_new, 'w') as fp:
            for item in list_instruments:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done Last_Adr.txt')

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)
    return


def fun_save_AlfaFactorLast():
    list_instruments = []
    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\AlfaFactor.txt"

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    del list_instruments[1::2]

    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file_new = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_AlfaFactor.txt"
    try:
        with open(str_file_new, 'w') as fp:

            int_count = 0
            for item in list_instruments:
                # write each item on a new line
                int_count = int_count + 1
                stritem = item + "__" + str(int_count)
                fp.write("%s\n" % stritem)
            print('Done Last_AlfaFactor.txt')

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)
    return


def fun_get_ShilinVolatile_NDays_Instruments(intNdays):
    list_instruments = []
    # str_date = datetime.now().strftime('%Y_%m_%d')
    strNdDays = str(intNdays)
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_" + strNdDays + "Days.txt"
    if (intNdays == "Adr"):
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_Adr.txt"

    try:
        with open(str_file, 'r') as f:
            list_instr = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    return list_instr


def fun_get_first_AlfaFactorLast():
    list_alfa = []

    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\Last_AlfaFactor.txt"

    try:
        with open(str_file, 'r') as f:
            list_alfa = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    int_SpecFile = 0
    try:
        int_SpecFile = int(input('Число первых записей( файл Last_AlfaFactor.txt): '))

    except ValueError:
        print('Недопустимый ввод')

    if (int_SpecFile > 0):
        del list_alfa[int_SpecFile:]
    elif (int_SpecFile < 0):
        del list_alfa[:int_SpecFile]

    return list_alfa

def fun_save_fileTV(strFileName):
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + strFileName + ".txt"
    list_in = []
    list_instrums = []
    try:
        strProb = "Проблема fun_save_fileTV 1 "
        with open(str_file, 'r') as f:
            list_in = [line[:-1] for line in f]

        strProb = "Проблема fun_save_fileTV 2 "
        for elem in list_in:
            text = elem
            hyper = text.split('/', -1)
            list_instrums.append(hyper.pop())

        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + strFileName + "_TV.txt"
        strProb = "Проблема fun_save_fileTV 3 "
        list_instrums.sort()
        with open(str_file, 'w') as fp:
            for item in list_instrums:
                # write each item on a new line
                fp.write("%s\n" % item)

    except:
        print(strProb)

    return


def fun_save_ListWorkLast(list_class_hyph: list, strFileName: str):
    list_class_hyph.sort(key=operator.attrgetter('prc'))

    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + strFileName

    try:
        with open(str_file, 'w') as fp:
            for item in list_class_hyph:
                # write each item on a new line
                if ("" != item.hyper):
                    str1 = str(item.prc) + '#' + item.hyper
                    fp.write("%s\n" % str1)
            print('Done list_huper')

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)
    return


def fun_save_list_workEMA_Work(list_class_hyph: list, strFileName: str):
    try:
        with open(strFileName, 'w') as fp:
            for item in list_class_hyph:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done list_huper')

    except ValueError:
        print("Проблема с файлом: ")
        print(strFileName)
    return


def fun_get_Shilin(boolShilin=True):
    # result =[]
    data_into_list = []
    list_class_hyphe = []

    int_MonNumber = 100
    if (boolShilin == True):
        pageURL = "https://shilintrade.pro/crypto_bot/crypto_best_volume.txt"
        webbrowser.open(pageURL)
        # pu = "https://www.coinbase.com/ru/explore/s/all?page=1"

        req = requests.get(pageURL)
        # req = requests.get(pu)
        soup = BeautifulSoup(req.content, 'html.parser')
        data = soup.text

        data_into_list = data.split("\r\n")

        print(data_into_list)
    else:
        try:
            int_MonNumber = int(input("Введите количество монет: "))

        except ValueError:
            print('Недопустимый ввод')

        list_instrt11, data_into_list = get_list_instrums(int_MonNumber)

    str_time = datetime.now().strftime('%H_%M_%S')
    str_date = datetime.now().strftime('%Y_%m_%d')

    if ("07_30_00" < str_time):

        data_into_list_true = []
        for name_elem in data_into_list:
            name_elem = fun_convert(name_elem)
            data_into_list_true.append(name_elem)

        data_into_list_true = fun_clear_LongList(data_into_list_true)
        str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoLong\\" + str_date + '_' + "cryptoles.txt"
        with open(str_file, 'w') as fp:
            data_into_list_sort = copy.deepcopy(data_into_list_true)
            data_into_list_sort.sort()
            for item in data_into_list_sort:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

    listInstruments = []
    intCount = 0
    intNumStop = 6

    debug_count = 0
    for elem in data_into_list:
        debug_count = debug_count + 1
        # if 4 < debug_count:
        #     break;
        ppname = fun_convert(elem)

        strhyper1 = 'https://www.bybit.com/trade/' + ppname
        webbrowser.open(strhyper1)  # Go to example.com

        bool_repeat = True
        print(strhyper1)
        intCount = intCount + 1
        print(elem)
        print(intCount)
        intNum = data_into_list.__len__() - intCount

        while (bool_repeat):
            try:
                text = input("type Enter for skip\nor percent value to save:")
                if text == "":
                    bool_repeat = False
                else:
                    float_percent = float(text)
                    aa = InstrData(float_percent, strhyper1)
                    list_class_hyphe.append(aa)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyphe


def fun_get_List_PreWork():
    list_instruments = []
    list_class_hyphe = []

    # str_date = datetime.now().strftime('%Y_%m_%d')
    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\cryptowork.txt"

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    intCount = 0

    for elem in list_instruments:
        text = elem
        hyper = ""
        try:
            separator, hyper = text.split('#', 1)

        except:
            hyper = text

        webbrowser.open(hyper)  # Go to example.com

        intCount = intCount + 1
        print(elem)
        print(intCount)

        bool_repeat = True
        while (bool_repeat):
            try:
                text = input("type Enter for skip\nor percent value to save:")
                if text == "":
                    bool_repeat = False
                else:
                    float_percent = float(text)
                    aa = InstrData(float_percent, elem)
                    list_class_hyphe.append(aa)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyphe


def fun_get_List_File_Ema(str_file, intTypeOpen=0):
    list_instruments = []

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    bool_repeat = True
    intType = 0
    while (bool_repeat):
        try:
            text = input("Введите число:\n0 - тип1 и тип2: \n1 - тип1: \n2 - тип2: ")
            if (int(text) == 0 or int(text) == 1 or int(text) == 2):
                intType = int(text)
                bool_repeat = False

        except ValueError:
            print('Недопустимый ввод, введите число')

    intCount = 0

    # strBrowse = 'https://www.bybit.com/trade/usdt/'
    list_class_hyphe = []
    for elem in list_instruments:
        text = elem
        hyper = ''
        cypher = ''
        try:
            hyper = text.split()
            intCypher = int(hyper[1])
            if (0 == intType or intType == intCypher):
                strBrowseHyper = 'https://www.bybit.com/trade/usdt/' + str(hyper[0])
                webbrowser.open(strBrowseHyper)  # Go to example.com

                intCount = intCount + 1
                print(elem)
                print(intCount)
            else:
                continue
        except:
            hyper = text

        bool_repeat = True

        while (bool_repeat):
            try:
                if (intTypeOpen == 0):
                    text = input("type Enter for skip\nor any cypher to save:")
                    if text == "":
                        bool_repeat = False
                    else:
                        strelem = str(hyper[0]) + ' ' + str(hyper[1])
                        list_class_hyphe.append(strelem)
                        bool_repeat = False
                elif (intTypeOpen == 1):
                    text = input("type Enter for next:")
                    bool_repeat = False


            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyphe


def fun_save_ListWork(list_huper: list):
    str_time = datetime.now().strftime('%H_%M_%S')
    str_date = datetime.now().strftime('%Y_%m_%d')

    str_file = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + str_date + '_' + "cryptowork.txt"
    try:
        with open(str_file, 'w') as fp:
            data_into_list_sort = copy.deepcopy(list_huper)
            data_into_list_sort.sort()
            for item in data_into_list_sort:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done list_huper')

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    return


def fun_save_withtime_ListWorkLast(strfilename="LastCrypto"):
    # str_time = datetime.now().strftime('%H_%M_%S')
    # str_date = datetime.now().strftime('%Y_%m_%d')

    str_fileCrypto = strfilename
    if strfilename != "LastCrypto":
        str_fileCrypto = str_fileCrypto

    str_fileCryptoFull = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + str_fileCrypto + ".txt"
    mtime = os.path.getmtime(str_fileCryptoFull)
    mtime_readable = datetime.fromtimestamp(mtime).strftime('%Y_%m_%d_%H_%M_%S')

    str_fileCryptoFullName = "E:\\YandexDisk\\КШ\\CryptoArchive\\CryptoShort\\" + mtime_readable + '_' + str_fileCrypto + ".txt"
    print(mtime_readable)
    try:
        shutil.copyfile(str_fileCryptoFull, str_fileCryptoFullName)
        print("Done  %s " % strfilename)

    except ValueError:
        print("Проблема с файлом: %s " % str_fileCrypto)

    return


def fun_clear_LongList(datalist: list):
    datalist_new = []
    for name_elem in datalist:
        # name_elem = fun_convert(name_elem)

        for sub_str in list_string_Remove:
            if (sub_str in name_elem):
                str_new = name_elem.replace(sub_str, '')
                datalist_new.append(str_new)

    if ('' in datalist_new):
        datalist_new.remove('')

    return datalist_new

def get_list_instrums(intN=-1):
    list_instrums = []
    list_instrumsn = []
    list_simple = []
    str_http = 'https://api.bybit.com/v5/market/tickers?category=linear'
    klines = requests.get(str_http)
    result = klines.json()
    result_result = result['result']
    list_data = result_result['list']
    for elem in list_data:
        if ('USDT-' in elem['symbol']):
            continue
        elif ('USDT' in elem['symbol']):

            class_elem = InstrInfo(elem['symbol'], elem['turnover24h'], elem['price24hPcnt'], elem['lastPrice'])
            list_instrums.append(class_elem)
            # list_simple.append(elem['symbol'])
            # pprint.pprint(elem)

    list_instrums.sort(key=lambda x: x.turnover24h)
    # if( intN != -1 ):
    #     list_instrumsn = list_instrums[-(intN):]
    # else:
    #     list_instrumsn = list_instrums

    # for elem in list_instrumsn:
    #     list_simple.append(elem.symbol)

    sleep(1)  # MUST BE!!!
    return list_instrums
def fun_convert(strName: str):
    # strName = "NEIROUSDT"
    strRet: str = ""
    if ("NEIROUSDT" == strName):
        strRet = 'usdt/' + "NEIROETHUSDT"
    elif ("RAYUSDT" == strName):
        strRet = 'usdt/' + "RAYDIUMUSDT"
    elif ("LADYSUSDT" == strName):
        strRet = 'usdt/' + "10000" + strName
    elif ("LAYERUSDT" == strName):
        strRet = 'usdt/' + "SO" + strName
    elif ("PEPEUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("1000SATSUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("BONKUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("XUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("CHEEMSUSDT" == strName):
        strRet = 'usdt/' + "1000000" + strName
    elif ("BONK-PERP" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("NEIROCTOUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("MOGUSDT" == strName):
        strRet = 'usdt/' + "1000000" + strName
    elif ("RATSUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("PEPE-PERP" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("TOSHIUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("CATSUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("FLOKIUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("MUMUUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    elif ("SHIBUSDT" == strName):
        strRet = 'futures/usdc/' + "SHIB1000-PERP"
    elif ("TURBOUSDT" == strName):
        strRet = 'usdt/' + "1000" + strName
    else:
        strRet = 'usdt/' + strName

    return strRet