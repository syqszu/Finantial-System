"""
主程序入口，不和前端联动，测试版
"""
import warnings

import pandas as pd

from script.get_format_col import get_format_col
from script.get_format_df import get_format_df
from script.get_name_and_filepath import get_name_and_filepath
from script.merge_col import merge_col
from script.pre_deal import pre_deal
from script.process import process

warnings.filterwarnings('ignore')

# 配置进项文件、销项文件还有输出文件的路径。
excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
excel_lastmonth_url = r"D:\dev\ExcelUtil\temp\2月匹配剩余表.xlsx"
excel_filled_url = r"D:\dev\ExcelUtil\temp\3月待填充表.xlsx"
union_outdir = r"D:\dev\ExcelUtil\temp\out"

# process_id代表第几种生成
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入有临时完成表、临时剩余表、待填充表。输出为匹配完成表+匹配剩余表。
# 第三种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。

process_id = 2

if __name__ == '__main__':
    print("get_name_and_filepath启动")
    union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir = \
        get_name_and_filepath(excel_in_url, union_outdir)
    print("get_name_and_filepath完成")
    #
    # print("pre_deal启动")
    # # tofill_flag=0表示生成了待填充表，tofill_flag=1表示直接生成了完成表和剩余表
    # in_col, out_col, column_names, match_in_col, match_out_col, tofill_flag = \
    #     pre_deal(excel_in_url, excel_out_url, union_tofill_outdir)
    # print("pre_deal完成")
    #
    # print("get_format_df启动")
    # union_df = get_format_df()
    # print("get_format_df完成")
    #
    # lastmonth_out_col, lastmonth_in_col ,match_out_col, match_in_col= pd.DataFrame()

    # if process_id == 3:
    #     print("第三种生成开始")
    #     print("输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。")
    #     lastmonth_out_col, lastmonth_in_col = get_format_col(excel_lastmonth_url)
    #     match_out_col = get_format_col(excel_out_url)
    #     match_in_col = get_format_col(excel_in_url)
    #
    #     print("process启动")
    #     process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir,
    #             union_temp_not_outdir, union_temp_yet_outdir)
    #     print("process完成")
    #
    #     print("第三种生成完毕")
    if process_id == 2:

        print("第二种生成开始")
        print("输入有临时完成表、临时剩余表、待填充表。输出为匹配完成表+匹配剩余表。")

        print("得到匹配临时完成表的out_col和in_col")
        temp_yet_out_col, temp_yet_in_col = get_format_col(union_temp_yet_outdir)

        print("得到匹配临时剩余表的out_col和in_col")
        temp_not_out_col, temp_not_in_col = get_format_col(union_temp_not_outdir)

        print("得到填充完成表的out_col和in_col")
        filled_out_col, filled_in_col = get_format_col(excel_filled_url)

        filled_out_col.to_excel("第二次生成filled_out_col.xlsx",index=False)
        filled_in_col.to_excel("第二次生成filled_in_col.xlsx",index=False)

        # 将匹配临时完成表和匹配临时剩余表合并起来
        temp_out_col1 = merge_col(temp_yet_out_col, temp_not_out_col)
        temp_in_col1 = merge_col(temp_yet_in_col, temp_not_in_col)

        # filled_out_col.to_excel("第二次生成temp_out_col1.xlsx",index=False)
        # filled_in_col.to_excel("第二次生成temp_in_col1.xlsx",index=False)

        # 再和填充完成表合并起来
        match_out_col= merge_col(temp_out_col1, filled_out_col)
        match_in_col = merge_col(temp_in_col1, filled_in_col)
        match_out_col.to_excel("第二次生成out.xlsx",index=False)
        match_in_col.to_excel("第二次生成in.xlsx", index=False)
        print("第二种生成完毕")

    # if process_id == 1:
    #     print("process启动")
    #     process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir,
    #             union_temp_not_outdir, union_temp_yet_outdir)
    #     print("process完成")
