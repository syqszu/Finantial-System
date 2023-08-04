import pandas as pd

def get_format_df():
    """
    生成临时完成表、临时剩余表、匹配完成表、匹配剩余表的统一格式的dataframe对象。
    """
    global union_yet_df, union_not_df, union_temp_not_df, union_temp_yet_df
    union_yet_df = pd.DataFrame(
        columns=['开票日期', '序号', '发票号码', '税收分类编码', '货物、应税劳务及服务', '规格型号', '单位',
                 '上月原数量', '上月程序出库数', '上月人工出库数', '本月剩余数量', '不含税单价',
                 '不含税金额', '含税单价', '含税总金额', '供应商',  # 16 销项

                 '开票日期1', '序号1', '发票号码1', '税收分类编码1', '货物、应税劳务及服务1', '规格型号1', '单位1',
                 '上月原数量1', '上月程序出库数1', '上月人工出库数1', '本月剩余数量1', '不含税单价1',
                 '不含税金额1', '含税单价1', '含税总金额1', '销方名称'  # 进项
                 ])
    union_not_df = union_yet_df.copy()  # 月匹配剩余表
    union_temp_not_df = union_yet_df.copy()  # 月临时匹配剩余表
    union_temp_yet_df = union_yet_df.copy()  # 月临时匹配完成表