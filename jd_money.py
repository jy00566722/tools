
import re
#成本价文件
a_file = 'jd_price.txt'
b_file =  'jd_sale.txt'

#给定价格文件，取得货号与价的字典
def get_price(a_file):
	#读取成本价，一行一款
	a_list = []
	with open(a_file,'rt',encoding='utf-8') as f:
		for a_line in f:
			a_list.append(a_line)

	#把成本价中的货号与单价分开
	b_list =[]
	for b_line in a_list:
		b_list.append(b_line.split('\t'))

	#print(b_list)

	#把列表转换为字典，方便查价
	pic_dic={}

	for c_line in b_list:
		pic_dic[c_line[0]] = int(c_line[1].strip('\n'))

	#print(pic_dic['1702K-39A'])
	return pic_dic


#读取销售记录

def get_sale(b_file):
	a_list=[]
	with open(b_file,'rt',encoding='utf-8') as f:
		for a_line in f:
			a_list.append(a_line)

	b_list =[]
	for b_line in a_list:
		b_list.append(b_line.split('\t'))



	return b_list



#清洗、统计数据，传入列表
def clear_data(a_list):
	cha_jia = 0
	cha_jia_gold=0
	zhen_pin = 0
	for a_line in a_list:
		#删除锁与取消的订单
		if a_line[12] == '锁定':
			#print(a_line[12])
			a_list.remove(a_line)
			continue
		if a_line[12] =='已取消':
			print(a_line[12])
			a_list.remove(a_line)
			continue
		#处理补差价
		if a_line[26] == '补差价':
			cha_jia +=1
			cha_jia_gold = int(a_line[9]) + cha_jia_gold if a_line[9] !='' else cha_jia_gold

			try:
				a_list.remove(a_line)
			except Exception as e:
				print(a_line)
				raise e 
			continue
			
		if (a_line[26] == '打蜡鞋带' or a_line[26] =='黑色打蜡鞋带'):
			a_list.remove(a_line)
			zhen_pin +=1

	return (a_list,cha_jia,cha_jia_gold,zhen_pin)

#把洗好的列表中，真实订单与刷的分开来
def real_no_list(a_list):
	no_list=[]
	real_list = []
	for a_line in a_list:
		if '送袜子' in a_line[17]:
			no_list.append(a_line)
		elif '袜子TP' in a_line[17]:
			no_list.append(a_line)

		elif re.match(r'送袜子[A-Za-z]+',a_line[18]):
			no_list.append(a_line)

		else:
			real_list.append(a_line)

	return (no_list,real_list)


#计算刷单成本
def no_gold(a_list):
	no_gold_a = 0
	for a_line in a_list:
		no_gold_a += float(a_line[10])*0.08+6+1.9+0.5

	return no_gold_a

#计算真实订单利润
def real_gold(a_list,a_dic):
	real_gold_a =0
	real_gold_b =0
	for a_line in a_list:
		try:
			real_gold_a+= float(a_line[9] if a_line[9] != '' else 0)*0.92-a_dic[a_line[26]]-12-0.5
			real_gold_b+= float(a_line[9] if a_line[9] != '' else 0)
			print(a_line[13]+str(real_gold_b))

		except Exception as e:
			print(a_line)
			continue

	return (real_gold_a,real_gold_b)

if __name__ == '__main__':
	pic_dic = get_price(a_file)
	#print(get_sale(b_file)[20][26])
	#print(get_sale(b_file)[21][26])
	sale_list,cha_jia,cha_jia_gold,zhen_pin=clear_data(get_sale(b_file))
	#print(cha_jia)
	#print(zhen_pin)
	#print(cha_jia_gold)
	no_list,real_list = real_no_list(sale_list)
	print('刷单数量:'+str(len(no_list)))
	print('真实订单:'+str(len(real_list)))
	no_gold_b = no_gold(no_list)
	real_gold_b,real_gold_c= real_gold(real_list,pic_dic)
	s   =  '刷单成本共计:'+str(no_gold_b)
	s4  =  '销售金额:'+str(real_gold_c)
	s1  =  '真实订单利润共计:'+str(real_gold_b)
	s2  =  '货品利润：'+str(real_gold_b - no_gold_b)
	s3  =  '算上人力成本,利润为:' +str(real_gold_b - no_gold_b - 667)

	print(s)
	print(s1)
	print(s4)
	print(s2)
	print(s3)