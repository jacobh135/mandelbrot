import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

def adjust(num, frac, clamp_active):
    if (not clamp_active):
        num %= (2 ** (frac + 3))
        if (num >= (2 ** (frac + 2))):
            num -= (2 ** (frac + 3))
    
    else:
        if (num >= (2 **(frac + 2))):
            num = ((2 ** (frac + 2)) - 1)
        if (num < -(2 **(frac + 2))):
            num = -(2 **(frac + 2))

    return num

# def adjust(num):
#     return num

def cranker(x_pos, y_pos, frac, clamp_active):
    c_x = x_pos * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
    c_y = y_pos * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

    z_x = 0
    z_y = 0
    count = 0
    while ((z_x ** 2 + z_y ** 2 <= 4 * (2 ** frac) ** 2) and (count < 24)):
        z_x_new = adjust((z_x ** 2) // (2 ** frac) - (z_y ** 2) // (2 ** frac) + c_x, frac, clamp_active)
        z_y_new = adjust(2 * ((z_x * z_y) // (2 ** frac)) + c_y, frac, clamp_active)
        z_x = z_x_new
        z_y = z_y_new
        count += 1
    
    return count;

def cranker_real(x_pos, y_pos):
    c_x = x_pos * 3.5 / 639 - 2.5
    c_y = y_pos * 2 / 479 - 1

    z_x = 0
    z_y = 0
    count = 0
    while ((((z_x ** 2) + (z_y ** 2)) <= 4) and (count < 24)):
        z_x_new = (z_x ** 2) - (z_y ** 2) + c_x
        z_y_new = (2 * z_x * z_y) + c_y
        z_x = z_x_new
        z_y = z_y_new
        count += 1
    
    return count;


frac = 15
clamp_active = False

# difference_count = 0
display_ba = [[0 for j in range(640)] for j in range(480)]
# display_real = [[0 for j in range(640)] for j in range(480)]
# display_difference = [[0 for j in range(640)] for j in range(480)]
for j in range(640 * 480):
    x_pos = j % 640
    y_pos = j // 640

    display_ba[y_pos][x_pos] = cranker(x_pos, y_pos, frac, clamp_active)
    # display_real[y_pos][x_pos] = cranker_real(x_pos, y_pos)
    # difference = abs(display_ba[y_pos][x_pos] - display_real[y_pos][x_pos])
    # display_difference[y_pos][x_pos] = difference
    # if (difference):
    #     difference_count += 1

## colormap

rgb222_table_A_huesweep = [
    (0, 0, 0),  # count=0
    (0, 0, 3),  # count=1
    (0, 1, 3),  # count=2
    (0, 1, 3),  # count=3
    (0, 2, 3),  # count=4
    (0, 2, 3),  # count=5
    (0, 3, 3),  # count=6
    (0, 3, 3),  # count=7
    (0, 3, 2),  # count=8
    (0, 3, 2),  # count=9
    (0, 3, 1),  # count=10
    (0, 3, 1),  # count=11
    (0, 3, 0),  # count=12
    (1, 3, 0),  # count=13
    (1, 3, 0),  # count=14
    (2, 3, 0),  # count=15
    (2, 3, 0),  # count=16
    (3, 3, 0),  # count=17
    (3, 3, 0),  # count=18
    (3, 2, 0),  # count=19
    (3, 2, 0),  # count=20
    (3, 1, 0),  # count=21
    (3, 1, 0),  # count=22
    (3, 0, 0),  # count=23
    (0, 0, 0),  # count=24
]

rgb222_table_B_greedy23unique = [
    (0, 0, 0),  # count=0
    (0, 0, 1),  # count=1
    (0, 0, 2),  # count=2
    (0, 0, 3),  # count=3
    (0, 1, 3),  # count=4
    (0, 1, 2),  # count=5
    (0, 2, 3),  # count=6
    (0, 2, 2),  # count=7
    (0, 3, 3),  # count=8
    (0, 3, 2),  # count=9
    (1, 3, 3),  # count=10
    (1, 3, 2),  # count=11
    (1, 3, 1),  # count=12
    (2, 3, 1),  # count=13
    (3, 3, 0),  # count=14
    (3, 2, 0),  # count=15
    (2, 2, 0),  # count=16
    (3, 1, 0),  # count=17
    (2, 1, 0),  # count=18
    (3, 0, 0),  # count=19
    (2, 0, 0),  # count=20
    (3, 0, 1),  # count=21
    (2, 0, 1),  # count=22
    (1, 0, 0),  # count=23
    (0, 0, 0),  # count=24
]

rgb222_table_C_anchored = [
    (0, 0, 0),  # count=0
    (0, 0, 3),  # count=1
    (0, 0, 2),  # count=2
    (0, 1, 3),  # count=3
    (1, 0, 3),  # count=4
    (0, 1, 2),  # count=5
    (0, 2, 3),  # count=6
    (0, 2, 2),  # count=7
    (0, 3, 3),  # count=8
    (0, 3, 2),  # count=9
    (1, 3, 3),  # count=10
    (1, 3, 2),  # count=11
    (1, 3, 1),  # count=12
    (2, 3, 1),  # count=13
    (3, 3, 0),  # count=14
    (3, 2, 0),  # count=15
    (2, 2, 0),  # count=16
    (3, 1, 0),  # count=17
    (2, 1, 0),  # count=18
    (3, 1, 1),  # count=19
    (2, 0, 0),  # count=20
    (3, 0, 1),  # count=21
    (2, 0, 1),  # count=22
    (3, 0, 0),  # count=23
    (0, 0, 0),  # count=24
]

rgb222_table_B_inverted = [
    (0, 0, 0),  # count=0
    (1, 0, 0),  # count=1
    (2, 0, 1),  # count=2
    (3, 0, 1),  # count=3
    (2, 0, 0),  # count=4
    (3, 0, 0),  # count=5
    (2, 1, 0),  # count=6
    (3, 1, 0),  # count=7
    (2, 2, 0),  # count=8
    (3, 2, 0),  # count=9
    (3, 3, 0),  # count=10
    (2, 3, 1),  # count=11
    (1, 3, 1),  # count=12
    (1, 3, 2),  # count=13
    (1, 3, 3),  # count=14
    (0, 3, 2),  # count=15
    (0, 3, 3),  # count=16
    (0, 2, 2),  # count=17
    (0, 2, 3),  # count=18
    (0, 1, 2),  # count=19
    (0, 1, 3),  # count=20
    (0, 0, 3),  # count=21
    (0, 0, 2),  # count=22
    (0, 0, 1),  # count=23
    (0, 0, 0),  # count=24
]

rgb222_table_optimal = [
    (0, 0, 0),  # count=0
    (0, 0, 1),  # count=1
    (0, 0, 2),  # count=2
    (1, 0, 3),  # count=3
    (0, 0, 3),  # count=4
    (0, 1, 3),  # count=5
    (0, 1, 2),  # count=6
    (0, 2, 3),  # count=7
    (0, 2, 2),  # count=8
    (0, 3, 3),  # count=9
    (1, 3, 3),  # count=10
    (1, 3, 2),  # count=11
    (1, 3, 1),  # count=12
    (2, 3, 1),  # count=13
    (2, 3, 0),  # count=14
    (3, 3, 0),  # count=15
    (3, 2, 0),  # count=16
    (2, 2, 0),  # count=17
    (3, 1, 0),  # count=18
    (2, 1, 0),  # count=19
    (3, 0, 0),  # count=20
    (3, 0, 1),  # count=21
    (2, 0, 0),  # count=22
    (1, 0, 0),  # count=23
    (0, 0, 0),  # count=24
]

rgb_table = rgb222_table_optimal

colors_list = [(r/3, g/3, b/3) for (r, g, b) in rgb_table]

my_cmap = ListedColormap(colors_list)
norm = BoundaryNorm(boundaries=range(len(colors_list)+1), ncolors=len(colors_list))

plt.imshow(display_ba, cmap=my_cmap, norm=norm)
plt.colorbar()
plt.show()