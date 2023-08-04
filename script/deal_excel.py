"""
主程序入口，不和前端联动，测试版
"""
import warnings

from script.get_format_df import get_format_df
from script.get_name_and_filepath import get_name_and_filepath
from script.pre_deal import pre_deal
from script.first_process import first_process

warnings.filterwarnings('ignore')

# 配置进项文件、销项文件还有输出文件的路径。
excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
union_outdir = r"D:\dev\ExcelUtil\temp\out"

# process_id代表第几种生成
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入有临时完成表、临时剩余表、待填充表。输出为匹配完成表+匹配剩余表。
# 第三种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。

last_month = 0
# last_month=0 表示输入没有上月剩余表，=1表示有上月剩余表
process_id = 1

if __name__ == '__main__':
    print("get_name_and_filepath启动")
    union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir = \
        get_name_and_filepath(excel_in_url, union_outdir)
    print("get_name_and_filepath完成")

    print("pre_deal启动")
    # flag=0表示生成了待填充表，flag=1表示直接生成了完成表和剩余表
    in_col, out_col, column_names, match_in_col, match_out_col, flag = \
        pre_deal(excel_in_url, excel_out_url, union_tofill_outdir)
    print("pre_deal完成")

    print("get_format_df启动")
    union_df = get_format_df()
    print("get_format_df完成")

    if process_id == 1:
        print("first_process启动")
        first_process(union_df, match_out_col, match_in_col, in_col, out_col, union_yet_outdir, union_not_outdir)
        print("first_process完成")
    # elif process_id == 2:
    #     print("second_process启动")
    #     second_process(match_out_col, match_in_col, in_col, out_col, column_names,
    #                   union_yet_outdir, union_not_outdir, union_temp_yet_outdir, union_temp_not_outdir)
    #     print("second_process完成")
    # elif process_id == 3:
    #     print("third_process启动")
    #     second_process(match_out_col, match_in_col, in_col, out_col, column_names,
    #                    union_yet_outdir, union_not_outdir, union_temp_yet_outdir, union_temp_not_outdir)
    #     print("third_process完成")


