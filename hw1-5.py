from collections import defaultdict
n = int(input())

ans = []
zeros = 0
pos_c, neg_c = [], []
pos_single, neg_single = [], []
pos_double, neg_double = [], []
n_dict = defaultdict(int)
for _ in range(n):
    number = int(input())
    if number > 0:
        if n_dict[number] == 0: pos_single.append(number)
        elif n_dict[number] == 1: pos_double.append(number)
    elif number < 0:
        if n_dict[number] == 0: neg_single.append(number)
        elif n_dict[number] == 1: neg_double.append(number)
    n_dict[number] += 1

pos_single.sort()
neg_single.sort(reverse=True)
pos_double.sort()
neg_double.sort(reverse=True)

def search_with_zero():
    c_single = neg_single[::-1] + pos_single
    l_idx, r_idx = 0, len(c_single)-1
    l, r = c_single[l_idx], c_single[r_idx]
    while l_idx < r_idx:
        if abs(l) == r:
            ans.append([l,0,r])
            l_idx += 1
            r_idx -= 1
        elif abs(l) > r:
            l_idx += 1
        elif abs(l) < r:
            r_idx -= 1
        l, r = c_single[l_idx], c_single[r_idx]

def search_double(c_single, c_double):
    single_idx, double_idx = 0, 0
    while single_idx <= len(c_single) - 1 and double_idx <= len(c_double) - 1:
        single_number, double_number = c_single[single_idx], c_double[double_idx]
        if abs(single_number) == 2 * abs(double_number):
            ans_pair = [double_number, double_number, single_number]
            ans_pair.sort()
            ans.append(ans_pair)
            single_idx += 1
            double_idx += 1
        elif abs(single_number) > 2 * abs(double_number):
            double_idx += 1
        elif abs(single_number) < 2 * abs(double_number):
            single_idx += 1

def search_single(c_single, c_double):
    for single_idx in range(len(c_single)):
        single_number = c_single[single_idx]
        for double_idx_i in range(len(c_double)-1):
            if abs(c_double[double_idx_i] + c_double[double_idx_i+1]) > abs(single_number):
                break
            for double_idx_j in range(double_idx_i+1, len(c_double)):
                double_number_i, double_number_j = c_double[double_idx_i], c_double[double_idx_j]
                if abs(double_number_i + double_number_j) == abs(single_number):
                    ans_pair = [single_number, double_number_i, double_number_j]
                    ans_pair.sort()
                    ans.append(ans_pair)
                elif abs(double_number_i + double_number_j) > abs(single_number):
                    break

if n_dict[0] >= 3:
    ans.append([0,0,0])
if n_dict[0] > 0:
    search_with_zero()
search_double(c_single=pos_single, c_double=neg_double)
search_double(c_single=neg_single, c_double=pos_double)
search_single(c_single=pos_single, c_double=neg_single)
search_single(c_single=neg_single, c_double=pos_single)

ans.sort(key=lambda x: tuple(x))
for i in range(len(ans)):
    print(ans[i])