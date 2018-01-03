import pymysql
import xlrd
import xlwt

"""
说明: 通过关联查询mysql,将查得的结果写入excel
主要是使用pymysql操作mysql数据库
"""

HOST = '192.168.1.198'
DB = 'featurefactory'
USERNAME = 'dev'
PWD = '123456'

conn = pymysql.connect(host=HOST, user=USERNAME, passwd=PWD, db=DB, charset='utf8')

# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cur = conn.cursor()

wb = xlwt.Workbook()
ws = wb.add_sheet('export_result')
ws.write(0, 0, u'序号')
ws.write(0, 1, u'姓名')
ws.write(0, 2, u'身份证')
ws.write(0, 3, u'审批结果')
ws.write(0, 4, u'拒绝原因')
ws.write(0, 5, u'返回码')

sql = "SELECT a.applicant_name, a.applicant_id_card, a.execution_msg, a.reject_reason, a.apply_id from " \
      "applicant_execution_record_list a WHERE a.execution_msg IN ('建议拒绝', '存在风险');"
sql2 = "SELECT result_code from formal_rule_execution_record WHERE apply_id = %s AND execution_status in (2,3,4) "
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    for i, row in enumerate(result):
        cur.execute(sql2, row[4])
        result_code = cur.fetchall()
        result_code = [i[0] for i in result_code if i[0] is not None]
        print(result_code)
        ws.write(i+1, 0, i + 1)
        ws.write(i+1, 1, row[0])
        ws.write(i+1, 2, row[1])
        ws.write(i+1, 3, row[2])
        ws.write(i+1, 4, row[3])
        ws.write(i+1, 5, result_code)

except Exception as e:
    print(e)

finally:
    wb.save("reslt.xls")
    cursor.close()
    cur.close()
    conn.close()


