import matplotlib.pyplot as plt

def adjust(num, clamp_active, frac):
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

def cranker(x_pos, y_pos, clamp_active, frac):
    c_x = x_pos * round(3.5 / 639 * (2 ** frac)) - round(2.5 * (2 ** frac))
    c_y = y_pos * round(2 / 479 * (2 ** frac)) - 1 * (2 ** frac)

    z_x = 0
    z_y = 0
    count = 0
    while ((z_x ** 2 + z_y ** 2 < 4 * (2 ** frac) ** 2) and (count < 24)):
        z_x_new = adjust((z_x ** 2) // (2 ** frac) - (z_y ** 2) // (2 ** frac) + c_x, clamp_active, frac)
        z_y_new = adjust(2 * ((z_x * z_y) // (2 ** frac)) + c_y, clamp_active, frac)
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
    while ((((z_x ** 2) + (z_y ** 2)) < 4) and (count < 24)):
        z_x_new = (z_x ** 2) - (z_y ** 2) + c_x
        z_y_new = (2 * z_x * z_y) + c_y
        z_x = z_x_new
        z_y = z_y_new
        count += 1
    
    return count;

for i in range(11, 18):
    frac = i
    clamp_active = False

    difference_count = 0
    display_ba = [[0 for j in range(640)] for j in range(480)]
    display_real = [[0 for j in range(640)] for j in range(480)]
    display_difference = [[0 for j in range(640)] for j in range(480)]
    for j in range(640 * 480):
        x_pos = j % 640
        y_pos = j // 640

        display_ba[y_pos][x_pos] = cranker(x_pos, y_pos, clamp_active, frac)
        display_real[y_pos][x_pos] = cranker_real(x_pos, y_pos)
        difference = abs(display_ba[y_pos][x_pos] - display_real[y_pos][x_pos])
        display_difference[y_pos][x_pos] = difference
        if (difference):
            difference_count += 1

    print(frac, ": ", difference_count)
    # plt.imshow(display_difference, cmap = 'hot')
    # plt.colorbar()
    # plt.show()
