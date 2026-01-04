import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# df=pd.DataFrame([[1,2,3,4],[4,5,6],[7,8,9]],columns=["A","B","C","D"])
# a=df.head()
# print(a)
# print(df.info())
cone=pd.read_csv("/home/ranvijay/softwaremodule1_IITBR/nump_tut/cones.csv")
# print(cone.head(10))
all_cones_x_arr=np.array([cone.loc[:,'x']])
all_cones_y_arr=np.array([cone.loc[:,'y']])
x_avg=np.mean(all_cones_x_arr)
y_avg=np.mean(all_cones_y_arr)
# print(x_avg,y_avg)
# print(all_cones_x_arr)
# print(cone.loc[["color"]])
cone_blue=cone.loc[cone['color']=='blue']

# print(cone_blue.head())
cone_blue_x=cone_blue.loc[:,'x']
cone_blue_y=cone_blue.loc[:,'y']
# print(cone_blue_x.head())
# print(cone_blue.index)
cone_yellow=cone.loc[cone['color']=='yellow']
cone_yellow_x=cone_yellow.loc[:,'x']
cone_yellow_y=cone_yellow.loc[:,'y']
cone_blue_x_arr=np.array(cone_blue_x)
cone_blue_y_arr=np.array(cone_blue_y)
cone_yellow_x_arr=np.array(cone_yellow_x)
cone_yellow_y_arr=np.array(cone_yellow_y)



# Sorting the cones 

blue_cone_angle_arr=[]
yellow_cone_angle_arr=[]
for i in range(len(cone_blue_x_arr)):
    angle=np.atan2((cone_blue_y_arr[i]-y_avg),(cone_blue_x_arr[i]-x_avg))
    blue_cone_angle_arr.append(angle)
for i in range(len(cone_yellow_x_arr)):
    angle=np.atan2((cone_yellow_y_arr[i]-y_avg),(cone_yellow_x_arr[i]-x_avg))
    yellow_cone_angle_arr.append(angle)
    # if(cone_blue_x_arr[i]>x_avg and cone_blue_y_arr[i]>y_avg):
# print(blue_cone_angle_arr)
# print(yellow_cone_angle_arr)
sorted_blue_angles=np.sort(blue_cone_angle_arr)
sorted_yellow_angles=np.sort(yellow_cone_angle_arr)
sorted_indexes_blue_angles=np.argsort(blue_cone_angle_arr)
sorted_indexes_yellow_angles=np.argsort(yellow_cone_angle_arr)
length=len(cone_blue_x_arr)
sorted_blue_x=[]
sorted_blue_y=[]
sorted_yellow_x=[]
sorted_yellow_y=[]
for i in range(length):
    sorted_blue_x.append(cone_blue_x_arr[sorted_indexes_blue_angles[i]])
    sorted_blue_y.append(cone_blue_y_arr[sorted_indexes_blue_angles[i]])
    sorted_yellow_x.append(cone_yellow_x_arr[sorted_indexes_yellow_angles[i]])
    sorted_yellow_y.append(cone_yellow_y_arr[sorted_indexes_yellow_angles[i]])
# print("Sorted blue cone angles " , sorted_blue_angles[:])
# print("Sorted yellow cone angles ",sorted_yellow_angles[:])
average_x=[]
average_y=[]
for i in range(len(sorted_blue_x)):
    average_x.append((sorted_blue_x[i]+sorted_yellow_x[i])/2)
    average_y.append((sorted_blue_y[i]+sorted_yellow_y[i])/2)

# This is just giving the track boundaries
# plt.scatter(x_avg,y_avg,color="black")
# plt.plot(sorted_blue_x,sorted_blue_y,color='blue')
# plt.plot(sorted_yellow_x,sorted_yellow_y,color='red')
# plt.plot(average_x,average_y,color="black")
# plt.show()

from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(figsize=(15,15))
ax.scatter(x_avg,y_avg)
ax.scatter(0,0)
# ax.scatter(sorted_blue_x,sorted_blue_y,color='blue')
# ax.scatter(sorted_yellow_x,sorted_yellow_y,color='red')
ax.plot(sorted_blue_x,sorted_blue_y,color='blue')   
ax.plot(sorted_yellow_x,sorted_yellow_y,color='red')
ax.plot(average_x, average_y, 'k-', linewidth=2)
ax.set_aspect('equal')

# Create the moving particle (dot)
dots_list=ax.plot([], [], 'ro', markersize=8)
dot=dots_list[0]

def update(frame):
    i = frame % len(average_x)                 # loop index
    dot.set_data([average_x[i]], [average_y[i]])      
    return dot,

ani = FuncAnimation(fig,update,frames=len(average_x),interval=500,blit=True)
ani.save("centerline_animation.mp4", fps=20)
plt.show()