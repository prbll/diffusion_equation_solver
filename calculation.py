import sys
import numpy as np


def calculate(D, N, DT, NT, S, f_input, u_input):
    def heterogeneity(u, t):
        try:
            return eval(f_input.get())
        except:
            sys.exit("F(u(x,t),t) ошибочна.")

    N = N if N % 2 == 0 else N + 1
    x = np.linspace(0, np.pi * 2, N)
    h = 2 * np.pi / N
    Z = np.zeros((NT, N))
    lmbd = [0.0]

    for k in range((-N // 2), 0):
        if k == -N // 2:
            lmbd.insert(1, 4 * D / h ** 2 * (np.sin(k * h / 4)) ** 2)
        else:
            lmbd.insert(1, 4 * D / h ** 2 * (np.sin(k * h / 4)) ** 2)
            lmbd.append(4 * D / h ** 2 * (np.sin(-k * h / 4)) ** 2)

    lmbd = np.array(lmbd)
    u0 = eval(u_input.get())
    Z[0] = u0

    for k in range(1, NT):
        u_prev = Z[k - 1]
        u_curr = u_prev
        for i in range(S):
            phi1 = heterogeneity(u_prev, (k - 1) * DT)
            phi2 = heterogeneity(u_curr, k * DT)
            phi = (phi1 + phi2)
            fu_curr = np.fft.fft(phi)
            fu_prev = np.fft.fft(u_prev)
            u = ((2 - lmbd * DT) * fu_prev + DT * fu_curr) / (2 + lmbd * DT)
            u_curr = np.fft.ifft(u)
        Z[k] = np.real(u_curr)
    return Z
