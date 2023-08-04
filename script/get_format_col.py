import pandas as pd


# 将表格的数据提取成match_in_col和match_out_col的形式

def get_format_col(url):
    if "待填充表" in url:
        # 将待填充表的数据提取成filled_in_col和filled_out_col
        df = pd.read_excel(url)
        filled_in_col = pd.DataFrame()
        filled_out_col = pd.DataFrame()
        for index, row in df.iterrows():
            if row['from'] == 'in':
                filled_in_col = filled_in_col.append(row)
            elif row['from'] == 'out':
                filled_out_col = filled_out_col.append(row)
        return filled_out_col, filled_out_col

    if "月匹配剩余表" in url:
        # 将上月匹配剩余表的数据提取成filled_in_col和filled_out_col
        df = pd.read_excel(url)
        lastmonth_in_col = pd.DataFrame()
        lastmonth_out_col = pd.DataFrame()
        for index, row in df.iterrows():
            if row['开票日期1']:
                # 说明该行数据是销项
                lastmonth_out_col = lastmonth_out_col.append(row[0:19])
            elif row['from'] == 'out':
                lastmonth_in_col = lastmonth_in_col.append(row[19:35])
        lastmonth_out_col = lastmonth_out_col.raname(
            columns={"本月剩余数量": "数量", "不含税单价": "单价", "不含税金额": "金额", "供应商": "购方名称"})
        lastmonth_out_col = lastmonth_out_col.drop(["上月原数量", "上月程序出库数", "上月人工出库数"], axis=1)
        return lastmonth_out_col, lastmonth_in_col
