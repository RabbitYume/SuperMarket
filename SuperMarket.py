import sqlite3
import time
import random

# 连接数据库
conn = sqlite3.connect('d:/test111.db') 


# 定义函数，def是关键字，User_Manage是函数名，()是形参列表
def User_Manage():
    while True:
        text = '''
                          欢迎光临用户管理模块     

                             1，管理员登录
                             2，会员登录
                             3，会员注册
                             4，退出    '''  # 三单引号可以定义多行文本字符串

        print (text)
        choose = input('请输入索引进行选择：')
        if choose == '1':
            Admin_Login()
        elif choose == '2':
            User_Login()
        elif choose == '3':
            User_registration()
        elif choose == '4':
            conn.close()  # conn是在主程序里定义的变量，在子函数中可以直接使用
            exit()  # 结束程序执行的内置函数
        else:
            print ('您的输入有误，请重新输入！')

def Admin_Login():
    '''
    管理员登录功能模块
    :return: None
    '''
    global currentAdmin  # 定义全局变量currentAdmin，用以保存当前登录管理员
    num = 0  # 累计密码输入次数
    while True:
        admin = input('请输入管理员名称：')
        admin_pwd = input('请输入密码：')
        # strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        if len(admin) != len(admin.strip()) or len(admin.strip().split()) != 1:
            print('登录名不能为空，且不能有空格，请重新输入！')
        else:
            cursor=conn.cursor()
            num=cursor.execute("select admin,admin_pwd from market where admin=? and admin_pwd=? and status='1'",(admin,admin_pwd)).fetchall()
            if len(num)==1:
                print('这个账号已经被锁定！')
                User_Manage()
                return
            num=cursor.execute("select admin,admin_pwd from market where admin=?",(admin,)).fetchall()
            if len(num)==0:
                print('没有这个管理员，请核对后再来！')
                User_Manage()
                return
            num=cursor.execute("select admin,admin_pwd from market where admin=? and admin_pwd=?",(admin,admin_pwd)).fetchall()
            if len(num)==0:
                print ('密码输入错误，请重新输入！')
                num=cursor.execute("update market set error=error+1 where admin=?",(admin,)) # 输错一次error+1
                num=cursor.execute("update market set status='1' where error>=3") # 输错三次锁定账号
                conn.commit()
                return
            else:
                 num=cursor.execute("select admin,admin_pwd from market where admin=? and admin_pwd=? and status='0'",(admin,admin_pwd)).fetchall()
                 if len(num)!=0:
                     print('管理员名称和密码校验成功！')
                     Admin_Main()
                     break
                 

def Admin_Main():
    '''
    管理员功能选择界面
    :return: None
    '''
    while True:
        text = '''
                                  欢迎您         

                               1，显示商品的信息
                               2，添加商品的信息
                               3，删除商品的信息
                               4, 修改商品的信息
                               5，商品销售记录
                               6，会员管理
                               7，返回登录页面
                               8，退出系统     '''
        print (text)

        # 定义Choose字典(python常用数据结构之一，字典里包含一系列的键值对)
        Choose = {'1': Goods_Show,  # :前为键，后为值，组成一组键值对
                '2': Goods_Add,
                '3': Goods_Delete,
                '4': Goods_modify,
                '5': Goods_selling,
                '6': Admin_Manage,
                '7': User_Manage,
                '8': Exit
                }
        
        choose = input('请输入索引进行选择：')

        if choose in Choose:  # 如果用户输入的是1-8（字典包含的键），则为真
            Choose[choose]()  # Choose[choose]得到对应的值（函数名）加上(),进行函数调用
        else:
            print ('您输入有误，请重新输入！')

def Goods_Show():
    '''
    展示商品模块
    '''
    while True:
        cursor=conn.cursor() # 连接数据库
        goodcursor=cursor.execute("select goods_num,goods_name,goods_stock,\
                              buyprice,sellprice from goods")
        rows = goodcursor.fetchall() # 返回元组
        for row in rows:  # 遍历
            print ('商品编号：{0}，商品名称：{1}，商品库存：{2}，商品进价：{3}元，商品卖价：{4}元'.format(row[0],row[1],row[2],row[3],row[4]))
        print ('''
                           您可以进行如下操作：
                            1，添加商品
                            2，删除商品
                            3，修改商品
                            4，返回菜单
              ''')
        while True:
            decide = input('请选择要完成的操作（1-4）：')
            if decide == '1':
                Goods_Add()
            elif decide == '2':
                Goods_Delete()
            elif decide == '3':
                Goods_modify()
            elif decide == '4':
                Admin_Main()
            else:
                print ('您的输入有误！')
                    
def Goods_Add():
    '''
    添加商品模块
    '''
    while True:
        goods_num = goods_num_input()
        if goods_num_input == None:
            return
        goods_name = goods_name_input()
        if goods_name_input == None:
            return
        goods_stock = goods_stock_input()
        if goods_stock_input == None:
            return
        sellprice = sellprice_input()
        if sellprice_input == None:
            return
        buyprice = buyprice_input()
        if buyprice_input == None:
            return
        while True:
            information = '''
                    您要添加的商品信息如下：

                    商品的编号：{0}
                    商品的名称：{1}
                    商品的库存：{2}
                    商品的进价：{3}
                    商品的售价：{4}    '''\
                    .format(goods_num,goods_name,goods_stock,buyprice,sellprice)
            print (information)
            decide = input('添加信息是否确认？（y/n）:')
            if decide == 'y':
                tm = time.localtime()  #格式化时间戳为本地时间
                year=str(tm.tm_year)
                month=str(tm.tm_mon)
                if int(month)<10:
                    month='0'+month
                day=str(tm.tm_mday) 
                if int(day)<10:
                    day='0'+day
                tm_text =year + month+ day
                print(tm_text)
                cursor=conn.cursor()  # 连接数据库
                cursor.execute("INSERT INTO goods (goods_num,goods_name,\
                goods_stock,sellprice,buyprice,tm_text) \
                VALUES (?,?,?,?,?,?)",\
                (goods_num,goods_name,goods_stock,sellprice,buyprice,tm_text))
                conn.commit() # 提交数据
                print ('添加成功！')
                cursor.close() # 关闭指针
                Goods_Show()  # 跳转商品展示页面
            elif decide == 'n':
                Admin_Main()  # 跳转管理员页面
            else:
                print ('您的输入有误，请重新输入！')

def goods_num_input():
    '''
    键盘输入商品编号
    :return: 新商品编号
    '''
    while True:
        goods_num = input('请输入商品编号(n=返回上级菜单)：')
        if goods_num == 'n':
            return
        elif len(goods_num) < 4:
            print('您输入的商品编号不能小于4位数字,请重新输入！')
        elif len(goods_num.strip().split()) != 1:
            print('您输入的商品编号不能有空格，请重新输入！')
        else:
            return goods_num

def goods_name_input():
    '''
    键盘输入商品名称
    :return:新商品名称
    '''
    while True:
        goods_name =input('请输入商品名称(n=返回上级菜单)：')
        if goods_name == 'n':
            return       
        #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        if len(goods_name) != len(goods_name.strip()) or len(goods_name.strip().split()) != 1:
            print('商品名称不能为空，且不能有空格，请重新输入！')
        else:
            cursor=conn.cursor()
            num=cursor.execute("select goods_name from goods \
                                where goods_name=?",(goods_name,)).fetchall()
            if len(num)!=0:
                print('你输入的商品名称已存在，请重新输入！')
            else:
                return goods_name  #将通过核查的商品名称作为函数返回值

def goods_stock_input():
    '''
    键盘输入商品库存
    :return: 新商品库存
    '''
    while True:
        goods_stock = input('请输入商品库存(n=返回上级菜单)：')
        if goods_stock == 'n':
            return
        # strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        elif len(goods_stock) != len(goods_stock.strip()) or len(goods_stock.strip().split()) != 1:
            print('商品库存不能为空，且不能有空格，请重新输入！')
        else:
            return goods_stock  #将通过核查的商品库存作为函数返回值

def sellprice_input():
    '''
    键盘输入商品进价
    :return: 新商品进价
    '''
    while True:
        sellprice = input('请输入商品进价(n=返回上级菜单)：')
        if sellprice == 'n':
            return
        #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        elif len(sellprice) != len(sellprice.strip()) or len(sellprice.strip().split()) != 1:
            print('商品进价不能为空，且不能有空格，请重新输入！')
        else:
            return sellprice  #将通过核查的商品进价作为函数返回值
 
def buyprice_input():
    '''
    键盘输入商品售价
    :return: 新商品售价
    '''
    while True:
        buyprice = input('请输入商品售价(n=返回上级菜单)：')
        if buyprice == 'n':
            return
        #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        elif len(buyprice) != len(buyprice.strip()) or len(buyprice.strip().split()) != 1:
            print('商品进价不能为空，且不能有空格，请重新输入！')
        else:
            return buyprice  #将通过核查的商品售价作为函数返回值

def Goods_Delete():
    '''
    删除商品模块
    '''
    id = input("请输入删除商品的编号:>>>")
    #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
    if len(id) != len(id.strip()) or len(id.strip().split()) != 1:
            print('商品编号不能为空，且不能有空格，请重新输入！')
    else:
        cursor=conn.cursor() # 连接数据库
        goodlist=cursor.execute("select goods_num,goods_name,goods_stock,\
        buyprice,sellprice from goods where goods_num=?",(id,)).fetchall() # 查询并返回元组
        cursor.close() # 关闭指针
        for row in goodlist:
            info= '''
                         商品信息如下：

                            商品编号：{0}
                            商品名称：{1}
                            商品库存：{2}
                            商品进价：{3}
                            商品售价：{4}
                    '''.format(row[0],row[1],row[2],row[3],row[4])
            print(info)
            decide = input('是否删除商品？(y/n)：')
            if decide == 'y':
                goodcursor=conn.cursor() # 连接数据库
                goodcursor.execute("delete from goods where goods_num=?",(id,)) # 根据输入的id删除
                conn.commit() # 提交数据
                num=conn.total_changes
                if num!=0:
                    print('删除成功')
                else:
                    print('删除失败，请重新操作')
                goodcursor.close()
                break
            elif decide == 'n':
                Admin_Main()
            else:
                print ('您的输入有误，请重新输入！')

def Goods_modify():
    '''
    修改商品信息模块
    '''
    while True:
        id = input('请输入要修改的商品的编号：')
        #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        if len(id) != len(id.strip()) or len(id.strip().split()) != 1:
            print('商品编号不能为空，且不能有空格，请重新输入！')
        else :
            cursor=conn.cursor() # 连接数据库
            goodlist=cursor.execute("select goods_num,goods_name,goods_stock,\
            buyprice,sellprice from goods where goods_num=?",(id,)).fetchall() # 查询并返回元组
            cursor.close() # 关闭指针
            for row in goodlist: # 遍历
                info= '''
                         商品信息如下：

                            商品编号：{0}
                            商品名称：{1}
                            商品库存：{2}
                            商品进价：{3}
                            商品售价：{4}
                    '''.format(row[0],row[1],row[2],row[3],row[4])
            print(info)
            print ('''
                           您可以进行如下操作：
                            1，修改商品编号
                            2，修改商品名称
                            3，修改商品库存
                            4，修改商品进价
                            5，修改商品售价
                            6，返回菜单
              ''')
            while True:
                decide = input('请选择要完成的操作（1-6）：')
                if decide == '1':
                    goods_num = goods_num_input()
                    if goods_num == None:
                        return
                    else:
                        goodcursor=conn.cursor() # 连接数据库
                        goodcursor.execute("update goods set goods_num=?  \
                         where goods_num=? ",(goods_num ,id))
                        conn.commit() # 提交数据
                        num=conn.total_changes
                        if num!=0:
                            print('商品编号修改成功')
                        else:
                            print('商品编号修改不成功，请重新操作')
                        goodcursor.close() # 关闭指针
                        Goods_Show() # 跳转至商品展示界面
                        break
                elif decide == '2':
                    goods_name = goods_name_input()
                    if goods_name == None:
                        return
                    else:
                        goodcursor=conn.cursor() # 连接数据库
                        goodcursor.execute("update goods set goods_name=?  \
                         where goods_num=? ",(goods_name ,id))
                        conn.commit() # 提交数据
                        num=conn.total_changes
                        if num!=0:
                            print('商品名称修改成功')
                        else:
                            print('商品名称修改不成功，请重新操作')
                        goodcursor.close() # 关闭指针
                        Goods_Show() # 跳转至商品展示界面
                        break
                elif decide == '3':
                    goods_stock = goods_stock_input()
                    if goods_stock == None:
                        return
                    else:
                        goodcursor=conn.cursor() # 连接数据库
                        goodcursor.execute("update goods set goods_stock=?  \
                         where goods_num=? ",(goods_stock ,id))
                        conn.commit() # 提交数据
                        num=conn.total_changes
                        if num!=0:
                            print('商品库存修改成功')
                        else:
                            print('商品库存修改不成功，请重新操作')
                        goodcursor.close() # 关闭指针
                        Goods_Show()
                        break
                elif decide == '4':
                    sellprice = sellprice_input() # 跳转至商品展示界面
                    if sellprice == None:
                        return
                    else:
                        goodcursor=conn.cursor() # 连接数据库
                        goodcursor.execute("update goods set sellprice=?  \
                         where goods_num=? ",(sellprice ,id))
                        conn.commit() # 提交数据
                        num=conn.total_changes
                        if num!=0:
                            print('商品进价修改成功')
                        else:
                            print('商品进价修改不成功，请重新操作')
                        goodcursor.close() # 关闭指针
                        Goods_Show() # 跳转至商品展示界面
                        break
                elif decide == '5':
                    buyprice = buyprice_input()
                    if buyprice == None:
                        return
                    else:
                        goodcursor=conn.cursor()# 连接数据库
                        goodcursor.execute("update goods set buyprice=?  \
                         where goods_num=? ",(buyprice ,id))
                        conn.commit() # 提交数据
                        num=conn.total_changes
                        if num!=0:
                            print('商品售价修改成功')
                        else:
                            print('商品售价修改不成功，请重新操作')
                        goodcursor.close() # 关闭指针
                        Goods_Show() # 跳转至商品展示界面
                        break
                elif decide == '6':
                    return
                else:
                    print ('您的输入有误！')
                        

def Goods_selling():
    '''
    销售统计模块
     统计每日各类商品销售数量、销售额&&超市日销售总额、盈利额、每位会员的消费总额
    '''
    while True:
        print ('''
                           您可以进行如下操作：
                            1，查询所有销售记录
                            2，查询每日销售
                            3，查询会员消费总额
                            4，返回菜单
              ''')
        while True:
            decide = input('请选择要完成的操作（1-4）：')
            if decide == '1':
                cursor=conn.cursor()
                usercursor=cursor.execute("select order_num,tm_text,user_login,goods_num,goods_name,buy_num,sellprice,buy_sum from shop")
                rows = usercursor.fetchall()
                for row in rows: #遍历所有订单
                    print ('订单编号：{0}，销售日期：{1}，用户：{2}，商品编号：{3}，商品名称{4}，销售数量：{5}，单价：{6}元，总额，{7}元'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
            elif decide == '2':
                tm = input("请输入查询的日期：（例20200612）")
                cursor=conn.cursor()
                usercursor=cursor.execute("select tm_text,order_num,goods_num,goods_name,buy_num,buy_sum from shop where tm_text=?",(tm,))
                rows = usercursor.fetchall()
                for row in rows: #按日期遍历
                    print ('销售日期：{0}，订单编号：{1}，商品编号：{2}，商品名称{3}，销售数量：{4}，销售额，{5}元'.format(row[0],row[1],row[2],row[3],row[4],row[5]))
                choose = input("输入y查询每日销售总额和盈利额，输入n返回菜单：")
                if choose =='y':
                    listcursor=cursor.execute("select tm_text,sum(buy_sum),sum(gain) from shop group by tm_text")
                    rows1 = listcursor.fetchall()
                    for row in rows1:  #按日期遍历
                        print ('销售日期：{0}，销售总额：{1}元，盈利额：{2}元'.format(row[0],row[1],row[2]))
                if choose == 'n':
                    Admin_Main()
                    return
            elif decide == '3':
                cursor=conn.cursor()
                usercursor=cursor.execute("select user_login,sum(buy_sum) from shop group by user_login")
                rows = usercursor.fetchall()
                for row in rows: #按会员遍历
                    print ('会员：{0}，消费总额：{1}元'.format(row[0],row[1]))
            elif decide == '4':
                Admin_Main()
                return
            else:
                print ('您的输入有误！')

def Admin_Manage():
    '''
    会员管理模块
    '''
    while True:
        cursor=conn.cursor()
        usercursor=cursor.execute("select user_num,user_login,pwd_login,\
        phone_login,level,discount,status,tm_text from market")
        rows = usercursor.fetchall()
        for row in rows:
            print ('会员卡编号：{0}，用户名：{1}，密码：{2}，手机号：{3}，\
            会员等级：{4}，会员折扣，{5}，会员卡状态{6}，注册日期：{7}'\
            .format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        print ('''
                           您可以进行如下操作：
                            1，添加会员
                            2，删除会员
                            3，修改会员资料
                            4，返回菜单
              ''')
        while True:
            decide = input('请选择要完成的操作（1-4）：')
            if decide == '1':
                User_registration()
            elif decide == '2':
                User_Delete()
            elif decide == '3':
                User_modify()
            elif decide == '4':
                Admin_Main()
            else:
                print ('您的输入有误！')

def User_Delete():
    '''
    删除会员模块
    '''
    id = input("请输入删除的会员卡编号:>>>")
    #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
    if len(id) != len(id.strip()) or len(id.strip().split()) != 1:
            print('会员卡编号不能为空，且不能有空格，请重新输入！')
    else:
        cursor=conn.cursor()
        userlist=cursor.execute("select user_num,user_login,pwd_login,phone_login,tm_text,\
        level,discount,status from market where user_num=?",(id,)).fetchall()
        cursor.close()
        for row in userlist:
            info= '''
                         会员信息如下：

                            会员卡编号：{0}
                            用户名：{1}
                            密码：{2}
                            手机号：{3}
                            注册日期：{4}
                            会员卡等级：{5}
                            会员卡折扣：{6}
                            会员卡状态：{7}
                    '''.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            print(info)
            decide = input('是否删除该会员？(y/n)：')
            if decide == 'y':
                usercursor=conn.cursor()
                usercursor.execute("delete from market where user_num=?",(id,))
                conn.commit()
                num=conn.total_changes
                if num!=0:
                    print('删除成功')
                else:
                    print('删除失败，请重新操作')
                usercursor.close()
                Admin_Manage()
                break
            elif decide == 'n':
                return
            else:
                print ('您的输入有误，请重新输入！')

def User_modify():
    '''
    修改会员信息模块
    '''
    while True:
        id = input('请输入要修改的会员卡编号：')
        #strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        if len(id) != len(id.strip()) or len(id.strip().split()) != 1:
            print('会员卡编号不能为空，且不能有空格，请重新输入！')
        else :
            cursor=conn.cursor()
            userlist=cursor.execute("select user_num,user_login,pwd_login,phone_login,tm_text,\
        level,discount,status from market where user_num=?",(id,)).fetchall()
            cursor.close()
            for row in userlist:
                info= '''
                         会员信息如下：

                            会员卡编号{0}
                            用户名：{1}
                            密码：{2}
                            手机号：{3}
                            注册日期：{4}
                            会员卡等级：{5}
                            会员卡折扣：{6}
                            会员卡状态：{7}
                    '''.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            print(info)
            print ('''
                           您可以进行如下操作：
                            1，修改会员卡编号
                            2，修改会员用户名
                            3，修改会员手机号
                            4，修改会员卡等级
                            5，修改会员卡折扣
                            6，修改会员卡状态
                            7，返回菜单
              ''')
            while True:
                decide = input('请选择要完成的操作（1-7）：')
                if decide == '1':
                    user_num = user_num_input()
                    if user_num == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set user_num=?  \
                         where user_num=? ",(user_num ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('会员卡编号修改成功')
                        else:
                            print('会员卡编号修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '2':
                    user_login = user_login_input()
                    if user_login == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set user_login=?  \
                         where user_num=? ",(user_login ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('用户名修改成功')
                        else:
                            print('用户名修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '3':
                    phone_login = phone_login_input()
                    if phone_login == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set phone_login=?  \
                         where user_num=? ",(phone_login ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('会员手机号修改成功')
                        else:
                            print('会员手机号修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '4':
                    level = level_input()
                    if level == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set level=?  \
                         where user_num=? ",(level ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('会员卡等级修改成功')
                        else:
                            print('会员卡等级修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '5':
                    discount = discount_input()
                    if discount == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set discount=?  \
                         where user_num=? ",(discount ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('会员卡折扣修改成功')
                        else:
                            print('会员卡折扣修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '6':
                    status = status_input()
                    if status == None:
                        return
                    else:
                        usercursor=conn.cursor()
                        usercursor.execute("update market set status=?  \
                         where user_num=? ",(status ,id))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('会员卡折扣修改成功')
                        else:
                            print('会员卡折扣修改不成功，请重新操作')
                        usercursor.close()
                        Admin_Manage()
                        break
                elif decide == '7':
                    return
                else:
                    print ('您的输入有误！')
    
def User_Login():
    '''
    用户登录功能模块
    :return: None
    '''
    global currentUser  # 定义全局变量currentUser，用以保存当前登录用户
    num = 0  # 累计密码输入次数
    while True:
        user_login = input('请输入用户名：')
        pwd_login = input('请输入密码：')
        if len(user_login) != len(user_login.strip()) or len(user_login.strip().split()) != 1:
            print('登录名不能为空，且不能有空格，请重新输入！')
        else:
            cursor=conn.cursor()
            num=cursor.execute("select user_login,pwd_login from market where user_login=? and pwd_login=? and status='1'",(user_login,pwd_login)).fetchall()
            if len(num)==1:
                print('这个账号已经被锁定！')
                User_Manage()
                return
            
            num=cursor.execute("select user_login,pwd_login from market where user_login=?",(user_login,)).fetchall()
            if len(num)==0:
                print('没有这个用户，请核对后再来！')
                User_Manage()
                return
            num=cursor.execute("select user_login,pwd_login from market where user_login=? and pwd_login=?",(user_login,pwd_login)).fetchall()
            if len(num)==0:
                print ('密码输入错误，请重新输入！')
                num=cursor.execute("update market set error=error+1 where user_login=?",(user_login,))
                num=cursor.execute("update market set status='1' where error>=3")
                conn.commit()
                User_Manage()
                return
            else:
                num=cursor.execute("select user_login,pwd_login from market where user_login=? and pwd_login=? and status='0'",(user_login,pwd_login)).fetchall() 
                if len(num)!=0:
                    print('名称和密码校验成功！')
                    currentUser=user_login
                    User_Main()
                    break
                
        

def User_registration():
    '''
    用户注册功能模块
    :return: None
    '''
    while True:
        user_login = user_login_input()     #得到新用户名
        if user_login == None:
            return
        pwd_login = pwd_login_input()        #得到新登录密码
        if pwd_login == None:
            return
        phone_login = phone_login_input()            #得到新手机号
        if phone_login == None:
            return
        else:
            level = 'empty'
            discount = 'empty'
        while True:
            information = '''
                    您要注册的信息如下：

                    登录用户名：{0}
                    登录的密码：{1}
                    手机号码：{2}    '''.\
            format(user_login,pwd_login,phone_login,level,discount)
            print (information)
            decide = input('注册信息是否确认？（y/n）:')
            if decide == 'y':
                tm = time.localtime()  # 格式化时间戳为本地时间
                year=str(tm.tm_year)
                month=str(tm.tm_mon)
                if int(month)<10:
                    month='0'+month
                day=str(tm.tm_mday) 
                if int(day)<10:
                    day='0'+day
                tm_text =year + month+ day
                print(tm_text)
                user_num = random.randint(0,99999)
                cursor=conn.cursor()  # 建立数据库连接
                cursor.execute("INSERT INTO market (user_login,\
                pwd_login,phone_login,level,discount,tm_text,status,user_num,error) \
                VALUES (?,?,?,?,?,?,?,?,?)",\
                (user_login,pwd_login,phone_login,0,0,tm_text,'0',user_num,'0'))
                conn.commit()
                print ('注册成功！')
                cursor.close()  # 关闭指针对象
                User_Manage()  # 跳转到用户管理页面
            elif decide == 'n':
                break
            else:
                print ('您的输入有误，请重新输入！')
                
def user_num_input():
    '''
    键盘输入会员卡编号
    :return: 新会员卡编号
    '''
    while True:
        user_num = input('请输入会员卡编号(n=返回上级菜单)：')
        if user_num == 'n':
            return
        elif len(user_num.strip().split()) != 1:
            print('您输入的会员卡编号不能有空格，请重新输入！')
        else:
            return user_num

def user_login_input():
    '''
    键盘输入登录名
    :return:新用户名
    '''
    while True:
        user_login =input('请输入登陆用户的用户名(n=返回上级菜单)：')
        if user_login == 'n':
            return
        
        # strip()去除字符串首尾的空白，split()分割字符串(默认按空格分割)
        if len(user_login) != len(user_login.strip()) or len(user_login.strip().split()) != 1:
            print('登录名不能为空，且不能有空格，请重新输入！')
        else:
            cursor=conn.cursor()  #建立数据库连接
            num=cursor.execute("select user_login,pwd_login from market \
                                where user_login=?",(user_login,)).fetchall()
            if len(num)!=0:
                print('你输入的用户名已存在，请重新输入！')
            else:
                return user_login  # 将通过核查的用户名作为函数返回值
            

def pwd_login_input():
    '''
    键盘输入登录密码
    :return:新登录密码
    '''
    while True:
        pwd_login = input('请输入登陆密码(n=返回上级菜单)：')
        if pwd_login == 'n':
            return
        elif len(pwd_login) < 8:
            print('您输入的密码不能小于8位数（8位以上字母数字+至少一位大写字母组合）,请重新输入！')
        elif len(pwd_login.strip().split()) != 1:
            print('您输入的密码不能有空格，密码也不能为空，请重新输入！')
        elif pwd_login.isdigit():
            print('密码不能全为数字（8位以上字母数字+至少一位大写字母组合），请重新输入！')
        elif pwd_login.lower() == pwd_login:
            print('请至少保留一位的大写字母（8位以上字母数字+至少一位大写字母组合），请重新输入！')
        else:
            return pwd_login


def phone_login_input():
    '''
    键盘输入手机号
    :return: 新手机号
    '''
    while True:
        phone_login = input('请输入手机号(如果没有可以为空)\
        (n=返回上级菜单)：')
        if phone_login.strip() == '':
            phone_login = 'empty'
            return phone_login
        elif phone_login == 'n':
            return
        elif len(phone_login.strip()) < 11:
            print('手机号是不能小于11位的纯数字，请重新输入！')
        elif phone_login.isdigit() != True:
            print('手机号是不能小于11位的纯数字，请重新输入！')
        else:
            return phone_login
        
def level_input():
    '''
    键盘输入会员卡等级
    :return: 新会员卡等级
    '''
    while True:
        level = input('请输入会员卡等级(n=返回上级菜单)：')
        if level == 'n':
            return
        elif len(level.strip().split()) != 1:
            print('您输入的等级不能有空格也不能为空，请重新输入！')
        else:
            return level

def discount_input():
    '''
    键盘输入会员卡折扣
    :return: 新会员卡折扣
    '''
    while True:
        discount = input('请输入会员卡折扣(n=返回上级菜单)：')
        if discount == 'n':
            return
        elif len(discount.strip().split()) != 1:
            print('您输入的会员卡折扣不能有空格也不能为空，请重新输入！')
        else:
            return discount

def status_input():
    '''
    键盘输入会员卡状态
    :return: 新会员卡状态
    '''
    while True:
        status = input('请输入会员卡状态(n=返回上级菜单)：')
        if status == 'n':
            return
        elif len(status.strip().split()) != 1:
            print('您输入的会员卡状态不能有空格也不能为空，请重新输入！')
        else:
            return status

def User_Main():
    '''
    用户功能选择界面
    :return: None
    '''
    while True:
        text = '''
                             欢迎光临会员制超市         

                               1，个人信息
                               2，购物
                               3，查询账单
                               4，退出系统     '''
        print (text)

        # 定义Choose字典(python常用数据结构之一，字典里包含一系列的键值对)
        Choose = {'1': User_information,
                '2': User_Shopping,
                '3': Select_Billing,
                '4': Exit
                }
        
        choose = input('请输入索引进行选择：')

        if choose in Choose:  # 如果用户输入的是1-4（字典包含的键），则为真
            Choose[choose]()  # Choose[choose]得到对应的值（函数名）加上(),进行函数调用
        else:
            print ('您输入有误，请重新输入！')
            

def User_information():
    '''
        个人信息查询模块
    :return:None
    '''
    global conn
    while True:
        if currentUser=='':
            print('您尚未登录，请先登录后再操作')
            return
        cursor=conn.cursor()
        mylist=cursor.execute("select * from market \
            where user_login=?",(currentUser,)).fetchall()  # fetchall将游标查询结果集的所有记录取出为二维元组列表
        cursor.close()
        for row in mylist:
            if row[2]=='empty':
                labb = '未绑定'
            else:
                labb='已绑定'
            text = '''
                         您的个人注册信息如下：

                            会员卡编号：{0}
                            用户名：{1}
                            手机号：{2}
                            注册时间：{3}
                            会员卡等级：{4}
                            会员卡折扣：{5}
                    '''.format(row[7],row[0],row[2],row[3],row[6],row[4])
            print(text)
            print ('''
                           您可以进行如下操作：
                            1，修改登录密码
                            2，绑定手机号
                            3，返回菜单
              ''')
            while True:
                decide = input('请选择要完成的操作（1-3）：')
                if decide == '1':
                    pwd_login = pwd_login_input()
                    if pwd_login == None:
                        return
                    else:
                        mycursor=conn.cursor()
                        mycursor.execute("update market set pwd_login=?  \
                         where user_login=? ",(pwd_login ,currentUser))
                        conn.commit()
                        num=conn.total_changes
                        if num!=0:
                            print('登录密码修改成功')
                        else:
                            print('登录密码修改不成功，请重新操作')
                        mycursor.close()
                        break
                    
                elif decide == '2':
                    if  labb=='已绑定':
                        print ('您已经绑定过手机号了！不能再次绑定！')
                        break
                    else:
                        phone_login = phone_login_input()
                        if phone_login == None:
                            return
                        else:
                            mycursor=conn.cursor()
                            mycursor.execute(" update market set phone_login=?  \
                            where user_login=?",(phone_login ,currentUser))
                            conn.commit()              
                            num=conn.total_changes
                            if num!=0:
                                print ('手机号绑定成功！')
                            else:
                                print ('手机号绑定不成功，请重新操作！')
                            mycursor.close()
                            break

                elif decide == '3':
                    return
                else:
                    print ('您的输入有误！')

def User_Shopping():
    '''
    用户购物模块
    :return:
    '''
    global conn
    while True:
        if currentUser=='':
            print('您尚未登录，请先登录后再操作')
            return
        cursor=conn.cursor()
        mylist=cursor.execute("select * from market \
            where user_login=?",(currentUser,)).fetchall()  # fetchall将游标查询结果集的所有记录取出为二维元组列表
        print("商品列表：")
        goodcursor=cursor.execute("select goods_num,goods_name,goods_stock,\
                              sellprice from goods")
        rows = goodcursor.fetchall()
        for row in rows:  #遍历
            print ('商品编号：{0}，商品名称：{1}，商品库存：{2}，商品价格：{3}元'\
                   .format(row[0],row[1],row[2],row[3]))
        print ('''
                           您可以进行如下操作：
                            1，输入编号和购买数量选购商品
                            2，返回菜单
              ''')
        while True:
                decide = input('请选择要完成的操作（1-2）：')
                if decide == '1':
                    cursor=conn.cursor()
                    goods_num = int(input('请输入要购买的商品编号：'))
                    if goods_num == None:
                        return
                    goods_name_list=cursor.execute("select goods_name from goods where goods_num=?",(goods_num,)).fetchone()
                    goods_name=str(goods_name_list)
                    sellprice_list=cursor.execute("select sellprice from goods where goods_num=?",(goods_num,)).fetchone()
                    sellprice=int(max(sellprice_list))
                    buy_num = int(input('请输入要购买的商品数量：'))
                    if buy_num == None:
                        return
                    buy_sum = buy_num * sellprice
                    while True:
                         information = '''
                                您要购买的商品信息如下：

                                商品的编号：{0}
                                商品的名称：{1}
                                商品的数量：{2}
                                商品的单价：{3} 元
                                总额：{4} 元    '''\
                                .format(goods_num,goods_name,buy_num,sellprice,buy_sum)
                         print (information)
                         while True:
                             decide = input('是否购买？（y/n）:')
                             if decide == 'y':
                                 cursor=conn.cursor()
                                 tm = time.localtime()  # 格式化时间戳为本地时间
                                 year=str(tm.tm_year)
                                 month=str(tm.tm_mon)
                                 if int(month)<10:
                                     month='0'+month
                                     day=str(tm.tm_mday) 
                                 if int(day)<10:
                                     day='0'+day
                                 tm_text =year + month+ day
                                 order_num = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-5:]
                                 cursor.execute("INSERT INTO shop (goods_num,goods_name,buy_num,sellprice,buy_sum,order_num,user_login,tm_text) \
                                   VALUES (?,?,?,?,?,?,?,?)",(goods_num,goods_name,buy_num,sellprice,buy_sum,order_num,currentUser,tm_text))
                                 goods_stock_list=cursor.execute("select goods_stock from goods where goods_num=?",(goods_num,)).fetchone()
                                 goods_stock=int(max(goods_stock_list))-buy_num
                                 cursor.execute("update goods set goods_stock=? where goods_num=?",(goods_stock,goods_num))
                                 buyprice=int(max(cursor.execute("select buyprice from goods where goods_num=?",(goods_num,)).fetchone()))
                                 gain=buy_sum - buyprice
                                 cursor.execute("update shop set gain=? where goods_num=?",(gain,goods_num))
                                 conn.commit()
                                 print ('成功购买！')
                                 cursor.close()
                                 User_Main()
                             elif decide == 'n':
                                 User_Main()  #跳转管理员页面
                                 return
                elif decide == '2':
                    User_Main()
                    return
                else:
                    print ('您的输入有误！')

def buy_num_input():
    '''
    键盘输入购买商品数量
    :return: 购买商品的数量
    '''
    while True:
        buy_num = input('请输入要购买的商品数量(n=返回上级菜单)：')
        if buy_num == 'n':
            return
        elif len(buy_num.strip().split()) != 1:
            print('您输入的商品数量不能有空格也不能为空，请重新输入！')
        else:
            return buy_num

def Select_Billing(log = None):
    '''
    用户账单查询模块
    :return:
    '''
    while True:
        if currentUser=='':
            print('您尚未登录，请先登录后再操作')
            return
        cursor=conn.cursor()
        listcursor=cursor.execute("select order_num,goods_num,goods_name,buy_num,sellprice,buy_sum,tm_text from shop where user_login=?",(currentUser,))
        rows = listcursor.fetchall()
        for row in rows:  #遍历
            print ('订单编号：{0}，商品编号：{1}，商品名称：{2}，购买数量：{3}，商品单价：{4}元，总额：{5}元，购买日期：{6}'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            while True:
                decide = input('输入n返回菜单：')
                if decide == 'n':
                    User_Main()
                    break
                else:
                    print ('您的输入有误！')
                    return

def Exit():
    '''
        系统退出
    :return:None
    '''
    print ('程序退出！')
    exit()


# 脚本程序执行的入口
if __name__ == '__main__':
    User_Manage()
