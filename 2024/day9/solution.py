def part1(instructions) -> int:
    curr_id = 0
    free_space = False
    blocks = []
    for num in instructions[0]:
        count = int(num)
        if free_space:
            blocks.extend([None] * count)
            free_space = False
        else:
            blocks.extend([curr_id] * count)
            free_space = True
            curr_id += 1

    for i in range(len(blocks)):
        if blocks[i] is None:
            for j in range(len(blocks) - 1, i, -1):
                if blocks[j] is not None:
                    blocks[i], blocks[j] = blocks[j], None
                    break

    checksum = 0
    for i, block in enumerate(blocks):
        if block is not None:
            checksum += block * i

    return checksum

def part2(instructions) -> int:
    curr_id = 0
    free_space = False
    blocks = []
    for num in instructions[0]:
        count = int(num)
        if free_space:
            blocks.append([None] * count)
            free_space = False
        else:
            blocks.append([curr_id] * count)
            free_space = True
            curr_id += 1
    
    for block_index in range(len(blocks))[::-1]:
        if all(data is None for data in blocks[block_index]):
            continue
        for check_block_index in range(block_index):
            if len([data for data in blocks[check_block_index] if data is None]) >= len(blocks[block_index]):
                len_free_space = len(blocks[check_block_index])
                len_data = len(blocks[block_index])
                blocks[check_block_index] = [None] * (len_free_space - len(blocks[block_index]))
                blocks.insert(check_block_index, blocks[block_index])
                
                blocks[block_index + 1] = [None] * len_data
                break
    
    filesystem = []
    
    for block in blocks:
        for data in block:
            if data is not None:
                filesystem.append(data)
            else:
                filesystem.append(None)
    
    checksum = 0
    for i, data in enumerate(filesystem):
        if data is not None:
            checksum += data * i
        
    
    return checksum

with open("2024/day9/input.txt") as f:
    instructions = f.readlines()

    print(part1(instructions))
    print(part2(instructions))