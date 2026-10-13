name=input("请输入姓名：")
hours=float(input("请输入每天学习小时数："))

days=int(input("每周学习天数："))
if hours < 0 or days < 0 or days > 7:
    print("输入数据不合理")
else:
    total=hours*days
    print(f"学习者: {name}")
    print(f"每周学习时间：{total}小时")
    if total<7:
        plan="轻量学习计划"
    elif total<14:
        plan="常规学习计划"
    else:
        plan="高强度学习计划" 
    print(f"推荐计划：{plan}")




