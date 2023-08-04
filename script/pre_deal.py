import pandas as pd


global in_col, out_col, match_in_col, match_out_col

def pre_deal(excel_in_url, excel_out_url, union_tofill_outdir):
    """
    # 预处理函数 对进项表单和销项表单进行一系列处理，变成match_in_col和match_out_col，同时判断这两个表单是否能生成待填充表
    excel_in_url 进项excel的绝对路径
    excel_out_url 进项excel的绝对路径
    union_tofill_url 待填充表的绝对路径
    # 1、读取表格
    # 2、将表格中含有空值的行提取出来，放到temp_in里，用以后续生成“待填充表”。同时表格中删去这些含有空值的行
    # 3、提取关键列，添加vis列。将税收分类编码、发票号码转化为object类型，数量转化为int类型，方便后续操作
    # 4、如果有关键数值含有单引号，去除单引号。税率改为float类型的数据。增加含税单价的列。
    # 5、将表单按照含税单价排列，输出进项表单为match_xx_col。
    # 6、如果2中有空值，生成”待填充表“。
    # 返回只含有关键列的进销项dataframe和关键列在原excel中的列名
    :return: match_in_col, match_out_col, [match_tofill_col]
    """
    global in_col, out_col, column_names, match_in_col, match_out_col
    in_col = ["税收分类编码", "发票号码", "开票日期", "销方名称", "货物、应税劳务及服务", "规格型号", "数量", "单价",
              "单位", "金额", "税率", "价税合计"]
    out_col = ["税收分类编码", "发票号码", "开票日期", "购方名称", "货物、应税劳务及服务", "规格型号", "数量", "单价",
               "单位", "金额", "税率", "价税合计", "备注"]
    column_names = ["开票日期", "序号", "发票号码", "税收分类编码", "货物、应税劳务及服务", "规格型号", "单位",
                    "上月原数量", "上月程序出库数",
                    "上月人工出库数", "本月剩余数量", "不含税单价", "不含税金额", "含税单价", "含税总金额", "供应商",
                    "开票日期1", "序号1", "发票号码1", "税收分类编码1", "货物、应税劳务及服务1", "规格型号1", "单位1",
                    "上月原数量1", "上月程序出库数1",
                    "上月人工出库数1", "本月剩余数量1", "不含税单价1", "不含税金额1", "含税单价1", "含税总金额1", "销方名称"]

    # 1、读取进项表格
    print("开始预处理进项表格")
    df_in = pd.read_excel(excel_in_url, "Sheet1", header=1)
    match_in_col = df_in[in_col]  # pandas.core.frame.DataFrame

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

    # 1、读取表格
    print("开始预处理销项表格")
    df_out = pd.read_excel(excel_out_url, "Sheet1", header=2)
    match_out_col = df_out[out_col]

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

    return in_col, out_col, column_names, match_in_col, match_out_col, flag