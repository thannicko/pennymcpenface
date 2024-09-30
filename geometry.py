import math

def cartesian_to_cylindrical(cartesian_points):
    cylindrical_points = []
    
    for point in cartesian_points:
        x = point[0]
        y = point[1]
        
        # Calculate r and θ
        r = math.sqrt(x**2 + y**2)
        theta = math.degrees(math.atan2(y, x))  # Convert θ to degrees
        
        cylindrical_points.append([r, theta])
    
    return cylindrical_points


def convert_radius_coordinates_to_mm(radius, r_offset=265):
    radius_mm = 0.3 * radius
    radius_mm = radius_mm + r_offset
    print(f"Radius in coordinates {radius} --> {radius_mm}mm")
    return radius_mm