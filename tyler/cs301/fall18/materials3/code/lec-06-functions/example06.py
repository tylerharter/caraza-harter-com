def area_of_circle(radius):
    area = 3.14 * radius * radius
    return area


def volume_of_cylinder(radius, height):
    volume = area_of_circle(radius) * height
    return volume


v = volume_of_cylinder(10, 20)
print('volume of cylinder =', v)
v = volume_of_cylinder(1, 2)
print('volume of cylinder =', v)
v = volume_of_cylinder(12.5, 7)
print('volume of cylinder =', v)

