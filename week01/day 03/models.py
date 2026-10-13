models = [
    {"name": "GPT", "company": "OpenAI"},
    {"name": "Claude", "company": "Anthropic"},
    {"name": "Gemini", "company": "Google"}
]

print("===== AI 模型管理器 =====")
print(f"模型数量: {len(models)}")
print(f"第一个模型：{models[0]['name']}")
print(f"第二个模型公司：{models[1]['company']}")

models.append({
    "name": "DeepSeek",
    "company": "DeepSeek"
})

print(f"添加后模型数量：{len(models)}")
print(f"新模型：{models[-1]['name']}")
