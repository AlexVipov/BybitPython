import copy
import os
import shutil
import traceback
import webbrowser

import ccxt
import pandas as pd
import numpy as np
import talib as ta
import pprint
from time import sleep

import numpy as nm
import talib as ta
import locale

import requests
from datetime import datetime

from ccxt import BadSymbol

# gl_strPathSave = "E:\\YandexDisk\\КШ\\CryptoArchive\\"
gl_strPathSave = "D:\\CryptoArchive\\"
gl_strCurrentWork = "CurrentWork\\"
gl_strShablon = "Шаблоны\\"

list_names_main = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT', 'ADAUSDT', 'AVAXUSDT', 'DOTUSDT', 'NEARUSDT',
                   'MATICUSDT', 'LTCUSDT']


def fun_ATR(symbol, period = '1d'):
    import ccxt
    import pandas as pd

    exchange = ccxt.bybit()

    sleep(1)
    # Загружаем данные
    df = pd.DataFrame(exchange.fetch_ohlcv(symbol,period, limit=100),
                      columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")

    # Расчёт ATR вручную
    df["tr"] = df["high"] - df["low"]
    df["tr"] = df["tr"].combine_first((df["high"] - df["close"].shift()).abs())
    df["tr"] = df["tr"].combine_first((df["low"] - df["close"].shift()).abs())
    df["atr"] = df["tr"].rolling(14).mean()

    current_atr = df["atr"].iloc[-1]
    mean_atr = df["atr"].mean()
    ratio = current_atr / mean_atr * 100

    print(f"Текущий ATR: {current_atr:.4f} | Средний ATR: {mean_atr:.4f} | Отношение: {ratio:.1f}%")

    if ratio < 60:
        print("📉 Внимание: Сжатие волатильности (ATR Squeeze) — возможен скорый breakout!")
    else:
        print("✅ Волатильность в норме")

def aux_CalculateEMA_ATR(listallsec, timeperiod=10):
    # Prepare data for numpy and talib

    return_data = []
    for each in listallsec:
        if( 0.0 == float(each)):
            each = 0.000001
        return_data.append(float(each))

    np_array = np.array(return_data)
    out = ta.EMA(np_array, timeperiod)

    return


def aux_atr_QuikFormula(name, df: pd.DataFrame,
                        length: int = 14,
                        bool_EMA: bool = False,
                        period_EMA: int = 75) -> pd.Series:

    high = []
    low = []
    close = []
    open = []
    time = []
    TR = []
    ATR_Quik = []

    # for elem in df:
    for i, elem in df.iterrows():
        high.append(elem.high)
        low.append(elem.low)
        open.append(elem.open)
        close.append(elem.close)
        time.append(elem.ts)
        ii = 1


    TR.append(abs(high[0] - low[0]))
    maxcount = high.__len__()
    for icount in range(1, maxcount):
        val1 = abs(high[icount] - low[icount])
        val2 = abs(high[icount] - close[icount-1])
        val3 = abs(low[icount] - close[icount - 1])
        val_res = max(val1, val2, val3)
        TR.append(val_res)

    for icount in range(0, maxcount):
        if( icount < length):
            ATR_Quik.append(0)
        if( icount == length ):
            val = sum(TR)/length
            ATR_Quik.append(val)
        if(icount > length):

            val = (ATR_Quik[icount-1]*(length-1) + TR[icount]) / length
            ATR_Quik.append(val)

    ii1 = 1
    # dictionary of lists

    if( False == bool_EMA):
        dict1 = {'NAME': [name,],
                'DATE': [time.pop(),],
                 # 'HIGH': [high.pop(),],
                 # 'LOW': [low.pop(),],
                 # 'OPEN': [open.pop(),],
                 # 'CLOSE': [close.pop(),],
                 'ATR_DAY': [ATR_Quik.pop(),]}
    else:
        EMA75 = aux_CalculateEMA_ATR(ATR_Quik, period_EMA)
        ii = 1234
        dict1 = {'NAME': [name, ],
                 'DATE_TIME': [time.pop(), ],
                 # 'HIGH': [high.pop(), ],
                 # 'LOW': [low.pop(), ],
                 # 'OPEN': [open.pop(), ],
                 # 'CLOSE': [close.pop(), ],
                 'ATR_EMA_H1': [EMA75[-1], ]}

    df_Full = pd.DataFrame(dict1)


    return df_Full

def fun_CalculateAtr():

    dfd_day = pd.DataFrame(columns={'ts': datetime, 'open': float, 'high': float,
                                    'low': float, 'close': float, 'volume': float})
    strMoney = str(input("Монета: "))
    if(strMoney == ""):
        return -1, dfd_day

    exchange = ccxt.bybit()

    try:
        sleep(1)
        dfd_day = pd.DataFrame(exchange.fetch_ohlcv(strMoney, "1d", limit=100),
            columns=["ts", "open", "high", "low", "close", "volume"])

    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
        return -1, dfd_day

    dfd_day["ts"] = pd.to_datetime(dfd_day["ts"], unit="ms")
    # Удаляем последнюю сторку - на сегодня
    dfd_day = dfd_day.iloc[:-1]
    # print(dfd_day.tail())

    df_DAY  = aux_atr_QuikFormula ( strMoney, dfd_day)

    return 0, df_DAY



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

    str_file_save = gl_strPathSave + "list_work150.txt"
    write_listelem_to_file(str_file_save, list_instrum)
    fun_save_withdatetime(str_file_save)

    list_workEMA = getinstrbybit70D(list_instrum, 'long')

    str_file_save = gl_strPathSave + "list_workEMA.txt"
    write_listelem_to_file(str_file_save, list_workEMA)
    fun_save_withdatetime(str_file_save)

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

# Функция подсчета среднего на основе библиотеки  talib
def CalculateEMA(listallsec, timeperiod=10):
    # Prepare data for numpy and talib

    return_data = []
    for each in listallsec:
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
            intxcheck_70 = 2 # инструмент торгуется малый период, новый и могут толкнуть
            floatEMA_70 = 0 # инструмент торгуется малый период, новый и могут толкнуть
            # continue
        intxcheck_10, floatEMA_10, priceLastDay = checkEMA(elem, 'D')
        if (intxcheck_10 == 999):  # инструмент торгуется малый период
            continue
        if (strdirection == 'long'):
            # if intxcheck_70 in [0, 1]:
            if intxcheck_70 in [0, 1, 2]: # 2 - инструмент торгуется малый период, новый и могут толкнуть
                if (floatEMA_10 >= floatEMA_70 and floatEMA_70 > 0 ):
                    # Заносим элемент в список если он сегодня торгуется так, что
                    # МА10Д больше МА70Д
                    boollist_ret_append = True
                    intType = 1
                elif (floatEMA_70 == 0 and priceLastDay > floatEMA_10):
                    #инструмент торгуется малый период, новый и могут толкнуть
                    # Заносим элемент в список если он сегодня торгуется так, что
                    # priceLastDay больше floatEMA_10
                    boollist_ret_append = True
                    intType = 1
                elif (priceLastDay > floatEMA_10 and priceLastDay > floatEMA_70):
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
            print("----------------------------------------")
            print(strprint)
            # fun_ATR(str(elem.symbol))


    return list_ret


def fun_open_List_Instruments(list_instr, boolSaveList=True):
    intCount = 0
    list_class_hyp1 = []

    for elem in list_instr:

        ppname = elem[:elem.find(':')]
        #Конвертируем если берем из КриптоБота
        ppname_forweb = fun_convert(ppname)

        ppercent = elem[elem.find(':'):]
        ppercent = ppercent[2:]

        strhyper1 = 'https://www.bybit.com/trade/' + ppname_forweb
        webbrowser.open(strhyper1)  # Go to example.com

        bool_repeat = True
        print(strhyper1)
        intCount = intCount + 1
        print(elem)
        strprint = str(intCount) + '\\' + str(len(list_instr))
        print(strprint)


        while (bool_repeat):
            try:
                if (boolSaveList == True):
                    text = input("type Enter for skip\nor any value to save:")
                else:
                    text = input("type Enter for skip\n")

                if text == "":
                    bool_repeat = False
                else:
                    # float_percent = float(text)
                    # aa = InstrData(ppercent, strhyper1)
                    aa = InstrData(ppercent, ppname)
                    list_class_hyp1.append(aa)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    return list_class_hyp1

def fun_get_choose_bot_file():

    bool_repeat = True
    while (bool_repeat):
        try:
            print("Выберите тип файла из бота:")
            print("AlfaFactor_5_Days введите 1")
            print("AlfaFactor_20_Days введите 2")
            print("AlfaFactor_60_Days ведите 3")
            print("AlfaFactor_All_Days  введите 4")
            print("------------------------")
            print("Vol_4_Days введите 5")
            print("Vol_10_Days введите 6")
            print("Vol_20_Days введите 7")
            print("------------------------")
            print("Adr введите 8")
            print("------------------------")
            text = input("Ввод числа (0 - выход): ")
            if text not in ['0', '1', '2', '3', '4', '5', '6', '7', '8']:
                print("Недопустимый ввод")
                bool_repeat = True
            elif (text == '0'):
                int_in = int(text)
                bool_repeat = False
                return
            else:
                int_in = int(text)
                bool_repeat = False

        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

    return text
def fun_getListFromBotShablon():

    # print("Создать Last_***.txt из бота")
    int_in  = int(fun_get_choose_bot_file())
    if( int_in == 0 ):
        return

    strfile = gl_strPathSave + gl_strShablon
    if int_in  == 1:
        strfile = strfile + "AlfaFactor_5_Days.txt"
    elif (int_in  == 2):
        strfile = strfile + "AlfaFactor_20_Days.txt"
    elif (int_in  ==3):
        strfile = strfile + "AlfaFactor_60_Days.txt"
    elif (int_in  == 4):
        strfile = strfile + "AlfaFactor_All_Days.txt"
    elif (int_in  == 5):
        strfile = strfile + "Vol_4_Days.txt"
    elif (int_in  == 6):
        strfile = strfile + "Vol_10_Days.txt"
    elif (int_in  == 7):
        strfile = strfile + "Vol_20_Days.txt"
    elif (int_in  == 8):
        strfile = strfile + "Adr.txt"
    else:
        return
    print(strfile)

    list_instruments = []
    try:
        with open(strfile, 'r') as f:
            list_instruments = [line[:-1] for line in f]

        del list_instruments[1::2]

    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())

    return int_in,list_instruments

def fun_createWorkListFromBot(int_in,list_instruments):

    list_zapis = list_instruments

    strfile_new = ""
    strfile = gl_strPathSave + gl_strCurrentWork
    if int_in == 1:
        strfile_new = strfile  + "AlfaFactor_5_Days_Works.txt"
        str_file = gl_strPathSave + "Last_AlfaFactor_5_Days.txt"
    elif (int_in == 2):
        strfile_new = strfile + "AlfaFactor_20_Days_Works.txt"
        str_file = gl_strPathSave + "Last_AlfaFactor_20_Days.txt"
    elif (int_in == 3):
        strfile_new = strfile + "AlfaFactor_60_Days_Works.txt"
        str_file = gl_strPathSave + "Last_AlfaFactor_60_Days.txt"
    elif (int_in == 4):
        strfile_new = strfile + "AlfaFactor_All_Days_Works.txt"
        str_file = gl_strPathSave + "Last_AlfaFactor_All_Days.txt"
    elif (int_in == 5):
        strfile_new = strfile + "Vol_4_Days_Works.txt"
        str_file = gl_strPathSave + "Last_Vol_4_Days.txt"
    elif (int_in == 6):
        strfile_new = strfile + "Vol_10_Days_Works.txt"
        str_file = gl_strPathSave + "Last_Vol_10_Days.txt"
    elif (int_in == 7):
        strfile_new = strfile + "Vol_20_Days_Works.txt"
        str_file = gl_strPathSave + "Last_Vol_20_Days.txt"
    elif (int_in == 8):
        strfile_new = strfile + "Adr_Works.txt"
        str_file = gl_strPathSave + "Last_Adr.txt"
    else:
        return list_zapis, strfile_new
    print(str_file)
    print(strfile_new)

    if( int_in in [1,2,3,4]):
        int_SpecFile = 0
        try:
            print('Число первых записей для лонга( файл Last_AlfaFactor_***.txt): ')
            print('Число последних записей для шорта( файл Last_AlfaFactor_***.txt): ')
            int_SpecFile = int(input('Число: '))

        except ValueError:
            print('Недопустимый ввод')

        if (int_SpecFile > 0):
            del list_zapis[int_SpecFile:]
        elif (int_SpecFile < 0):
            del list_zapis[:int_SpecFile]
            res = list_zapis.reverse()
        else:
            list_zapis.clear()

    if (len(list_zapis) != 0):
        list_class_work = fun_open_List_Instruments(list_zapis)

    return list_class_work,strfile_new

def fun_save_FileWork(list_class_hyph: list, strFileName: str):

    try:
        with open(strFileName, 'w') as fp:
            for item in list_class_hyph:
                # write each item on a new line
                if ("" != item.hyper):
                    str1 = str(item.prc) + '#' + item.hyper
                    fp.write("%s\n" % str1)
            print('Done list_huper')

    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())
        print(strFileName)

    return

def fun_save_ListBotWork(list_class_hyph: list, strFileName: str):

    try:
        with open(strFileName, 'w') as fp:
            for item in list_class_hyph:
                # write each item on a new line
                if ("" != item.hyper):
                    str1 = item.hyper + ' ' + str(item.prc)
                    fp.write("%s\n" % str1)
            print('Done list_huper')


    except Exception as e:
        print('++++++ Ошибка +++++:\n' + traceback.format_exc())

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


def fun_viewListFiles(str_file = ""):

    if( str_file == ""):
        strdir = str(input("Директория: "))
        strfile = str(input("Файл: "))
        if(".txt" in strfile):
            str_file = strdir + '\\' + strfile
        else:
            str_file = strdir + '\\' + strfile + '.txt'

    list_instruments = []
    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)
    except Exception as e:
        print('++++++ Ошибка +++++:\n' + traceback.format_exc())

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
        except Exception as e:
            print('++++++ Ошибка +++++:\n' + traceback.format_exc())

    for intCount, elem in enumerate(list_instruments):
        text = elem
        try:
            hyper = text.split()
            intCypher = int(hyper[1])
            if (0 == intType or intType == intCypher):
                strBrowseHyper = 'https://www.bybit.com/trade/usdt/' + str(hyper[0])
                webbrowser.open(strBrowseHyper)  # Go to example.com

                print(elem)
                strfullprint = str(intCount) + '/' + str(len(list_instruments))
                print(strfullprint)
            else:
                continue
        except Exception as e:
            print('++++++ Ошибка +++++:\n' + traceback.format_exc())

        input("type Enter for next:")
    return

def fun_createList_Ema_IKD(str_file, intTypeOpen=0):
    list_instruments = []

    try:
        with open(str_file, 'r') as f:
            list_instruments = [line[:-1] for line in f]

    except ValueError:
        print("Проблема с файлом: ")
        print(str_file)

    bool_repeat = True
    intType = 0
    if( intTypeOpen != 2 ):
        while (bool_repeat):
            try:
                text = input("Введите число:\n0 - тип1 и тип2: \n1 - тип1: \n2 - тип2: ")
                if (int(text) == 0 or int(text) == 1 or int(text) == 2):
                    intType = int(text)
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

    list_class_hyphe = []
    list_class_IKD = []
    for intCount, elem in enumerate(list_instruments):
        text = elem
        hyper = ''
        cypher = ''
        try:
            hyper = text.split()
            intCypher = int(hyper[1])
            strBrowseHyper = 'https://www.bybit.com/trade/usdt/' + str(hyper[0])
            webbrowser.open(strBrowseHyper)  # Go to example.com

            # intCount = intCount +
            print('---------------------------------------------------')
            print(elem)
            strfullprint = str(intCount) + '/' + str(len(list_instruments))
            print(strfullprint)
            # fun_ATR(str(hyper[0]))

        except:
            hyper = text

        bool_repeat = True

        while (bool_repeat and intTypeOpen != 2):
            try:
                if (intTypeOpen == 0):
                    text = input("type Enter for skip\nor 2 - list_workIKD_1.txt\nor 3 - list_workEMA_1.txt :")
                    if text == "":
                        bool_repeat = False
                    elif( text == "3"):
                        strelem = str(hyper[0]) + ' ' + str(hyper[1])
                        list_class_hyphe.append(strelem)
                        bool_repeat = False
                    elif (text == "2"):
                        strelem = str(hyper[0]) + ' ' + str(hyper[1])
                        list_class_IKD.append(strelem)
                        bool_repeat = False
                elif (intTypeOpen == 1):
                    text = input("type Enter for next:")
                    bool_repeat = False

            except ValueError:
                print('Недопустимый ввод, введите число')

        if( intTypeOpen == 2):
            text = input("type Enter for skip\nor 2 - list_workIKD_1.txt\nor 3 - list_workEMA_1.txt :")

    return list_class_hyphe, list_class_IKD

def fun_save_withdatetime(strfilename, strpostfix = ""):
    str_time = datetime.now().strftime('%H_%M_%S')
    str_date = datetime.now().strftime('%Y_%m_%d')
    head, tail = os.path.split(strfilename)
    if( strpostfix != "" ):
        str_fileCryptoFullName = head + '//' + str_date + '_' + str_time + '_' + strpostfix + '_' + tail
    else:
        str_fileCryptoFullName = head + '//' + str_date + '_' + str_time + '_' + tail

    print(str_fileCryptoFullName)
    try:
        shutil.copyfile(strfilename, str_fileCryptoFullName)
        print("Done  %s " % strfilename)

    except ValueError:
        print("Проблема с файлом: %s " % strfilename)

    return

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