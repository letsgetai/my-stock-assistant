import json
import os

def save_to_json(data: any, file_path: str, encoding: str = 'utf-8') -> bool:
    """
    将 Python 对象（如字典或列表）保存为 JSON 文件。

    Args:
        data (any): 要保存的 Python 对象 (必须是 JSON 可序列化的)。
        file_path (str): 目标文件的完整路径 (例如: './data/output.json')。
        encoding (str, optional): 文件编码。默认为 'utf-8'。

    Returns:
        bool: 如果保存成功，返回 True；如果失败，返回 False。
    """
    try:
        # 确保目录存在
        # os.path.dirname(file_path) 会获取文件所在的目录
        directory = os.path.dirname(file_path)
        
        # 如果目录非空 (即 file_path 不是像 "test.json" 这样的相对路径)
        # 且目录不存在，则创建它
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True) # exist_ok=True 避免并发问题

        # 写入文件
        # 使用 'w' 模式会覆盖已存在的文件
        with open(file_path, 'w', encoding=encoding) as f:
            # json.dump 将 data 序列化为 JSON 格式并写入文件 f
            # indent=4 让 JSON 文件格式化，更易读
            # ensure_ascii=False 确保中文等非 ASCII 字符能正确显示
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"数据已成功保存到: {file_path}")
        return True
        
    except (IOError, TypeError) as e:
        # IOError 可能是权限问题或路径错误
        # TypeError 可能是 data 中包含无法序列化的对象 (如 class 实例)
        print(f"错误: 无法将数据保存到 {file_path}。原因: {e}")
        return False

# --- 如何使用 ---
if __name__ == "__main__":
    
    # 1. 准备一个 Python 字典
    my_data = {
        "name": "贵州茅台",
        "code": "600519",
        "analysis": {
            "result": "看好",
            "reasons": [
                "品牌护城河强",
                "现金流充裕"
            ]
        },
        "price_history": [1800.5, 1820.0, 1815.3]
    }

    # 2. 指定保存路径
    # (推荐) 保存到子目录
    file1 = "output/stock_data.json" 
    save_to_json(my_data, file1)

    # (也行) 保存到当前目录
    file2 = "another_data.json"
    my_list = [1, 2, "你好", {"key": "value"}]
    save_to_json(my_list, file2)
    
    # 3. 模拟一个无法序列化的错误
    print("\n--- 模拟错误 ---")
    class MyObject:
        pass
    
    bad_data = {"key": MyObject()} # MyObject 实例默认无法被 JSON 序列化
    save_to_json(bad_data, "bad.json")