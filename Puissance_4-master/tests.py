






def function():
    G = [[0,1,0,0,0,1],[0,0,1,0,0,1],[0,0,0,1,1,0],[1,0,0,0,1,0],[0,1,1,0,0,0],[1,0,0,0,1,0]]
    k = [ I [:] for I in G]
    for i in range (len(G)):
        for j in range (len(G[0])):
            if k[i][j] != 0 :
                k[j][i] = k[i][j]
    return(k)

print(function())
