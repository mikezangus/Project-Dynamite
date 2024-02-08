import os
import sys
from pathlib import Path
from pyspark.sql import SparkSession, DataFrame

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_src_file_dir


def load_df(year: str, file_type: str, file_name: str, spark: SparkSession, headers: list, cols: list) -> DataFrame:
    print("\nStarted loading Main DataFrame")
    src_dir = get_src_file_dir(year, file_type)
    src_path = os.path.join(src_dir, file_name)
    df = spark.read.csv(
        path = src_path,
        sep = "|",
        header = False,
        inferSchema = False
    )
    for i, col_name in enumerate(headers):
        df = df.withColumnRenamed(f"_c{i}", col_name)
    df = df.select(*[headers[index] for index in cols])
    print(f"Finished loading Main DataFrame")
    print(f"Total items: {df.count():,}")
    return df