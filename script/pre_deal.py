import pandas as pd


global in_col, out_col, match_in_col, match_out_col

def pre_deal(match_in_col, match_out_col, union_tofill_outdir):
    """
    # 预处理函数 对match_in_col和match_out_col进行额外的处理，同时判断这两个表单是否能生成待填充表
    union_tofill_url 待填充表的绝对路径
    # 1、将表格中含有空值的行提取出来，放到temp_in里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    # 2、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    # 3、如果有关键数值含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    # 4、将表单按照含税单价排列，输出进项表单为match_xx_col。
    # 5、如果2中有空值，生成”待填充表“。
    # 返回只含有关键列的进销项dataframe和关键列在原excel中的列名
    :return: in_col, out_col, match_in_col, match_out_col, flag
    """

    # 2、将表格中含有空值的行提取出来，放到temp_in里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    temp_in = match_in_col[match_in_col.isna().any(axis=1)]
    temp_in["from"] = "in"
    match_in_col = match_in_col.dropna()

    # 3、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    match_in_col["vis"] = 0

    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].astype(str)
    match_in_col["发票号码"] = match_in_col["发票号码"].astype(str)
    match_in_col["数量"] = match_in_col["数量"].astype(int)

    # 4、如果税收分类编码含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].str.replace("'", "")
    match_in_col['税率'] = match_in_col['税率'].str.strip().str.rstrip('%').astype(float) / 100
    match_in_col["含税单价"] = match_in_col["单价"] * (1 + match_in_col["税率"])

    # 5、将进项表单按照含税单价排列，输出进项表单为match_in_col。
    match_in_col = match_in_col.sort_values('含税单价')
    match_in_col.to_excel("match_in_col.xlsx", index=False)
    print("进项表单预处理结束")


    # 2、将表格中含有空值的行提取出来，放到temp_out里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    temp_out = match_out_col[match_out_col.isna().any(axis=1)]
    temp_out["from"] = "out"
    match_out_col = match_out_col.dropna()


    # 3、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    match_out_col["vis"] = 0

    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].astype(str)
    match_out_col["发票号码"] = match_out_col["发票号码"].astype(str)
    match_out_col["数量"] = match_out_col["数量"].astype(int)

    # 4、如果税收分类编码含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].str.replace("'", "")
    match_out_col['税率'] = match_out_col['税率'].str.strip().str.rstrip('%').astype(float) / 100
    match_out_col["含税单价"] = match_out_col["单价"] * (1 + match_in_col["税率"])

    # 5、将销项表单按照含税单价排列，输出销项表单为match_out_col。
    match_out_col = match_out_col.sort_values('含税单价')
    match_out_col.to_excel("match_out_col.xlsx", index=False)
    print("销项表单预处理结束")

    # 6、如果2中有空值，生成”待填充表“。
    match_tofill_col = pd.concat([temp_in, temp_out], ignore_index=True)
    flag = 0
    if match_tofill_col.empty:
        print("待填充表为空")
    else:
        flag = 1
        match_tofill_col.to_excel(union_tofill_outdir, index=False)
        print("待填充表生成完毕")

    return in_col, out_col, match_in_col, match_out_col, flag