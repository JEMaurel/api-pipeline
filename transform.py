import pandas as pd
import logging

logger= logging.getLogger(__name__)

def transform_data(raw_data: dict)-> pd.DataFrame:
    """tranforma y enriquece datos """
    logger.info("transformando datos ...")
    orders = raw_data.get('tables', {}).get('orders',[])
    df= pd.DataFrame(orders)

    if df.empty:
        logger.warning("no hay datos para procesar")
        return df
    logger.info(f"columnas disponibles : {list(df.columns)}")
    if 'total_amount'in df.columns and 'total' not in df.columns:
        df= df.rename(columns={'total_amount':'total'})
        
    df['order_date']= pd.to_datetime(df['order_date'])
    df['total']= pd.to_numeric(df['total'],errors='coerce')
    df['order_month']= df['order_date'].dt.to_period('M').astype(str)
    df['order_year']= df['order_date'].dt.year
    df['is_high_value']= df['total']>100
    df['day_of_week']= df['order_date'].dt.day_name()

    invalid_totals= df['total'].isna().sum()
    if invalid_totals>0:
        logger.warning(f"{invalid_totals} registros con totales invalidos encontrados")
    logger.info(f"transformadas {len(df)} ordenes")
    return df

