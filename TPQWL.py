import netCDF4 as nc
import numpy as np
 
 

dataset = nc.Dataset("clmforc.0.1x0.1.TPQWL-2010-01.nc")
print(dataset)
print('---------------------------------------')



#查看nc文件中的变量
print(dataset.variables.keys())
for x in dataset.variables.keys():
	print(x)
print('---------------------------------------')
 
#查看时间变量的信息
print(dataset.variables['time'])
datatime=dataset.variables['time'][:].data
print(datatime)
#查看变量属性
print('---------------------------------------')
var_list=['FLDS','PSRF','TBOT','WIND','QBOT']
for i in var_list:
    print(dataset.variables[i])
    print(dataset.variables[i].ncattrs())
#修改时间
newtime=np.zeros(31)
for i in range(31):
	newtime[i]=datatime[8*(i+1)-1]
print(newtime)

#读取变量数据值
srcvar_list=[]
for i in var_list:
    datasal = dataset.variables[i][:].data
    srcvar_list.append(datasal)

print('---------------------------------------')



#进行三维数组累加操作
newvar_list=[]
for var in srcvar_list:
    newdata=np.zeros((31,400,700))
    for i in range(31):
        for j in range(8*i,8*(i+1)):
            newdata[i][:][:]+=(var[j][:][:]*3)
    newvar_list.append(newdata)
    print(newdata)


for var in newvar_list:
    for i in range(31):
        for j in range(400):
            for k in range(700):
                if var[i][j][k]<-5000:
                    var[i][j][k]=-32767.0
                else:
                    var[i][j][k]=var[i][j][k]/24

#复制与替换
toexclude = ['FLDS', 'time','PSRF','TBOT','WIND','QBOT'] #'FLDS', 
dst= nc.Dataset("newclmforc.0.1x0.1.TPQWL-2010-01.nc", "w") 
# copy global attributes all at once via dictionary
dst.setncatts(dataset.__dict__)
# copy dimensions
for name, dimension in dataset.dimensions.items():
	if name!='time':
		dst.createDimension(
			name, (len(dimension) if not dimension.isunlimited() else None))
times=dst.createDimension('time',size=31)
# copy all file data except for the excluded
for name, variable in dataset.variables.items():
    if  name not in toexclude:
        x = dst.createVariable(name, variable.datatype, variable.dimensions)
        dst[name].setncatts(dataset[name].__dict__)
        dst[name][:] = dataset[name][:]
        # copy variable attributes all at once via dictionary
new_time=dst.createVariable('time','f4', dimensions='time')
#替换时间
print(dataset['time'].__dict__)
for i in range(31):
	new_time[i]=newtime[i]
print(new_time)
tempdic=dataset['time'].__dict__
tempdic["calendar"]="gregorian"
dst['time'].setncatts(tempdic)

print(type(dst['time']))
print(type(new_time))
print(new_time)
ntime=dst.variables['time'][:].data
print(np.size(ntime))
print(ntime)
print(type(new_time))

#替换变量
for name,var in zip(var_list,newvar_list):
    new_var = dst.createVariable(name,'f4', dimensions=('time','lat','lon'))
    print(type(new_var))
    dst[name].setncatts(dataset[name].__dict__)
    new_var[:]=var[:]
    print(new_var[0][0][0])


print(dst['FLDS'].__dict__)
nprec=dst.variables['FLDS'][:].data
print(np.shape(nprec))
print(nprec[25][256][148])


#输出nc