#coding:utf-8

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

#原始数据集
class STATION_BASE(): 
    def __init__(self, lon, lat, var):
        self.lat = lat
        self.lon = lon
        self.var = var
        
#加入待插入点
class Addpoints(object):
    def __init__(self, stn):
        self.lat = stn.lat
        self.lon = stn.lon
#三角插值
    def triinterp_var(self, stb):
#Delaunay三角化
        tri = mtri.Triangulation(stb.lon, stb.lat)
        plt.triplot(tri)
        plt.tricontourf(stb.lon, stb.lat, stb.var)
        plt.scatter(stb.lon, stb.lat, c="r")
        for i in range(len(stb.lon)):
            plt.text(stb.lon[i], stb.lat[i], stb.var[i])
#分片线性插值
        interp = mtri.LinearTriInterpolator(tri, stb.var)
        z = interp(self.lon, self.lat)
        return z

#随机测试

n = 50
x = np.random.rand(n)
y = np.random.rand(n)
z = np.rint(np.exp(np.random.rand(n)*8)) #模拟PM10浓度

#50个原始数据点
stb = STATION_BASE(x, y, z)

m = 10
x1 = np.random.rand(m)
x2 = np.random.rand(m)

#10个待插值点
stn = STATION_BASE(x1, x2, 0)

#三角插值
o = Addpoints(stn)
stn.var = np.rint(o.triinterp_var(stb))

#plot
plt.scatter(stn.lon, stn.lat, c="b")
for i in range(len(stn.lon)):
    plt.text(stn.lon[i], stn.lat[i], stn.var[i])
plt.show()


