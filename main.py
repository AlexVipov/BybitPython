
from auxfun import get_list_instrums, fun_convert, fun_clear_LongList, fun_get_Shilin, fun_save_ListWorkLast, \
    fun_save_fileTV, fun_get_List_PreWork, fun_get_ListWorkLast, fun_save_withtime_ListWorkLast, fun_save_volatileLast, \
    fun_get_ShilinVolatile_NDays_Instruments, fun_open_List_Instruments, fun_save_AlfaFactorLast, \
    fun_get_first_AlfaFactorLast, get_listMonets, fun_save_list_workEMA_Work, fun_get_List_File_Ema, fun_save_AdrLast, \
    fun_createAdrVolAlfa, fun_save_withdatetime

if __name__ == '__main__':

    # listmon = get_listMonets(50)

    bool_repeat = True
    int_SpecFile = 0

    while (bool_repeat):
        print("Выбор пункта:"
              # "\n 0 - КШ Файл(веб-50), создать cryptowork.txt"
              # "\n 1 - Создать LastCrypto.txt из cryptowork.txt: "
              # "\n 2 - Открыть рабочий файл LastCrypto.txt: "
              # "\n 3 - Сохранить текущий cryptowork.txt with times"
              # "\n 4 - Сохранить текущий LastCrypto.txt with timestamp: "
              "\n ============================================== "
              "\n 8 -  Создать Last_***.txt из бота: "
              "\n 9 -  Создать текущий date_time_***_Work.txt из Last_***.txt: "
              "\n 10 - Сохранить текущий Last_AlfaFactor.txt with timestamp: "
              "\n 20 - Открыть текущий AlfaWork.txt : "
              # "\n ============================================== "
              # "\n 14 - Создать Last_Adr.txt из Adr.txt(берем из бота): "
              # "\n 15 - Открыть текущий Last_Adr.txt: "
              # "\n 16 - Сохранить текущий Last_Adr.txt with timestamp: "
              "\n ============================================== "
              # "\n 21 - Сохранить текущий AlfaWork.txt with timestamp: "
              # "\n 22 - Файл( N ), создать cryptowork.txt: "
              "\n ============================================== "
              "\n 23 - Cоздать list_workEMA.txt и list_work150.txt: "
              "\n 24 - Открыть list_workEMA.txt и создать list_workEMA_Work.txt: "
              "\n 25 - Открыть list_work150.txt: "
              "\n 26 - Открыть list_workEMA_1.txt: "
              "\n 27 - Открыть list_workIKD_1.txt: "
              "\n 28 - Открыть ___.txt: "
              "\n ============================================== "
              # "\n 5 - Сохранить текущий Last_4Days.txt: "
              # "\n 6 - Открыть текущий Last_4Days.txt: "
              # "\n 7 - Сохранить текущий Last_4Days.txt with timestamp: "
              # "\n ============================================== "
              # "\n 8 - Сохранить текущий AlfaFactor5.txt: "
              # "\n 9 - Открыть текущий AlfaFactor5.txt (за 5 дней): "
              # "\n 10 - Сохранить текущий AlfaFactor5.txt with timestamp: "
              # "\n ============================================== "
              # "\n 11 - Сохранить текущий Last_10Days.txt: "
              # "\n 12 - Открыть текущий Last_10Days.txt: "
              # "\n 13 - Сохранить текущий Last_10Days.txt with timestamp: "
              # "\n ============================================== "
              # "\n 14 - Сохранить текущий Adr.txt: "
              # "\n 15 - Открыть текущий Last_Adr.txt: "
              # "\n 16 - Сохранить текущий Last_Adr.txt with timestamp: "
              # "\n ============================================== "
              # "\n 17 - Создать файл из 4Days, AlfaFactor и Adr: "
              # "\n 18 - Сохранить текущий cryptowork_Combi.txt with timestamp:: "
              # "\n 19 - Открыть текущий cryptowork_Combi.txt: "
              )

        try:
            int_SpecFile = int(input('Число: '))
            if (0 == int_SpecFile or
                    1 == int_SpecFile or
                    2 == int_SpecFile or
                    3 == int_SpecFile or
                    4 == int_SpecFile or
                    5 == int_SpecFile or
                    6 == int_SpecFile or
                    7 == int_SpecFile or
                    8 == int_SpecFile or
                    9 == int_SpecFile or
                    10 == int_SpecFile or
                    11 == int_SpecFile or
                    12 == int_SpecFile or
                    13 == int_SpecFile or
                    14 == int_SpecFile or
                    15 == int_SpecFile or
                    16 == int_SpecFile or
                    17 == int_SpecFile or
                    18 == int_SpecFile or
                    19 == int_SpecFile or
                    20 == int_SpecFile or
                    21 == int_SpecFile or
                    22 == int_SpecFile or
                    23 == int_SpecFile or
                    24 == int_SpecFile or
                    25 == int_SpecFile or
                    26 == int_SpecFile or
                    27 == int_SpecFile or
                    28 == int_SpecFile
            ):
                bool_repeat = False

        except ValueError:
            print('Недопустимый ввод')

    # list_class_hyp = []
    if (int_SpecFile == 0):
        list_class_hyp = fun_get_Shilin()
        fun_save_ListWorkLast(list_class_hyp, 'cryptowork.txt')
        fun_save_fileTV('cryptowork')
    elif (int_SpecFile == 1):
        list_class_hyp = fun_get_List_PreWork()
        fun_save_ListWorkLast(list_class_hyp, "LastCrypto.txt")
        fun_save_fileTV('LastCrypto')
    elif (int_SpecFile == 2):
        fun_get_ListWorkLast("LastCrypto.txt")
    elif (int_SpecFile == 3):
        fun_save_withtime_ListWorkLast("cryptowork")
    elif (int_SpecFile == 4):
        fun_save_withtime_ListWorkLast()
    elif (int_SpecFile == 5):
        fun_save_volatileLast(4)
    elif (int_SpecFile == 6):
        list_instr = fun_get_ShilinVolatile_NDays_Instruments(4)
        fun_open_List_Instruments(list_instr)
    elif (int_SpecFile == 7):
        fun_save_withtime_ListWorkLast("Last_4Days")

    elif (int_SpecFile == 8):
        fun_save_AlfaFactorLast()
    elif (int_SpecFile == 9):
        list_open, strFileZps = fun_get_first_AlfaFactorLast()
        fun_save_ListWorkLast(list_open, strFileZps)
        if(len(list_open) != 0):
            list_class_hyp = fun_open_List_Instruments(list_open)
            fun_save_ListWorkLast(list_class_hyp, "AlfaWork.txt")
            fun_save_fileTV('AlfaWork')
    elif (int_SpecFile == 10):
        fun_save_withtime_ListWorkLast("Last_AlfaFactor")
    elif (int_SpecFile == 20):
        fun_get_ListWorkLast("AlfaWork.txt")
    elif (int_SpecFile == 21):
        fun_save_withtime_ListWorkLast("AlfaWork")
    if (int_SpecFile == 22):
        list_class_hyp = fun_get_Shilin(False)
        fun_save_ListWorkLast(list_class_hyp, 'cryptowork.txt')
        fun_save_fileTV('cryptowork')
    if (int_SpecFile == 23):
        get_listMonets()  # intQvnt=150
    if (int_SpecFile == 24):
        strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workEMA.txt"
        list_class_EMA, list_class_IKD = fun_get_List_File_Ema(strFile, 0)
        if (len(list_class_EMA) > 0):
            strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workEMA_1.txt"
            fun_save_list_workEMA_Work(list_class_EMA, strFile)
            fun_save_withdatetime(strFile)
        if (len(list_class_IKD) > 0):
            strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workIKD_1.txt"
            fun_save_list_workEMA_Work(list_class_IKD, strFile)
            fun_save_withdatetime(strFile)
    if (int_SpecFile == 25):
        strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_work150.txt"
        fun_get_List_File_Ema(strFile, 0)
    if (int_SpecFile == 26):
        strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workEMA_1.txt"
        list_class_EMA = fun_get_List_File_Ema(strFile, 1)
    if (int_SpecFile == 27):
        strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\list_workIKD_1.txt"
        list_class_EMA = fun_get_List_File_Ema(strFile, 1)
    if (int_SpecFile == 28):
        textFile = input("Введите имя файла: ")
        strFile = "E:\\YandexDisk\\КШ\\CryptoArchive\\" + textFile
        list_class_EMA = fun_get_List_File_Ema(strFile, 1)

    elif (int_SpecFile == 11):
        fun_save_volatileLast(10)
    elif (int_SpecFile == 12):
        list_instr = fun_get_ShilinVolatile_NDays_Instruments(10)
        fun_open_List_Instruments(list_instr)
    elif (int_SpecFile == 13):
        fun_save_withtime_ListWorkLast("Last_10Days")
    elif (int_SpecFile == 14):
        fun_save_AdrLast()
    elif (int_SpecFile == 15):
        list_instr = fun_get_ShilinVolatile_NDays_Instruments("Adr")
        list_class_hyp = fun_open_List_Instruments(list_instr)
        fun_save_ListWorkLast(list_class_hyp, "AdrWork.txt")
        fun_save_fileTV('AdrWork')
    elif (int_SpecFile == 16):
        fun_save_withtime_ListWorkLast("Last_Adr")
    elif (int_SpecFile == 17):
        list_instr = fun_createAdrVolAlfa()
        list_class_hyp = fun_open_List_Instruments(list_instr)
        fun_save_ListWorkLast(list_class_hyp, 'cryptowork_Combi.txt')
    elif (int_SpecFile == 18):
        fun_save_withtime_ListWorkLast("cryptowork_Combi")
    elif (int_SpecFile == 19):
        pass
        # list_instr = fun_get_ShilinVolatile_NDays_Instruments("cryptowork_Combi")
        # fun_open_List_Instruments(list_instr)

    pass
