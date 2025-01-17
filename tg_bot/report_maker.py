import logging
import os
import uuid
from pathlib import Path
from dataclasses import dataclass
from datetime import timedelta
import re

from aiogram.fsm.context import FSMContext
from tinkoff.invest import CandleInterval
from tinkoff.invest.utils import now

import plot
import tinkoff_api
from analysis.functions import getSimplePriceChangeByTicker
from tg_bot.user.localizations.get_localizations import getText
from tinkoff_api.utilities import getStockCostByTicker, getStockDataByTicker
from ai_experiments.ai_model import predict

tickers = {'ABIO': "'Артген'", 'ABRD': 'Абрау-Дюрсо', 'AFKS': "АФК 'Система'", 'AFLT': 'Аэрофлот-росс.авиалинао',
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


@dataclass
class Report:
    status: bool
    status_description: str = None
    text: str = None
    photos: list[Path] = None

    async def clear(self):
        for photo_path in self.photos:
            os.remove(photo_path)


class ReportMaker:
    DEFAULT_REPORT_DAYS = 30
    DEFAULT_REPORT_INTERVAL = CandleInterval.CANDLE_INTERVAL_DAY

    @staticmethod
    async def _getReportText(
            ticker: str,
            days: int
    ) -> str:
        price_change = await getSimplePriceChangeByTicker(
            ticker,
            now() - timedelta(days=days),
            now()
        )

        price_month_ago = await getStockCostByTicker(ticker, now() - timedelta(days=days))
        price_now = await getStockCostByTicker(ticker)

        # price_change = 0
        # price_month_ago = 0
        # price_now = 0

        perspectivity_explanation = predict(ticker)

        return (f"*{ticker.upper()}* цена актива изменилась на *{round(price_change * 100)}%*\n"
                f"Цена {days} дней назад была *{price_month_ago}₽*\n"
                f"Сейчас цена *{price_now}₽*\n\n"
                f"{perspectivity_explanation}")

    @staticmethod
    async def _getReportChart(
            ticker: str,
            days: int,
            interval: CandleInterval
    ) -> Path:
        """returns the path to the chart image"""

        candles = await tinkoff_api.utilities.getStockDataByTicker(
            ticker,
            now() - timedelta(days=days),
            now(),
            interval
        )
        time_and_close = []
        for candle in candles:
            time_and_close.append((candle.time, candle.close.units + candle.close.nano / 10 ** 9))

        img_name = str(uuid.uuid4())
        img_path = Path("images", img_name + ".png")
        plot.utilities.renderPlot(time_and_close, ticker, img_path)

        return img_path

    @staticmethod
    async def makeReport(
            state: FSMContext,
            ticker: str,
            days: int = DEFAULT_REPORT_DAYS,
            interval: CandleInterval = DEFAULT_REPORT_INTERVAL
    ) -> Report:

        if not ticker or ticker.upper() not in tickers:
            report_status = "Неожиданный тикер"
            return Report(False, report_status)

        try:
            img_path = await ReportMaker._getReportChart(ticker, days, interval)
            text = await ReportMaker._getReportText(ticker, days)

            logging.info(f"Final text: {text}")

            return Report(True, text=text, photos=[img_path])

        except Exception as ex:
            import urllib.parse
            text = urllib.parse.quote(str(ex), safe='/', encoding=None, errors=None)
            logging.error(ex)
            raise ex
            return Report(False, f"Unhandled ERROR: {text}")

