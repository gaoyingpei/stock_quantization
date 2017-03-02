import tushare as ts
import pymongo
import json
import os
from sqlalchemy import create_engine

comprehensive = ts.get_k_data('600000', ktype='5') #获取k线数据
print(comprehensive)

data = ts.get_hist_data('600848') #一次性获取全部日k线数据
print(data)

fq = ts.get_stock_basics() #获取历史复权数据，接口提供股票上市以来所有历史数据
print(fq)
onlinedate = fq.ix['600848']['timeToMarket'] #上市日期YYYYMMDD
print(onlinedate)

test = ts.get_h_data('002337', start='2015-03-01', end='2015-03-10') #两个日期之间的前复权数据
print(test)

allStock = ts.get_today_all() #一次性获取当前交易所有股票的行情数据
print(allStock)

history = ts.get_tick_data('600848',date='2014-01-09') #获取个股以往交易历史的分笔数据明细
history.head(10)
print(history)

today = ts.get_today_ticks('601333') #获取当前交易日（交易进行中使用）已经产生的分笔明细数据
today.head(10)
print(today)

df = ts.get_realtime_quotes('000581') #获取实时分笔数据
print(df[['code','name','price','bid','ask','volume','amount','time']])
szzs = ts.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb']) #上证指数 深圳成指 沪深300指数 上证50 中小板 创业板
print(szzs)

dp = ts.get_index() #大盘指数实时行情
print(dp)

ds = ts.get_sina_dd('002379', date='2015-12-24', vol=500)  #指定大于等于500手的数据
print(ds)

share = ts.profit_data(top=60) #上市公司利润分配预案
share.sort('shares',ascending=False)
print(share)
print(share[share.shares>=10]) #每10股送转在10以上

predict = ts.forecast_data(2016,4) #按年度、季度获取业绩预告数据
print(predict)

forbid = ts.xsg_data() #以月的形式返回限售股解禁情况
print(forbid)

jjcg = ts.fund_holdings(2014, 4) #获取每个季度基金持有上市公司股票的数据
print(jjcg)

newstock = ts.new_stocks() #获取IPO发行和上市的时间列表
print(newstock)

rzrqsh = ts.sh_margins(start='2015-01-01', end='2015-04-19') #沪市的融资融券数据从上海证券交易所网站直接获取，提供了有记录以来的全部汇总和明细数据
print(rzrqsh)
rzshdetail = ts.sh_margin_details(start='2015-01-01', end='2015-04-19', symbol='601989') #沪市融资融券明细数据
print(rzshdetail)

rzrqsz = ts.sz_margins(start='2015-01-01', end='2015-04-19') #深市的融资融券数据从深圳证券交易所网站直接获取，提供了有记录以来的全部汇总和明细数据
print(rzrqsz)
rzszdetail = ts.sz_margin_details('2015-04-20') #深市融资融券明细数据
print(rzszdetail)

ic = ts.get_industry_classified() #行业分类
print(ic)

concept = ts.get_concept_classified() #概念分类
print(concept)

area = ts.get_area_classified() #地域分类
print(area)

sme = ts.get_sme_classified() #中小板
print(sme)

gem = ts.get_gem_classified() #创业板
print(gem)

st = ts.get_st_classified() #风险警示板
print(st)

hs300 = ts.get_hs300s() #沪深300当前成份股及所占权重
print(hs300)

sz50 = ts.get_sz50s() #上证50成份股
print(sz50)

zz500 = ts.get_zz500s() #中证500成份股
print(zz500)

terminal = ts.get_terminated() #已经被终止上市的股票列表
print(terminal)

suspend = ts.get_suspended() #被暂停上市的股票列表
print(suspend)

stocks = ts.get_stock_basics() #获取沪深上市公司基本情况
print(stocks)

content = ts.get_report_data(2014,3) #获取2014年第3季度的业绩报表数据
print(content)

profit = ts.get_profit_data(2014,3) #获取2014年第3季度的盈利能力数据
print(profit)

operation = ts.get_operation_data(2014,3) #获取2014年第3季度的营运能力数据
print(operation)

growth = ts.get_growth_data(2014,3) #获取2014年第3季度的成长能力数据
print(growth)

debtpay = ts.get_debtpaying_data(2014,3) #获取2014年第3季度的偿债能力数据
print(debtpay)

cashflow = ts.get_cashflow_data(2014,3) #获取2014年第3季度的现金流量数据
print(cashflow)

deposit = ts.get_deposit_rate() #存款利率
print(deposit)

loan = ts.get_loan_rate() #贷款利率
print(loan)

rrr = ts.get_rrr() #存款准备金率
print(rrr)

supply = ts.get_money_supply() #货币供应量
print(supply)

supplyBal = ts.get_money_supply_bal() #货币供应量(年底余额)
print(supplyBal)

GDP = ts.get_gdp_year() #GDP
print(GDP)

gdpquarter = ts.get_gdp_quarter() #GDP(季度)
print(gdpquarter)

sx = ts.get_gdp_for() #三大需求(出口，投资，消费)对GDP贡献
print(sx)

sc = ts.get_gdp_pull() #三大产业对GDP拉动
print(sc)

scg = ts.get_gdp_contrib() #三大产业贡献率
print(scg)

cpi = ts.get_cpi() #居民消费价格指数
print(cpi)

ppi = ts.get_ppi() #工业品出厂价格指数
print(ppi)

news = ts.get_latest_news(top=5,show_content=True) #显示最新5条新闻，并打印出新闻内容
print(news)

notice = ts.get_notices() #获取个股信息地雷数据
print(notice)

gb = ts.guba_sina(True) #新浪股吧
print(gb)

topList = ts.top_list('2015-06-12') #按日期获取历史当日上榜的个股数据
print(topList)

capTop = ts.cap_tops() #获取近5、10、30、60日个股上榜统计数据
print(capTop)

broker = ts.broker_tops() #获取营业部近5、10、30、60日上榜次数、累积买卖等情况
print(broker)

inst = ts.inst_tops() #机构席位追踪
print(inst)

instDetail = ts.inst_detail() #获取最近一个交易日机构席位成交明细统计数据
print(instDetail)

shibor = ts.shibor_data() #获取银行间同业拆放利率数据
print(shibor.sort('date', ascending=False).head(10))

bank = ts.shibor_quote_data() #银行报价数据
print(bank.sort('date', ascending=False).head(10))

shiborMa = ts.shibor_ma_data(2014) #Shibor均值数据
print(shiborMa)

loadRate = ts.lpr_data() #贷款基础利率
print(loadRate)

lrma = ts.lpr_ma_data() #贷款基础利率均值
print(lrma)


data = ts.get_hist_data('000875')
data.to_csv('D:/Python/test/000875.csv') #直接保存CSV
data.to_csv('D:/Python/test/000875.csv',columns=['open','high','low','close']) #选择保存CSV
def insertCsv():
	filename = 'D:/Python/test/bigfile.csv'
	for code in ['000875', '600848', '000981']:
	    df = ts.get_hist_data(code)
	    if os.path.exists(filename):
	        df.to_csv(filename, mode='a', header=None)
	    else:
	        df.to_csv(filename)


excel = ts.get_hist_data('000875')
excel.to_excel('D:/Python/test/000875.xlsx') #直接保存EXCEL
excel.to_excel('D:/Python/test/000875.xlsx', startrow=2,startcol=5) #EXCEL设定数据位置（从第3行，第6列开始插入数据）


hdf = ts.get_hist_data('000875')
hdf.to_hdf('D:/Python/test/hdf.h5','000875') #保存为HDF5格式


json = ts.get_hist_data('000875')
json.to_json('D:/Python/test/000875.json',orient='records') #保存为JSON格式


mysql = ts.get_tick_data('600848', date='2014-12-22')
engine = create_engine('mysql://user:passwd@127.0.0.1/db_name?charset=utf8') #链接数据库
mysql.to_sql('tick_data',engine) #存入数据库
mysql.to_sql('tick_data',engine,if_exists='append') #追加数据到现有表


conn = pymongo.Connection('127.0.0.1', port=27017) #链接mongodb
mongo = ts.get_tick_data('600848',date='2014-12-22')
conn.db.tickdata.insert(json.loads(mongo.to_json(orient='records')))


pf = ts.realtime_boxoffice() #电影票房
print(pf)

dpf = ts.day_boxoffice('2015-12-24') #当日电影票房
print(dpf)

mpf = ts.month_boxoffice('2015-10') #取2015年10月的数据
print(mpf)

cinema = ts.day_cinema('2017-02-25') #取指定日期的影院票房
print(cinema)


def get_all_price():  
    '''''process all stock'''  
    STOCK = ['600219',       ##南山铝业  
             '000002',       ##万  科Ａ  
             '000623',       ##吉林敖东  
             '000725',       ##京东方Ａ  
             '600036',       ##招商银行  
             '601166',       ##兴业银行  
             '600298',       ##安琪酵母  
             '600881',       ##亚泰集团  
             '002582',       ##好想你  
             '600750',       ##江中药业  
             '601088',       ##中国神华  
             '000338',       ##潍柴动力  
             '000895',       ##双汇发展  
             '000792']       ##盐湖股份  
    df = ts.get_realtime_quotes(STOCK)  
    print(df)

#简易量化模型
def parse(code_list):  
    '''''process stock'''  
    is_buy    = 0  
    buy_val   = []  
    buy_date  = []  
    sell_val  = []  
    sell_date = []  
    df = ts.get_hist_data(STOCK)  
    ma20 = df[u'ma20']  
    close = df[u'close']  
    rate = 1.0  
    idx = len(ma20)  
  
    while idx > 0:  
        idx -= 1  
        close_val = close[idx]  #当日收盘价
        ma20_val = ma20[idx]  	#20日线
        if close_val > ma20_val:  
                if is_buy == 0:  #之前没有买入
                        is_buy = 1  #买入
                        buy_val.append(close_val)  
                        buy_date.append(close.keys()[idx])  
        elif close_val < ma20_val:  
                if is_buy == 1:  
                        is_buy = 0  #卖出
                        sell_val.append(close_val)  
                        sell_date.append(close.keys()[idx])  
  
    print("stock number: %s" %STOCK)
    print("buy count   : %d" %len(buy_val))  
    print("sell count  : %d" %len(sell_val))  
  
    for i in range(len(sell_val)):  
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i]) #印花税
        print("buy date : %s, buy price : %.2f" %(buy_date[i], buy_val[i]))
        print("sell date: %s, sell price: %.2f" %(sell_date[i], sell_val[i]))
  
    print("rate: %.2f" % rate) 


#通联接口
ts.set_token('466a9d168864270832cf5a495de9d9179b893b8b14abf4c43aa63b93fa02a225') #设置通联数据账户的token凭证码
ts.get_token() #获取token
mkt = ts.Master() #证券概况类
st = ts.Market() #行情数据类
bd = ts.Fundamental() #基本面数据类
eq = ts.Equity() #股票信息类
hk = ts.HKequity() #港股信息类
fd = ts.Fund() #基金信息类
fu = ts.Future() #期货信息类
op = ts.Options() #期权信息类
iv = ts.IV() #期权隐含波动率类
bo = ts.Bond() #债券信息类
idx = ts.Idx() #指数信息类
mac = ts.Macro() #宏观行业类
sub = ts.Subject() #特色大数据类
def example(): #例子(1:设置token;2:在通联数据商城里购买/试用相关数据;3:调用tushare相关类;4:调用类里所需函数;5:查看通联数据api里对应函数的参数;6:设置同样参数调用;7:参照api获取返回值)
	ts.set_token('466a9d168864270832cf5a495de9d9179b893b8b14abf4c43aa63b93fa02a225')
	eq = ts.Equity()
	df = eq.Equ(equTypeCD='A', listStatusCD='L', field='ticker,secShortName,totalShares,nonrestFloatShares')
	df['ticker'] = df['ticker'].map(lambda x: str(x).zfill(6))
	print(df)

if __name__ == '__main__':  
	get_all_price()
	parse('600000')	##浦发银行
	insertCsv()
	example()
