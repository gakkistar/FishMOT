import random

def match_fish(iou_info):
    '''
    iou_info: 一个字典，包含当前帧每条鱼与下一帧每条鱼的iou信息，格式为{fish_id: [(next_fish_id_1, iou_1), (next_fish_id_2, iou_2), ...]}
    返回值: 一个字典，包含每条鱼的匹配信息，格式为{fish_id: matched_next_fish_id}
    '''
    matched_dict = {} # 存储匹配信息
    assigned_next_fish = set() # 存储已经分配的下一帧鱼的ID

    # 先处理iou较大且没有其他iou或者其他iou很小的鱼类id
    sorted_iou_info = sorted(iou_info.items(), key=lambda x: max([y[1] for y in x[1]]), reverse=True)
    for fish_id, next_fish_iou_list in sorted_iou_info:
        next_fish_iou_list = sorted(next_fish_iou_list, key=lambda x: x[1], reverse=True)
        next_fish_id = next_fish_iou_list[0][0]
        iou = next_fish_iou_list[0][1]
        if next_fish_id not in assigned_next_fish and (iou > 0.5 or (iou > 0.3 and len(next_fish_iou_list) == 1)):
            matched_dict[fish_id] = next_fish_id
            assigned_next_fish.add(next_fish_id)

    # 再处理iou为0或者有两个大小相似的iou的鱼类id
    unassigned_fish = set(iou_info.keys()) - set(matched_dict.keys())
    for fish_id in unassigned_fish:
        next_fish_iou_list = iou_info[fish_id]
        next_fish_iou_list = sorted(next_fish_iou_list, key=lambda x: x[1], reverse=True)
        next_fish_id = next_fish_iou_list[0][0]
        iou = next_fish_iou_list[0][1]
        if iou == 0:
            continue
        if len(next_fish_iou_list) > 1 and next_fish_iou_list[0][1] - next_fish_iou_list[1][1] < 0.1:
            continue
        if next_fish_id in assigned_next_fish:
            continue
        matched_dict[fish_id] = next_fish_id
        assigned_next_fish.add(next_fish_id)

    return matched_dict


def unmatch_fish(iou_info, fish_position):
    '''
    iou_info: 一个字典，包含当前帧每条鱼与下一帧每条鱼的iou信息，格式为{fish_id: [(next_fish_id_1, iou_1), (next_fish_id_2, iou_2), ...]}
    fish_position: 一个字典，包含当前帧每条鱼的位置信息，格式为{fish_id: (x, y)}
    返回值: 一个字典，包含每条鱼的匹配信息和位置信息，格式为{fish_id: (matched_next_fish_id, (x, y))}
           一个列表，包含未匹配的鱼类ID，格式为[fish_id_1, fish_id_2, ...]
    '''
    matched_dict = {} # 存储匹配信息和位置信息
    assigned_next_fish = set() # 存储已经分配的下一帧鱼的ID

    # 先处理iou较大且没有其他iou或者其他iou很小的鱼类id
    sorted_iou_info = sorted(iou_info.items(), key=lambda x: max([y[1] for y in x[1]]), reverse=True)
    for fish_id, next_fish_iou_list in sorted_iou_info:
        next_fish_iou_list = sorted(next_fish_iou_list, key=lambda x: x[1], reverse=True)
        next_fish_id = next_fish_iou_list[0][0]
        iou = next_fish_iou_list[0][1]
        if next_fish_id not in assigned_next_fish and (iou > 0.5 or (iou > 0.3 and len(next_fish_iou_list) == 1)):
            matched_dict[fish_id] = (next_fish_id, fish_position[fish_id])
            assigned_next_fish.add(next_fish_id)

    # 再处理iou为0或者有两个大小相似的iou的鱼类id
    unassigned_fish = set(iou_info.keys()) - set(matched_dict.keys())
    for fish_id in unassigned_fish:
        next_fish_iou_list = iou_info[fish_id]
        next_fish_iou_list = sorted(next_fish_iou_list, key=lambda x: x[1], reverse=True)
        next_fish_id = next_fish_iou_list[0][0]
        iou = next_fish_iou_list[0][1]
        if iou == 0:
            continue
        if len(next_fish_iou_list) > 1 and next_fish_iou_list[0][1] - next_fish_iou_list[1][1] < 0.1:
            continue
        if next_fish_id in assigned_next_fish:
            continue
        matched_dict[fish_id] = (next_fish_id, fish_position[fish_id])
        assigned_next_fish.add(next_fish_id)

    unmatched_fish = list(set(iou_info.keys()) - set(matched_dict.keys()))
    return matched_dict, unmatched_fish


def save_positions(matched_dict, file_path, frame):
    with open(file_path, 'a') as f:
        for fish_id, position in matched_dict.items():
            f.write(f'{str(int(fish_id))} {str(int(position[0]))} {position[1][0]} {position[1][1]} {position[1][2]} {position[1][3]}\n')


def save_fish_position(fish_position, file_path):
    '''
    将鱼的位置信息保存到文本文件
    fish_position: 一个字典，包含每条鱼的位置信息，格式为{fish_id: (x, y)}
    file_path: 保存文本文件的路径
    '''
    with open(file_path, 'a') as f:
        for fish_id, position in fish_position.items():
            f.write(str(fish_id) + ' ' + str(position[0]) + ' ' + str(position[1]) + '\n')

def load_fish_position(file_path):
    '''
    从文本文件读取鱼的位置信息并按照位置和ID信息将每条鱼关联起来
    file_path: 保存位置信息的文本文件路径
    返回值: 一个列表，包含每条鱼的位置和匹配信息，格式为[(fish_id_1, (x_1, y_1), matched_next_fish_id_1), (fish_id_2, (x_2, y_2), matched_next_fish_id_2), ...]
    '''
    fish_list = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        lines = [line.strip().split(' ') for line in lines]
        fish_id_to_position = {int(line[0]): (float(line[1]), float(line[2])) for line in lines}
        fish_id_to_matched_next_fish_id = {}
        for i in range(len(lines)):
            if i == len(lines) - 1:
                # 处理最后一个鱼类
                fish_id, position = int(lines[i][0]), fish_id_to_position[int(lines[i][0])]
                fish_list.append((fish_id, position, None))
            else:
                # 处理中间的鱼类
                fish_id, position = int(lines[i][0]), fish_id_to_position[int(lines[i][0])]
                matched_next_fish_id = int(lines[i+1][1])
                fish_list.append((fish_id, position, matched_next_fish_id))
                fish_id_to_matched_next_fish_id[fish_id] = matched_next_fish_id
        # 处理未匹配的鱼类
        for fish_id in fish_id_to_position.keys() - fish_id_to_matched_next_fish_id.keys():
            position = fish_id_to_position[fish_id]
            fish_list.append((fish_id, position, None))
    return fish_list


def save_matched_fish_info(fish_list, file_path):
    '''
    将所有鱼类的位置和匹配信息保存到文本文件
    fish_list: 包含每条鱼的位置和匹配信息的列表，格式为[(fish_id_1, (x_1, y_1), matched_next_fish_id_1), (fish_id_2, (x_2, y_2), matched_next_fish_id_2), ...]
    file_path: 保存文本文件的路径
    '''
    with open(file_path, 'a') as f:
        for fish_id, position, matched_next_fish_id in fish_list:
            if matched_next_fish_id is None:
                f.write(str(fish_id) + ' ' + str(position[0]) + ' ' + str(position[1]) + ' ' + str(matched_next_fish_id) + '\n')
            else:
                f.write(str(fish_id) + ' ' + str(position[0]) + ' ' + str(position[1]) + ' ' + str(matched_next_fish_id) + '\n')




def match_fishes(iou_dict):
    fish_ids = list(iou_dict.keys())
    next_fish_ids = set([next_fish_id for iou_list in iou_dict.values() for next_fish_id, iou in iou_list if iou > 0])
    matched_next_fish_ids = {next_fish_id: None for next_fish_id in next_fish_ids}
    fish_matches = {fish_id: None for fish_id in fish_ids}
    fish_iou_lists = {fish_id: sorted(iou_list, key=lambda x: -x[1]) for fish_id, iou_list in iou_dict.items()}

    # Match fish with high iou and no other matches or low iou matches
    for fish_id in fish_ids:
        for next_fish_id, iou in fish_iou_lists[fish_id]:
            if iou == 0:
                continue
            if matched_next_fish_ids[next_fish_id] is None or iou >= 0.5 * fish_iou_lists[next_fish_id][0][1]:
                fish_matches[fish_id] = next_fish_id
                matched_next_fish_ids[next_fish_id] = fish_id
                break

    # Match fish with low iou matches or no matches
    for fish_id in fish_ids:
        if fish_matches[fish_id] is None:
            for next_fish_id, iou in fish_iou_lists[fish_id]:
                if iou == 0:
                    continue
                if matched_next_fish_ids[next_fish_id] is None:
                    fish_matches[fish_id] = next_fish_id
                    matched_next_fish_ids[next_fish_id] = fish_id
                    break

    # Assign random matches for fish with iou=0
    unmatched_fish_ids = [fish_id for fish_id in fish_ids if fish_matches[fish_id] is None]
    random.shuffle(unmatched_fish_ids)
    unmatched_next_fish_ids = [next_fish_id for next_fish_id in next_fish_ids if matched_next_fish_ids[next_fish_id] is None]
    random.shuffle(unmatched_next_fish_ids)
    for fish_id, next_fish_id in zip(unmatched_fish_ids, unmatched_next_fish_ids):
        fish_matches[fish_id] = next_fish_id

    return fish_matches



def match_fish_byid(iou_dict):
    # Initialize matched_dict, unmatched_ids and zero_iou_ids
    matched_dict = {fish_id: -1 for fish_id in iou_dict.keys()}
    unmatched_ids = list(iou_dict.keys())
    zero_iou_ids = [fish_id for fish_id, iou_list in iou_dict.items() if all(iou == 0 for _, iou in iou_list)]

    # Sort iou_dict by max iou value
    sorted_iou_list = [(fish_id, iou_list) for fish_id, iou_list in iou_dict.items()]
    sorted_iou_list.sort(key=lambda x: max([iou for _, iou in x[1]]), reverse=True)

    # Match fish by iou value
    for fish_id, iou_list in sorted_iou_list:
        if fish_id in zero_iou_ids:
            unmatched_ids.remove(fish_id)
            continue

        max_iou = max([iou for _, iou in iou_list])
        other_max_iou_ids = [next_fish_id for next_fish_id, iou in iou_list if iou == max_iou and next_fish_id in unmatched_ids]

        if max_iou == 0 or (len(other_max_iou_ids) > 1):
            unmatched_ids.remove(fish_id)
            continue

        if len(other_max_iou_ids) == 1:
            matched_dict[fish_id] = other_max_iou_ids[0]
            unmatched_ids.remove(fish_id)
            unmatched_ids.remove(other_max_iou_ids[0])
        else:
            match_fish_id = -1
            match_iou = -1
            for next_fish_id, iou in iou_list:
                if next_fish_id in unmatched_ids and iou > match_iou:
                    match_fish_id = next_fish_id
                    match_iou = iou
            if match_fish_id != -1:
                matched_dict[fish_id] = match_fish_id
                unmatched_ids.remove(fish_id)
                unmatched_ids.remove(match_fish_id)

    # Randomly match zero iou fish
    for zero_iou_id in zero_iou_ids:
        if unmatched_ids:
            match_id = random.choice(unmatched_ids)
            matched_dict[zero_iou_id] = match_id
            unmatched_ids.remove(match_id)

    return matched_dict


def match_fish_po(iou_info, fish_position):
    matched_fish = {}
    next_fish_matched = set()
    iou_threshold = 0.5  # 可调整iou阈值

    # 分配iou较大且没有其他iou或者其他iou很小的鱼类id
    for fish_id, iou_list in iou_info.items():
        iou_list.sort(key=lambda x: x[1], reverse=True)
        next_fish_id, iou = iou_list[0]
        if iou >= iou_threshold:
            if next_fish_id not in next_fish_matched:
                matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                next_fish_matched.add(next_fish_id)

    # 分配其他的id
    next_fish_unmatched = set(iou_info.keys()) - next_fish_matched
    for fish_id in fish_position.keys():
        if fish_id not in matched_fish.keys():

            if next_fish_unmatched:
                print('----')
                print(fish_id)
                matched_next_fish_id = next_fish_unmatched.pop()
                matched_fish[fish_id] = (matched_next_fish_id, fish_position[fish_id])

    # 分配iou为0的鱼类在没有被匹配到的鱼类id上
    for fish_id, iou_list in iou_info.items():
        if fish_id not in matched_fish.keys():
            iou_list.sort(key=lambda x: x[1], reverse=True)
            next_fish_id, iou = iou_list[0]
            if iou == 0:
                for i in range(len(iou_list)):
                    next_fish_id, _ = iou_list[i]
                    if next_fish_id not in next_fish_matched:
                        matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                        next_fish_matched.add(next_fish_id)
                        break

    return matched_fish


def match_fish_po1(iou_info, fish_position, frame):
    matched_fish = {}
    next_fish_matched = set()
    iou_threshold = 0.01  # 可调整iou阈值

    # 分配iou较大且没有其他iou或者其他iou很小的鱼类id
    for fish_id, iou_list in iou_info.items():
        iou_list.sort(key=lambda x: x[1], reverse=True)
        next_fish_id, iou = iou_list[0]
        if iou >= iou_threshold:
            if next_fish_id not in next_fish_matched:
                matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                next_fish_matched.add(next_fish_id)
            else:
                for i in range(1, len(iou_list)):
                    next_fish_id, iou = iou_list[i]
                    if iou >= iou_threshold and next_fish_id not in next_fish_matched:
                        matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                        next_fish_matched.add(next_fish_id)
                        break

        # 分配iou较小的鱼类id
        else:
            for i in range(len(iou_list)):
                next_fish_id, iou = iou_list[i]
                if iou >= iou_threshold and next_fish_id not in next_fish_matched:
                    matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                    next_fish_matched.add(next_fish_id)
                    break

    # 分配其他的id
    next_fish_unmatched = set(iou_info.keys()) - next_fish_matched
    for fish_id, iou_list in iou_info.items():
        if fish_id not in matched_fish.keys():

            if next_fish_unmatched:
                matched_next_fish_id = next_fish_unmatched.pop()
                matched_fish[fish_id] = (matched_next_fish_id, fish_position[fish_id])

    # 分配iou不大但比列表里其他iou大的鱼类id
    for fish_id, iou_list in iou_info.items():
        if fish_id not in matched_fish.keys():
            iou_list.sort(key=lambda x: x[1], reverse=True)
            for next_fish_id, iou in iou_list:
                if iou < iou_threshold and next_fish_id not in next_fish_matched:
                    matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                    next_fish_matched.add(next_fish_id)
                    break

    # 分配iou不大但没有其他iou的鱼类id
    for fish_id, iou_list in iou_info.items():
        if fish_id not in matched_fish.keys():
            iou_list.sort(key=lambda x: x[1], reverse=True)
            next_fish_id, iou = iou_list[0]
            if iou < iou_threshold:
                for i in range(len(iou_list)):
                    next_fish_id, iou = iou_list[i]
                    if iou < iou_threshold and next_fish_id not in next_fish_matched:
                        matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                        next_fish_matched.add(next_fish_id)
                        break

    # 分配iou都为0的鱼类在没有被匹配到的鱼类id上
    for fish_id, iou_list in iou_info.items():
        if fish_id not in matched_fish.keys():
            iou_list.sort(key=lambda x: x[1], reverse=True)
            next_fish_id, iou = iou_list[0]
            if iou == 0:
                for i in range(len(iou_list)):
                    next_fish_id, _ = iou_list[i]
                    if next_fish_id not in next_fish_matched:
                        matched_fish[fish_id] = (next_fish_id, fish_position[fish_id])
                        next_fish_matched.add(next_fish_id)
                        break

    return matched_fish, frame