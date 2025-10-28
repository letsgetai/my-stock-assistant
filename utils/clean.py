import math
def clean_dict_nan_none(d):
    # 过滤规则：值不是 None，且不是 NaN（需排除字符串等非数值类型，避免 math.isnan 报错）
    return {
        key: value 
        for key, value in d.items() 
        if value is not None  # 排除 None
        and not (isinstance(value, float) and math.isnan(value))  # 排除 NaN
    }