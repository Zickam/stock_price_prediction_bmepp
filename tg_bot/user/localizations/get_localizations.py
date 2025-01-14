from pathlib import Path
import os

import yaml
from aiogram.fsm.context import FSMContext

locales = {}

def loadLocale(locale_path: Path) -> dict[str, str | dict]:
    with open(locale_path, "r") as file:
        locale = yaml.safe_load(file)
        return locale

def loadLocalizations() -> dict[str, dict]:
    global locales

    os.chdir("tg_bot/user")
    locale_files = os.listdir("localizations")
    for locale_file in locale_files:
        if locale_file == "__pycache__" or locale_file == "get_localizations.py":
            continue
        locale = loadLocale(Path("localizations", locale_file))\

        locale_name = locale_file.split(".")[0]
        locales[locale_name] = locale

    print("Locales loaded:", *locales.keys())

    os.chdir("../")

    return locales


async def getTextByLang(path: str, lang: str) -> str:
    if not (lang in locales.keys()):
        raise Exception(f"{lang} localization is not supported")

    path_splitted = path.split(".")
    ok, string = _get(path_splitted, locales[lang])
    if ok:
        return string

    return f"Error getting the locale for: [{path}] for lang [{lang}]. {string}"


def _get(path: list[str], tmp_locale: dict) -> tuple[bool, str]:
    if path[0] in tmp_locale:
        tmp_locale = tmp_locale[path.pop(0)]
        if not path:
            return True, tmp_locale
        return _get(path, tmp_locale)

    else:
        return False, f"Not found [{path[0]}] among {list(tmp_locale.keys())}"

async def getText(path: str, state: FSMContext) -> str:
    return await getTextByLang(path, (await state.get_data())["ru"])


loadLocalizations()

if __name__ == "__main__":
    print(getTextByLang("keyboards.m enu.catalog", "en"))
