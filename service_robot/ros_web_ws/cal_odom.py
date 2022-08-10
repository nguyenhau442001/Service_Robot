import math

w=0.9238795325112867
z=0.3826834323650898
theta=math.atan2(w*z,0.5-z*z)
theta=theta*180/(math.pi)
print(theta)