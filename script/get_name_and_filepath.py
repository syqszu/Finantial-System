import os

global union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir

def get_name_and_filepath(excel_in_url, union_outdir):
    """
    通过进项文件的绝对路径和进项文件的绝对父路径，生成匹配完成表、匹配剩余表的绝对路径。
    excel_in_url:进项文件的绝对路径
    union_outdir:进项文件的绝对父路径
    :return:临时完成表、临时剩余表、待填充表、匹配完成表、匹配剩余表的绝对路径。
    """
    global union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir
    excel_in_name = os.path.basename(excel_in_url)

    # print("进项文件名字：", excel_in_name)
    month = excel_in_name[0]

    union_yet_name = month + "月匹配完成表.xlsx"
    # print(union_yet_name)
    union_not_name = month + "月匹配剩余表.xlsx"
    # print(union_not_name)
    union_tofill_name = month + "月待填充表.xlsx"
    union_temp_yet_name = month + "月临时匹配完成表.xlsx"
    union_temp_not_name = month + "月临时匹配剩余表.xlsx"

    union_not_outdir = os.path.join(union_outdir, union_not_name)
    union_yet_outdir = os.path.join(union_outdir, union_yet_name)
    union_tofill_outdir = os.path.join(union_outdir, union_tofill_name)
    union_temp_yet_outdir = os.path.join(union_outdir, union_temp_yet_name)
    union_temp_not_outdir = os.path.join(union_outdir, union_temp_not_name)

    print("union_not_outdir", union_not_outdir)
    print("union_yet_outdir", union_yet_outdir)
    print("union_tofill_outdir", union_tofill_outdir)
    print("union_temp_yet_outdir", union_temp_yet_outdir)
    print("union_temp_not_outdir", union_temp_not_outdir)

    return union_not_outdir, union_yet_outdir, union_tofill_outdir, union_temp_not_outdir, union_temp_yet_outdir