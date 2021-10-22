# GLOBAL
M = 397
N = 624
A = 0x9908B0DF
U = 1 << 31
L = U - 1
B = 0x9d2c5680
C = 0xefc60000


# first element of prev_state is not recoverd and this is not bug
# todo: re-implement for not dirty and smart algorithm
def prev_state(next_state):
    # reverse state
    state_lsb = [0 for _ in range(N)]
    state_msb = [0 for _ in range(N)]
    recovered_state = [0 for _ in range(N)]

    # 1st part
    start_i = N - M
    for i in range(start_i, N):
        xi = next_state[i]
        xim = next_state[(i + M) % N]

        xored = xi ^ xim
        y_lsb = 0
        if xored & U != 0:
            xored = xored ^ A
            y_lsb = 1

        y = (xored << 1) + y_lsb

        if i != N - 1:
            state_lsb[(i+1) % N] = y & L
        state_msb[i] = y & U

        if i != start_i:
            recovered_state[i] = state_msb[i] + state_lsb[i]

    # 2nd part
    for i in range(0, start_i):
        xi = next_state[i]
        xim = recovered_state[(i + M) % N]

        xored = xi ^ xim
        y_lsb = 0
        if xored & U != 0:
            xored = xored ^ A
            y_lsb = 1

        y = (xored << 1) + y_lsb

        state_lsb[(i+1) % N] = y & L
        state_msb[i] = y & U

        if i != 0:
            recovered_state[i] = state_msb[i] + state_lsb[i]

    recovered_state[start_i] = state_lsb[start_i] + state_msb[start_i]

    return recovered_state


# dirty and using my poor calculation
# but it's more trivial for me than usual implementation
def untemper(x):
    x ^= (x >> 18)        # reverse of 4
    x ^= ((x << 15) & C)  # reverse of 3
    # reverse of 2
    x_bottom_14 = (x ^ (x << 7) & B) # & ((1 << 14) - 1)
    x_bottom_21 = (x ^ (x_bottom_14 << 7) & B) # & ((1 << 21) - 1)
    x_bottom_28 = (x ^ (x_bottom_21 << 7) & B) # & ((1 << 28) - 1)
    x ^= (x_bottom_28 << 7) & B
    # reverse of 1
    x_top_22 = x ^ (x >> 11)
    x ^= (x_top_22 >> 11)

    return x


# recover raw state
# random.getstate()[1][:-1] <- counter is not included
def recover_state(rs):
    ret = []
    for r in rs:
        ret.append(untemper(r))

    return ret


# same format as random.getstate()
def create_state(state, i=624):
    state = tuple(state) + (i,)
    return (3, state, None)