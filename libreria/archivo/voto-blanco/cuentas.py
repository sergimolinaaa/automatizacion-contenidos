V = {"ESTRELLA": 38000, "CÍRCULO": 30000, "TRIÁNGULO": 17900, "CUADRADO": 10000, "ROMBO": 3100}
def dh(votes, seats, valid):
    ok = {n: v for n, v in votes.items() if v >= 0.03 * valid}
    q = sorted(((v / k, n) for n, v in ok.items() for k in range(1, seats + 1)), reverse=True)[:seats]
    r = {n: 0 for n in votes}
    for _, n in q: r[n] += 1
    return r
if __name__ == "__main__":
    assert sum(V.values()) == 99000
    for S in range(10, 40):
        a = dh(V, S, 100000); b = dh(V, S, 109000)
        if a["ROMBO"] and not b["ROMBO"]:
            print(S, a, b)
    print(0.03*100000, 0.03*109000, 3100/100000, 3100/109000)
