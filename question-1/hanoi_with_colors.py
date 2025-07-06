def is_valid_move(source, target, disk):
    if not target or (target[-1][0] > disk[0] and target[-1][1] != disk[1]):
        return True
    return False

def hanoi(n, source, auxiliary, target, disks, moves, source_name='A', target_name='C', aux_name='B'):
    if n == 0:
        return
    hanoi(n - 1, source, target, auxiliary, disks, moves, source_name, aux_name, target_name)

    disk = disks[len(disks) - n]
    if is_valid_move(source, target, disk):
        moves.append((disk[0], source_name, target_name))
        source.remove(disk)
        target.append(disk)
    else:
        hanoi(n - 1, auxiliary, source, target, disks, moves, aux_name, target_name, source_name)
        moves.append((disk[0], source_name, target_name))
        source.remove(disk)
        target.append(disk)
        hanoi(n - 1, target, source, auxiliary, disks, moves, target_name, aux_name, source_name)
        return

    hanoi(n - 1, auxiliary, source, target, disks, moves, aux_name, target_name, source_name)

def solve_hanoi(n, disks):
    source = disks.copy()
    target = []
    auxiliary = []
    moves = []

    hanoi(n, source, auxiliary, target, disks, moves)
    if len(target) != n:
        return -1
    return moves

if __name__ == "__main__":
    n = 3
    disks = [(3, "red"), (2, "blue"), (1, "red")]
    result = solve_hanoi(n, disks)
    print(result)
