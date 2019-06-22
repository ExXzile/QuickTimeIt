
from QuickTimeIt import quick_timeit


@quick_timeit()
def beaufort_cipher_mathematical(m, key):

    u = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    key = (key * (int(len(m) / len(key) + 1)))[0: len(m)]
    answr = [u[(u.index(k) - u.index(m))] for m, k in zip(m, key)]

    return ''.join(answr)


@quick_timeit(runs=100, repeat=9, timing='milli', logfile=True)
def beaufort_cipher_manual(message, key):

    UPPERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    alpha_len = len(UPPERS)
    answer = ''
    matrix = [[UPPERS[(n + mod) % alpha_len] for n in range(alpha_len)]
              for mod in range(alpha_len)]

    while len(key) <= len(message):
        key += key
    key = key[0: len(message)]

    for m, k in zip(message, key):
        idx = matrix[0].index(m)
        for check in matrix:
            if check[idx] == k:
                answer += check[0]
                break
    return answer


print(
    beaufort_cipher_mathematical(
        'N_PHW_AHXFVHTYKEAJSGEHWLMTD_KI_BFJJELOJL_ALAWIHWBKQNH',
        'KNIGHTS_WHO_SAY_NI'
    )
)

print(
    beaufort_cipher_manual(
        'N_PHW_AHXFVHTYKEAJSGEHWLMTD_KI_BFJJELOJL_ALAWIHWBKQNH',
        'KNIGHTS_WHO_SAY_NI'
    )
)
