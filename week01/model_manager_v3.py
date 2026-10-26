import json
models = [
    {"name": "GPT", "score": 95},
    {"name": "Claude", "score": 88},
    {"name": "Gemini", "score": 92},
    {"name": "DeepSeek", "score": 85}
]


def show_models(models):
    for model in models:
        print(f"{model["name"]}: {model["score"]}分")


def add_model(models,name,score):

    models.append({"name": name,"score": score})
def save_models(models):
    with open("models.json", "w", encoding="utf-8") as file:
        json.dump(models, file, ensure_ascii=False, indent=4)
    print("数据保存成功")
def load_models():
 try:
        with open("models.json", "r", encoding="utf-8") as file:
            return json.load(file)
 except FileNotFoundError:
        print("文件不存在")
        return []
 except json.JSONDecodeError:
        print("JSON 文件格式错误")
        return []
def input_score():
    while True:
        try:
            score = float(input("请输入模型评分："))

            if not 0 <= score <= 100:
                raise ValueError("评分必须在0到100之间")

            return int(score) if score.is_integer() else score

        except ValueError as error:
            print(f"输入错误，请重新输入")                
# 测试代码
# 测试代码
# 第一步：启动时读取历史数据
#models = load_models()
# 第二步：显示已有数据
#print("当前模型：")
#show_models(models)
# 第三步：添加新模型
#add_model(models, "ccc", 98)
# 第四步：保存更新后的数据
#save_models(models)
# 第五步：显示最终结果
#print("更新后的模型：")
#show_models(models)
#任务c测试
# 任务 C 测试
models = load_models()

print("加载结果：", models)
print("数据类型：", type(models))
