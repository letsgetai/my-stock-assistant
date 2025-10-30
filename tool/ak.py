import akshare as ak
import pandas as pd
from camel.toolkits import FunctionTool, SearchToolkit

from akshare import stock_research_report_em, stock_financial_analysis_indicator_em, stock_profit_sheet_by_report_em,stock_zh_a_spot_em,stock_news_em, stock_profit_forecast_em, stock_rank_forecast_cninfo
import math
def clean_dict_nan_none(d):
    # 过滤规则：值不是 None，且不是 NaN（需排除字符串等非数值类型，避免 math.isnan 报错）
    return {
        key: value 
        for key, value in d.items() 
        if value is not None  # 排除 None
        and not (isinstance(value, float) and math.isnan(value))  # 排除 NaN
    }

def A_stock_research_report_em(symbol: str = "000001") -> pd.DataFrame:
    """
    东方财富网-数据中心-研究报告-个股研报-根据对应的股票代码返回近期的各大机构的研报的主要信息以及对应pdf链接
    https://data.eastmoney.com/report/stock.jshtml
    :param symbol: 个股代码, 纯数字， 如 600519
    :type symbol: str
    :return: 个股研报
    :rtype: pandas.DataFrame
    """
    big_df = stock_research_report_em(symbol)
    return big_df.head().to_string()

def get_financial_data(symbol: str = "301389.SZ"):
    """
    东方财富-A股-财务分析-主要指标
    https://emweb.securities.eastmoney.com/pc_hsf10/pages/index.html?type=web&code=SZ301389&color=b#/cwfx
    :param symbol: 股票代码（带市场标识）, 如 301389.SZ
    :type symbol: str
    :param indicator: choice of {"按报告期", "按单季度"}
    :type indicator: str
    :return: 东方财富-A股-财务分析-主要指标
    :rtype: pandas.DataFrame
    """
    big_df = stock_financial_analysis_indicator_em(symbol)
    caiwu = clean_dict_nan_none(big_df.iloc[0].to_dict())
    caiwu_string = str(caiwu)
    return caiwu_string
    #stock_profit_sheet_by_report_em
    # pass

def get_latest_market_info(symbol: str = "600519"):
    """
    东方财富-个股新闻-最近 100 条新闻
    https://so.eastmoney.com/news/s?keyword=603777
    :param symbol: 股票代码
    :type symbol: str
    :return: 个股新闻
    :rtype: pandas.DataFrame
    """
    # stock_zh_a_spot_em   # 获取A股列表,都是中文信息
    stock_news_em_df = stock_news_em(symbol=symbol)
    news = stock_news_em_df.head().to_string()
    if len(news) < 5000:
        return news
    return news[:5000]

search_research_reports = FunctionTool(A_stock_research_report_em)
search_financial_data = FunctionTool(get_financial_data)
search_market_info = FunctionTool(get_latest_market_info)

ak_tools = [search_research_reports, search_financial_data, search_market_info]

if __name__ == "__main__":
    get_financial_data("301389.SZ")
    exit()
    print(A_stock_research_report_em("301389"))
    print(search_research_reports("301389"))

# # 获取市场最新公告
# try:
#     latest_notices_df = ak.stock_notice_report()
#     print("最新公告获取成功:")
#     print(latest_notices_df.head())
# except Exception as e:
#     print(f"数据获取失败: {e}")

# # 示例 1: 获取贵州茅台（600519）的所有“财务报告”
# try:
#     financial_reports_df = ak.stock_notice_report(symbol="600519", report_type="财务报告")
#     print("\n贵州茅台 - 财务报告:")
#     print(financial_reports_df.head())
# except Exception as e:
#     print(f"数据获取失败: {e}")

# # 示例 2: 获取贵州茅台（600519）的所有“重大事项”公告
# try:
#     major_events_df = ak.stock_notice_report(symbol="600519", report_type="重大事项")
#     print("\n贵州茅台 - 重大事项:")
#     print(major_events_df.head())
# except Exception as e:
#     print(f"数据获取失败: {e}")

# # 示例 3: 获取贵州茅台（600519）的所有“融资公告”
# try:
#     financing_announcements_df = ak.stock_notice_report(symbol="600519", report_type="融资公告")
#     print("\n贵州茅台 - 融资公告:")
#     print(financing_announcements_df.head())
# except Exception as e:
#     print(f"数据获取失败: {e}")