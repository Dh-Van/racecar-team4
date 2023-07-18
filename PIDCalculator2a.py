# Gains
kP = 0.6
kI = 0.1
kD = -0.1

# Goal
setPoint = 320

data =  [(0.0, 270), (0.2,  280), (0.4, 290), (0.8, 300), (1.0, 310)]

# Slope formula: 
derivative = (310-300) / (1.0 - 0.8)

# Riemann Sum
integral = 0
for d in range(1, len(data)):
    # Difference between referance signal and x value in data
    width = data[d][0] - data[d-1][0]
    integral += width * (data[d][1] - setPoint)

output_px = (kP * (310 - 320)) + (kD * derivative) + (kI * integral)
output_rc = ((output_px + setPoint) * 2 / 640) - 1
print(output_px, output_rc)
