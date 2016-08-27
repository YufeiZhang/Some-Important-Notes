def main():
    try:
        number = str(input("partial_order_"))
        filename = "partial_order_" + number + ".txt"
            
        #filename = str(input("Which data file do you want to use? "))
        txt = open(filename)
        t1 = datetime.datetime.now()


        nodes = []; edges = []
        for line in txt:            
            line = line.replace(" ", "")
            pair = line.split(',')
            pair[0], pair[1] = pair[0][2:], pair[1][:-2]

            edges.append(tuple(pair))
            if pair[0] not in nodes:
                nodes.append(pair[0])
            if pair[1] not in nodes:
                nodes.append(pair[1])

        nodes = sorted(nodes)
        print(nodes)
        print(edges)

        for x in nodes:
            for y in nodes:
                for z in nodes:
                    if (x,y) != (y,z) and (x,y) != (x,z):
                        if (x,y) in edges and (y,z) in edges:
                            print("remove", x, z)
                            try:
                                edges.remove((x,z))
                            except:
                                pass

        print(edges)


        t2 = datetime.datetime.now()
        print(t2-t1)

    except OSError as err:
        print("OS error: {0}".format(err))





if __name__ == '__main__':
    import datetime    
    main()

