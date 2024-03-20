import datetime
import pandas as pd
from dateutil import parser

COLUMN_WIDTHS = [7, 7, 9, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 13]


class SalesTable(object):
    def __init__(self, date, sales_data_range):
        self.date = date
        self.sales_data_range = sales_data_range


def run():

    rows = []

    file = open("input.txt")
    input_data = file.read().splitlines()
    header, raw_sales_tables = extract_raw_sales_tables(input_data)

    split_header = separate_columns(header)
    rows.append(["DATE", *split_header])

    for st in raw_sales_tables:
        st_data = input_data[st.sales_data_range[0] : st.sales_data_range[1]]
        date = datetime.datetime.strftime(st.date, "%d/%m/%Y")
        for st_row in st_data:
            split_st = separate_columns(st_row)
            if not all(item == "" for item in split_st):
                row = [date, *split_st]
                rows.append(row)

    df = pd.DataFrame(rows)
    print(df)
    df.to_csv("output.csv")


def extract_raw_sales_tables(data) -> list:
    sales_tables = []
    current_table = SalesTable(date="", sales_data_range=(0, 0))
    table_start = 0
    header = ""

    for index, line in enumerate(data):
        if str(line).startswith("STYPE"):
            header = line if not header else header
            date = str(data[index - 3]).strip()
            try:
                current_table.date = parser.parse(date)
                table_start = index + 2
            except:
                pass

        if table_start and "UNSOLD" in line:
            table_end = index - 1
            current_table.sales_data_range = (table_start, table_end)
            sales_tables.append(current_table)

            current_table = SalesTable(
                date="",
                sales_data_range=(0, 0),
            )

            table_start = 0

    return header, sales_tables


def separate_columns(string):
    start = 0
    columns = []

    for width in COLUMN_WIDTHS:
        end = start + width
        value = string[start:end].strip()
        columns.append(value)
        start += width

    return columns


if __name__ == "__main__":
    run()
