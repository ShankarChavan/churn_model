import pandas as pd
import pandera as pa

from pandera.typing import Index, DataFrame, Series

class ChurnModelInputSchema(pa.SchemaModel):
    """
    Class to hold the input schema for input dataframe 
    """
    number_vmail_messages: Series[int] = pa.Field(ge=0, le=52)
    total_day_calls: Series[int]= pa.Field(ge= 0, le= 165)
    total_eve_minutes: Series[float]= pa.Field(ge = 0, le= 360)
    total_eve_charge: Series[float]= pa.Field(ge = 0, le= 31)
    total_intl_minutes: Series[float]= pa.Field(ge = 0, le= 20)
    number_customer_service_calls: Series[int]= pa.Field(ge= 0, le= 9)

@pa.check_types      
def validate_inputs(df: DataFrame[ChurnModelInputSchema]):
    return df