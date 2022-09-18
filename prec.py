import netCDF4 as nc
import numpy as np
import tkinter as tk
from tkinter import filedialog
root=tk.Tk()
root.withdraw()
Folderpath=filedialog.askdirectory()
filepath=filedialog.askopenfilename()
print(filepath)

dataset = nc.Dataset(filepath)
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

print('---------------------------------------')
 
#查看变量的属性
print(dataset.variables['PRECTmms'])
print(dataset.variables['PRECTmms'].ncattrs())

#读取变量数据值
datasal = dataset.variables['PRECTmms'][:].data
print(datasal)
print(np.size(datasal))
x,y,z=np.shape(datasal)
newdata=np.zeros((int(x/8),int(y),int(z)))
print(np.shape(newdata))
print('---------------------------------------')
#修改时间
newtime=np.zeros(31)
for i in range(31):
	newtime[i]=datatime[8*(i+1)-1]
print(newtime)


#进行三维数组累加操作
for i in range(31):
	for j in range(8*i,8*(i+1)):
		newdata[i][:][:]+=(datasal[j][:][:]*3)
print(newdata)


for i in range(31):
	for j in range(int(y)):
		for k in range(int(z)):
			if newdata[i][j][k]<0:
				newdata[i][j][k]=-32767.0
			elif newdata[i][j][k]>0:
				newdata[i][j][k]=newdata[i][j][k]/24

#复制与替换
toexclude = ['PRECTmms', 'time'] #'PRECTmms', 
dst= nc.Dataset("newclmforc.0.1x0.1.prec-2012-02.nc", "w") 
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

print(dataset['time'].__dict__)
for i in range(31):
	new_time[i]=newtime[i]
print(new_time)
tempdic=dataset['time'].__dict__
tempdic["calendar"]="gregorian"
dst['time'].setncatts(tempdic)
print(dst['time'].__dict__)

print(type(dst['time']))
print(type(new_time))
print(new_time)
ntime=dst.variables['time'][:].data
print(np.size(ntime))
print(ntime)
print(type(new_time))


new_var = dst.createVariable('PRECTmms','f4', dimensions=('time','lat','lon'))
print(type(new_var))
dst['PRECTmms'].setncatts(dataset['PRECTmms'].__dict__)

new_var[:]=newdata[:]
print(new_var[0][0][0])


print(dst['PRECTmms'].__dict__)
nprec=dst.variables['PRECTmms'][:].data
print(np.shape(nprec))
print(nprec[0][0][0])


#输出nc