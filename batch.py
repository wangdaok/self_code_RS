import os
import netCDF4 as nc
import numpy as np
import tkinter as tk
from tkinter import filedialog

def sintra3htody(filename,outname): #单值改变
    filetime=0  #设置文件时间初值
    if '-02' in filename:
        filetime=29
    elif '-04' in filename or '-06'  in filename or'-09' in filename or '-11' in filename:
        filetime=30
    else:
        filetime=31
    dataset = nc.Dataset(filename)
    '''
    print(dataset)
    print('---------------------------------------')



    #查看nc文件中的变量
    print(dataset.variables.keys())
    for x in dataset.variables.keys():
        print(x)
    print('---------------------------------------')
    
    #查看时间变量的信息
    print(dataset.variables['time'])
    '''
    datatime=dataset.variables['time'][:].data
    '''
    print(datatime)

    print('---------------------------------------')
    '''
    if 'prec' in filename:
        binvar='PRECTmms'
    elif 'solar' in filename:
        binvar='FSDS'

    # solar文件
    #查看变量的属性
    '''
    print(dataset.variables[binvar])
    print(dataset.variables[binvar].ncattrs())
    '''
    #读取变量数据值
    datasal = dataset.variables[binvar][:].data
    x,y,z=np.shape(datasal)
    newdata=np.zeros((int(x/8),int(y),int(z)))
    print('---------------------------------------')
    #修改时间
    newtime=np.zeros(filetime)
    for i in range(filetime):
        newtime[i]=datatime[8*(i+1)-1]
    
    #print(newtime)


    #进行三维数组累加操作
    for i in range(filetime):
        for j in range(8*i,8*(i+1)):
            newdata[i][:][:]+=(datasal[j][:][:]*3)


    for i in range(filetime):
        for j in range(int(y)):
            for k in range(int(z)):
                if newdata[i][j][k]<0:
                    newdata[i][j][k]=-32767.0
                elif newdata[i][j][k]>0:
                    newdata[i][j][k]=newdata[i][j][k]/24

    #复制与替换
    toexclude = [binvar, 'time'] 
    dst= nc.Dataset(outname, "w") 
    # copy global attributes all at once via dictionary
    dst.setncatts(dataset.__dict__)
    # copy dimensions
    for name, dimension in dataset.dimensions.items():
        if name!='time':
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
    times=dst.createDimension('time',size=filetime)
    # copy all file data except for the excluded
    for name, variable in dataset.variables.items():
        if  name not in toexclude:
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name].setncatts(dataset[name].__dict__)
            dst[name][:] = dataset[name][:]
            # copy variable attributes all at once via dictionary
    new_time=dst.createVariable('time','f4', dimensions='time')

    #print(dataset['time'].__dict__)
    for i in range(filetime):
        new_time[i]=newtime[i]
    tempdic=dataset['time'].__dict__
    tempdic["calendar"]="gregorian"
    dst['time'].setncatts(tempdic)

    ntime=dst.variables['time'][:].data
    new_var = dst.createVariable(binvar,'f4', dimensions=('time','lat','lon'))
    dst[binvar].setncatts(dataset[binvar].__dict__)

    new_var[:]=newdata[:]
   # print(new_var[0][0][0])

    '''
    print(dst[binvar].__dict__)
    nprec=dst.variables[binvar][:].data
    print(np.shape(nprec))
    print(nprec[0][0][0])
    '''
    print(filename+" succeeding")

def mutitra3htody(filename,outname):
    filetime=0  #设置文件时间初值
    if '-02' in filename:
        filetime=29
    elif '-04' in filename or '-06'  in filename or'-09' in filename or '-11' in filename:
        filetime=30
    else:
        filetime=31
    dataset = nc.Dataset(filename)
    '''
    print(dataset)
    print('---------------------------------------')


    #查看nc文件中的变量
    print(dataset.variables.keys())
    for x in dataset.variables.keys():
        print(x)
    print('---------------------------------------')

    #查看时间变量的信息
    print(dataset.variables['time'])
    '''
    datatime=dataset.variables['time'][:].data
    '''
    print(datatime)

    #查看变量属性
    print('---------------------------------------')
    '''
    var_list=['FLDS','PSRF','TBOT','WIND','QBOT']
    '''
    for i in var_list:
        print(dataset.variables[i])
        print(dataset.variables[i].ncattrs())
    '''
    #修改时间
    newtime=np.zeros(filetime)
    for i in range(filetime):
        newtime[i]=datatime[8*(i+1)-1]
    #print(newtime)

    #读取变量数据值
    srcvar_list=[]
    for i in var_list:
        datasal = dataset.variables[i][:].data
        srcvar_list.append(datasal)

    print('---------------------------------------')



    #进行三维数组累加操作
    newvar_list=[]
    for var in srcvar_list:
        newdata=np.zeros((filetime,400,700))
        for i in range(filetime):
            for j in range(8*i,8*(i+1)):
                newdata[i][:][:]+=(var[j][:][:]*3)
        newvar_list.append(newdata)
        #print(newdata)


    for var in newvar_list:
        for i in range(filetime):
            for j in range(400):
                for k in range(700):
                    if var[i][j][k]<-5000:
                        var[i][j][k]=-32767.0
                    else:
                        var[i][j][k]=var[i][j][k]/24

    #复制与替换
    toexclude = ['FLDS', 'time','PSRF','TBOT','WIND','QBOT'] #'FLDS', 
    dst= nc.Dataset(outname, "w") 
    # copy global attributes all at once via dictionary
    dst.setncatts(dataset.__dict__)
    # copy dimensions
    for name, dimension in dataset.dimensions.items():
        if name!='time':
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
    times=dst.createDimension('time',size=filetime)
    # copy all file data except for the excluded
    for name, variable in dataset.variables.items():
        if  name not in toexclude:
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name].setncatts(dataset[name].__dict__)
            dst[name][:] = dataset[name][:]
            # copy variable attributes all at once via dictionary
    new_time=dst.createVariable('time','f4', dimensions='time')
    #替换时间
    #print(dataset['time'].__dict__)
    for i in range(filetime):
        new_time[i]=newtime[i]
    #print(new_time)
    tempdic=dataset['time'].__dict__
    tempdic["calendar"]="gregorian"
    dst['time'].setncatts(tempdic)
    '''
    print(type(dst['time']))
    print(type(new_time))
    print(new_time)
    ntime=dst.variables['time'][:].data
    print(np.size(ntime))
    print(ntime)
    print(type(new_time))
    '''
    #替换变量
    for name,var in zip(var_list,newvar_list):
        new_var = dst.createVariable(name,'f4', dimensions=('time','lat','lon'))
        #print(type(new_var))
        dst[name].setncatts(dataset[name].__dict__)
        new_var[:]=var[:]
        #print(new_var[0][0][0])

    '''
    print(dst['FLDS'].__dict__)
    nprec=dst.variables['FLDS'][:].data
    print(np.shape(nprec))
    print(nprec[25][256][148])
    '''
    print(filename+" succeeding")

if __name__ == '__main__':
    root=tk.Tk()
    root.withdraw()
    filepath=filedialog.askdirectory()
    resdir=filepath+"/"+"results"
    if not os.path.exists(resdir):
        os.makedirs(resdir)

    #直接替换闰年二月
    '''
    mon29=['-02']
    mon30=['-04','-06','-09','-11']
    mon31=['-01','-03','-05','-07','-08','-10','-12']
    '''
    for file in os.listdir(filepath):
        if '.nc' in file:
            outname=resdir+"/"+"new"+file
            filename=filepath+"/"+file
            if 'prec' in file or 'solar' in file:
                sintra3htody(filename,outname)
            else:
                mutitra3htody(filename,outname)
    print("everything done")


