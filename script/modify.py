import os

def set_union_outdir(dir):
    global union_outdir
    print("进入process_union_outdir")
    union_outdir =  dir

def get_union_outdir():
    return union_outdir


# process_id代表第几种生成
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
def modify_process(dir):
    """
    # 1、配置进销项、上月剩余匹配文件的地址 2、配置进销项、匹配剩余表的文件路径 3、判断process_id
    :param dir:
    :return:
    """
    excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
    excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
    excel_lastmonth_url = r"D:\dev\ExcelUtil\temp\2月匹配剩余表.xlsx"

    # 获取输出文件夹下的所有内容
    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append((file, file_path))

    # 配置进销项、匹配剩余表的文件路径
    for file_name, file_path in file_list:
        if "进项.xlsx" in file_name:
            excel_in_url = file_path
            month = file_name[0]
        if "销项.xlsx" in file_name:
            excel_out_url = file_path
        if "月匹配剩余表.xlsx" in file_name:
            excel_lastmonth_url = file_path

    # 生成匹配完成表、匹配剩余表和填充指引文件的绝对路径。
    union_yet_name = month + "月匹配完成表.xlsx"
    union_not_name = month + "月匹配剩余表.xlsx"
    union_tofill_name = "填充指引文件"
    union_not_outdir = os.path.join(union_outdir, union_not_name)
    union_yet_outdir = os.path.join(union_outdir, union_yet_name)
    union_tofill_outdir = os.path.join(union_outdir, union_tofill_name)

    # 判断process_id
    if len(file_list) == 2:
        process_id = 1
    else:
        process_id = 2

    return excel_in_url, excel_out_url, excel_lastmonth_url, process_id, union_not_outdir, union_yet_outdir, union_tofill_outdir