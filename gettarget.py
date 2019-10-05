# 漏洞盒子入驻厂商爬虫
import requests
import time
import sys
import getopt
import json
import xlwt
from openpyxl import Workbook

list1=[]

def payload(start,page):
	header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
			'Accept':'application/json, text/javascript, */*; q=0.01',
			'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Accept-Encoding':'gzip, deflate',
			'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
			'X-Requested-With':'XMLHttpRequest',
			'Cookie':'PHPSESSID=7j1eh1dq0n3miito3kae5m9ni7; Hm_lvt_8dd9d540bb282c90af2121009e254daa=1570241551; Hm_lpvt_8dd9d540bb282c90af2121009e254daa=1570244953'}
	time1=time.localtime()
	enddate=str(time.strftime("%Y-%m-%d",time1))
	startdate=str(start)
	page=str(page)
	#从开始时间至今
	postdata='startDate='+startdate+'&endDate='+enddate+'&page='+page+'&search='
	r=requests.post('https://www.vulbox.com/json/getCompanyInfoByName',data=postdata,headers=header)
	#print(postdata)
	#print(r.text)
	return (r.text)


def getarg(argv):
	startdate=' '
	try:
		opts,args=getopt.getopt(argv,"hd:",["help","startdate="])
	except getopt.GetoptError:
		# 获取到想要的开始时间
		print('python gettarget.py -d 2019-01-01')
		sys.exit(2)
	for opt,arg in opts:
		if opt == '-h':
			print ('python gettarget.py -d 2019-01-01')
			sys.exit()
		elif opt == '-d':
			startdate=arg
			print(startdate)
			return (startdate)

def page_info(data):
	json1=json.loads(data)
	# print(json1)
	json2=json1.get('data')
	# print(json2)
	page=json2.get('page_num')
	# print(page)
	# data=json2.get('info')
	# print(data)
	return(page)

def dic_info(data):
	json1=json.loads(data)
	json2=json1.get('data')
	informations=json2.get('info')
	for i in informations:
		list1.append(i)


def output(informations):
	# 创建表格
	time1=time.localtime()
	date=str(time.strftime("%Y_%m_%d_%H",time1))
	file_name=str(date)+'.xls'
	wb = Workbook()
	sheet=wb.active
	sheet.title="sheet1"
	sheet["A1"].value='公司名'
	sheet["B1"].value="注册时间"
	sheet["C1"].value="url"
	sheet["D1"].value="type"
	j=2
	for i in informations:
		sheet["A"+str(j)].value=i.get("bus_name")
		sheet["B"+str(j)].value=i.get("user_registered")
		sheet["C"+str(j)].value=i.get("bus_url")
		sheet["D"+str(j)].value=i.get("bus_type")
		j=j+1
	wb.save(file_name)
	print("OK")

if __name__ == '__main__':
	page=2
	startdate=getarg(sys.argv[1:])
	data=payload(startdate,page)
	page=page_info(data)
	for i in range(2,page+1):
		data1=payload(startdate,i)
		dic_info(data1)
		output(list1)
		