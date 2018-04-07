#########################################################
#########################################################
nullable_rules = list()
nullable_nonTerminals = list()
BDW = list()
BW_from_BDW = list()
BW_transitive = list()
BW_reflexive = list()
first_x = dict()
first_right = dict()
FDB = list()
DEO = list()
EO_from_DEO = list()
EO_transitive = list()
EO_reflexive = list()
EO = list()
BW = list()
FB = list()
FOL = dict()
SEL = dict()

#########################################################
#########################################################
# 1 - Find nullable rules and nullable nonterminals.
def stepOne(rules):
    firstIsUpper = 0
    for rule in rules :
        if rule[4].isupper() :
            firstIsUpper = 1
        if rule[4] == "@" :
            if rule[0] not in nullable_nonTerminals :
                nullable_rules.append(rule)
                nullable_nonTerminals.append(rule[0])
    for rule in rules :
        count = 0
        ruleCount = len(rule)

        for x in range(4,len(rule)):
            if rule[x] in nullable_nonTerminals and rule[0] not in nullable_nonTerminals :
                count = count + 1

        if ruleCount - count == 4 :
            nullable_rules.append(rule)
            nullable_nonTerminals.append(rule[0])
    if len(nullable_rules) == 0:
        print("-----> Step one ")
        print("- No Nullable Rules :")
        return 0
    else:
        print("-----> Step one ")
        print("Find nullable rules and nullable nonterminals.")
        print("- nullable rules :")
        for x in nullable_rules :
            print (x)
        print("- nullable non-Terminals :")
        for y in nullable_nonTerminals :
            print (y)
        print("#########################################################")
        return 1
#########################################################
# 2 - Find Begins Directly With relation (BDW).
def stepTow(rules):
    for rule in rules :
        if(len(rule) == 5):
            if rule[4] != '@':
                BDW.append(rule[0]+" BDW "+rule[4])
        else:
            for x in range(4,len(rule)):
                if rule[x] in nullable_nonTerminals :
                    BDW.append(rule[0]+" BDW "+rule[x])
                else:
                    BDW.append(rule[0]+" BDW "+rule[x])
                    break
    print("-----> Step Two ")
    print("Find Begins Directly With relation (BDW).")
    print("- BDW's :")
    for x in BDW :
        print (x)
    print("#########################################################")
#########################################################
# 3 - Find Begins With relation (BW).
def stepThree():
    # (from BDW)
    for x in BDW :
        BW_from_BDW.append(x.replace(x[3],""))

    # (reflexive)
    for z in BDW :
        if z[0]+" BW "+z[0] not in BW_from_BDW:
            if z[0]+" BW "+z[0] not in BW_reflexive :
                BW_reflexive.append(z[0]+" BW "+z[0])
        if z[6]+" BW "+z[6] not in BW_from_BDW:
            if z[6]+" BW "+z[6] not in BW_reflexive :
                BW_reflexive.append(z[6]+" BW "+z[6])
    # (transitive)
    for x in BDW :
        chra = x[6]
        for y in BDW :
            if y != x :
                if y[0] == chra and y[6] != x[6]:
                    if x[0]+" BW "+y[6] not in  BDW :
                        if x[0]+" BW "+y[6] not in BW_reflexive and BW_from_BDW:
                            BW_transitive.append(x[0]+" BW "+y[6])
    print("-----> Step Three ")
    print("Find Begins With relation (BW).")
    print("- from BDW :")
    for index in BW_from_BDW:
        print(index)

    print("- Transitive :")
    for index in BW_transitive:
        print(index)
    if len(BW_transitive) == 0:
        print ("  (no transitive)")
    print("- Reflexive :")
    for index in BW_reflexive:
        print(index)
    print("#########################################################")
#########################################################
# 4 - Find First(x) for each symbol, x
def stepFour():
    for x in BW_from_BDW :
        for y in BW_from_BDW :
            if x[0] == y[0] and y[5].islower():
                if x[0] not in first_x.keys():
                    first_x.update({x[0]:[y[5]]})
                else :
                    first_x[x[0]].append(y[5])
    for x in BW_transitive :
        for y in BW_transitive :
            if x[0] == y[0] and y[5].islower():
                if x[0] not in first_x.keys():
                    first_x.update({x[0]:[y[5]]})
                else :
                    if y[5] not in first_x[x[0]]:
                            first_x[x[0]].append(y[5])
    for x in BW_reflexive :
        for y in BW_reflexive :
            if x[0] == y[0] and y[5].islower():
                if x[0] not in first_x.keys():
                    first_x.update({x[0]:[y[5]]})
                else :
                    if y[5] not in first_x[x[0]]:
                            first_x[x[0]].append(y[5])
    print("-----> Step Four ")
    print("Find First(x) for each symbol, x")
    for x in first_x.keys():
        stt =str(first_x[x])
        print("F("+x+") = " + stt)
    print("#########################################################")
#########################################################
# 5 - Find First(n) for the right side of each rule, n.
def stepFive(rules):
    for rule in rules:
        right_HS = rule[4:len(rule)]
        if right_HS  != '@':
            for x in right_HS :
                if right_HS not in first_right.keys() :
                    first_right.update({right_HS:[first_x[x]]})
                else:
                    if x in first_x.keys():
                        first_right[right_HS].append(first_x[x])

                if x not in nullable_nonTerminals :
                    break
        else :
            if '@'in  first_right.keys():
                pass
            else:
                first_right.update({'@':[]})
    print("-----> Step Five ")
    print("Find First(n) for the right side of each rule, n.")
    for x in first_right :
        print (x + " = " +str(first_right[x]) )
    print("#########################################################")
#########################################################
# 6 - Find Followed Directly By relation (FDB).
def stepSix(rules):

    for rule in rules :
        right = rule[4:len(rule)]
        count = len(rule) - 4
        index = 0
        for x in right :
            if x.isupper() and count != index + 1 :
                if right[index+1] not in nullable_nonTerminals :
                    FDB.append(right[index]+" FDB "+right[index+1])
            index += 1
    print("-----> Step Six ")
    print("Find Followed Directly By relation (FDB).")
    for x in FDB :
        print (x)
    print("#########################################################")
#########################################################
# 7 - Find Is Direct End Of relation (DEO).
def stepSeven(rules):
    for rule in rules :
        count = len(rule) - 4
        right = rule[4:len(rule)][::-1]
        for x in right :
            if x != '@':
                    DEO.append( x +" DEO " + rule[0])
                    if x not in nullable_nonTerminals :
                        break
    print("-----> Step Seven ")
    print("Find Is Direct End Of relation (DEO).")
    for x in DEO :
        print (x)
    print("#########################################################")
#########################################################
# 8 - Find Is End Of relation (EO).
def stepEight():
    # (from DEO)
    for x in DEO :
        EO_from_DEO.append(x.replace(x[2],""))

    # (reflexive)
    for z in DEO :
        if z[0]+" EO "+z[0] not in EO_from_DEO :
            if z[0]+" EO "+z[0] not in EO_reflexive :
                EO_reflexive.append(z[0]+" EO "+z[0])
        if z[6]+" EO "+z[6] not in EO_from_DEO :
            if z[6]+" EO "+z[6] not in EO_reflexive :
                EO_reflexive.append(z[6]+" EO "+z[6])

    # (transitive)
    for x in DEO :
        chra = x[6]
        for y in DEO :
            if y != x :
                if y[0] == chra and y[6] != x[6]:
                    if x[0]+" EO "+y[6] not in EO_from_DEO and EO_reflexive:
                        EO_transitive.append(x[0]+" EO "+y[6])
    print("-----> Step Eight ")
    print("Find Is End Of relation (EO).")
    print("- from DEO :")
    for index in EO_from_DEO:
        print(index)

    print("- Transitive :")
    for index in EO_transitive:
        print(index)
    if len(EO_transitive) == 0:
        print ("  (no transitive)")
    print("- Reflexive :")
    for index in EO_reflexive:
        print(index)

    print("#########################################################")
#########################################################
# 9 - Find Is Followed By relation (FB).
def stepNine():
    for x in FDB:
        for y in EO_from_DEO:
            if x[0] == y[5]:
                EO.append(y)
        for y in EO_transitive:
            if x[0] == y[5]:
                EO.append(y)
        for y in EO_reflexive:
            if x[0] == y[5]:
                EO.append(y)
    for x in FDB:
        for y in BW_from_BDW:
            if x[6] == y[0]:
                BW.append(y)

        for y in BW_transitive:
            if x[6] == y[0]:
                BW.append(y)
        for y in BW_reflexive:
            if x[6] == y[0]:
                BW.append(y)
    for x in FDB:
        for y in EO :
            for z in BW:
                if y[5] == x[0] and z[0] == x[6]:
                    FB.append(y[0]+" FB " +z[5])
    print("-----> Step Nine ")
    print("Find Is Followed By relation (FB).")
    for index in FB:
        print(index)
    print("#########################################################")
#########################################################
# 10 - Extend FB to include endmarker.
def stepTen():
    print("-----> Step Ten ")
    print("Extend FB to include endmarker.")
    msg = "FB not extended "
    for x in EO_from_DEO:
        if x[0].isupper() and x[5] == 'S':
            FB.append(x[0]+" FB <")
            msg = "FB relation Is Extended "
    for x in EO_transitive:
        if x[0].isupper() and x[5] == 'S':
            FB.append(x[0]+" FB <")
            msg = "FB relation Is Extended "
    for x in EO_reflexive:
        if x[0].isupper() and x[5] == 'S':
            FB.append(x[0]+" FB <")
            msg = "FB relation Is Extended "
    print(msg)
    if msg == "FB relation Is Extended " :
        print(FB)
    print("#########################################################")
#########################################################
# 11 - Find Follow Set, Fol(A), for each nullable nonterminal, A.
def stepEleven():
    for x in nullable_nonTerminals :
        for y in FB :
            if y[0] == x and y[5].islower():
                if x not in FOL.keys() :
                    FOL.update({x:[y[5]]})
                else:
                    if x in first_x.keys():
                        FOL[x].append(y[5])

    print("-----> Step Eleven ")
    print("Find Follow Set, Fol(A), for each nullable nonterminal, A.")
    for x in FOL :
        print(x +" = "+ str(FOL[x]))
    print("#########################################################")
#########################################################
# 12 - Find Selection Set, Sel(n), for each rule, n.
def stepTwelve(rules):
    index = 0
    for rule in rules:
        right = rule[4:len(rule)]
        if rule in nullable_rules and rule[0]  in FOL.keys():
            SEL.update({index:[FOL[rule[0]]]})
        else:
            SEL.update({index:[first_right[right]]})
        index += 1
    print("-----> Step Twelve ")
    print("Find Selection Set, Sel(n), for each rule, n.")
    print("- Selection Set :")
    for x in SEL :
        y = str(SEL[int(x)])
        print ("sel("+str(x)+") = "+ y )
    print("- Grammar is LL(1) ????..")
    msg = "Not LL(1) Grammar "
    ind = 0
    for rule in rules:
        x = rule[0]
        ind2 =0
        for y in rules :
            if x == y[0] and ind != ind2 :
                if SEL[int(ind2)] != SEL[int(ind)]:
                    msg = "yes , Is LL(1) Grammar "
                    break
            ind2 += 1
        ind += 1
    print (msg)
    print("#########################################################")
#########################################################
#########################################################
#########################################################
#Loading rules from rules.txt and starting test ..
file = open("rules.txt","r")
file.seek(0)
rules = file.read().strip().split("\n")
file.close()
x = stepOne(rules)
stepTow(rules)
stepThree()
stepFour()
stepFive(rules)
if x == 0 :
    stepTwelve(rules)
else:
    stepSix(rules)
    stepSeven(rules)
    stepEight()
    stepNine()
    stepTen()
    stepEleven()
    stepTwelve(rules)
