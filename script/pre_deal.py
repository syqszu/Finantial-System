import re

import pandas as pd


global in_col, out_col, match_in_col, match_out_col

def pre_deal(match_in_col, match_out_col, union_tofill_outdir):
    """
    # 预处理函数 1、判断两个表单是否能生成待填充表
     2、对match_in_col和match_out_col增加“vis”和“含税单价”列，按照“含税单价”排列，处理某些列的数据类型

    # 1、将表格中含有空值的行提取出来，放到temp_in里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    # 2、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    # 3、如果有关键数值含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    # 4、将表单按照含税单价排列，输出进项表单为match_xx_col。
    # 5、如果2中有空值，生成”待填充表“。

    # 返回处理后的match_in_col和match_out_col。tofill_flag=1表示生成待填充表，=0表示没生成。
    :return: match_in_col, match_out_col, tofill_flag
    """
    # print("处理前的match_in_col")
    # for column, dtype in match_in_col.dtypes.iteritems():
    #     print(f"列名：{column}，数据类型：{dtype}")


    # 2、将表格中含有空值的行提取出来，放到temp_in里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    temp_in = match_in_col[match_in_col.isna().any(axis=1)]
    temp_in["from"] = "in"
    match_in_col = match_in_col.dropna()

    # 3、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    match_in_col["vis"] = 0

    match_in_col["税收分类编码"]=match_in_col["税收分类编码"].astype(str)
    print(match_in_col["税收分类编码"].dtype)
    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].str.replace("'", "")

    def expand_scientific_notation(data):
        # 如果是科学计数法的形式
        if 'e+' in data:
            # 将科学计数法转换为浮点数，并使用字符串格式化展示
            return '{:.0f}'.format(float(data))
        else:
            return data

    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].apply(expand_scientific_notation)

    match_in_col["发票号码"] = match_in_col["发票号码"].astype(str)
    match_in_col["数量"] = match_in_col["数量"].astype(int)

    # 4、如果税收分类编码含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。

    if match_in_col['税率'].dtype == object:
        print("开始处理税率")
        # match_in_col['税率'] = match_in_col['税率'].str.replace('%', '').astype(float) / 100
        match_in_col['税率'] = match_in_col['税率'].astype(str).apply(lambda x: float(re.sub('%', '', x)) / 100)
    match_in_col["含税单价"] = match_in_col["单价"] * (1 + match_in_col["税率"])

    # 5、将进项表单按照含税单价排列，输出进项表单为match_in_col。
    match_in_col = match_in_col.sort_values('含税单价')
    # match_in_col.to_excel("match_in_col.xlsx", index=False)


    # print("处理后的match_in_col")
    # for column, dtype in match_in_col.dtypes.iteritems():
    #     print(f"列名：{column}，数据类型：{dtype}")

    # print("match_in_col")
    # print(match_in_col)

    print("进项表单预处理结束")

    # ***********************************************************************************************

    # print("处理前的match_out_col")
    # for column, dtype in match_out_col.dtypes.iteritems():
    #     print(f"列名：{column}，数据类型：{dtype}")

    # 2、将表格中含有空值的行提取出来，放到temp_out里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    temp_out = match_out_col[match_out_col.isna().any(axis=1)]
    temp_out["from"] = "out"
    match_out_col = match_out_col.dropna()


    # 3、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    match_out_col["vis"] = 0

    match_out_col["发票号码"] = match_out_col["发票号码"].astype(str)
    match_out_col["数量"] = match_out_col["数量"].astype(int)

    # 4、如果税收分类编码含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    match_out_col["税收分类编码"]=match_out_col["税收分类编码"].astype(str)
    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].str.replace("'", "")
    print(match_out_col["税收分类编码"].dtype)

    def expand_scientific_notation(data):
        # 如果是科学计数法的形式
        if 'e+' in data:
            # 将科学计数法转换为浮点数，并使用字符串格式化展示
            return '{:.0f}'.format(float(data))
        else:
            return data

    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].apply(expand_scientific_notation)

    if match_out_col['税率'].dtype == object:
        print("开始处理税率")
        match_out_col['税率'] = match_out_col['税率'].astype(str).apply(lambda x: float(re.sub('%', '', x)) / 100)
    match_out_col["含税单价"] = match_out_col["单价"] * (1 + match_out_col["税率"])


    # print("处理后的match_out_col")
    # for column, dtype in match_out_col.dtypes.iteritems():
    #     print(f"列名：{column}，数据类型：{dtype}")
    #
    # print("match_out_col")
    # print(match_out_col)

    # 5、将销项表单按照含税单价排列，输出销项表单为match_out_col。
    match_out_col = match_out_col.sort_values('含税单价')
    # match_out_col.to_excel("match_out_col.xlsx", index=False)

    # print("处理后的match_out_col")
    # for column, dtype in match_out_col.dtypes.iteritems():
    #     print(f"列名：{column}，数据类型：{dtype}")

    print("销项表单预处理结束")

    return match_in_col, match_out_col, tofill_flag