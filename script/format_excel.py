import openpyxl
from openpyxl.styles import Alignment, PatternFill


def format_excel(url):
    wb = openpyxl.load_workbook(url)
    ws = wb.active

    # 定义填充颜色
    blue_fill = PatternFill(fill_type='solid', fgColor='FFDDEBF7')
    orange_fill = PatternFill(fill_type='solid', fgColor='FFFFE699')

    # 填充A-P列为蓝色 Q-AF列为橙色
    for col in range(1, 17):
        ws.cell(row=1, column=col).fill = blue_fill
    for col in range(17, 33):
        ws.cell(row=1, column=col).fill = orange_fill

    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=16)
    ws.cell(row=1, column=1).value = "销项"
    ws.cell(row=1, column=1).fill = blue_fill
    ws.cell(row=1, column=1).alignment = Alignment(horizontal='center')

    # 合并Q-AF列，并设置文本为"进项"
    ws.merge_cells(start_row=1, start_column=17, end_row=1, end_column=32)
    ws.cell(row=1, column=17).value = "进项"
    ws.cell(row=1, column=17).fill = orange_fill
    ws.cell(row=1, column=17).alignment = Alignment(horizontal='center')

    # 定义列名列表
    column_names = ["开票日期", "序号", "发票号码", "税收分类编码", "货物、应税劳务及服务", "规格型号", "单位",
                    "上月原数量", "上月程序出库数",
                    "上月人工出库数", "本月剩余数量", "不含税单价", "不含税金额", "含税单价", "含税总金额", "销方名称",
                    "开票日期", "序号", "发票号码", "税收分类编码", "货物、应税劳务及服务", "规格型号", "单位",
                    "上月原数量", "上月程序出库数",
                    "上月人工出库数", "本月剩余数量", "不含税单价", "不含税金额", "含税单价", "含税总金额", "供应商"]
    # 设置第二行的列名
    for index, name in enumerate(column_names):
        ws.cell(row=2, column=index + 1).value = name

    bigger_columns = ['D', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'T', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AE']
    for column in bigger_columns:
        ws.column_dimensions[column].width = 15
    ws.column_dimensions['E'].width = 25
    ws.column_dimensions['AF'].width = 25

    # 保存文件
    # wb.save('union_table.xlsx')