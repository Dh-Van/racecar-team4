# Gains
kP = 0.5
kI = -0.25
kD = 0.39

# Goal
setPoint = 960

data =  [(0.0, 250), (0.5, 600), (1.0,  780), (1.5, 912), (2.0, 1100), 
         (2.5, 1500), (3.0, 1300), (3.5, 1102), (4.0, 924), (4.5, 882), 
         (5.0, 956), (5.5, 1025), (6.0, 998), (6.5, 950), (7.0, 956), (7.5, 968)] 


# Slope formula: 
derivative = (968-956) / (7.5 - 7.0)
print(derivative)
# Riemann Sum
integral = 0
for d in range(1, len(data)):
    width = data[d][0] - data[d-1][0]
    integral += width * (data[d][1] - setPoint)

output_px = (kP * (968 - 1920)) + (kD * derivative) + (kI * integral)
output_rc = ((output_px + setPoint) * 2 / 1920) - 1
print(output_px, output_rc)
