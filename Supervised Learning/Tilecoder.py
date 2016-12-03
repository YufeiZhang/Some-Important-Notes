numTilings = 8
    
def tilecode(in1,in2,tileIndices):
    " write your tilecoder here (5 lines or so)"
    for i in range (0, numTilings):
        offset = i * 0.6 / numTilings
        index1 = int(10 * (in1 + offset)/6.0)
        index2 = int(10 * (in2 + offset)/6.0)
        tileIndices[i] = int((121 * i) + (11 * index2) + index1)    
    
def printTileCoderIndices(in1,in2):
    tileIndices = [-1]*numTilings
    tilecode(in1,in2,tileIndices)
    print('Tile indices for input (',in1,',',in2,') are : ', tileIndices)

printTileCoderIndices(0.1,0.1)
printTileCoderIndices(4.0,2.0)
printTileCoderIndices(5.99,5.99)
printTileCoderIndices(4.0,2.1)
    

