def searching_blanks(aa):
    Base1 = []
    flag=False
    for i in range(len(aa)):
        if i =='"' and flag==False:
            if aa[i] == " ":
                Base1.append(i)
            if aa[i] == '"':
                flag=True
                continue
    print("空格位置有:", Base1)