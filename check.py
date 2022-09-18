import gzip as gz
import netCDF4 as nc
ncgz=gz.open("shum_CMFD_V0106_B-01_01dy_010deg_201001-201012.nc.gz")
date=nc.Dataset('dummy',mode='r',memory=ncgz.read())

print(date.variables)
iradvar=date.variables['shum'][:].data
print(iradvar[23][256][240])
print("+++++++++++++++++++++++++")
hoursnc=nc.Dataset("clmforc.0.1x0.1.TPQWL-2010-01.nc")
shumvar=hoursnc.variables['QBOT'][:].data
meanshum=0
for i in range(184,192):
    meanshum+=(shumvar[i][256][240]*3)
    print(shumvar[i][256][240])

meanshum=meanshum/24
print("mean:"+str(meanshum))
a=meanshum
cfnc=nc.Dataset("newclmforc.0.1x0.1.TPQWL-2010-01.nc")
cfvar=cfnc.variables['QBOT'][:].data
print("newvar:"+str(cfvar[23][256][240]))

dgz=gz.open("shum_CMFD_V0106_B-01_03hr_010deg_201001.nc.gz")
ddata=nc.Dataset('dummy',mode='r',memory=dgz.read())
print(ddata.variables)
deshum=ddata.variables['shum'][:].data
meanshum=0
for i in range(184,192):
    meanshum+=(deshum[i][256][240]*3)
    print(deshum[i][256][240])
meanshum=meanshum/24
print("------------")
print("demean:"+str(meanshum))
b=float((a-meanshum)/a)
print("error:"+str(b))