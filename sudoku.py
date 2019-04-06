import numpy as np

DIAP_VAL = np.arange(1, 10)


def get_free_val(gamemap, i, j):
    pos_x, pos_y = 3 * int(i / 3), 3 * int(j / 3)

    uniq = np.unique([gamemap[i],
                      gamemap[:, j],
                      gamemap[pos_x: pos_x + 3, pos_y: pos_y + 3].reshape(9)
                      ])

    return np.setdiff1d(DIAP_VAL, uniq)


def find_unambiguous_cells(gamemap):
    zero_pos_i, zero_pos_j = np.where(gamemap == 0)
    while True:
        if not zero_pos_i.size:
            return 0
        for numb_zero in range(zero_pos_i.size):
            free_val = get_free_val(gamemap, zero_pos_i[numb_zero], zero_pos_j[numb_zero])
            if free_val.size == 0:
                return 2
            if free_val.size == 1:
                gamemap[zero_pos_i[numb_zero], zero_pos_j[numb_zero]] = free_val[0]
                zero_pos_i, zero_pos_j = np.where(gamemap == 0)
                break
        else:
            return 1


def rec_sudoku(gamemap):
    zero_pos_i, zero_pos_j = np.where(gamemap == 0)

    if not zero_pos_i.size:
        return gamemap, True

    free_val = get_free_val(gamemap, zero_pos_i[0], zero_pos_j[0])

    for guess in free_val:
        gamemap[zero_pos_i[0], zero_pos_j[0]] = guess
        gamemap_copy = gamemap.copy()
        flag = find_unambiguous_cells(gamemap_copy)

        if flag == 1:
            gamemap_copy, flag = rec_sudoku(gamemap_copy.copy())

        if not flag:
            return gamemap_copy, False

    return gamemap, True


if __name__ == '__main__':
    a = np.array(
        [[8, 0, 0,  0, 0, 0,  0, 0, 0],
         [0, 0, 3,  6, 0, 0,  0, 0, 0],
         [0, 7, 0,  0, 9, 0,  2, 0, 0],

         [0, 5, 0,  0, 0, 7,  0, 0, 0],
         [0, 0, 0,  0, 4, 5,  7, 0, 0],
         [0, 0, 0,  1, 0, 0,  0, 3, 0],

         [0, 0, 1,  0, 0, 0,  0, 6, 8],
         [0, 0, 8,  5, 0, 0,  0, 1, 0],
         [0, 9, 0,  0, 0, 0,  4, 0, 0]],
        int
    )

    answer, err = rec_sudoku(a)

    if not err:
        print(answer)
    else:
        print('Answer not found')
