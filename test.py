# from datetime import date
#
#
# def calculate_age_simple(birth_date_str):
#     # 解析出生日期
#     year, month, day = map(int, birth_date_str.split('-'))
#     birth_date = date(year, month, day)
#     # 当前日期
#     today = date.today()
#     # 计算年龄
#     age = today.year - birth_date.year
#     if today < birth_date.replace(year=today.year):
#         age -= 1
#     return age
#
#
# # 使用示例
# birth_date = "2001-04-16"
# age = calculate_age_simple(birth_date)
# print(f"出生日期: {birth_date}")
# print(f"当前年龄: {age} 岁")