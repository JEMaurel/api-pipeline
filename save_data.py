import os
import logging
import pandas as pd

logger = logging.getLogger(__name__)
def limpiar_s3_prefix(s3_client, bucket_name, prefix):
    """Borra todos los archivos dentro de un prefijo en S3 para evitar duplicados"""
    logger.info(f"🧹 Limpiando destino en S3: s3://{bucket_name}/{prefix}...")
    
    # Listamos los objetos que ya existen
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if 'Contents' in response:
        objetos_a_borrar = [{'Key': obj['Key']} for obj in response['Contents']]
        
        # Borrado masivo (hasta 1000 objetos de un saque)
        s3_client.delete_objects(
            Bucket=bucket_name,
            Delete={'Objects': objetos_a_borrar}
        )
        logger.info(f"✨ Se eliminaron {len(objetos_a_borrar)} archivos viejos.")
    else:
        logger.info("📂 La carpeta ya estaba limpia. Nada que borrar.")

def save_data(df: pd.DataFrame, output_dir:str = "output"):
    """guarda datos particionados por anio y mes """
    logger.info(f"guardando datos particionados en { output_dir}/...")
    os.makedirs(output_dir, exist_ok = True)

    df.to_parquet(f"{output_dir}/orders",partition_cols=["order_year","order_month"],index=False)
    
    df.to_parquet(f"{output_dir}/orders_all.parquet",index=False)

    logger.info(f"guardadas {len(df)} ordenes")

    logger.info(f"particiones creadas : {df['order_month'].nunique()} meses")
    

