
models = [
    {"name": "GPT", "score": 95},
    {"name": "Claude", "score": 88},
    {"name": "Gemini", "score": 92},
    {"name": "DeepSeek", "score": 85}
]
while True:
    print("\n===== AI 模型管理器 V2 =====")
    print("1. 查看全部模型")
    print("2. 查找模型")
    print("3. 查看高分模型")
    print("4. 统计模型数量")
    print("5. 新增模型和评分")
    print("6. 计算平均分")
    print("7. 修改评分")
    print("0. 退出")

    choice = input("请选择功能：")

    if choice == "1":
        for model in models:
            print(model["name"], model["score"])

    elif choice == "2":
        keyword = input("请输入模型名称：").strip().lower()
        found = False

        for model in models:
            if keyword in model["name"].lower():
                print("找到模型：", model["name"])
                found = True

        if not found:
            print("没有找到相关模型")

    elif choice == "3":
        for model in models:
            if model["score"] >= 90:
                print(model["name"], model["score"])

    elif choice == "4":
        print("模型总数：", len(models))
    elif choice =="5":
        keyword=input("请输入模型名称：")
        keyword2 = float(input("请输入模型评分："))
        models.append({
    "name": keyword,
    "score": keyword2
})
    elif choice=="6":
        total=0
        for model in models:
            total += model["score"]
        pingjun=total/len(models)
        print(pingjun)
    elif choice=="7":
        keyword = input("请输入模型名称：").strip().lower()
        found = False
        
        for model in models:
            if keyword in model["name"].lower():
            
                found = True
                change=float(input("请输入需要修改的评分："))
                model["score"] = change 
                print("评分修改成功！")
                break

        
            if not found:
                print("没有找到相关模型")
           
    elif choice == "0":
        print("程序结束")
        break

    else:
        print("输入无效，请重新选择")
