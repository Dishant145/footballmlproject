
from pydantic import BaseModel

class FootballFeature(BaseModel):
    Home_Fatigue: object
    Away_Fatigue: object
    Temp: object
    Humidity: object
    Wind: object
    Referee_Bias: object
    # Home_Attacking_Form: float
    # Away_Attacking_Form: float
    # Home_Assisting_Form: float
    # Away_Assisting_Form: float
    # xG_Diff:float
    # xGA_Diff:float
    xG_Home: float
    xG_Away: float
    xGA_Home: float
    xGA_Away: float
    # xGA_Ratio_Home: float