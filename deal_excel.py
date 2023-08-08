"""
主程序入口
"""
import warnings
import pandas as pd

from script.get_format_col import get_format_col
from script.get_format_df import get_format_df
from script.get_name_and_filepath import get_name_and_filepath
from script.merge_col import merge_col
from script.modify import get_union_outdir, modify_process

warnings.filterwarnings('ignore')


# 配置进项文件、销项文件还有输出文件的路径。
# excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
# excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
# excel_lastmonth_url = r"D:\dev\ExcelUtil\temp\2月匹配剩余表.xlsx"
# union_outdir = r"D:\dev\ExcelUtil\temp\out"



# process_id代表第几种生成
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。



def main():
    union_outdir = get_union_outdir()
    print("union_outdir",union_outdir)

    print("modify启动")
    excel_in_url, excel_out_url, excel_lastmonth_url, process_id, union_not_outdir, union_yet_outdir, union_tofill_outdir\
        = modify_process(union_outdir)
    print("process_id", process_id)
    print("modify完成")

    # print("get_name_and_filepath启动")
    # union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir = \
    #     get_name_and_filepath(excel_in_url, union_outdir)
    # print("get_name_and_filepath完成")

    print("get_format_df启动")
    union_df, in_col, out_col = get_format_df()
    print("get_format_df完成")

    match_out_col = match_in_col = pd.DataFrame()

    if process_id == 2:
        print("第三种生成开始")

        print("得到进项表和销项表和上月剩余表的out_col和in_col")
        lastmonth_out_col, lastmonth_in_col = get_format_col(excel_lastmonth_url)
        match_out_col = get_format_col(excel_out_url)
        match_in_col = get_format_col(excel_in_url)

        print("将lastmonth_out_col和match_out_col结合")
        match_out_col = merge_col(lastmonth_out_col, match_out_col)
        match_in_col = merge_col(lastmonth_in_col, match_in_col)

        print("第二种生成完毕")


    if process_id == 1:
        print("第一种生成开始")
        print("得到进项表和销项表的out_col和in_col")
        match_out_col = get_format_col(excel_out_url)

        match_in_col = get_format_col(excel_in_url)

        print("第一种生成完毕")


    print("共同部分")
    print("pre_deal开始")
    match_in_col, match_out_col, tofill_flag = pre_deal(match_in_col, match_out_col, union_tofill_outdir)
    print("pre_deal完成")
    print("tofill_flag")
    print(tofill_flag)

    print("match_out_col")
    print(match_out_col)
    print("match_in_col")
    print(match_in_col)

    print("process启动")
    if tofill_flag == 0:
        process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir)
    else:
        process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_temp_yet_outdir, union_temp_not_outdir)
    print("process完成")

    return
