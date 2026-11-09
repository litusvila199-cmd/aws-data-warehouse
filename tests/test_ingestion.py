import csv


import openpyxl

from src.ingestion import convert_excel_to_csv


def test_convert_excel_to_csv(tmp_path):
    input_path = tmp_path / "input.xlsx"
    output_path = tmp_path / "output.csv"

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Online Retail"


    worksheet.append(["InvoiceNo", "Quantity", "Country"])
    worksheet.append(["536365", 6, "United Kingdom"])

    workbook.save(input_path)
    workbook.close()

    records_processed = convert_excel_to_csv(
        input_path,
        output_path,
    )


    with output_path.open(
        mode="r",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        rows = list(csv.reader(csv_file))


    assert records_processed == 2
    assert rows[0] == ["InvoiceNo", "Quantity", "Country"]
    assert rows[1] == ["536365", "6", "United Kingdom"]     