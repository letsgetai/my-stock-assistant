
import akshare as ak
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
import pandas as pd
logger = logging.getLogger(__name__)
from camel.toolkits import FunctionTool
def get_stock_hist(symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    获取股票历史数据
    :param symbol: 股票代码，如'00700'（腾讯控股）
    :param start_date: 开始日期，格式'YYYY-MM-DD'
    :param end_date: 结束日期，格式'YYYY-MM-DD'
    :return: 包含历史数据的字典列表
    """
    logger.info(f"Fetching stock history for {symbol} from {start_date} to {end_date}")
    df = ak.stock_hk_hist(symbol=symbol, start_date=start_date, end_date=end_date)
    return df.to_dict('records')
 

def get_stock_info(symbol: str) -> Dict[str, Any]:
    """
    获取股票基本信息
    :param symbol: 股票代码
    :return: 包含股票基本信息的字典
    """
    logger.info(f"Fetching stock info for {symbol}")
    df = ak.stock_hk_spot()
    stock_info = df[df['代码'] == symbol].iloc[0].to_dict()
    return stock_info
 

def get_macro_economic_data(indicator: str) -> List[Dict[str, Any]]:
    """
    获取宏观经济数据
    :param indicator: 指标名称，如'GDP'、'CPI'等
    :return: 包含宏观经济数据的字典列表
    """
    indicator_map = {
        'GDP': ak.macro_china_gdp,
        'CPI': ak.macro_china_cpi,
        'PMI': ak.macro_china_pmi
    }
    if indicator not in indicator_map:
        raise ValueError(f"Unsupported indicator: {indicator}")
    
    logger.info(f"Fetching macroeconomic data for {indicator}")
    df = indicator_map[indicator]()
    return df.to_dict('records')
 
get_stock_hist = FunctionTool(get_stock_hist)
get_stock_info = FunctionTool(get_stock_info)
get_macro_economic_data = FunctionTool(get_macro_economic_data)

fin_tools = [get_stock_hist, get_stock_info, get_macro_economic_data]

if __name__ == '__main__':
    print(get_stock_hist('00700', '2022-01-01', '2022-01-31'))
    print('-'*20)
    print(get_stock_info('00700'))
    print('-'*20)
    print(get_macro_economic_data('GDP'))