"""
数学计算器程序
功能：加减乘除、幂运算、开方，记录计算历史
"""

import math
import json
import os
from datetime import datetime


# ============ 数学运算函数 ============

def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


def multiply(a, b):
    """乘法"""
    return a * b


def divide(a, b):
    """除法"""
    if b == 0:
        raise ZeroDivisionError("除数不能为0！")
    return a / b


def power(a, b):
    """幂运算"""
    return a ** b


def square_root(a):
    """开方运算"""
    if a < 0:
        raise ValueError("不能对负数开方！")
    return math.sqrt(a)


# ============ 文件操作函数 ============

def save_history(history, filename='calculator_history.json'):
    """保存历史记录到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=2)
        return True
    except Exception as error:
        print(f"保存历史记录失败: {error}")
        return False


def load_history(filename='calculator_history.json'):
    """从文件加载历史记录"""
    try:
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            history = json.load(file)
            return history if isinstance(history, list) else []
    except Exception:
        return []


def display_history(history):
    """显示历史记录"""
    if not history:
        print("\n暂无计算历史记录")
        return

    print("\n" + "=" * 60)
    print("        计算历史记录")
    print("=" * 60)

    # 显示最近10条
    start = max(0, len(history) - 10)
    for i in range(start, len(history)):
        record = history[i]
        print(f"[{i + 1}] {record.get('timestamp', '未知时间')}")
        print(f"    {record.get('expression', '')}")
        print("-" * 40)

    print("=" * 60)


# ============ 辅助函数 ============

def get_number(prompt):
    """获取有效的数字输入"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("错误：请输入有效数字！")


def show_menu():
    """显示菜单"""
    print("\n" + "=" * 60)
    print("        数学计算器")
    print("=" * 60)
    print("1. 加法 (+)")
    print("2. 减法 (-)")
    print("3. 乘法 (*)")
    print("4. 除法 (/)")
    print("5. 幂运算 (x^y)")
    print("6. 开方 (√x)")
    print("7. 查看历史记录")
    print("8. 退出程序")
    print("=" * 60)


# ============ 核心计算函数 ============

def calculate(operator, a, b=None):
    """
    执行计算

    参数:
        operator: 运算符 (+, -, *, /, ^, √)
        a: 第一个数
        b: 第二个数（开方不需要）

    返回值:
        (结果, 表达式字符串)
    """
    operations = {
        '+': (add, f"{a} + {b}"),
        '-': (subtract, f"{a} - {b}"),
        '*': (multiply, f"{a} * {b}"),
        '/': (divide, f"{a} / {b}"),
        '^': (power, f"{a} ^ {b}"),
        '√': (square_root, f"√{a}")
    }

    if operator not in operations:
        raise ValueError(f"未知运算符: {operator}")

    func, expression = operations[operator]

    try:
        if operator == '√':
            result = func(a)
        else:
            result = func(a, b)
        return result, f"{expression} = {result}"
    except (ZeroDivisionError, ValueError) as error:
        print(f"计算错误：{error}")
        return None, None


def add_to_history(history, expression, result):
    """添加记录到历史"""
    record = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'expression': expression,
        'result': result
    }
    history.append(record)
    save_history(history)


# ============ 主程序 ============

def run_calculator():
    """运行计算器"""
    history = load_history()
    print(f"已加载 {len(history)} 条历史记录")

    while True:
        show_menu()
        choice = input("请选择操作 (1-8): ").strip()

        # 退出
        if choice == '8':
            print("\n感谢使用计算器，再见！")
            break

        # 查看历史
        if choice == '7':
            display_history(history)
            continue

        # 执行计算
        if choice in ['1', '2', '3', '4', '5', '6']:
            # 映射选择到运算符
            op_map = {'1': '+', '2': '-', '3': '*', '4': '/', '5': '^', '6': '√'}
            operator = op_map[choice]

            # 获取输入
            if operator == '√':
                a = get_number("请输入要开方的数: ")
                result, expression = calculate(operator, a)
            else:
                a = get_number("请输入第一个数: ")
                b = get_number("请输入第二个数: ")
                result, expression = calculate(operator, a, b)

            # 显示结果并保存
            if result is not None:
                print(f"\n结果: {expression}")
                add_to_history(history, expression, result)
            else:
                print("\n计算失败")
        else:
            print("错误：无效选项，请重新选择！")


# ============ 程序入口 ============

if __name__ == "__main__":
    try:
        run_calculator()
    except KeyboardInterrupt:
        print("\n\n程序已退出")