import gspread

import properties

gc = gspread.service_account_from_dict(properties.GOOGLE_SPREADSHEET_SERVICE_ACCOUNT)

ACCESS_TOKEN_INDEX = 1
DISCORD_USER_ID_INDEX = 2


def get_sheet():
    return gc.open_by_key(properties.GOOGLE_SPREADSHEET_SHEET_KEY).get_worksheet(0)


def find_all_tokens():
    sheet = get_sheet()
    # skip header row
    return sheet.col_values(1)[1:]


def upsert(access_token, discord_user_id):
    sheet = get_sheet()
    cell = sheet.find(discord_user_id)
    if cell is None:
        sheet.append_row([access_token, discord_user_id])
    else:
        sheet.update_cell(cell.row, ACCESS_TOKEN_INDEX, access_token)