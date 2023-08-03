import pandas as pd

from script.deal_excel import excel_in_url, excel_out_url, union_tofill_outdir


def pre_deal():
    """
    # 预处理函数
    excel_in_url 进项excel的绝对路径
    excel_out_url 进项excel的绝对路径
    # 1、读取表格
    # 2、如果有关键数据为空值，输出空值的行列索引并将该行额外存到一个新表中。
    # 3、提取关键列，添加vis列，将税收分类编码转化为str，方便后续操作
    # 4、如果税收分类编码含有单引号，去除单引号
    # 返回只含有关键列的进销项dataframe和关键列在原excel中的列名
    :return:
    """
    global in_col, out_col, match_in_col, match_out_col
    in_col = ["税收分类编码", "发票号码", "开票日期", "销方名称", "货物、应税劳务及服务", "规格型号", "数量", "单价",
              "单位", "金额", "税率", "价税合计"]
    out_col = ["税收分类编码", "发票号码", "开票日期", "购方名称", "货物、应税劳务及服务", "规格型号", "数量", "单价",
               "单位", "金额", "税率", "价税合计", "备注"]

    # 1、读取表格
    print("开始遍历进项表格")
    df_in = pd.read_excel(excel_in_url, "Sheet1", header=1)
    match_in_col = df_in[in_col]  # pandas.core.frame.DataFrame

    temp_in = match_in_col[match_in_col.isna().any(axis=1)]
    temp_in["from"] = "in"
    match_in_col = match_in_col.dropna()
    print("进项表单遍历结束")

    # 3、提取关键列，添加vis列。将税收分类编码转化为str，方便后续操作
    match_in_col["vis"] = 0
    # print("type of match_in_col[税收分类编码] before")
    # print(match_in_col["税收分类编码"].dtype)
    # float64
    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].astype(str)
    match_in_col["发票号码"] = match_in_col["发票号码"].astype(str)
    print("type of match_in_col[发票号码] after")
    print(match_in_col["发票号码"].dtype)

    match_in_col["数量"] = match_in_col["数量"].astype(int)
    print("type of match_in_col[数量] after")
    print(match_in_col["数量"].dtype)

    # match_in_col["税率"] = float(match_in_col["税率"].strip("%")) / 100  # 销项税率
    match_in_col['税率'] = match_in_col['税率'].str.strip().str.rstrip('%').astype(float) / 100
    match_in_col["含税单价"] = match_in_col["单价"] * (1 + match_in_col["税率"])
    match_in_col = match_in_col.sort_values('含税单价')
    match_in_col.to_excel("test.xlsx", index=False)
    # object

    # 4、如果有关键数值含有单引号，去除单引号
    match_in_col["税收分类编码"] = match_in_col["税收分类编码"].str.replace("'", "")

    print("开始遍历销项表格")
    df_out = pd.read_excel(excel_out_url, "Sheet1", header=2)
    match_out_col = df_out[out_col]

    # for idx, row in match_out_col.iterrows():
    #     for col in match_out_col.columns:
    #         if pd.isna(row[col]):
    #             print("表单中存在空值，请补全后重启程序。行索引-{},列索引-{}".format(idx + 4, col))

    temp_out = match_out_col[match_out_col.isna().any(axis=1)]
    temp_out["from"] = "out"
    match_out_col = match_out_col.dropna()

    temp_col = pd.concat([temp_in, temp_out], ignore_index=True)
    temp_col.to_excel(union_tofill_outdir, index=False)

    print("销项表单遍历结束")
    match_out_col["vis"] = 0
    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].fillna(0).astype(str)
    # print()
    # print(match_out_col["税收分类编码"])
    match_out_col["税收分类编码"] = match_out_col["税收分类编码"].str.replace("'", "")
    # match_out_col["数量"] = match_out_col["数量"].str.replace("'", "")
    # match_out_col["单价"] = match_out_col["单价"].str.replace("'", "")
    print("match_out_col")
    for col_name, dtype in match_out_col.dtypes.iteritems():
        print(f"列名: {col_name}, 数据类型: {dtype}")
    print("match_in_col")
    for col_name, dtype in match_in_col.dtypes.iteritems():
        print(f"列名: {col_name}, 数据类型: {dtype}")

    return match_in_col, match_out_col, in_col, out_col