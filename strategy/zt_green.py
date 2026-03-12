import pandas as pd
import logging


# 判断是否满足特定模式的函数
def check(code_name, data, end_date=None, threshold=60):
    # 确保数据按日期排序
    data = data.sort_values(by='日期')

    if end_date is not None:
        mask = (data['日期'] <= end_date)
        data = data.loc[mask]

    data = data.tail(n=threshold)

    if len(data) < threshold:
        logging.debug(f"{code_name}:样本小于{threshold}天...\n")
        return False

    for i in range(len(data) - 1):
        # 第一天涨停判断
        if data.iloc[i]['p_change'] >= 9.9:

            # 第二天收绿或开盘价高于收盘价判断
            if data.iloc[i + 1]['p_change'] < 0 or data.iloc[i + 1]['开盘'] > data.iloc[i + 1]['收盘']:

                # 成交量放大倍数判断
                if (data.iloc[i]['成交量'] >= 2 * data['成交量'].mean()) and (
                        data.iloc[i + 1]['成交量'] >= 2 * data['成交量'].mean()):

                    # 涨停前短期涨幅判断
                    start_date_zt = data.iloc[i]['日期']
                    before_zt_data = data[data['日期'] < start_date_zt]
                    before_zt_data = before_zt_data.tail(15)
                    max_gain = (before_zt_data['收盘'].max() - before_zt_data['收盘'].min()) / before_zt_data[
                        '收盘'].min()
                    if max_gain <= 0.4:
                        return True

    return False