a=[]
temp2={}
temp = []
temp2['d'] = 'd1'
temp2['c'] = []
a.append(temp2)
temp.append(a[0]['c'])
temp2 = {}
temp2['d'] = 'd2'
temp2['c'] = []

# temp[0].append(temp2)
[print(j) for i,j in enumerate(a)]
