import pandas as pd
import os
import execjs

# 将表格的数据提取成match_in_col和match_out_col的形式

def get_format_col(url):

    if ("月匹配剩余表" in url) or ("月匹配完成表" in url):

        # 将数据提取成filled_in_col和filled_out_col
        df = pd.read_excel(url, skiprows=1)
        # print("df.columns")
        # print(df.columns)

        if os.path.exists(url):
            os.remove(url)
            print("匹配表删除成功")
        else:
            print("匹配表不存在")

        lastmonth_in_col = pd.DataFrame(columns=df.columns[18:36])
        lastmonth_out_col = pd.DataFrame(columns=df.columns[0:18])

        if ("月临时匹配完成表" in url):
            for index, row in df.iterrows():
                if index>=1:
                    lastmonth_in_col = lastmonth_in_col.append(row[18:36])
                    lastmonth_out_col = lastmonth_out_col.append(row[0:18])

        else:
            for index, row in df.iterrows():
                if pd.isna(row[0]):
                    lastmonth_in_col = lastmonth_in_col.append(row[18:36])
                else:
                    lastmonth_out_col = lastmonth_out_col.append(row[0:18])


        # print("改名前")
        # print("out.columns")
        # print(lastmonth_out_col.columns)
        #
        # print("in.columns")
        # print(lastmonth_in_col.columns)

        lastmonth_out_col = lastmonth_out_col.rename(
            columns={"本月剩余数量": "数量", "不含税单价": "单价", "不含税金额": "金额","含税总金额":"价税合计", "供应商": "购方名称"})
        lastmonth_out_col = lastmonth_out_col.drop(["上月原数量", "上月程序出库数", "上月人工出库数"], axis=1)

        lastmonth_in_col = lastmonth_in_col.rename(
            columns={"开票日期1": "开票日期", "发票号码1": "发票号码", "税收分类编码1": "税收分类编码",
                     "规格型号1": "规格型号", "单位1": "单位", "货物、应税劳务及服务1":"货物、应税劳务及服务",
                     "本月剩余数量1": "数量", "不含税单价1": "单价", "税率1": "税率", "含税单价1": "含税单价",
                     "含税总金额1": "价税合计",
                     "不含税金额1": "金额"})
        lastmonth_in_col = lastmonth_in_col.drop(["上月原数量1", "上月程序出库数1", "上月人工出库数1"], axis=1)

        # print("改名后")
        # print("out.columns")
        # print(lastmonth_out_col.columns)
        #
        # print("in.columns")
        # print(lastmonth_in_col.columns)

        return lastmonth_out_col, lastmonth_in_col

    if "进项.xlsx" in url:
        in_col = ["税收分类编码", "发票号码", "开票日期", "销方名称", "货物、应税劳务及服务", "规格型号", "数量", "单价",
                  "单位", "金额", "税率", "价税合计"]
        print("开始处理进项表格")
        # 从第二行开始读取，且跳过最后一行，因为是“总计”
        df_in = pd.read_excel(url, "Sheet1", header=1, skipfooter=1)
        # print(df_in.tail(1))


        # 从文件中读取 JavaScript 代码
        with open('../static/if_tofill.js', 'r') as f:
            js_code = f.read()
        # 编译并加载 JavaScript 代码
        ctx = execjs.compile(js_code)
        # 调用 JavaScript 中的函数
        result = ctx.call('if_tofill')



        if os.path.exists(url):
            os.remove(url)
            print("进项表删除成功")
        else:
            print("进项表不存在")

        match_in_col = df_in[in_col]
        return match_in_col

    if "销项.xlsx" in url:
        out_col = ["税收分类编码", "发票号码", "开票日期", "购方名称", "货物、应税劳务及服务", "规格型号", "数量",
                   "单价", "单位", "金额", "税率", "价税合计", "备注"]
        print("开始处理销项表格")
        # 从第三行开始读取，且跳过最后一行，因为是“总计”
        df_out = pd.read_excel(url, "Sheet1", header=2, skipfooter=1)
        # print(df_out.tail(1))

        match_out_col = df_out[out_col]

        if os.path.exists(url):
            os.remove(url)
            print("销项表删除成功")
        else:
            print("销项表不存在")
        return match_out_col
