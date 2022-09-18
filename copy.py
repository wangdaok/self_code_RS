import netCDF4 as nc
toexclude = ['PRECTmms','time'] 
src=nc.Dataset("clmforc.0.1x0.1.prec-2010-01.nc") 
dst= nc.Dataset("out.nc", "w") 
# copy global attributes all at once via dictionary
dst.setncatts(src.__dict__)
# copy dimensions
for name, dimension in src.dimensions.items():
    print(name)
    dst.createDimension(
        name, (len(dimension) if not dimension.isunlimited() else None))
# copy all file data except for the excluded
for name, variable in src.variables.items():
    if  name not in toexclude:
        x = dst.createVariable(name, variable.datatype, variable.dimensions)
        dst[name].setncatts(src[name].__dict__)
        print(src[name][:])
        print(type(src[name][:]))
        dst[name][:] = src[name][:]
        
        
        
        
'''
print(src['PRECTmms'].__dict__)
new_var = dst.createVariable('PRECTmms','f4', dimensions=('time','lat','lon'))
dst['PRECTmms'].setncatts(src['PRECTmms'].__dict__)
print(dst['PRECTmms'].__dict__)
print(new_var)
'''