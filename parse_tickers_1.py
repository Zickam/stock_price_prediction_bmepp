

all_tickers = {'ABIO': "'Артген'", 'ABRD': 'Абрау-Дюрсо', 'AFKS': "АФК 'Система'", 'AFLT': 'Аэрофлот-росс.авиалинао',
           'AKRN': 'Акрон', 'ALRS': 'АЛРОСА', 'AMEZ': 'Ашинский метзавод', 'APRI': 'АПРИ',
           'APTK': '"Аптечная сеть 36,6"', 'AQUA': 'ИНАРКТИКА', 'ARSA': 'УК Арсагера', 'ASSB': "'Астраханская ЭСК'",
           'ASTR': 'Группа Астра', 'AVAN': "АКБ 'АВАНГАРД'", 'BANE': 'Башнефть АНК', 'BELU': 'НоваБев Групп',
           'BLNG': 'Белон ОАО', 'BRZL': 'Бурятзолото', 'BSPB': "'Банк 'Санкт-Петербург'", 'CARM': 'СТГ',
           'CBOM': "'МКБ'", 'CHGZ': 'РН-Западная Сибирь', 'CHKZ': "'ЧКПЗ'", 'CHMF': 'Северсталь ао', 'CHMK': "'ЧМК'",
           'CNTL': "'Центральный Телеграф'", 'DATA': 'Группа Аренадата', 'DELI': 'Каршеринг Руссия', 'DIAS': 'Диасофт',
           'DIOD': 'Завод ДИОД', 'DSKY': 'Детский мир', 'DVEC': "'ДЭК'", 'DZRD': 'Донской завод радиодеталей',
           'EELT': "'ЕвропЭлектротехника'", 'ELFV': "'ЭЛ5-Энерго'", 'ELMT': 'Элемент', 'ENPG': 'МКЭН+ ГРУП',
           'EUTR': 'ЕвроТранс', 'FEES': 'ФСК - Россети', 'FESH': 'ДВ морское пароходство', 'FLOT': 'Совкомфлот',
           'GAZA': 'ГАЗ', 'GAZP': "'Газпром'", 'GCHE': 'Группа Черкизово', 'GECO': 'ЦГРМ ГЕНЕТИКО', 'GEMA': 'ММЦБ',
           'GEMC': 'Юнайтед Медикал Груп', 'GMKN': "ГМК 'Нор.Никель'", 'GTRK': "'ГТМ'", 'HEAD': 'МКХэдхантер',
           'HNFG': 'ХЭНДЕРСОН', 'HYDR': "'РусГидро'", 'IGST': 'Ижсталь ао 2в.', 'INGR': 'ИНГРАД', 'IRAO': "'Интер РАО'",
           'IRKT': "'Яковлев' ак.об.-3", 'IVAT': 'ИВА', 'JNOS': 'Славнефть-ЯНОС', 'KAZT': 'Куйбышевазот',
           'KBSB': 'ТНС энерго Кубань', 'KCHE': 'Камчатскэнерго', 'KGKC': 'Курганская генер.комп.',
           'KLSB': "'Калужская сбыт.комп.'", 'KLVZ': 'Алкогольная Группа Кристалл', 'KMAZ': 'КАМАЗ',
           'KMEZ': 'Ковровский механический завод', 'KOGK': 'Коршуновский ГОК', 'KRKN': 'Саратовский НПЗ',
           'KROT': "'КрасныйОктябрь' -", 'KRSB': 'Красноярскэнергосбыт', 'KUBE': "'Россети Кубань'",
           'KUZB': "Банк 'Кузнецкий'", 'KZOS': "'Органический синтез'", 'LEAS': '«ЛК «Европлан»', 'LENT': 'Лента МК',
           'LIFE': 'Фармсинтез', 'LKOH': 'НК ЛУКОЙЛ  -', 'LNZL': "'Лензолото'", 'LPSB': 'Липецкая энергосбыт.ком.ОАО',
           'LSNG': 'Россети Ленэнерго', 'LSRG': 'Группа ЛСР', 'LVHK': 'Левенгук', 'MAGE': "'Магаданэнерго'",
           'MAGN': "'Магнитогорск.мет.комб'", 'MBNK': 'МТС-Банк', 'MDMG': 'МК«МД Медикал Груп»',
           'MFGS': "'Славнефть-Мегионнефтегаз'", 'MGKL': 'МГКЛ', 'MGNT': "'Магнит'", 'MGTS': "'МГТС' ао (5 в)",
           'MISB': 'ТНС энерго Марий Эл', 'MOEX': 'Московская Биржа', 'MRKC': "'Россети Центр'",
           'MRKK': 'Россети Сев. Кавказ', 'MRKP': 'Россети Центр и Приволжье', 'MRKS': 'Россети Сибирь',
           'MRKU': 'Россети Урал', 'MRKV': 'Россети Волга', 'MRKY': 'Россети Юг', 'MRKZ': 'Россети Северо-Запад',
           'MRSB': 'Мордовск.энергсбыт.комп.', 'MSNG': 'МосЭнерго акции обыкн.', 'MSRS': 'Россети Моск.рег.',
           'MSTT': "'МОСТОТРЕСТ'", 'MTLR': 'Мечел', 'MTSS': 'Мобильные ТелеСистемы', 'MVID': "'М.видео'",
           'NAUK': 'НПО Наука', 'NFAZ': 'НЕФАЗ', 'NKHP': 'НКХП', 'NKNC': "'Нижнекамскнефтехим'",
           'NKSH': 'Нижнекамскшина', 'NLMK': "'НЛМК'", 'NMTP': 'НМТП', 'NNSB': 'ТНС энерго Нижний Новг.',
           'NSVZ': 'Наука-Связь', 'NVTK': "'НОВАТЭК'", 'OGKB': 'ОГК-2', 'OZPH': 'Озон Фармацевтика',
           'PAZA': 'Павловский автобус', 'PHOR': 'ФосАгро', 'PIKK': 'ПИК СЗ', 'PLZL': 'Полюс',
           'PMSB': "'Пермэнергосбыт'", 'POSI': 'Группа Позитив', 'PRFN': 'ЧЗПСН-Профнастил', 'PRMB': "АКБ 'Приморье'",
           'PRMD': 'ПРОМОМЕД', 'RASP': 'Распадская', 'RBCM': 'ГК РБК', 'RDRB': 'РоссийскийДорож Банк',
           'RENI': 'Ренессанс Страхование', 'RGSS': 'Росгосстрах СК', 'RKKE': 'РКК Энергия им.С.П.Королева',
           'RNFT': 'РуссНефть НК', 'ROLO': "'Русолово'", 'ROSB': 'РОСБАНК', 'ROSN': 'НК Роснефть',
           'ROST': 'РОСИНТЕР РЕСТОРАНТС', 'RTGZ': 'Газпром газорасп Р-н-Д', 'RTKM': 'Ростелеком  ао.',
           'RTSB': 'ТНС энерго Ростов.', 'RUAL': 'РУСАЛ ОК МК', 'RUSI': 'РУСС-ИНВЕСТ ИК',
           'RZSB': "'Рязанская энергосб.комп'", 'SAGO': 'Самараэнерго  -', 'SARE': 'Саратовэнерго',
           'SBER': 'Сбербанк России', 'SELG': "'Селигдар'", 'SFIN': 'ЭсЭфАй', 'SGZH': 'Сегежа', 'SIBN': 'Газпром нефть',
           'SLEN': "'Сахалинэнерго'", 'SMLT': 'ГК Самолет', 'SNGS': 'Сургутнефтегаз акции об.', 'SOFL': 'Софтлайн',
           'SPBE': 'СПБ Биржа', 'STSB': 'Ставрополэнергосбыт', 'SVAV': "'СОЛЛЕРС'", 'SVCB': 'Совкомбанк',
           'SVET': 'Светофор Групп', 'TASB': "'Тамбов.энергсбыт.комп.'", 'TATN': "'Татнефть'", 'T': 'ТКС Холдинг МК',
           'TGKA': "'ТГК-1'", 'TGKB': "'ТГК-2'", 'TGKN': "'ТГК-14'", 'TNSE': "ГК 'ТНС энерго'",
           'TORS': "'Россети Томск'", 'TRMK': 'ТМК', 'TTLK': "'Таттелеком'", 'TUZA': 'Туймаз. завод автобетоновозов',
           'UGLD': 'ЮГК', 'UKUZ': 'Южный Кузбасс', 'UNAC': 'Об.авиастр.корп.', 'UNKL': 'Южно-Уральский никел. комб.',
           'UPRO': 'Юнипро', 'URKZ': "'Уральская кузница'", 'USBN': 'БАНК УРАЛСИБ', 'UTAR': "Авиакомпания 'ЮТэйр'",
           'UWGN': 'НПК ОВК', 'VEON-RX': 'VEON Ltd. ORD SHS', 'VGSB': "'Волгоград.энергосбыткомп'",
           'VJGZ': 'ННК-Варьеганнефтегаз', 'VKCO': 'Международная компания ВК', 'VLHZ': 'Владимирский химич.з-д',
           'VRSB': 'ТНС энерго Воронеж', 'VSEH': 'ВИ.ру', 'VSMO': 'Корп. ВСМПО-АВИСМА', 'VSYD': 'Выборгский Суд.Завод',
           'VTBR': 'Банк ВТБ', 'WTCM': "'Центр междун. торговли'", 'WUSH': 'ВУШ Холдинг',
           'YAKG': 'Якутская топл.-энерг. комп.', 'YDEX': 'МКЯНДЕКС', 'YKEN': "АК 'Якутскэнерго'",
           'YRSB': 'ТНС энерго Ярославль', 'ZAYM': 'Займер', 'ZILL': 'Завод им. И.А.Лихачева', 'ZVEZ': 'ЗВЕЗДА'}
needed_tickers = sorted(['TATN', 'ABIO', 'WUSH', 'NVTK', 'KUBE', 'NMTP', 'AFLT', 'RTKM', 'RUAL', 'MVID', 'DSKY', 'APTK', 'MSTT', 'CBOM', 'MTLR', 'DIAS', 'MRKV', 'VJGZ', 'UWGN', 'YDEX', 'AFKS', 'DATA', 'AKRN', 'ALRS', 'TNSE', 'RENI', 'BRZL', 'GAZP', 'MSRS', 'BELU', 'ROST', 'IRKT', 'HEAD', 'MRKS', 'UNKL', 'SMLT', 'RASP', 'JNOS', 'YAKG', 'FEES', 'MRKP', 'PLZL', 'MTSS', 'GTRK', 'FLOT', 'UPRO', 'SVCB', 'ASTR', 'GCHE', 'UNAC', 'NKHP', 'SPBE', 'KMAZ', 'SVAV', 'BLNG', 'VKCO', 'FESH', 'PHOR', 'T', 'MFGS', 'ABRD', 'SFIN', 'LIFE', 'ELMT', 'RNFT', 'MRKZ', 'NLMK', 'SIBN', 'LSNG', 'LENT', 'MGKL', 'LKOH', 'MGNT', 'OZPH', 'NKNC', 'PAZA', 'MSNG', 'CARM', 'GMKN', 'MRKK', 'LVHK', 'UTAR', 'LSRG', 'OGKB', 'URKZ', 'GAZA', 'POSI', 'BANE', 'VTBR', 'SELG', 'MRKU', 'SOFL', 'LEAS', 'GEMC', 'ROSB', 'ROLO', 'AMEZ', 'HYDR', 'SBER', 'KROT', 'NAUK', 'MOEX', 'IRAO', 'CHMF', 'BSPB', 'ZAYM', 'USBN', 'CNTL', 'MDMG', 'IGST', 'TTLK', 'LNZL', 'EUTR', 'AVAN', 'UKUZ', 'UGLD', 'SNGS', 'TGKA', 'KRKN', 'AQUA', 'MAGN', 'PIKK', 'VSMO', 'MBNK', 'RKKE', 'SGZH', 'RBCM', 'MRKC', 'MRKY', 'ELFV', 'ENPG', 'KOGK', 'TRMK', 'CHMK', 'DELI', 'HNFG', 'ROSN'])
needed_tickers_dict = {}
for needed_ticker in needed_tickers:
    needed_tickers_dict[all_tickers[needed_ticker]] = needed_ticker

needed_tickers = sorted(needed_tickers_dict.keys())

with open("tickers.txt", "w") as file:
    file.write("Компания - Тикер")
    for needed_ticker in needed_tickers:
        file.write(needed_ticker.replace("'", ""))
        file.write(" - ")
        file.write(needed_tickers_dict[needed_ticker])
        file.write("\n")
