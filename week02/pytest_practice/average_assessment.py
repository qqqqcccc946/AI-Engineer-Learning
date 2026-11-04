def calculate_average(models):   
    if not models:
        
      return 0
    total=0 
    for model in models :
        total += model["score"]
    average=total/len(models)
    return average

# 假设你的 calculate_average 函数定义在这个文件里，或者从其他文件 import 了

def test_empty_list():
    """测试空列表情况"""
    assert calculate_average([]) == 0

def test_single_model():
    """测试单个模型"""
    result = calculate_average([
        {"name": "GPT", "score": 95}
    ])
    assert result == 95.0

def test_multiple_models():
    """测试多个模型"""
    result = calculate_average([
        {"name": "GPT", "score": 80},
        {"name": "Claude", "score": 90},
        {"name": "Gemini", "score": 100}
    ])
    assert result == 90.0