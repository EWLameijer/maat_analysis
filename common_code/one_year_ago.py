from datetime import datetime 
from dateutil.relativedelta import relativedelta

def one_year_ago_str() -> str: 
    one_year_ago = datetime.today() - relativedelta(years=1)
    return one_year_ago.strftime("%Y-%m-%d")