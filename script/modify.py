import os

def set_union_outdir(dir):
    global union_outdir
    print("进入process_union_outdir")
    union_outdir =  dir

def get_union_outdir():
    return union_outdir

def modify_process(dir):
    excel_in_url = r"D:\dev\ExcelUtil\temp\3月份进项.xlsx"
    excel_out_url = r"D:\dev\ExcelUtil\temp\3月份销项.xlsx"
    excel_lastmonth_url = r"D:\dev\ExcelUtil\temp\2月匹配剩余表.xlsx"
    process_id = 0

    file_list = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append((file, file_path))

    for file_name, file_path in file_list:
        if "进项.xlsx" in file_name:
            excel_in_url = file_path
        if "销项.xlsx" in file_name:
            excel_out_url = file_path
        if "月匹配剩余表.xlsx" in file_name:
            excel_lastmonth_url = file_path

    if len(file_list) == 2:
        process_id = 1
    elif len(file_list) == 3:
        for file_name, file_path in file_list:
            if "临时" in file_name:
                process_id =  2
                break
            process_id =  3
    print("process_id",process_id)

    return excel_in_url, excel_out_url, excel_lastmonth_url, process_id