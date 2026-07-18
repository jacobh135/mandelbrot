import matplotlib.pyplot as plt

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

display = [[0 for i in range(640)] for i in range(480)]
for i in range(640 * 480):
    x_pos = i % 640
    y_pos = i // 640

    display[y_pos][x_pos] = cranker(x_pos, y_pos)

plt.imshow(display, cmap = 'hot')
plt.colorbar()
plt.show()