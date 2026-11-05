# 02-互动热可可.py
# 功能：和程序对话，让它帮你算账

print("=== 暖爪咖啡 · 今日销售播报 ===")
print()

# 让用户输入数字
today = input("天卖了多少杯热可可？请输入数字：")
today = int(today)  # 把输入的文字转成数字

# 计算一周和一月
week = today * 7
month = today * 30

print()
print(f"按今天这个销量：")
print(f"一周能卖 {week} 杯")
print(f"一个月能卖 {month} 杯")
print()

# 根据销量给评价
if month >= 3000:
    print("生意不错！可以考虑开分店了 🎉")
elif month >= 1000:
    print("稳扎稳打，继续保持 ☕")
else:
    print("刚开始，慢慢来，雪绒热可可是慢热产品 ❄️")

# 让窗口暂停，不要跑完就关
input("\n按回车键退出...")
