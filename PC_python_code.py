import time
import socket
import numpy as np
import matplotlib.pyplot as plt


def vision_grid(distance1, distance2):  # call to update state-space with new info
    global prev_dist
    global center_x
    global center_y
    global myFile
    global y_len
    global x_len
    auto_adjust = True
    if auto_adjust and may_adjust and abs(distance2 - prev_dist) <= 3 and distance2 <= 65:
        if orientation == 0:
            center_x += prev_dist - distance2
        elif orientation == 2:
            center_y += distance2 - prev_dist
        elif orientation == 4:
            center_x += distance2 - prev_dist
        else:
            center_y += prev_dist - distance2
    prev_dist = distance2

    if orientation == 0:
        if center_y + 12 + distance1 > y_len:
            v_add = np.zeros((200, x_len))
            myFile = np.vstack((myFile, v_add))
            y_len += 200
        fill_up(0, 12, distance1)
        if center_x + 14 + distance1 > x_len:
            h_add = np.zeros((y_len, 200))
            myFile = np.hstack((myFile, h_add))
            x_len += 200
        fill_right(14, 1, distance2)
    elif orientation == 2:
        if center_x + 12 + distance1 > x_len:
            h_add = np.zeros((y_len, 200))
            myFile = np.hstack((myFile, h_add))
            x_len += 200
        fill_right(12, 0, distance1)
        if center_y - 14 - distance1 < 0:
            v_add = np.zeros((200, x_len))
            myFile = np.vstack((v_add, myFile))
            y_len += 200
            center_y += 200
        fill_down(1, -14, distance2)
    elif orientation == 4:
        if center_y - 12 - distance1 < 0:
            v_add = np.zeros((200, x_len))
            myFile = np.vstack((v_add, myFile))
            y_len += 200
            center_y += 200
        fill_down(0, -12, distance1)
        if center_x - 14 - distance1 < 0:
            h_add = np.zeros((y_len, 200))
            myFile = np.hstack((h_add, myFile))
            x_len += 200
            center_x += 200
        fill_left(-14, -1, distance2)
    elif orientation == 6:
        if center_x - 12 - distance1 < 0:
            h_add = np.zeros((y_len, 200))
            myFile = np.hstack((h_add, myFile))
            x_len += 200
            center_x += 200
        fill_left(-12, 0, distance1)
        if center_y + 14 + distance1 > y_len:
            v_add = np.zeros((200, x_len))
            myFile = np.vstack((myFile, v_add))
            y_len += 200
        fill_up(-1, 14, distance2)


def fill_up(offset_x, offset_y, dist):
    global myFile
    grid_count = 0
    grid_adj = 0
    start_y = center_y + offset_y
    start_x = center_x + offset_x
    for i in range(start_y, start_y + dist + 1):
        start_p = start_x - grid_adj
        end_p = start_x + grid_adj + 1
        if start_p < 0:
            start_p = 0
        if end_p > x_len:
            end_p = x_len

        if i == start_y + dist:  # At termination point
            if dist <= 50:  # Designated certain wall distance
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < 3, 3, temp_data)
                myFile[i, start_p:end_p] = temp_data2
            else:  # tentative wall
                temp_data = myFile[i, start_p+grid_adj//2:end_p-grid_adj//2]
                temp_data2 = np.where(temp_data < 3, 2, temp_data)
                myFile[i, start_p+grid_adj//2:end_p-grid_adj//2] = temp_data2
        else:  # in scanned region
            if dist <= 50:  # Designated certain traversable space distance
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < 3, 1, temp_data)
                myFile[i, start_p:end_p] = temp_data2
            else:  # tentative traversable space
                if i - start_y < 50:
                    update_param = 3
                else:
                    update_param = 1
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < update_param, 1, temp_data)
                myFile[i, start_p:end_p] = temp_data2
        grid_count += 1
        if grid_count == 8:
            grid_adj += 1
            grid_count = 0
        if i == start_y + 200:
            break


def fill_right(offset_x, offset_y, dist):
    global myFile
    grid_count = 0
    grid_adj = 0
    start_x = center_x + offset_x
    start_y = center_y + offset_y
    for i in range(start_x, start_x + dist + 1):
        start_p = start_y - grid_adj
        end_p = start_y + grid_adj + 1
        if start_p < 0:
            start_p = 0
        if end_p > x_len:
            end_p = x_len

        if i == start_x + dist:  # At termination point
            if dist <= 50:  # Designated certain wall distance
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < 3, 3, temp_data)
                myFile[start_p:end_p, i] = temp_data2
            else:  # tentative wall
                temp_data = myFile[start_p+grid_adj//2:end_p-grid_adj//2, i]
                temp_data2 = np.where(temp_data < 3, 2, temp_data)
                myFile[start_p+grid_adj//2:end_p-grid_adj//2, i] = temp_data2
        else:  # in scanned region
            if dist <= 50:  # Designated certain traversable space distance
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < 3, 1, temp_data)
                myFile[start_p:end_p, i] = temp_data2
            else:  # tentative traversable space
                if i - start_x < 50:
                    update_param = 3
                else:
                    update_param = 1
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < update_param, 1, temp_data)
                myFile[start_p:end_p, i] = temp_data2
        grid_count += 1
        if grid_count == 8:
            grid_adj += 1
            grid_count = 0
        if i == start_x + 200:
            break


def fill_down(offset_x, offset_y, dist):
    global myFile
    grid_count = 0
    grid_adj = 0
    start_y = center_y + offset_y
    start_x = center_x + offset_x
    for i in range(start_y, start_y - dist - 1, -1):
        start_p = start_x - grid_adj
        end_p = start_x + grid_adj + 1
        if start_p < 0:
            start_p = 0
        if end_p > x_len:
            end_p = x_len

        if i == start_y - dist:  # At termination point
            if dist <= 50:  # Designated certain wall distance
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < 3, 3, temp_data)
                myFile[i, start_p:end_p] = temp_data2
            else:  # tentative wall
                temp_data = myFile[i, start_p+grid_adj//2:end_p-grid_adj//2]
                temp_data2 = np.where(temp_data < 3, 2, temp_data)
                myFile[i, start_p+grid_adj//2:end_p-grid_adj//2] = temp_data2
        else:  # in scanned region
            if dist <= 50:  # Designated certain traversable space distance
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < 3, 1, temp_data)
                myFile[i, start_p:end_p] = temp_data2
            else:  # tentative traversable space
                if i - start_y > -50:
                    update_param = 3
                else:
                    update_param = 1
                temp_data = myFile[i, start_p:end_p]
                temp_data2 = np.where(temp_data < update_param, 1, temp_data)
                myFile[i, start_p:end_p] = temp_data2
        grid_count += 1
        if grid_count == 8:
            grid_adj += 1
            grid_count = 0
        if i == start_y - 200:
            break


def fill_left(offset_x, offset_y, dist):
    global myFile
    grid_count = 0
    grid_adj = 0
    start_y = center_y + offset_y
    start_x = center_x + offset_x
    for i in range(start_x, start_x-dist-1, -1):
        start_p = start_y - grid_adj
        end_p = start_y + grid_adj + 1
        if start_p < 0:
            start_p = 0
        if end_p > x_len:
            end_p = x_len

        if i == start_x - dist:  # At termination point
            if dist <= 50:  # Designated certain wall distance
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < 3, 3, temp_data)
                myFile[start_p:end_p, i] = temp_data2
            else:  # tentative wall
                temp_data = myFile[start_p+grid_adj//2:end_p-grid_adj//2, i]
                temp_data2 = np.where(temp_data < 3, 2, temp_data)
                myFile[start_p+grid_adj//2:end_p-grid_adj//2, i] = temp_data2
        else:  # in scanned region
            if dist <= 50:  # Designated certain traversable space distance
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < 3, 1, temp_data)
                myFile[start_p:end_p, i] = temp_data2
            else:  # tentative traversable space
                if i - start_x > -50:
                    update_param = 3
                else:
                    update_param = 1
                temp_data = myFile[start_p:end_p, i]
                temp_data2 = np.where(temp_data < update_param, 1, temp_data)
                myFile[start_p:end_p, i] = temp_data2
        grid_count += 1
        if grid_count == 8:
            grid_adj += 1
            grid_count = 0
        if i == start_x - 200:
            break


def plot_color(dataset):
    plt.figure(figsize=(7, 6))
    plt.pcolormesh(dataset)
    plt.colorbar()
    plt.show()


def interpret_response():
    data1 = s.recv(1024)
    sdata1 = data1.decode('utf-8')

    while sdata1[-1] != '!':
        time.sleep(1)
        data1 = s.recv(1024)
        sdata1 = sdata1 + data1.decode('utf-8')

    inc_message = sdata1.strip()
    trim_message = inc_message.rstrip('!')
    print(trim_message)

    #  Interpret data into space map
    index = trim_message.find(',')

    distance1 = int(trim_message[0:index])
    distance2 = int(trim_message[index+1:])

    vision_grid(distance1, distance2)


def scan_up():
    travel = 75
    tail = 75
    check_tail = True
    for i in range(center_y, center_y+56):
        array_check = myFile[i, center_x-r_width-4:center_x+r_width+5]
        if (3 in array_check) or (2 in array_check):
            travel = i - center_y
            break
        if i - center_y < r_height+4:
            continue
        if check_tail and (myFile[i, center_x] == 4):
            tail = i - center_y
            check_tail = False
    return travel, tail


def scan_down():
    travel = 75
    tail = 75
    check_tail = True
    for i in range(center_y, center_y-56, -1):
        array_check = myFile[i, center_x-r_width-4:center_x+r_width+5]
        if (3 in array_check) or (2 in array_check):
            travel = (i - center_y)*-1
            break
        if center_y - i < r_height+4:
            continue
        if check_tail and (myFile[i, center_x] == 4):
            tail = (i - center_y)*-1
            check_tail = False
    return travel, tail


def scan_right():
    travel = 75
    tail = 75
    check_tail = True
    for i in range(center_x, center_x+56):
        array_check = myFile[center_y-r_width-4:center_y+r_width+5, i]
        if (3 in array_check) or (2 in array_check):
            travel = i - center_x
            break
        if i - center_x < r_height+4:
            continue
        if check_tail and (myFile[center_y, i] == 4):
            tail = i - center_x
            check_tail = False
    return travel, tail


def scan_left():
    travel = 75
    tail = 75
    check_tail = True
    for i in range(center_x, center_x-56, -1):
        array_check = myFile[center_y-r_width-4:center_y+r_width+5, i]
        if (3 in array_check) or (2 in array_check):
            travel = (i - center_x)*-1
            break
        if center_x - i < r_height+4:
            continue
        if check_tail and (myFile[center_y, i] == 4):
            tail = (i - center_x)*-1
            check_tail = False
    return travel, tail


def scan_around():
    or0 = or1 = or2 = or3 = 0
    skip = 0
    for i in range(0, 150):
        if or0 == 0:
            skip += 1
            array_check1 = myFile[center_y+i+r_height, center_x-3*r_width:center_x+3*r_width]
            array_check2 = myFile[center_y+i-r_height, center_x-r_width:center_x+r_width+1]
            if 3 in array_check1:
                or0 = -1
            elif (0 in array_check2) or (1 in array_check2):
                or0 = i
        if or1 == 0:
            skip += 1
            array_check1 = myFile[center_y-3*r_width:center_y+3*r_width, center_x+i+r_height]
            array_check2 = myFile[center_y-r_width:center_y+r_width+1, center_x+i-r_height]
            if 3 in array_check1:
                or1 = -1
            elif (0 in array_check2) or (1 in array_check2):
                or1 = i
        if or2 == 0:
            skip += 1
            array_check1 = myFile[center_y-i-r_height, center_x-3*r_width:center_x+3*r_width]
            array_check2 = myFile[center_y-i+r_height, center_x-r_width:center_x+r_width+1]
            if 3 in array_check1:
                or2 = -1
            elif (0 in array_check2) or (1 in array_check2):
                or2 = i
        if or3 == 0:
            skip += 1
            array_check1 = myFile[center_y-3*r_width:center_y+3*r_width, center_x-i-r_height]
            array_check2 = myFile[center_y-r_width:center_y+r_width+1, center_x-i+r_height]
            if 3 in array_check1:
                or3 = -1
            elif (0 in array_check2) or (1 in array_check2):
                or3 = i
        if skip == 0:
            return or0, or1, or2, or3
        skip = 0

    return or0, or1, or2, or3


def spin_left():
    global may_adjust
    out_message = b'0231460'  # Timing may need to change
    s.sendall(out_message)
    may_adjust = False

    print('Spun left')

    global orientation
    global center_x
    global center_y
    if orientation == 0:
        orientation = 6
        center_y = center_y - 3
        center_x = center_x - 4
    elif orientation == 2:
        orientation = 0
        center_y = center_y + 4
        center_x = center_x - 3
    elif orientation == 4:
        orientation = 2
        center_y = center_y + 3
        center_x = center_x + 4
    else:
        orientation = 4
        center_y = center_y - 4
        center_x = center_x + 3

    update_traversed_stat()

    time.sleep(1)


def spin_right():
    global may_adjust
    out_message = b'2031460'  # Timing may need to change
    s.sendall(out_message)
    may_adjust = False

    print('Spun right')

    global orientation
    global center_x
    global center_y
    if orientation == 0:
        orientation = 2
        center_y = center_y - 3
        center_x = center_x + 4
    elif orientation == 2:
        orientation = 4
        center_y = center_y - 4
        center_x = center_x - 3
    elif orientation == 4:
        orientation = 6
        center_y = center_y + 3
        center_x = center_x - 4
    else:
        orientation = 0
        center_y = center_y + 4
        center_x = center_x + 3

    update_traversed_stat()

    time.sleep(1)


def turn_right():
    global may_adjust
    out_message = b'1032750'  # Timing may need to change
    s.sendall(out_message)
    may_adjust = False

    print('Turned right')

    global orientation
    global center_x
    global center_y
    if orientation == 0:
        orientation = 2
        center_y = center_y + 7
        center_x = center_x + 15
    elif orientation == 2:
        orientation = 4
        center_y = center_y - 15
        center_x = center_x + 7
    elif orientation == 4:
        orientation = 6
        center_y = center_y - 7
        center_x = center_x - 15
    else:
        orientation = 0
        center_y = center_y + 15
        center_x = center_x - 7

    update_traversed_stat()

    time.sleep(1)


def turn_left():
    global may_adjust
    out_message = b'0132750'  # Timing may need to change
    s.sendall(out_message)
    may_adjust = False

    print('Turned left')

    global orientation
    global center_x
    global center_y
    if orientation == 0:
        orientation = 6
        center_y = center_y + 7
        center_x = center_x - 15
    elif orientation == 2:
        orientation = 0
        center_y = center_y + 15
        center_x = center_x + 7
    elif orientation == 4:
        orientation = 2
        center_y = center_y - 7
        center_x = center_x + 15
    else:
        orientation = 4
        center_y = center_y - 15
        center_x = center_x - 7

    update_traversed_stat()

    time.sleep(1)


def explore_forward(cm, scan):
    global may_adjust
    timestep = str(round(73.9 * cm + 40.4))

    while len(timestep) < 4:
        timestep = '0' + timestep

    exp_message = '00' + scan + timestep
    update_traversed_dyn(cm)
    exp_message2 = exp_message.encode('utf-8')
    s.sendall(exp_message2)
    may_adjust = True
    print('Moved forward (cm): ' + str(cm))


def move_backwards(cm, scan):
    global clean_step
    global clean_seq
    global center_x
    global center_y
    timestep = str(round(73.9 * cm + 40.4))

    while len(timestep) < 4:
        timestep = '0' + timestep

    exp_message = '22' + scan + timestep
    clean_seq.append(exp_message)

    if orientation == 0:
        center_y -= cm
    elif orientation == 2:
        center_x -= cm
    elif orientation == 4:
        center_y += cm
    else:
        center_x += cm


def update_traversed_stat():
    # Updates the map after rotation
    global myFile
    global center_x
    global center_y
    if orientation == 0:
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = 4
    elif orientation == 2:
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = 4
    elif orientation == 4:
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = 4
    else:
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = 4


def update_traversed_dyn(dist):
    # Updates the map after moving
    global myFile
    global center_x
    global center_y
    global done_count
    if orientation == 0:
        check_array = myFile[center_y+r_height:center_y+r_height+dist+1, center_x-r_width:center_x+r_width+1]
        change_count = np.count_nonzero(check_array == 0) + np.count_nonzero(check_array == 1)
        if change_count < 10 * dist:
            done_count += 1
        else:
            done_count = 0
        myFile[center_y+r_height:center_y+r_height+dist+1, center_x-r_width:center_x+r_width+1] = 4
        center_y = center_y + dist
    elif orientation == 2:
        check_array = myFile[center_y-r_width:center_y+r_width+1, center_x+r_height:center_x+r_height+dist+1]
        change_count = np.count_nonzero(check_array == 0) + np.count_nonzero(check_array == 1)
        if change_count < 10 * dist:
            done_count += 1
        else:
            done_count = 0
        myFile[center_y-r_width:center_y+r_width+1, center_x+r_height:center_x+r_height+dist+1] = 4
        center_x = center_x + dist
    elif orientation == 4:
        check_array = myFile[center_y-r_height-dist:center_y-r_height+1, center_x-r_width:center_x+r_width+1]
        change_count = np.count_nonzero(check_array == 0) + np.count_nonzero(check_array == 1)
        if change_count < 10 * dist:
            done_count += 1
        else:
            done_count = 0
        myFile[center_y-r_height-dist:center_y-r_height+1, center_x-r_width:center_x+r_width+1] = 4
        center_y = center_y - dist
    else:
        check_array = myFile[center_y-r_width:center_y+r_width+1, center_x-r_height-dist:center_x-r_height+1]
        change_count = np.count_nonzero(check_array == 0) + np.count_nonzero(check_array == 1)
        if change_count < 10 * dist:
            done_count += 1
        else:
            done_count = 0
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height-dist:center_x-r_height+1] = 4
        center_x = center_x - dist


def movement():
    global explore_complete
    global phase
    global phase_2_count
    global phase_3_count
    travel0, tail0 = scan_up()
    travel2, tail2 = scan_right()
    travel4, tail4 = scan_down()
    travel6, tail6 = scan_left()
    travel_list = [travel0, travel2, travel4, travel6]
    tail_list = [tail0, tail2, tail4, tail6]
    if max(tail_list) < 20:
        phase = 2
        phase_2_count = 20
    # Check to hug the right wall
    if phase == 1:
        print('phase 1')
        if phase_2_count > 0:
            phase_2_count -= 1
        front_dir = orientation // 2
        right_dir = front_dir + 1
        if right_dir == 4:
            right_dir = 0
        if travel_list[right_dir] > 40:
            if tail_list[right_dir] < 20:
                pass
            elif travel_list[right_dir] < 48:
                spin_right()
                interpret_response()
                explore_forward(travel_list[right_dir] - 32, '3')
                interpret_response()
                spin_left()
                return
            elif travel_list[front_dir] > 44:
                explore_forward(15, '3')
                interpret_response()
                spin_right()
                return
            else:
                explore_forward(travel_list[front_dir] - 22, '3')
                interpret_response()
                spin_right()
                return
        if travel_list[front_dir] > 32:
            if travel_list[right_dir] > 40:
                if travel_list[front_dir] > 63:
                    explore_forward(45, '3')
                    return
                else:
                    explore_forward(travel_list[front_dir] - 32, '3')
                    interpret_response()
                    spin_left()
                    return
            if not may_adjust:
                explore_forward(8, '3')
                return
            elif travel_list[front_dir] > 47:
                if tail_list[front_dir] < 35:
                    phase = 2
                explore_forward(15, '3')
                return
            else:
                explore_forward(travel_list[front_dir] - 32, '3')
                return
        else:
            spin_left()
            return
    if phase == 2:
        print('phase 2')
        if phase_2_count < 20:
            phase = 1
            phase_2_count += 5
        p2_list = [min(tail0, travel0-45), min(tail2, travel2-45), min(tail4, travel4-45), min(tail6, travel6-45)]
        front_dir = orientation // 2
        right_dir = front_dir + 1
        left_dir = front_dir - 1
        back_dir = front_dir + 2
        if right_dir == 4:
            right_dir = 0
        if left_dir == -1:
            left_dir = 3
        if back_dir > 3:
            back_dir -= 4
        if p2_list[right_dir] > 20:
            spin_right()
            interpret_response()
            explore_forward(min(p2_list[right_dir] - 14, 15), '3')
            return
        elif p2_list[front_dir] > 20:
            explore_forward(min(p2_list[front_dir] - 14, 15), '3')
            return
        elif p2_list[left_dir] > 20:
            spin_left()
            interpret_response()
            explore_forward(min(p2_list[left_dir] - 14, 15), '3')
            return
        else:
            phase_3_count += 1
            if phase_3_count >= 5:
                explore_complete = True
                return
            dir0, dir1, dir2, dir3 = scan_around()
            p3_list = [dir0, dir1, dir2, dir3]
            if p3_list[front_dir] >= r_height:
                explore_forward(p3_list[front_dir] - 8, '3')
                return
            elif p3_list[right_dir] >= r_height:
                spin_left()
                interpret_response()
                explore_forward(p3_list[right_dir] - 8, '3')
                return
            elif p3_list[left_dir] >= r_height:
                spin_right()
                interpret_response()
                explore_forward(p3_list[left_dir] - 8, '3')
                return
            elif p3_list[back_dir] >= r_height:
                spin_left()
                interpret_response()
                spin_left()
                interpret_response()
                explore_forward(p3_list[back_dir] - 8, '3')
                return
            else:
                explore_complete = True
    return


def fill_up_ones(l_wall, y, r_wall):
    global newspacemap
    jj = y
    x = (l_wall + r_wall) // 2
    i = x
    prev_l_wall = l_wall
    prev_r_wall = r_wall
    new_down_starts = []
    new_up_starts = []
    while newspacemap[jj, i] != 3 and newspacemap[jj, i] != 1:
        # left pass
        while newspacemap[jj, i] != 3:
            if newspacemap[jj - 1, i] == 1 or newspacemap[jj - 1, i] == 3:
                newspacemap[jj, i] = 1
            if newspacemap[jj - 1, i] == 0:
                newspacemap[jj, i] = 1
                if newspacemap[jj - 1, i + 1] == 3:  # right edge of new section below
                    new_down_starts.append(i)
                    new_down_starts.append(jj-1)
                if newspacemap[jj - 1, i - 1] == 3:  # usual case, left edge of new section
                    new_down_starts.append(i)
                elif newspacemap[jj, i - 1] == 3:  # fringe case, perfect mismatch
                    new_down_starts.append(i)
            i -= 1
        if i > prev_l_wall + 20:  # checks for a new section above that got cut off
            for ii in range(i, prev_l_wall, -1):
                if newspacemap[jj, ii] == 0:
                    if newspacemap[jj, ii + 1] == 3:  # right edge
                        new_up_starts.append(ii)
                        new_up_starts.append(jj)
                    if newspacemap[jj, ii - 1] == 3:  # usual case, left edge
                        new_up_starts.append(ii)
                    elif newspacemap[jj - 1, ii - 1] == 3:  # fringe case, perfect mismatch
                        new_up_starts.append(ii)
        prev_l_wall = i

        # right pass
        i = x + 1
        while newspacemap[jj, i] != 3:
            if newspacemap[jj - 1, i] == 1 or newspacemap[jj - 1, i] == 3:
                newspacemap[jj, i] = 1
            if newspacemap[jj - 1, i] == 0:
                newspacemap[jj, i] = 1
                if newspacemap[jj - 1, i - 1] == 3:  # left edge
                    new_down_starts.append(i)
                    new_down_starts.append(jj-1)
                if newspacemap[jj - 1, i + 1] == 3:  # usual case, right edge
                    new_down_starts.append(i)
                elif newspacemap[jj, i + 1] == 3:  # fringe case, perfect mismatch
                    new_down_starts.append(i)
            i += 1
        if i < prev_r_wall - 20:
            for ii in range(i, prev_r_wall):
                if newspacemap[jj, ii] == 0:
                    if newspacemap[jj, ii - 1] == 3:  # left edge
                        new_up_starts.append(ii)
                        new_up_starts.append(jj)
                    if newspacemap[jj, ii + 1] == 3:  # usual case, right edge
                        new_up_starts.append(ii)
                    elif newspacemap[jj - 1, ii + 1] == 3:  # fringe case, perfect mismatch
                        new_up_starts.append(ii)
        prev_r_wall = i
        # find a good starting point
        start_found = False
        x = (prev_r_wall + prev_l_wall) // 2
        for ii in range(1, x-prev_l_wall):
            if newspacemap[jj+1, x+ii] == 0:
                i = x+ii
                start_found = True
                break
            if newspacemap[jj+1, x-ii] == 0:
                i = x-ii
                start_found = True
                break
        if not start_found:
            i = x

        jj += 1

    # recursive part
    length_up = len(new_up_starts) // 3
    for i in range(0, length_up):
        var1 = (new_up_starts[length_up*3] + new_up_starts[length_up*3 + 2]) // 2
        var2 = max(new_up_starts[length_up*3], new_up_starts[length_up*3 + 2])
        fill_up_ones(var1, new_up_starts[length_up*3 + 1], var2)

    length_up = len(new_down_starts) // 3
    for i in range(0, length_up):
        var1 = (new_up_starts[length_up*3] + new_up_starts[length_up*3 + 2]) // 2
        var2 = min(new_up_starts[length_up*3], new_up_starts[length_up*3 + 2])
        fill_up_ones(var1, new_down_starts[length_up*3 + 1], var2)
    return


def fill_down_ones(r_wall, y, l_wall):
    global newspacemap
    jj = y
    x = (r_wall + l_wall) // 2
    i = x
    prev_l_wall = l_wall
    prev_r_wall = r_wall
    new_down_starts = []
    new_up_starts = []
    while newspacemap[jj, i] != 3 and newspacemap[jj, i] != 1:
        # left pass
        while newspacemap[jj, i] != 3:
            if newspacemap[jj + 1, i] == 1 or newspacemap[jj + 1, i] == 3:
                newspacemap[jj, i] = 1
            if newspacemap[jj + 1, i] == 0:
                newspacemap[jj, i] = 1
                if newspacemap[jj + 1, i + 1] == 3:  # right edge
                    new_up_starts.append(i)
                    new_up_starts.append(jj+1)
                if newspacemap[jj + 1, i - 1] == 3:  # usual left edge
                    new_up_starts.append(i)
                elif newspacemap[jj, i - 1] == 3:  # fringe left edge
                    new_up_starts.append(i)
            i -= 1
        if i > prev_l_wall + 20:
            for ii in range(i, prev_l_wall, -1):
                if newspacemap[jj, ii] == 0:
                    if newspacemap[jj, ii + 1] == 3:  # right edge
                        new_down_starts.append(ii)
                        new_down_starts.append(jj)
                    if newspacemap[jj, ii - 1] == 3:  # usual left edge
                        new_down_starts.append(ii)
                    elif newspacemap[jj - 1, ii - 1] == 3:  # fringe left edge
                        new_down_starts.append(ii)
        prev_l_wall = i

        # right pass
        i = x + 1
        while newspacemap[jj, i] != 3:
            if newspacemap[jj + 1, i] == 1 or newspacemap[jj + 1, i] == 3:
                newspacemap[jj, i] = 1
            if newspacemap[jj + 1, i] == 0:
                newspacemap[jj, i] = 1
                if newspacemap[jj + 1, i - 1] == 3:  # left edge
                    new_up_starts.append(i)
                    new_up_starts.append(jj+1)
                if newspacemap[jj + 1, i + 1] == 3:  # usual right edge
                    new_up_starts.append(i)
                elif newspacemap[jj, i + 1] == 3:  # fringe right edge
                    new_up_starts.append(i)
            i += 1
        if i < prev_r_wall - 20:
            for ii in range(i, prev_r_wall):
                if newspacemap[jj, ii] == 0:
                    if newspacemap[jj, ii - 1] == 3:  # left edge
                        new_down_starts.append(ii)
                        new_down_starts.append(jj)
                    if newspacemap[jj, ii + 1] == 3:  # usual right edge
                        new_down_starts.append(ii)
                    elif newspacemap[jj + 1, ii + 1] == 3:  # fringe right edge
                        new_down_starts.append(ii)
        prev_r_wall = i
        # find a good starting point
        start_found = False
        x = (prev_r_wall + prev_l_wall) // 2
        for ii in range(1, x-prev_l_wall):
            if newspacemap[jj-1, x+ii] == 0:
                i = x+ii
                start_found = True
                break
            if newspacemap[jj-1, x-ii] == 0:
                i = x-ii
                start_found = True
                break
        if not start_found:
            i = x
        jj -= 1

    # recursive part
    length_up = len(new_up_starts) // 3
    for i in range(0, length_up):
        var1 = (new_up_starts[length_up*3] + new_up_starts[length_up*3 + 2]) // 2
        var2 = max(new_up_starts[length_up*3], new_up_starts[length_up*3 + 2])
        fill_up_ones(var1, new_up_starts[length_up*3 + 1], var2)

    length_up = len(new_down_starts) // 3
    for i in range(0, length_up):
        var1 = (new_up_starts[length_up*3] + new_up_starts[length_up*3 + 2]) // 2
        var2 = min(new_up_starts[length_up*3], new_up_starts[length_up*3 + 2])
        fill_up_ones(var1, new_down_starts[length_up*3 + 1], var2)

    return


def clean_right(option):
    global clean_seq
    if option:
        move_backwards(7, '1')

    out_message = '1032750'  # Timing may need to change
    clean_seq.append(out_message)

    global orientation
    global center_x
    global center_y
    global myFile
    global clean_step
    if orientation == 0:
        orientation = 2
        center_y = center_y + 7
        center_x = center_x + 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    elif orientation == 2:
        orientation = 4
        center_x = center_x + 7
        center_y = center_y - 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step
    elif orientation == 4:
        orientation = 6
        center_y = center_y - 7
        center_x = center_x - 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    else:
        orientation = 0
        center_x = center_x - 7
        center_y = center_y + 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step

    clean_step = clean_step + 0.1
    time.sleep(1)


def clean_reverse_right():
    global clean_seq
    global orientation
    global center_x
    global center_y
    global myFile
    global clean_step

    out_message = '1232750'  # Timing may need to change
    clean_seq.append(out_message)

    if orientation == 2:
        orientation = 0
        center_y = center_y - 7
        center_x = center_x - 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    elif orientation == 4:
        orientation = 2
        center_x = center_x - 7
        center_y = center_y + 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step
    elif orientation == 6:
        orientation = 4
        center_y = center_y + 7
        center_x = center_x + 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    else:
        orientation = 6
        center_x = center_x + 7
        center_y = center_y - 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step

    clean_step = clean_step + 0.1
    time.sleep(1)


def clean_left(option):
    global clean_seq
    if option:
        move_backwards(7, '1')

    out_message = '0132750'  # Timing may need to change
    clean_seq.append(out_message)

    global orientation
    global center_x
    global center_y
    global myFile
    global clean_step
    if orientation == 0:
        orientation = 6
        center_y = center_y + 7
        center_x = center_x - 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    elif orientation == 2:
        orientation = 0
        center_x = center_x + 7
        center_y = center_y + 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step
    elif orientation == 4:
        orientation = 2
        center_y = center_y - 7
        center_x = center_x + 15
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height:center_x+r_height+1] = clean_step
    else:
        orientation = 4
        center_x = center_x - 7
        center_y = center_y - 15
        myFile[center_y-r_height:center_y+r_height+1, center_x-r_width:center_x+r_width+1] = clean_step

    clean_step = clean_step + 0.1
    time.sleep(1)


def clean_up(cm, scan):
    time_step = str(round(73.9 * cm + 40.4))

    while len(time_step) < 4:
        time_step = '0' + time_step

    exp_message = '00' + scan + time_step

    global myFile
    global center_x
    global center_y
    global clean_step
    global clean_seq
    if orientation == 0:
        myFile[center_y+r_height:center_y+r_height+cm+1, center_x-r_width:center_x+r_width+1] = clean_step
        center_y = center_y + cm
    elif orientation == 2:
        myFile[center_y-r_width:center_y+r_width+1, center_x+r_height:center_x+r_height+cm+1] = clean_step
        center_x = center_x + cm
    elif orientation == 4:
        myFile[center_y-r_height-cm:center_y-r_height+1, center_x-r_width:center_x+r_width+1] = clean_step
        center_y = center_y - cm
    else:
        myFile[center_y-r_width:center_y+r_width+1, center_x-r_height-cm:center_x-r_height+1] = clean_step
        center_x = center_x - cm

    clean_step = clean_step + 0.1
    clean_seq.append(exp_message)


def clean_scan():
    three_list = [0, 0, 0, 0]  # nearest wall
    four_list = [0, 0, 0, 0]  # nearest cleaned space
    one_list = [0, 0, 0, 0]  # nearest uncleaned space on the right

    i = center_y + r_height + 1  # scan up
    three_not_found = True
    four_not_found = True
    one_not_found = True
    while three_not_found:
        if 3 in myFile[i, center_x-r_width:center_x+r_width+1]:
            three_list[0] = i - center_y
            if one_not_found:
                one_list[0] = i - center_y
            if four_not_found:
                four_list[0] = i - center_y
            break
        if four_not_found:
            if (myFile[i, center_x-r_width: center_x+r_width+1] >= 4).all():
                four_list[0] = i - center_y
                four_not_found = False
        if one_not_found:
            if myFile[i, center_x+r_width+1] == 1:
                one_list[0] = i - center_y
                one_not_found = False
        i += 1

    i = center_y - r_height - 1  # scan down
    three_not_found = True
    four_not_found = True
    one_not_found = True
    while three_not_found:
        if myFile[i, center_x] == 3:
            three_list[2] = center_y - i
            if one_not_found:
                one_list[2] = center_y - i
            if four_not_found:
                four_list[2] = center_y - i
            break
        if four_not_found:
            if (myFile[i, center_x-r_width: center_x+r_width+1] >= 4).all():
                four_list[2] = center_y - i
                four_not_found = False
        if one_not_found:
            if myFile[i, center_x-r_width-1] == 1:
                one_list[2] = center_y - i
                one_not_found = False
        i -= 1

    i = center_x + r_height + 1  # scan right
    three_not_found = True
    four_not_found = True
    one_not_found = True
    while three_not_found:
        if myFile[center_y, i] == 3:
            three_list[1] = i - center_x
            if one_not_found:
                one_list[1] = i - center_x
            if four_not_found:
                four_list[1] = i - center_x
            break
        if four_not_found:
            if (myFile[center_y-r_width:center_y+r_width+1, i] >= 4).all():
                four_list[1] = i - center_x
                four_not_found = False
        if one_not_found:
            if myFile[center_y-r_width-1, i] == 1:
                one_list[1] = i - center_x
                one_not_found = False
        i += 1

    i = center_x - r_height - 1  # scan left
    three_not_found = True
    four_not_found = True
    one_not_found = True
    while three_not_found:
        if myFile[center_y, i] == 3:
            three_list[3] = center_x - i
            if one_not_found:
                one_list[3] = center_x - i
            if four_not_found:
                four_list[3] = center_x - i
            break
        if four_not_found:
            if (myFile[center_y-r_width:center_y+r_width+1, i] >= 4).all():
                four_list[3] = center_x - i
                four_not_found = False
        if one_not_found:
            if myFile[center_y+r_width+1, i] == 1:
                one_list[3] = center_x - i
                one_not_found = False
        i -= 1

    return one_list, three_list, four_list


def clean_search():
    global xx
    global yy
    global clean_complete
    global myFile

    while xx < x_dim:
        while yy < y_dim:
            if myFile[yy, xx] == 1:
                success_ccw, path_1 = clean_path(xx, yy, True)
                success_cw, path_2 = clean_path(xx, yy, False)

                if not (success_cw or success_ccw):
                    myFile[yy, xx] = 0
                elif success_ccw and (not success_cw):
                    interpret_path(path_1)
                elif success_cw and (not success_ccw):
                    interpret_path(path_2)
                elif len(path_1) < len(path_2):
                    interpret_path(path_1)
                else:
                    interpret_path(path_2)
                return

            yy += 1
        xx += 1
        yy = 0

    clean_complete = True
    return


def interpret_path(path):
    for iteration in range(0, len(path)):
        if path[iteration] == 'l':
            clean_left(True)
            move_backwards(15, '1')
        elif path[iteration] == 'r':
            clean_right(True)
            move_backwards(15, '1')
        else:
            clean_up(path[iteration], '3')

        # interpret_response()
    return


def check_path(direction, current_x, current_y, intended):
    if direction == 0:
        for i in range(current_y + r_height, intended + r_height + 1):
            if 3 in myFile[i, current_x-r_width:current_x+r_width+1]:
                return i - current_y - r_height - 1, False
        return intended - current_y, True
    elif direction == 4:
        for i in range(current_y - r_height, intended - r_height - 1, -1):
            if 3 in myFile[i, current_x-r_width:current_x+r_width+1]:
                return (i - current_y + 1) * -1 - r_height, False
        return (intended - current_y) * -1, True
    elif direction == 2:
        for i in range(current_x + r_height, intended + r_height + 1):
            if 3 in myFile[current_y-r_width:current_y+r_width+1, i]:
                return i - current_x - r_height - 1, False
        return intended - current_x, True
    elif direction == 6:
        for i in range(current_x - r_height, intended - r_height, -1):
            if 3 in myFile[current_y-r_width:current_y+r_width, i]:
                return (i - current_x + 1) * -1 - r_height, False
        return (intended - current_x) * -1, True


def change_orientation(target_orientation, current_orientation):
    if current_orientation - target_orientation == 0:
        return []
    elif current_orientation - target_orientation == 2:
        return ['l']
    elif current_orientation - target_orientation == 4:
        return ['l', 'l']
    elif current_orientation - target_orientation == 6:
        return ['r']
    elif current_orientation - target_orientation == -2:
        return ['r']
    elif current_orientation - target_orientation == -4:
        return ['r', 'r']
    else:
        return ['l']


def update_position(cur_or, distance, x_cur, y_cur):
    if cur_or == 0:
        y_new = y_cur + distance
        x_new = x_cur
    elif cur_or == 2:
        x_new = x_cur + distance
        y_new = y_cur
    elif cur_or == 4:
        y_new = y_cur - distance
        x_new = x_cur
    else:
        x_new = x_cur - distance
        y_new = y_cur
    return x_new, y_new


def convolutional_smoothing(x_start, y_start):
    global newspacemap
    dir_check = [0, 0, 0, 0]
    if 3 in newspacemap[y_start:y_start+6, x_start:x_start+6]:
        if 3 in newspacemap[y_start+6, x_start:x_start+6]:
            dir_check[0] = 1
        if 3 in newspacemap[y_start:y_start+6, x_start+6]:
            dir_check[1] = 1
        if 3 in newspacemap[y_start-1, x_start:x_start+6]:
            dir_check[2] = 1
        if 3 in newspacemap[y_start:y_start+6, x_start-1]:
            dir_check[3] = 1
        if dir_check.count(1) == 0:
            newspacemap[y_start:y_start+6, x_start:x_start+6] = 0
        elif dir_check.count(1) == 1:
            newspacemap[y_start:y_start+6, x_start:x_start+6] = 0
            if dir_check[0] == 1:
                convolutional_smoothing(x_start, y_start+1)
            elif dir_check[1] == 1:
                convolutional_smoothing(x_start+1, y_start)
            elif dir_check[2] == 1:
                convolutional_smoothing(x_start, y_start-1)
            else:
                convolutional_smoothing(x_start-1, y_start)
    return


def try_to_match(x_cur, y_cur, x_target, y_target):
    if x_cur == x_target:
        if y_target > y_cur:
            for h_adj in range(0, r_width+1):
                if not(3 in myFile[y_cur-r_height:y_target+1, x_cur+h_adj-r_width:x_cur+h_adj-r_width+1]):
                    return True, [2, 0], [h_adj, y_target-y_cur-r_height]
                elif not(3 in myFile[y_cur-r_height:y_target+1, x_cur-h_adj-r_width:x_cur-h_adj-r_width+1]):
                    return True, [6, 0], [h_adj, y_target-y_cur-r_height]
            return False, 0, 0
        if y_target < y_cur:
            for h_adj in range(0, r_width+1):
                if not(3 in myFile[y_target:y_cur+r_height+1, x_cur+h_adj-r_width:x_cur+h_adj-r_width+1]):
                    return True, [2, 4], [h_adj, y_cur-r_height-y_target]
                elif not(3 in myFile[y_target:y_cur+r_height+1, x_cur-h_adj-r_width:x_cur-h_adj-r_width+1]):
                    return True, [6, 4], [h_adj, y_cur-r_height-y_target]
            return False, 0, 0
    if y_cur == y_target:
        if x_target > x_cur:
            for h_adj in range(0, r_width+1):
                if not(3 in myFile[y_cur+h_adj-r_width:y_cur+h_adj+r_width+1, x_cur-r_height:x_target+1]):
                    return True, [0, 2], [h_adj, x_target-x_cur-r_height]
                elif not(3 in myFile[y_cur-h_adj-r_width:y_cur-h_adj+r_width+1, x_cur-r_height:x_target+1]):
                    return True, [4, 2], [h_adj, x_target-x_cur-r_height]
            return False, 0, 0
        if x_target < x_cur:
            for h_adj in range(0, r_width+1):
                if not(3 in myFile[y_cur+h_adj-r_width:y_cur+h_adj+r_width+1, x_target:x_cur-r_height+1]):
                    return True, [0, 6], [h_adj, x_cur-r_height-x_target]
                elif not(3 in myFile[y_cur-h_adj-r_width:y_cur-h_adj+r_width+1, x_target:x_cur-r_height+1]):
                    return True, [4, 6], [h_adj, x_cur-r_height-x_target]
            return False, 0, 0
    return


def check_ahead(cur_or, cur_x, cur_y):
    if cur_or == 0:
        if 3 in myFile[cur_y+r_height+1, cur_x-r_width:cur_x+r_width+1]:
            return True
        else:
            return False
    elif cur_or == 2:
        if 3 in myFile[cur_y-r_width:cur_y+r_width, cur_x+r_height+1]:
            return True
        else:
            return False
    elif cur_or == 4:
        if myFile[cur_y-r_height-1, cur_x-r_width:cur_x+r_width+1] == 3:
            return True
        else:
            return False
    else:
        if myFile[cur_y-r_width:cur_y+r_width+1, cur_x-r_height-1] == 3:
            return True
        else:
            return False


def check_path_ahead(cur_or, cur_x, cur_y, target_x, target_y, rot):
    # rot is whether the rotation is ccw (True) or cw (False)
    # returns 1) the distance to travel, 2) whether or not the distance was cut short
    # to allow movement to destination, and 3) whether it was stopped because the
    # right wall is no longer being hugged.
    dist_travel = 1
    if rot:
        if cur_or == 0:
            while True:
                if 3 in myFile[cur_y+r_height+dist_travel, cur_x-r_width:cur_x+r_width+1]:
                    dist_travel -= 1
                    if cur_y < target_y <= cur_y+dist_travel:
                        return target_y - cur_y, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y+dist_travel-r_height:cur_y+dist_travel+r_height+1, cur_x+r_width+1]):
                    if cur_y < target_y <= cur_y+dist_travel:
                        return target_y - cur_y, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        elif cur_or == 2:
            while True:
                if 3 in myFile[cur_y-r_width:cur_y+r_width+1, cur_x+r_height+dist_travel]:
                    dist_travel -= 1
                    if cur_x < target_x <= cur_x+dist_travel:
                        return target_x - cur_x, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y-r_width-1, cur_x+dist_travel-r_height:cur_x+dist_travel+r_height+1]):
                    if cur_x < target_x <= cur_x+dist_travel:
                        return target_x - cur_x, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        elif cur_or == 4:
            while True:
                if 3 in myFile[cur_y-r_height-dist_travel, cur_x-r_width:cur_x+r_width+1]:
                    dist_travel -= 1
                    if cur_y > target_y >= cur_y-dist_travel:
                        return cur_y - target_y, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y-dist_travel-r_height:cur_y-dist_travel+r_height+1, cur_x-r_width-1]):
                    if cur_y > target_y >= cur_y-dist_travel:
                        return cur_y - target_y, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        else:
            while True:
                if 3 in myFile[cur_y-r_width:cur_y+r_width+1, cur_x-r_height-dist_travel]:
                    dist_travel -= 1
                    if cur_x > target_x >= cur_x-dist_travel:
                        return cur_x - target_x, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y+r_width+1, cur_x+dist_travel-r_height:cur_x+dist_travel+r_height+1]):
                    if cur_x > target_x >= cur_x-dist_travel:
                        return cur_x - target_x, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
    else:
        if cur_or == 0:
            while True:
                if 3 in myFile[cur_y+r_height+dist_travel, cur_x-r_width:cur_x+r_width+1]:
                    dist_travel -= 1
                    if cur_y < target_y <= cur_y+dist_travel:
                        return target_y - cur_y, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y+dist_travel-r_height:cur_y+dist_travel+r_height+1, cur_x-r_width-1]):
                    if cur_y < target_y <= cur_y+dist_travel:
                        return target_y - cur_y, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        elif cur_or == 2:
            while True:
                if 3 in myFile[cur_y-r_width:cur_y+r_width+1, cur_x+r_height+dist_travel]:
                    dist_travel -= 1
                    if cur_x < target_x <= cur_x+dist_travel:
                        return target_x - cur_x, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y+r_width+1, cur_x+dist_travel-r_height:cur_x+dist_travel+r_height+1]):
                    if cur_x < target_x <= cur_x+dist_travel:
                        return target_x - cur_x, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        elif cur_or == 4:
            while True:
                if 3 in myFile[cur_y-r_height-dist_travel, cur_x-r_width:cur_x+r_width+1]:
                    dist_travel -= 1
                    if cur_y > target_y >= cur_y-dist_travel:
                        return cur_y - target_y, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y-dist_travel-r_height:cur_y-dist_travel+r_height+1, cur_x+r_width+1]):
                    if cur_y > target_y >= cur_y-dist_travel:
                        return cur_y - target_y, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1
        else:
            while True:
                if 3 in myFile[cur_y-r_width:cur_y+r_width+1, cur_x-r_height-dist_travel]:
                    dist_travel -= 1
                    if cur_x > target_x >= cur_x-dist_travel:
                        return cur_x - target_x, True, False
                    else:
                        return dist_travel, False, False
                if not (3 in myFile[cur_y-r_width-1, cur_x+dist_travel-r_height:cur_x+dist_travel+r_height+1]):
                    if cur_x > target_x >= cur_x-dist_travel:
                        return cur_x - target_x, True, True
                    else:
                        return dist_travel, False, True
                dist_travel += 1


def clean_path(x_target, y_target, ccw):
    path = []
    x_cur = center_x
    y_cur = center_y
    or_cur = orientation
    try_counter = 0
    path_found = False

    # x first, ccw
    if x_target - x_cur < -1 * r_width:
        path = path + change_orientation(6, or_cur)
        or_cur = 6
        x_inc, success_check = check_path(or_cur, x_cur, y_cur, x_target)
        path.append(x_inc)
        x_cur, y_cur = update_position(or_cur, x_inc, x_cur, y_cur)
    elif x_target - x_cur > r_width:
        path = path + change_orientation(2, or_cur)
        or_cur = 2
        x_inc, success_check = check_path(or_cur, x_cur, y_cur, x_target)
        path.append(x_inc)
        x_cur, y_cur = update_position(or_cur, x_inc, x_cur, y_cur)
    else:
        success_check = True

    if success_check:
        if y_target - y_cur < -1 * r_width:
            path = path + change_orientation(4, or_cur)
            or_cur = 4
            y_inc, success_check = check_path(or_cur, x_cur, y_cur, y_target)
            path.append(y_inc)
            x_cur, y_cur = update_position(or_cur, y_inc, x_cur, y_cur)
        elif y_target - y_cur > r_width:
            path = path + change_orientation(0, or_cur)
            or_cur = 0
            y_inc, success_check = check_path(or_cur, x_cur, y_cur, y_target)
            path.append(y_inc)
            x_cur, y_cur = update_position(or_cur, y_inc, x_cur, y_cur)

        if (abs(x_cur - x_target) < r_width) and (abs(y_cur - y_target) < r_width):
            return True, path

    if ccw:
        while try_counter < 3:
            if (x_cur-r_width < x_target < x_cur+r_width) and (y_cur-r_width < y_target < y_cur+r_width):
                path_found = True
                break

            if (x_cur == x_target) or (y_cur == y_target):
                path_found, or_des, dist_des = try_to_match(x_cur, y_cur, x_target, y_target)
                if path_found:
                    path = path + change_orientation(or_des[0], or_cur)
                    path.append(dist_des[0])
                    path = path + change_orientation(or_des[1], or_cur)
                    path.append(dist_des[1])
                    break
                else:
                    try_counter += 1

            if check_ahead(or_cur, x_cur, y_cur):
                path.append('l')
                or_cur -= 2
                if or_cur < 0:
                    or_cur += 8
            else:
                f_movement, intersect, sec_rot = check_path_ahead(or_cur, x_cur, y_cur, x_target, y_target, True)
                if intersect:
                    path.append(f_movement)
                    x_cur, y_cur = update_position(or_cur, f_movement, x_cur, y_cur)
                    continue
                else:
                    path.append(f_movement)
                    x_cur, y_cur = update_position(or_cur, f_movement, x_cur, y_cur)

                if sec_rot:
                    path.append('r')
                    or_cur += 2
                    if or_cur > 6:
                        or_cur -= 8
    else:
        while try_counter < 3:
            if (x_cur-r_width < x_target < x_cur+r_width) and (y_cur-r_width < y_target < y_cur+r_width):
                path_found = True
                break

            if (x_cur == x_target) or (y_cur == y_target):
                path_found, or_des, dist_des = try_to_match(x_cur, y_cur, x_target, y_target)
                if path_found:
                    path = path + change_orientation(or_des[0], or_cur)
                    path.append(dist_des[0])
                    path = path + change_orientation(or_des[1], or_cur)
                    path.append(dist_des[1])
                    break
                else:
                    try_counter += 1

            if check_ahead(or_cur, x_cur, y_cur):
                path.append('r')
                or_cur += 2
                if or_cur > 6:
                    or_cur -= 8
            else:
                f_movement, intersect, sec_rot = check_path_ahead(or_cur, x_cur, y_cur, x_target, y_target, False)
                if intersect:
                    path.append(f_movement)
                    x_cur, y_cur = update_position(or_cur, f_movement, x_cur, y_cur)
                    continue
                else:
                    path.append(f_movement)
                    x_cur, y_cur = update_position(or_cur, f_movement, x_cur, y_cur)

                if sec_rot:
                    path.append('l')
                    or_cur -= 2
                    if or_cur < 0:
                        or_cur += 8

    return path_found, path


def clean_movement():
    one_list, three_list, four_list = clean_scan()
    # Check to hug the right perimeter
    front_dir = orientation // 2
    front = min(three_list[front_dir], four_list[front_dir])
    if max(four_list) <= r_height+2:  # if surrounded by cleaned area
        clean_search()
        return
    if one_list[front_dir] >= front:
        # if the distance to next wall or cleaned area is less than the
        # distance to next uncleaned area on the right
        i = 1
        if orientation == 0:  # check distance to left wall
            while myFile[center_y+front-1, center_x-r_width-i] != 3:
                i += 1
        elif orientation == 2:
            while myFile[center_y+r_width+i, center_x+front-1] != 3:
                i += 1
        elif orientation == 4:
            while myFile[center_y-front+1, center_x+r_width+i] != 3:
                i += 1
        else:
            while myFile[center_y-r_width-i, center_x-front+1] != 3:
                i += 1

        if i < 15:
            ii = 0
            r_adj1 = r_width+15
            r_adj2 = r_width+7
            while True:
                if orientation == 0:
                    if not (3 in myFile[center_y-r_adj1-ii:center_y+r_width-ii+1, center_x-r_width:center_x+r_adj2+1]):
                        break
                elif orientation == 2:
                    if not (3 in myFile[center_y-r_adj2:center_y+r_width+1, center_x-r_adj1-ii:center_x+r_width-ii+1]):
                        break
                elif orientation == 4:
                    if not (3 in myFile[center_y-r_width+ii:center_y+r_adj1+ii+1, center_x-r_adj2:center_x+r_width+1]):
                        break
                else:
                    if not (3 in myFile[center_y-r_width:center_y+r_adj2+1, center_x-r_width+ii:center_x+r_adj1+ii+1]):
                        break
                ii += 1

            clean_up(front - 1 - r_height, '3')
            move_backwards(front - 1 - r_height + ii, '3')
            clean_reverse_right()
            clean_up(i+6, '3')
            clean_right(True)
            clean_up(front + ii - r_height - 1, '3')
            move_backwards(front + ii - r_height - 1, '3')
            clean_reverse_right()
            clean_left(False)

        else:
            clean_up(front - 1 - r_height, '3')
            clean_left(True)
        return
    else:  # there is an uncleaned area before the next wall or cleaned area
        # check how deep the uncleaned area is
        i = 1
        if orientation == 0:
            while myFile[center_y+one_list[front_dir], center_x+r_width+i] == 1:
                i += 1
        elif orientation == 2:
            while myFile[center_y-r_width-i, center_x+one_list[front_dir]] == 1:
                i += 1
        elif orientation == 4:
            while myFile[center_y-one_list[front_dir], center_x-r_width-i] == 1:
                i += 1
        else:
            while myFile[center_y+r_width+i, center_x-one_list[front_dir]] == 1:
                i += 1

        if i < 15:
            if one_list[front_dir] > 1:
                clean_up(one_list[front_dir] - r_height - 1, '3')
            clean_left(False)
            clean_right(False)
            clean_right(False)
            clean_up(i + 6, '3')
        else:
            clean_up(one_list[front_dir] + r_height, '3')
            clean_right(True)
        return


mode = 2

if mode == 0:  # Change to True to engage search and explore mode
    myFile = np.genfromtxt('/Users/Games/Documents/SpaceMaps/data1000.csv', delimiter=',')

    HOST = '192.168.4.1'
    PORT = 80

    center_x = 500
    center_y = 500
    y_len, x_len = myFile.shape
    r_width = 14
    r_height = 14
    dist1 = 0
    orientation = 0
    explore_complete = False
    phase = 1
    phase_2_count = 0
    phase_3_count = 0
    done_count = 0
    may_adjust = False
    prev_dist = 0
    update_traversed_stat()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        explore_forward(10, '3')

        while True:
            #  Receive data from arduino
            interpret_response()

            #  Save to file
            np.savetxt('/Users/Games/Documents/SpaceMaps/data_room_2.csv', myFile, delimiter=',')

            #  Determine new instruction
            movement()

            #  Check for completion
            if explore_complete:
                break
            if done_count >= 5:
                break

    plot_color(myFile)

if mode == 1:  # Change to True to engage direct communication with ESP8266
    HOST = '192.168.4.1'
    PORT = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            message = input('send:')
            bytemessage = message.encode('utf-8')
            s.sendall(bytemessage)

            data = s.recv(1024)
            sdata = data.decode('utf-8')

            while sdata[-1] != '!':
                time.sleep(1)
                data = s.recv(1024)
                sdata = sdata + data.decode('utf-8')

            print('Received: ', sdata)

if mode == 2:  # plot space map : change to true to reach
    myFile = np.genfromtxt('/Users/Games/Documents/SpaceMaps/data_room_example.csv', delimiter=',')
    plot_color(myFile)

if mode == 3:  # smooth space map
    myFile = np.genfromtxt('/Users/Games/Documents/SpaceMaps/data_room_2.csv', delimiter=',')

    # first figure out the bounds of the space
    y_min = 0
    y_max = 1
    x_min = 0
    x_max = 1
    y_dim, x_dim = myFile.shape
    newspacemap = np.zeros((y_dim, x_dim))
    for j in range(0, y_dim):
        line_check = myFile[j, :]
        if (3 in line_check) or (4 in line_check):
            y_min = j
            break
    for j in range(y_dim - 1, -1, -1):
        line_check = myFile[j, :]
        if (3 in line_check) or (4 in line_check):
            y_max = j
            break
    for j in range(0, x_dim):
        line_check = myFile[:, j]
        if (3 in line_check) or (4 in line_check):
            x_min = j
            break
    for j in range(x_dim - 1, -1, -1):
        line_check = myFile[:, j]
        if (3 in line_check) or (4 in line_check):
            x_max = j
            break

    # start sampling rows and cols
    local_min = 0
    local_max = 0
    continuous = False
    line_length = 0
    ex_top = 0
    ex_bot = 0
    for j in range(y_min, y_max+1):
        line_check = myFile[j, x_min:x_max+1]
        if np.count_nonzero(line_check == 3) > 4:
            line_check = myFile[j:j+2, x_min:x_max+1]
            for k in range(x_min, x_max+1):
                if 3 in myFile[j:j+2, k]:
                    if not continuous:
                        local_min = k
                        continuous = True
                    line_length += 1
                else:
                    if continuous:
                        local_max = k
                        continuous = False
                        if line_length > 4:
                            for h in range(0, 52):
                                if (myFile[j, local_max+h] == 4) or (myFile[j+1, local_max+h] == 4):
                                    ex_top = h-1
                                    break
                                if h == 51:
                                    ex_top = h

                            for h in range(0, 52):
                                if (myFile[j, local_min-h] == 4) or (myFile[j+1, local_min-h] == 4):
                                    ex_bot = h-1
                                    break
                                if h == 51:
                                    ex_bot = h
                            newspacemap[j:j+2, local_min-ex_bot:local_max+ex_top] = 3
                        line_length = 0

    for k in range(x_min, x_max+1):
        line_check = myFile[y_min:y_max+1, k]
        if np.count_nonzero(line_check == 3) > 4:
            line_check = myFile[y_min:y_max+1, k:k+2]
            for j in range(y_min, y_max+1):
                if 3 in myFile[j, k:k+2]:
                    if not continuous:
                        local_min = j
                        continuous = True
                    line_length += 1
                else:
                    if continuous:
                        local_max = j
                        continuous = False
                        if line_length > 4:
                            for h in range(0, 52):
                                if (myFile[local_max+h, k] == 4) or (myFile[local_max+h, k+1] == 4):
                                    ex_top = h-1
                                    break
                                if h == 51:
                                    ex_top = h

                            for h in range(0, 52):
                                if (myFile[local_min-h, k] == 4) or (myFile[local_min-h, k+1] == 4):
                                    ex_bot = h-1
                                    break
                                if h == 51:
                                    ex_bot = h
                            newspacemap[local_min-ex_bot:local_max+ex_top, k:k+2] = 3
                        line_length = 0

    # Accommodate for new boundaries
    y_min -= 50
    y_max += 50
    x_min -= 50
    x_max += 50
    if y_min < 0:
        y_min = 0
    if x_min < 0:
        x_min = 0
    if y_max > y_dim:
        y_max = y_dim
    if x_max > x_dim:
        x_max = x_dim

    # connect small segments of walls
    for j in range(y_min, y_max+1):
        local_min = local_max = x_min
        for k in range(x_min, x_max):
            if newspacemap[j, k] == 3:
                local_min = local_max
                local_max = k
                if 2 < local_max - local_min < 30:
                    newspacemap[j, local_min:local_max] = 3

    for k in range(x_min, x_max):
        local_min = local_max = y_min
        for j in range(y_min, y_max+1):
            if newspacemap[j, k] == 3:
                local_min = local_max
                local_max = j
                if 2 < local_max - local_min < 30:
                    newspacemap[local_min:local_max, k] = 3

    # smooth edges
    for j in range(y_min+1, y_max-5):
        for k in range(x_min+1, x_max-5):
            convolutional_smoothing(k, j)

    # make interior spaces equal to 1
    center_x = 500
    center_y = 500
    j = center_x
    while newspacemap[center_y, j] != 3:
        newspacemap[center_y, j] = 1
        j -= 1
    begin_x1 = j + 1
    begin_y1 = center_y + 1
    j = center_x + 1
    while newspacemap[center_y, j] != 3:
        newspacemap[center_y, j] = 1
        j += 1
    begin_x2 = j - 1
    begin_y2 = center_y - 1
    fill_up_ones(begin_x1, begin_y1, begin_x2)
    fill_down_ones(begin_x2, begin_y2, begin_x1)

    # remove extra space
    for j in range(0, y_dim):
        if 3 in newspacemap[j, :]:
            y_min = j
            break
    for j in range(y_dim-1, 0, -1):
        if 3 in newspacemap[j, :]:
            y_max = j+1
            break
    for k in range(0, x_dim):
        if 3 in newspacemap[:, k]:
            x_min = k
            break
    for k in range(x_dim-1, 0, -1):
        if 3 in newspacemap[:, k]:
            x_max = k+1
            break

    trimmedspacemap = newspacemap[y_min:y_max, x_min:x_max]

    np.savetxt('/Users/Games/Documents/SpaceMaps/data_room_2_smoothed.csv', trimmedspacemap, delimiter=',')
    plot_color(trimmedspacemap)

if mode == 4:  # make the cleaning sequence and export as csv file
    myFile = np.genfromtxt('/Users/Games/Documents/SpaceMaps/data_room_2_smoothed.csv', delimiter=',')
    center_x = 343
    center_y = 24
    xx = 0
    yy = 0
    r_width = 14
    r_height = 14
    orientation = 0
    clean_complete = False
    y_dim, x_dim = myFile.shape
    clean_step = 4
    clean_seq = []

    update_traversed_stat()
    clean_step = clean_step + 0.1

    while not clean_complete:
        clean_movement()

    plot_color(myFile)
    np.savetxt('/Users/Games/Documents/SpaceMaps/data_room_2_pathing.csv', myFile, delimiter=',')
    # Do not run this segment twice, make a new blank txt doc and change the name
    with open('/Users/Games/Documents/SpaceMaps/data_room_2_sequence.txt', 'w') as filehandle:
        for element in clean_seq:
            filehandle.write('%s\n' % element)

if mode == 5:
    HOST = '192.168.4.1'
    PORT = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # First make it to the left corner
        bytemessage = b'3310010'
        s.sendall(bytemessage)

        data = s.recv(1024)
        sdata = data.decode('utf-8')

        while sdata[-1] != '!':
            time.sleep(1)
            data = s.recv(1024)
            sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

        bytemessage = b'0132750'
        s.sendall(bytemessage)

        data = s.recv(1024)
        sdata = data.decode('utf-8')

        while sdata[-1] != '!':
            time.sleep(1)
            data = s.recv(1024)
            sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

        # made it to the first wall
        bytemessage = b'3310010'
        s.sendall(bytemessage)

        data = s.recv(1024)
        sdata = data.decode('utf-8')

        while sdata[-1] != '!':
            time.sleep(1)
            data = s.recv(1024)
            sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

        bytemessage = b'0132750'
        s.sendall(bytemessage)

        data = s.recv(1024)
        sdata = data.decode('utf-8')

        while sdata[-1] != '!':
            time.sleep(1)
            data = s.recv(1024)
            sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

        bytemessage = b'2211075'
        s.sendall(bytemessage)

        data = s.recv(1024)
        sdata = data.decode('utf-8')

        while sdata[-1] != '!':
            time.sleep(1)
            data = s.recv(1024)
            sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

        # start cleaning sequence
        with open('/Users/Games/Documents/SpaceMaps/data_room_2_sequence.txt', 'r') as filehandle:
            file_content = filehandle.readlines()
        for element in file_content:
            instruction = element[:-1]
            if len(instruction) > 7:
                partial = int(instruction[3:])
                while partial // 10000 >= 1:
                    message = instruction[:3]+'9999'
                    bytemessage = message.encode('utf-8')
                    s.sendall(bytemessage)
                    partial -= 9999
                partial = str(partial)
                while len(partial) < 4:
                    partial = '0' + partial
                message = instruction[:3]+partial
                bytemessage = message.encode('utf-8')
                s.sendall(bytemessage)
            else:
                message = instruction
                bytemessage = message.encode('utf-8')
                s.sendall(bytemessage)

            data = s.recv(1024)
            sdata = data.decode('utf-8')
    
            while sdata[-1] != '!':
                time.sleep(1)
                data = s.recv(1024)
                sdata = sdata + data.decode('utf-8')

        print('Received: ', sdata)

if mode == 6:  # test code
    pass
