import csv
from pathlib import Path

import openpyxl

from src.logger import get_logger

logger = get_logger(__name__)


def convert_excel_to_csv(input_path: Path, output_path: Path) -> int:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Input path is not a file: {input_path}"
        )

    if input_path.resolve() == output_path.resolve():
        raise ValueError(
            "Input and output paths must be different."
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "Starting Excel to CSV conversion: %s",
        input_path,
        )

    workbook = None

    try:
        workbook = openpyxl.load_workbook(
           input_path,
           read_only=True,
           data_only=True,
        )

   
        worksheet = workbook["Online Retail"]
        records_processed = 0

        with output_path.open(
            mode="w",
            newline="", 
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)


            for row in worksheet.iter_rows(values_only=True):
                writer.writerow(row)
                records_processed += 1

    except Exception:
        logger.exception(
            "Failed to convert Excel file to CSV."
        )
        raise

    finally:
        if workbook is not None:
            workbook.close()           

    logger.info(
        "Conversion completed successfully. Records processed: %s",
        records_processed,
        )
    
    return records_processed

