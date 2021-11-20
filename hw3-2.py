def win(nums):
    # do something
    # you can change variable names
    rounds, path = 0, []
    pos, step = 0, nums[0]
    while pos != len(nums)-1:
        rounds += 1
        if pos + step >= len(nums)-1:
            pos = len(nums)-1
            path.append(pos)
        else:
            candidate = nums[pos:pos+step+1]
            best_pos, best_step = 0, -1
            for i in range(1, len(candidate)):
                if i + candidate[i] >= best_pos + best_step:
                    best_pos, best_step = i, candidate[i]
            pos  = pos + best_pos
            step = best_step
            path.append(pos)
    return (rounds, path)