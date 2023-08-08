import pandas as pd

from script.format_excel import format_excel


def process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir):
    """
    输入match_in_col和match_out_col。根据tofill_flag生成
    1、临时完成表+临时剩余表（tofill_flag=1）
    2、匹配完成表+匹配剩余表。(tofill_flag=0)
    """
    process_yet(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir)
    # 第一次匹配，生成匹配完成表
    process_not(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_not_outdir)
    # 第二次匹配，生成匹配剩余表
    return


def process_yet(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir):
    union_yet_df = union_df.copy()
    id = 1
    # 暴力循环
    print("月匹配完成表开始生成")

    for idx_out, row_out in match_out_col.iterrows():
        for idx_in, row_in in match_in_col.iterrows():

            shuishou_out = row_out["税收分类编码"]
            shuishou_in = row_in["税收分类编码"]

            date_out = row_out["开票日期"]  # 2023-03-05
            date_in = row_in["开票日期"]

            number_out = row_out["发票号码"]
            number_in = row_in["发票号码"]

            loads_out = row_out["货物、应税劳务及服务"]
            loads_in = row_in["货物、应税劳务及服务"]

            size_out = row_out["规格型号"]
            size_in = row_in["规格型号"]

            unit_out = row_out["单位"]
            unit_in = row_in["单位"]

            origin_nums_out = row_out["数量"]  # 销项上月原数量
            origin_nums_in = row_in["数量"]  # 进项上月原数量

            notax_perprice_out = row_out["单价"]  # 销项不含税单价
            notax_perprice_in = row_in["单价"]  # 进项不含税单价

            notax_money_out = row_out["金额"]  # 销项不含税金额
            notax_money_in = row_in["金额"]  # 进项不含税金额

            tax_out = row_out["税率"]  # 销项税率
            tax_in = row_in["税率"]  # 进项税率

            tax_perprice_out = row_out["含税单价"]  # 销项含税单价
            tax_perprice_in = row_in["含税单价"]  # 进项含税单价

            tax_money_out = row_out["价税合计"]  # 销项含税总金额
            tax_money_in = row_in["价税合计"]  # 进项含税总金额

            name_in = row_in["销方名称"]  # 销方名称
            name_out = row_out["购方名称"]  # 供应商

            note = row_out["备注"]

            difference = abs(tax_perprice_in - tax_perprice_out)
            percentage_differ = (difference / tax_perprice_in) * 100

            case1 = (shuishou_in == shuishou_out) and (row_out["vis"] == 0) and (row_in["vis"] == 0)
            # print("case1")
            # print(case1)
            shuishou_front7_in = row_in[0][0:6]
            shuishou_front7_out = row_out[0][0:6]

            case2 = (shuishou_front7_in == shuishou_front7_out) and (row_out["vis"] == 0) and (row_in["vis"] == 0) and (
                        percentage_differ <= 10)

            # 第一次遍历，将税收分类编码完美匹配的vis打上1的标记   前七位相同，含税单价相差不超过10%的vis打上2的标记
            if case1 or case2:
                # print("进入case1 or case 2")
                yet_row = {"开票日期": date_out, "序号": id, "发票号码": number_out,
                           "税收分类编码": shuishou_out, "货物、应税劳务及服务": loads_out, "规格型号": size_out,
                           "单位": unit_out, "上月原数量": origin_nums_out}

                outbound_pro_nums_out = outbound_pro_nums_in = 0  # 上月程序出库数
                remain_nums_out = remain_nums_in = 0  # 本月剩余数量

                if origin_nums_in < origin_nums_out:  # 进项上月原数量<销项上月原数量
                    outbound_pro_nums_out = outbound_pro_nums_in = origin_nums_in  # 销进项上月程序出库数=进项上月原数量
                    remain_nums_out = origin_nums_out - origin_nums_in  # 销项本月剩余量=销项上月原数量-进项上月原数量
                    remain_nums_in = 0  # 进项本月剩余量=0
                    temp_row = {}
                    for col in out_col:
                        temp_row.update({col: row_out[col]})
                    temp_row.update({"数量": remain_nums_out})
                    # print(temp_row)
                    match_out_col.loc[len(match_out_col)] = temp_row

                else:  # 进项上月原数量>销项上月原数量
                    outbound_pro_nums_out = outbound_pro_nums_in = origin_nums_out
                    remain_nums_in = origin_nums_in - origin_nums_out
                    remain_nums_out = 0
                    temp_row = {}
                    for col in in_col:
                        temp_row.update({col: row_in[col]})
                    temp_row.update({"数量": remain_nums_in})
                    # print(temp_row)
                    match_in_col.loc[len(match_in_col)] = temp_row

                yet_row.update(
                    {"上月程序出库数": outbound_pro_nums_out, "上月人工出库数": 0, "本月剩余数量": remain_nums_out})

                yet_row.update(
                    {"不含税单价": notax_perprice_out, "不含税金额": notax_money_out, "税率": tax_out,
                     "含税单价": tax_perprice_out,
                     "含税总金额": tax_money_out, "供应商": name_out, "备注": note})
                yet_row.update({"开票日期1": date_in, "序号1": id, "发票号码1": number_in, "税收分类编码1": row_in[0],
                                "货物、应税劳务及服务1": loads_in, "规格型号1": size_in, "单位1": unit_in,
                                "上月原数量1": origin_nums_in, "上月程序出库数1": outbound_pro_nums_in,
                                "上月人工出库数1": 0,
                                "本月剩余数量1": remain_nums_in, "不含税单价1": notax_perprice_in,
                                "不含税金额1": notax_money_in, "税率1": tax_in,
                                "含税单价1": tax_perprice_in, "含税总金额1": tax_money_in, "销方名称": name_in})

                union_yet_df = union_yet_df.append(yet_row, ignore_index=True)

                if case1:
                    match_out_col.at[idx_out, "vis"] = match_in_col.at[idx_in, "vis"] = 1
                if case2:
                    match_out_col.at[idx_out, "vis"] = match_in_col.at[idx_in, "vis"] = 2

                id += 1

    if tofill_flag == 0:

        union_yet_df["人工备注"] = ""
        union_yet_df["日期错位警告"] = ""
        union_yet_df["利润警告(10%利润警告/亏本警告)"] = ""
        union_yet_df.loc[union_yet_df['开票日期'] < union_yet_df['开票日期1'], '日期错位警告'] = '警告'
        union_yet_df.loc[union_yet_df['含税单价'] < union_yet_df['含税单价1'], '利润警告(10%利润警告/亏本警告)'] = '亏本警告'
        union_yet_df.loc[((union_yet_df["含税单价"] - union_yet_df["含税单价1"]) / union_yet_df["含税单价1"] * 100) >= 10,
        "利润警告(10%利润警告/亏本警告)"] = "10%利润警告"

        union_yet_df.to_excel(union_yet_outdir, index=False)
        print("月匹配完成表生成完毕")
    else:
        # print("union_yet_df", union_yet_df)
        union_yet_df.to_excel(union_yet_outdir, index=False)
        print("月匹配临时完成表生成完毕")

    print("format_excel启动")
    format_excel(tofill_flag, union_yet_outdir)
    print("format_excel完成")


def process_not(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_not_outdir):
    union_not_df = union_df.copy()
    print("月匹配剩余表开始生成")
    # 生成未匹配表
    id = 1
    for idx_out, row_out in match_out_col.iterrows():
        if row_out["vis"] == 0:
            shuishou_out = row_out["税收分类编码"]
            date_out = row_out["开票日期"]  # 2023-03-05
            number_out = row_out["发票号码"]
            loads_out = row_out["货物、应税劳务及服务"]
            size_out = row_out["规格型号"]
            unit_out = row_out["单位"]
            origin_nums_out = remain_nums_out = row_out["数量"]  # 销项上月原数量=本月剩余数量=销项文件的数量
            notax_perprice_out = row_out["单价"]  # 销项不含税单价
            notax_money_out = row_out["金额"]  # 销项不含税金额
            tax_out = row_out["税率"]
            tax_perprice_out = row_out["含税单价"]  # 销项含税单价
            tax_money_out = row_out["价税合计"]  # 销项含税总金额
            name_out = row_out["购方名称"]  # 供应商
            note = row_out["备注"]
            not_row = {"开票日期": date_out, "序号": id, "发票号码": number_out,
                       "税收分类编码": shuishou_out, "货物、应税劳务及服务": loads_out, "规格型号": size_out,
                       "单位": unit_out, "上月原数量": origin_nums_out, "上月程序出库数": 0,
                       "上月人工出库数": 0, "本月剩余数量": remain_nums_out, "不含税单价": notax_perprice_out,
                       "不含税金额": notax_money_out, "税率": tax_out, "含税单价": tax_perprice_out,
                       "含税总金额": tax_money_out, "供应商": name_out, "备注":note}
            union_not_df = union_not_df.append(not_row, ignore_index=True)
            id += 1
        # union_not_df = union_not_df.append(not_row, ignore_index=True)

    id = 1
    for idx_in, row_in in match_in_col.iterrows():
        if row_in["vis"] == 0:
            shuishou_in = row_in["税收分类编码"]
            date_in = row_in["开票日期"]
            number_in = row_in["发票号码"]
            loads_in = row_in["货物、应税劳务及服务"]
            size_in = row_in["规格型号"]
            unit_in = row_in["单位"]
            origin_nums_in = remain_nums_in = row_in["数量"]  # 进项上月原数量=本月剩余数量=销项文件的数量
            notax_perprice_in = row_in["单价"]  # 进项不含税单价
            notax_money_in = row_in["金额"]  # 进项不含税金额
            tax_in = row_in["税率"]
            tax_perprice_in = row_in["含税单价"]  # 进项含税单价
            tax_money_in = row_in["价税合计"]  # 进项含税总金额
            name_in = row_in["销方名称"]  # 销方名称
            not_row = {"开票日期1": date_in, "序号1": id, "发票号码1": number_in, "税收分类编码1": shuishou_in,
                       "货物、应税劳务及服务1": loads_in, "规格型号1": size_in, "单位1": unit_in,
                       "上月原数量1": origin_nums_in, "上月程序出库数1": 0,
                       "上月人工出库数1": 0,
                       "本月剩余数量1": remain_nums_in, "不含税单价1": notax_perprice_in,
                       "不含税金额1": notax_money_in,"税率1":tax_in,
                       "含税单价1": tax_perprice_in, "含税总金额1": tax_money_in, "销方名称": name_in}
            union_not_df = union_not_df.append(not_row, ignore_index=True)

    union_not_df.to_excel(union_not_outdir, index=False)
    print("format_excel启动")
    format_excel(1, union_not_outdir)
    print("format_excel完成")
    if tofill_flag == 0:
        print("月匹配剩余表生成完毕")
    else:
        print("月匹配临时剩余表生成完毕")

