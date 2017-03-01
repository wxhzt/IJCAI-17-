def evaluation(real,pred):
    N = len(pred)
    T = 14.0
    sums = 0
    for k in range(0,N):
        for i in range(0,int(T)):
            cha = abs(pred[k][i]-real[k][i])
            he = float(pred[k][i]+real[k][i])
            if (he==0):
                sums+=0
            else:
                sums +=cha/he
    return sums/(N+T)
