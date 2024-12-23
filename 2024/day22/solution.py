import sys

def mix(sn, b):
    return sn ^ b

def prune(sn):
    return sn % 16777216

def get_windows(lst, n):
    return list(map(tuple, zip(*[lst[i:] for i in range(n)])))

def get_next(sn):
    sn = prune(mix(sn, sn * 64))
    sn = prune(mix(sn, sn // 32))
    sn = prune(mix(sn, sn * 2048))
    
    return sn
    
def part1(nums) -> int:
    total = 0
    for num in nums:
        for i in range(2000):
            num = get_next(num)
        total += num
    
    return total

def part2(nums) -> int:
    
    windows = {}
    for num in nums:
        last_price = num % 10
        price_deltas = []
        buyer_windows = set()
        for i in range(2000):
            new_num = get_next(num)
            price = new_num % 10
            price_deltas.append((price - last_price))
            num = new_num
            if i > 4:
                last_window = tuple(price_deltas[-4:])
                if last_window not in buyer_windows:
                    buyer_windows.add(last_window)
                    
                    if last_window not in windows:
                        windows[last_window] = 0
                    
                    windows[last_window] += price
            last_price = price
    
    windows = sorted(windows.items(), key=lambda x: x[1])
    
    return windows[-1][1]

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    nums = [int(n) for n in f.readlines()]

    print(part1(nums))
    print(part2(nums))