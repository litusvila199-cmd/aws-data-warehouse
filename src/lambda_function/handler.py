import os
import tempfile
from pathlib import Path
from urllib.parse import unquote_plus

import boto3

from src.ingestion import convert_excel_to_csv
from src.logger import get_logger

logger = get_logger(__name__)

s3_client = boto3.client("s3")



def lambda_handler(event, context):


    bucket = os.environ["DATA_LAKE_BUCKET"]
    raw_prefix = os.environ["RAW_PREFIX"]
    processed_prefix = os.environ["PROCESSED_PREFIX"]

    try:
        record = event["Records"][0]
        source_bucket = record["s3"]["bucket"]["name"]
        source_key = unquote_plus(record["s3"]["object"]["key"])

        if source_bucket != bucket:
            raise ValueError("Unexpected S3 bucket.")

        if not source_key.startswith(raw_prefix):
            raise ValueError("The object is outside the raw prefix.")

        filename = Path(source_key).stem
        output_key = f"{processed_prefix}{filename}.csv"

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.xlsx"
            output_path = Path(temp_dir) / "output.csv"

            logger.info("Downloading file: %s", source_key)

            s3_client.download_file(
                bucket,
                source_key,
                str(input_path),
            )

            records_processed = convert_excel_to_csv(
                input_path,
                output_path
            )

            logger.info("Uploading processed file: %s", output_key)


            s3_client.upload_file(
                str(output_path),
                bucket,
                output_key,
            )

        return {
            "statusCode": 200,
            "body": {
                "message": "File processed successfully",
                "output_key": output_key,
                "records_processed": records_processed,
            },
        }

    except Exception:
        logger.exception("Lambda processing failed.")
        raise


