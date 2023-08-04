"""
主程序入口，不和前端联动，测试版
"""

import pandas as pd
import warnings

from script.get_name_and_filepath import get_name_and_filepath
from script.pre_deal import pre_deal
from script.first_process import first_process

warnings.filterwarnings('ignore')

global excel_in_url, excel_out_url, excel_tofill_url, union_outdir, union_not_outdir, union_yet_outdir, union_tofill_outdir, \
    match_out_col, match_in_col, temp_col, union_yet_df, union_not_df, union_temp_not_outdir, union_temp_yet_outdir, \
    in_col, out_col

# 配置进项文件、销项文件还有输出文件的路径。
excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
union_outdir = r"D:\dev\ExcelUtil\temp\out"
temp_col = pd.DataFrame()

if __name__ == '__main__':

    print("get_name_and_filepath启动")
    get_name_and_filepath(excel_in_url, union_outdir)
    print("get_name_and_filepath完成")

    print("pre_deal启动")
    pre_deal(excel_in_url, excel_out_url, union_tofill_outdir)
    print("pre_deal完成")

    print("first_process启动")
    first_process(match_out_col, match_in_col, in_col, out_col)
    print("first_process完成")

