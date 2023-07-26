def affine_transformation(value, old_range, new_range):
    return (value - old_range[0]) * ((new_range[1] - new_range[0]) / (old_range[1] - old_range[0])) + new_range[0]

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
