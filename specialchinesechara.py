def specialchinesechara(am):
    inthearea=False
    Base0=[]
    SPeca = ["（", "）", 
             "［", "］", "｛", "｝", "：", "，", "．", "’",
               "＜", "＞", "＝", "－", "＿","＋", "＊", "／",
                 "＼", "？", "！", "“", "”", "＃", "＠", "＆",
                   "％", "＄", "＾", "￥", "｜", "｀","‘"]
    for i in am:
        if True:
            if i== '"' or i== "'":
                inthearea=not inthearea
                continue
            elif ord(i) >= 0x4E00 and ord(i) <= 0x9FFF and inthearea==False:
                if i in Base0:
                    continue
                else:
                    Base0.append(i)
            if i in SPeca and inthearea==False:
                if i in Base0:
                    continue
                else:
                    Base0.append(i)
    print("特殊字符有:", Base0)

