models = [
    {"name": "GPT", "score": 95},
    {"name": "Claude", "score": 88},
    {"name": "Gemini", "score": 92},
    {"name": "DeepSeek", "score": 85}
]
while True:
    keyword=input("请输入模型名称：").strip().lower()
    if keyword=="exit":
        print("程序已退出")
        break
    found =False
    for model in models:
        if keyword in model["name"].lower():
            print("找到模型：", model["name"],"评分：",model["score"])
            found=True
    if not found:
        print("没有找到相关模型")
