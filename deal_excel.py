"""
主程序入口，不和前端联动，测试版
"""
import warnings
import pandas as pd

from script.get_format_col import get_format_col
from script.get_format_df import get_format_df
from script.get_name_and_filepath import get_name_and_filepath
from script.judge_process_id import judge_process_id
from script.merge_col import merge_col
from script.modify import modify_process, get_union_outdir
from script.pre_deal import pre_deal
from script.process import process

warnings.filterwarnings('ignore')


# 配置进项文件、销项文件还有输出文件的路径。
# excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
# excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
# excel_lastmonth_url = r"D:\dev\ExcelUtil\temp\2月匹配剩余表.xlsx"
# union_outdir = r"D:\dev\ExcelUtil\temp\out"



# process_id代表第几种生成
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入有临时完成表、临时剩余表、待填充表。输出为匹配完成表+匹配剩余表。
# 第三种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。



def main():
    union_outdir = get_union_outdir()
    print("union_outdir",union_outdir)
    print("modify_process启动")
    excel_in_url, excel_out_url, excel_lastmonth_url, process_id = modify_process(union_outdir)
    print("modify_process完成")

    print("get_name_and_filepath启动")
    union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir = \
        get_name_and_filepath(excel_in_url, union_outdir)
    print("get_name_and_filepath完成")

    print("get_format_df启动")
    union_df, in_col, out_col = get_format_df()
    print("get_format_df完成")

    match_out_col = match_in_col = pd.DataFrame()

    if process_id == 3:
        print("第三种生成开始")

        print("得到进项表和销项表和上月剩余表的out_col和in_col")
        lastmonth_out_col, lastmonth_in_col = get_format_col(excel_lastmonth_url)
        match_out_col = get_format_col(excel_out_url)
        match_in_col = get_format_col(excel_in_url)

        print("将lastmonth_out_col和match_out_col结合")
        match_out_col = merge_col(lastmonth_out_col, match_out_col)
        match_in_col = merge_col(lastmonth_in_col, match_in_col)

        print("第三种生成完毕")

    if process_id == 2:
        print("第二种生成开始")

        print("得到临时匹配完成表的out_col和in_col")
        temp_yet_out_col, temp_yet_in_col = get_format_col(union_temp_yet_outdir)

        print("得到临时匹配剩余表的out_col和in_col")
        temp_not_out_col, temp_not_in_col = get_format_col(union_temp_not_outdir)

        print("得到填充完成表的out_col和in_col")
        filled_out_col, filled_in_col = get_format_col(union_tofill_outdir)

        # filled_out_col.to_excel("第二次生成filled_out_col.xlsx",index=False)
        # filled_in_col.to_excel("第二次生成filled_in_col.xlsx",index=False)

        # 将匹配临时完成表和匹配临时剩余表合并起来
        temp_out_col1 = merge_col(temp_yet_out_col, temp_not_out_col)
        temp_in_col1 = merge_col(temp_yet_in_col, temp_not_in_col)

        # filled_out_col.to_excel("第二次生成temp_out_col1.xlsx",index=False)
        # filled_in_col.to_excel("第二次生成temp_in_col1.xlsx",index=False)

        # 再和填充完成表合并起来
        match_out_col = merge_col(temp_out_col1, filled_out_col)
        match_in_col = merge_col(temp_in_col1, filled_in_col)
        # match_out_col.to_excel("第二次生成out.xlsx",index=False)
        # match_in_col.to_excel("第二次生成in.xlsx", index=False)
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

    print("process启动")
    if tofill_flag == 0:
        process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir)
    else:
        process(tofill_flag, union_df, match_out_col, match_in_col, in_col, out_col, union_temp_yet_outdir, union_temp_not_outdir)
    print("process完成")

    return
