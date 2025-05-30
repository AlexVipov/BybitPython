
from datetime import datetime

from auxfun import fun_createWorkListFromBot, fun_save_ListBotWork, get_listMonets, fun_save_list_workEMA_Work, \
    fun_save_withdatetime, fun_getListFromBotShablon, gl_strPathSave, fun_createList_Ema_IKD, fun_viewListFiles, \
    fun_CalculateAtr

if __name__ == '__main__':

    # listmon = get_listMonets(50)

    bool_repeat = True
    int_SpecFile = 0

    while (bool_repeat):
        print("Выбор пункта:"
              "\n ============================================== "
              "\n 8 - Создать ***_Work.txt из бота: "
              "\n 9 - Открыть datetime_bot___.txt: "
              "\n ============================================== "
              "\n 23 - Cоздать list_workEMA.txt и list_work150.txt: "
              "\n 24 - Открыть list_workEMA.txt и создать list_workEMA_1\\list_workIKD_1: "
              "\n 25 - Открыть list_work150.txt: "
              "\n 26 - Открыть list_workEMA_1.txt: "
              "\n 27 - Открыть list_workIKD_1.txt: "
              "\n 28 - Открыть datetime_list___.txt: "
              "\n ============================================== "
              "\n 29 - Вычислить АТР для ____ "
              "\n ============================================== "
              )

        try:
            int_SpecFile = int(input('Число: '))
            if ( 8 == int_SpecFile or
                    9 == int_SpecFile or
                    23 == int_SpecFile or
                    24 == int_SpecFile or
                    25 == int_SpecFile or
                    26 == int_SpecFile or
                    27 == int_SpecFile or
                    28 == int_SpecFile or
                    29 == int_SpecFile

            ):
                bool_repeat = False

        except ValueError:
            print('Недопустимый ввод')

    if (int_SpecFile == 8):
        int_in,list_instruments = fun_getListFromBotShablon()
        list_zapis, strFileZps = fun_createWorkListFromBot(int_in, list_instruments)
        fun_save_ListBotWork(list_zapis, strFileZps)
        fun_save_withdatetime(strFileZps)
    if (int_SpecFile == 9):
        ...
    if (int_SpecFile == 23):
        get_listMonets()  # intQvnt=150
    if (int_SpecFile == 24):
        strFile = gl_strPathSave + "list_workEMA.txt"
        list_class_EMA, list_class_IKD = fun_createList_Ema_IKD(strFile, 0)
        if (len(list_class_EMA) > 0):
            strFile = gl_strPathSave + "list_workEMA_1.txt"
            fun_save_list_workEMA_Work(list_class_EMA, strFile)
            fun_save_withdatetime(strFile)
        if (len(list_class_IKD) > 0):
            strFile = gl_strPathSave + "list_workIKD_1.txt"
            fun_save_list_workEMA_Work(list_class_IKD, strFile)
            fun_save_withdatetime(strFile)
    if (int_SpecFile == 25):
        strFile = gl_strPathSave + "list_work150.txt"
        fun_viewListFiles(strFile)
    if (int_SpecFile == 26):
        strFile = gl_strPathSave + "list_workEMA_1.txt"
        fun_viewListFiles(strFile)
    if (int_SpecFile == 27):
        strFile = gl_strPathSave + "list_workIKD_1.txt"
        fun_viewListFiles(strFile)
    if (int_SpecFile == 28):
        fun_viewListFiles()
    if (int_SpecFile == 29):
        int_error, df_atr = fun_CalculateAtr()
        if( int_error == 0 ):
            strprint = str(df_atr.loc[0, 'NAME']) + ':  ' + str(df_atr.loc[0, 'ATR_DAY'])
            print(strprint)

    pass
