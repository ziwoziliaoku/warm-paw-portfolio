# 03-three-cases.py
# 功能：一次对比 3 个销量，看 if/elif/else 怎么工作

print("=" * 40)
print("暖爪咖啡 · 销量评价对比实验")
print("=" * 40)

# 三个不同的日销量，一次跑完
test_cases = [5, 50, 200]

for cups in test_cases:
    month = cups * 30
    print()
    print(f"今天卖了 {cups} 杯 → 一个月约 {month} 杯")

    if month >= 3000:
        print("  → 评价：生意不错！可以考虑开分店了 🎉")
    elif month >= 1000:
        print("  → 评价：稳扎稳打，继续保持 ☕")
    else:
        print("  → 评价：刚开始，慢慢来 ❄️")

print()
print("=" * 40)
print("看到了吗？同一个程序，输入不同数字，评价不一样。")
print("这就是 if / elif / else —— 程序根据条件做判断。")

input("\n按回车键退出...")
