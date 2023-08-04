"""
该函数是用来判断第几次生成的。返回process_id。
# 第一种生成，输入只有进项表和销项表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
# 第二种生成，输入有临时完成表、临时剩余表、待填充表。输出为匹配完成表+匹配剩余表。
# 第三种生成，输入为进项表、销项表、上月剩余表。输出有两种可能。1、临时完成表+临时剩余表+待填充表。2、匹配完成表+匹配剩余表。
"""
def judge_process_id(file_names):
    if len(file_names) == 2:
        return 1
    elif len(file_names) == 3:
        for filename in file_names:
            if "临时" in filename:
                return 2
        return 3