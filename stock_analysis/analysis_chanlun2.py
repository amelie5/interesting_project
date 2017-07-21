from sqlalchemy import create_engine, Table, Column, MetaData, FLOAT, String, DATE, Integer, TIMESTAMP
from chanlun_util import find_peak_and_bottom, KLineDTO, fen_bi
from datetime import datetime

date = '2017-06-01'
date2 = '2017-07-20'

# 连接数据库
engine = create_engine('mysql+pymysql://root:wxj555@127.0.0.1/my_db?charset=utf8')
conn = engine.connect()

r_c = conn.execute('select code from price_amount where date=%s and code not like %s and code!=%s', date, '%300%', 'sh')
resc = r_c.fetchall()
for c in resc:
    k_line_list = []
    code = c[0]
    r = conn.execute('select date,high,low,open,close from price_amount where code=%s and date>=%s and date<=%s', code,
                     date, date2)
    res = r.fetchall()
    for x in res:
        date_time = x[0]
        open_price = x[3]
        close_price = x[4]
        high_price = x[1]
        low_price = x[2]
        k_line_dto = KLineDTO(date_time, date_time, date_time, open_price, high_price, low_price, close_price)
        k_line_list.append(k_line_dto)

    merge_line_list = find_peak_and_bottom(k_line_list, "down")
    fenbi_result, final_result_array, fenbi_seq_list = fen_bi(merge_line_list)


    # 最后的规则整合

    for i in range(len(final_result_array)):
        if final_result_array[i]:
            m_line_dto=merge_line_list[fenbi_seq_list[i]]
            if m_line_dto.is_bottom == 'Y':
                s_d=m_line_dto.begin_time
                if s_d>=datetime.strptime('2017-07-19', "%Y-%m-%d").date():
                    a = conn.execute('select close>m5 from '
                                     '(select close from price_amount where date=%s and code=%s)t1 '
                                     'INNER JOIN '
                                     '(select close as m5 from five_day_price where date=%s and code=%s)t2 '
                                     'on 1=1 ', s_d,code, s_d,code )
                    a_res = a.fetchall()
                    if(a_res[0][0]):
                        print(code+"\t"+
                          m_line_dto.begin_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                          m_line_dto.end_time.strftime('%Y-%m-%d %H:%M:%S') + "\t" +
                          "合并[" + str(m_line_dto.stick_num) + "]条K线" + "\t" +
                          "底[" + str(m_line_dto.low) + "][" + str(m_line_dto.high) + "]")