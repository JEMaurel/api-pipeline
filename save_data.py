import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def save_data(df: pd.DataFrame, output_dir:str = "output"):
    """guarda datos particionados por anio y mes """
    logger.info(f"guardando datos particionados en { output_dir}/...")
    os.makedirs(output_dir, exist_ok = True)

    df.to_parquet(f"{output_dir}/orders",partition_cols=["order_year","order_month"],index=False)
    
    df.to_parquet(f"{output_dir}/orders_all.parquet",index=False)

    logger.info(f"guardadas {len(df)} ordenes")

    logger.info(f"particiones creadas : {df['order_month'].nunique()} meses")
    

