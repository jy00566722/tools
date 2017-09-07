import re
#地址文件
a_file = 'jd.txt'
b_file =  'jd_good.txt'


#把第一行地址读取列表
a_list = []
with open(a_file,'rt',encoding='utf-8') as f:
	for a_line in f:
		a_list.append(a_line)

#把上列表中的第一项，分割为想要的三部分，生成新的列表
b_list =[]
for b_line in a_list:
	b_list.append(b_line.split('\t'))


#把第二个列表中的第一项中的三部分，连成想要的地址
c_list= []

#地址匹配模式
adddata= re.compile(r'(\S{2})(\S{1:3}[市|区])(\S{1:3}[县|市|区|镇])')

for c_line in b_list:
	jd_name = c_line[0]
	jd_phone = c_line[2].strip('\n')
	jd_address = c_line[1]
	jd_address1 = re.sub(r'(\S{2})(\S{1,3}[市|区])(\S{1,3}[区|县|市|镇])',r'\1 \2 \3 ',jd_address)
	#jd_address1 = adddata.sub()
	print(jd_address1)


	c_list.append(jd_name+','+jd_phone+','+jd_address1+',100000\r\n')

#写入文件

with open(b_file,'wt',encoding='utf-8') as f:
	for d_line in c_list:
		f.write(d_line)