from pydantic import BaseModel,Field

class churnModelFeilds(BaseModel):
    """
    Datamodel class for input data with feild Validation.This class will ensure that input data-points are validated for within min-max range values.
    This is important because our model is trained accordingly.  
    """
    number_vmail_messages:float = Field(..., ge=0.0, le=52.0)
    total_day_calls:float= Field(...,ge= 0.0, le= 165.0)
    total_eve_minutes:float= Field(...,ge = 0.0, le= 359.3)
    total_eve_charge:float= Field(...,ge = 0.0, le= 30.54)
    total_intl_minutes:float= Field(...,ge = 0.0, le= 20.0)
    number_customer_service_calls:float= Field(...,ge= 0.0, le= 9.0)
    
    class Config:
        validate_assignment = True
        schema_extra = {
            "example": {
                "number_vmail_messages": 32.0,
                "total_day_calls": 15.0,
                "total_eve_minutes": 20.0,
                "total_eve_charge": 24.0,
                "total_intl_minutes": 3.0,
                "number_customer_service_calls":4.0,
            }
        }
