import gspread  # Импортируем gspread — библиотека для работы с Google Sheets
from google.oauth2.service_account import \
    Credentials  # Импортируем класс Credentials из Google API Используется для авторизации через файл credentials.json, который ты скачал при создании сервисного аккаунта.
from datetime import datetime

scopes = [
    'https://www.googleapis.com/auth/spreadsheets']  # Указываем область доступа (scopes) Это означает: «даю доступ к Google Sheets полностью».
creds = Credentials.from_service_account_file('credentials.json',
                                              scopes=scopes)  # Загружаем credentials.json и создаём объект creds #/etc/secrets/credentials.json

client = gspread.authorize(creds)  # Авторизуемся в gspread
sheet_id = '1bUJq4hJAROo9CfcCaorSGJXo1Ecz5UgdmNpRouBBQjY'  # Указываем ID твоей таблицы
workbook = client.open_by_key(sheet_id)  # Открываем саму таблицу

sheet1 = workbook.worksheet('отскок')
sheet2 = workbook.worksheet('Лист2')
sheet3 = workbook.worksheet('пробой')
sheet4 = workbook.worksheet('fastbot')
sheet5 = workbook.worksheet('arbitrage')


def write_to_sheet(coin_name, sol, amount, input_mint):
    """
    Записывает данные в первую пустую строку
    A - coin_name
    B - sol
    C - amount
    D - input_mint
    """

    # Берём все значения из колонки A
    col_a = sheet2.col_values(1)

    # Номер первой пустой строки
    row = len(col_a) + 1

    sheet2.update(
        f"A{row}:D{row}",
        [[coin_name, sol, amount, input_mint]]
    )


def write_to_arbitrage(buy, sell, spread, need_base, current_time, pair):
    """
    Записывает данные в первую пустую строку
    A - coin_name
    B - sol
    C - amount
    D - input_mint
    """

    # Берём все значения из колонки A
    col_a = sheet5.col_values(1)

    # Номер первой пустой строки
    row = len(col_a) + 1

    sheet5.update(
        f"A{row}:F{row}",
        [[buy, sell, spread, need_base, current_time, pair]]
    )
