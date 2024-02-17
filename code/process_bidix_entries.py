import os

pdm_path = '' # used to check if paradigm path has changed
pdms = [] # imported paradigms # [paradigm_name_i, [[entry_j_left, entry_j_right]]]
punc_path = '' # used to check if punctuation path has changed
puncs = [] # punctuations
c_entry_repeat = False # True -> repetitive correct entry
c_entry_color = 1 # switch between 1 and 2; 1 is default

def process_entries(output_type, lsx_type, addr, pdm, punc, l1, l2):
    global pdm_path, punc_path
    global pdms, puncs
    global c_entry_repeat
    global c_entry_color



    # ignore white spaces if not bounded by alpha numeric characters

    gen_dix = [] # generated dix entries
    l1_lsx = [] # generated lsx entries
    l2_lsx = [] # generated lsx entries
    l1_ent = [[]] # append new list on the basis of two consecutive \n
    l2_ent = [[]] # append new list on the basis of two consecutive \n
    msg_rtn = '' # message to be returned
    
    if len(addr) == 0:
        msg_rtn = 'Output directory not specified'
        c_entry_repeat = False
        return msg_rtn, 0
    if len(l1) == 0 and len(l2) == 0:
        msg_rtn = 'No data entered for both languages'
        c_entry_repeat = False
        return msg_rtn, 0
    elif len(l1) == 0:
        msg_rtn = 'No data entered for language 1'
        c_entry_repeat = False
        return msg_rtn, 0
    elif len(l2) == 0:
        msg_rtn = 'No data entered for language 2'
        c_entry_repeat = False
        return msg_rtn, 0
    
    if len(pdm) != 0:
        if pdm != pdm_path:
            pdm_path = pdm
            pdms = []
            pdm_file = open(pdm, 'r', newline='', encoding='utf-8')
            pdm_readline = pdm_file.readlines()
            flag1 = False
            for line in pdm_readline:
                if (line.__contains__('/pardef') == False):
                    if flag1 == True:
                        i1 = 1
                        while (i1 < len(line)):
                            if line[i1] == '>' and line[i1 - 1] == 'l':
                                break
                            i1 += 1

                        if i1 < len(line):
                            pdms[-1][-1].append([])
                            temp_entry = ''
                            i1 += 1
                            while (i1 < len(line)):
                                if line[i1 + 1] == '/' and line[i1 + 2] == 'l':
                                    break
                                else:
                                    temp_entry += line[i1]
                                i1 += 1
                            pdms[-1][-1][-1].append(temp_entry)

                            i1 = 1
                            while (i1 < len(line)):
                                if line[i1] == '>' and line[i1 - 1] == 'r':
                                    break
                                i1 += 1
                            temp_entry = ''
                            i1 += 1
                            while (i1 < len(line)):
                                if line[i1 + 1] == '/' and line[i1 + 2] == 'r':
                                    break
                                else:
                                    temp_entry += line[i1]
                                i1 += 1
                            pdms[-1][-1][-1].append(temp_entry)

                    elif (line.__contains__('pardef') == True):
                        flag1 = True
                        pdms.append([])
                        temp_name = ''
                        flag2 = False
                        for i in range(6, len(line)):
                            if line[i] == '"':
                                if flag2 == False:
                                    flag2 = True
                                else:
                                    break
                            elif flag2 == True:
                                temp_name += line[i]
                        pdms[-1].append(temp_name)
                        pdms[-1].append([])
                    
                else:
                    flag1 = False

    if len(punc) != 0:
        if punc != punc_path:
            punc_path = punc
            puncs = []
            punc_file = open(punc, 'r', newline='', encoding='utf-8')
            punc_readline = punc_file.readlines()
            for line in punc_readline:
                puncs += line
        #print(puncs, len(puncs))
        
        # delete unwanted and repeating
        i1 = 0
        while (i1 < len(puncs)):
            if puncs[i1] == ' ' or puncs[i1] == '\r' or puncs[i1] == '\n':
                del puncs[i1]
            else:
                i1 += 1
        i1 = 0
        while (i1 < len(puncs) - 1):
            i2 = i1 + 1
            while (i2 < len(puncs)):
                if puncs[i1] == puncs[i2]:
                    del puncs[i2]
                else:
                    i2 += 1
            i1 += 1


    l1_lines = l1.splitlines() # segment content of l1 as individual lines
    l2_lines = l2.splitlines() # segment content of l2 as individual lines



    # delete unwanted blank lines

    i1 = 0
    while (l1_lines[i1] == '' or l1_lines[i1].isspace()):
        del l1_lines[i1]

    i1 = 0
    while (i1 < len(l1_lines) - 1):
        flag1 = False
        if l1_lines[i1] == '':
            if l1_lines[i1 + 1] == '':
                del l1_lines[i1 + 1]
                flag1 = True
            else:
                flag2 = False
                j1 = 0
                while (j1 < len(l1_lines[i1 + 1])):
                    if l1_lines[i1 + 1][j1].isspace():
                        j1 += 1
                    else:
                        flag2 = True
                        break
                if flag2 == False:
                    del l1_lines[i1 + 1]
                    flag1 = True
        else:
            flag2 = False
            j1 = 0
            while (j1 < len(l1_lines[i1])):
                if l1_lines[i1][j1].isspace():
                    j1 += 1
                else:
                    flag2 = True
                    break
            if flag2 == False:
                l1_lines[i1][j1] = ''
                if l1_lines[i1 + 1] == '':
                    del l1_lines[i1 + 1]
                    flag1 = True
                else:
                    flag2 = False
                    j1 = 0
                    while (j1 < len(l1_lines[i1 + 1])):
                        if l1_lines[i1 + 1][j1].isspace():
                            j1 += 1
                        else:
                            flag2 = True
                            break
                    if flag2 == False:
                        del l1_lines[i1 + 1]
                        flag1 = True

        if flag1 == False:
            i1 += 1
    
    i1 = len(l1_lines) - 1
    while (l1_lines[i1] == '' or l1_lines[i1].isspace()):
        del l1_lines[i1]
        i1 -= 1



    # store in l1_ent

    flag1g = True
    for i in l1_lines:
        if i != '':
            if i.__contains__('↤') == True:
                i1 = 0
                while (i[i1].isspace()): # detect empty
                    i1 += 1

                temp1 = ''
                while (i1 < len(i)): # root
                    if (i[i1].isspace() == False) and i[i1] == '↤':
                        break
                    temp1 += i[i1]
                    i1 += 1
                i1 += 1 

                right_limit = len(temp1) - 1
                for i2 in reversed(range(len(temp1))):
                    if temp1[i2].isspace() == False:
                        right_limit = i2
                        break
                temp2 = ''
                for i2 in range(right_limit + 1):
                    temp2 += temp1[i2]
                l1_ent[-1].append(temp2)

                temp1 = ''
                l1_ent[-1].append([])
                while (i1 < len(i)):
                    if i[i1].isspace() or i[i1] == '⋅':
                        if temp1 != '':
                            l1_ent[-1][-1].append(temp1)
                            temp1 = ''
                    else:
                        temp1 += i[i1]
                    i1 += 1
                if (i[-1].isspace() == False) or i[i1] != '⋅':
                    l1_ent[-1][-1].append(temp1)

            elif (i.__contains__('[') == True) and (i.__contains__(']') == True):
                l1_ent[-1].append([])
                flag1g_i = False
                temp1 = ''
                for j in i:
                    if j == '<' or j.isspace() or j == '[':
                        pass
                    elif j == '>' or j == ',' or j == '⋅' or j == ']':
                        l1_ent[-1][-1].append(temp1)
                        temp1 = ''
                    else:
                        temp1 += j
                        flag1g_i = True
                if flag1g == True and flag1g_i == False:
                    flag1g = False

            elif (i.__contains__('<') == True) and (i.__contains__('>') == True) and (i.__contains__('<b/>') == False):
                temp_inf = i.split('/')
                if temp_inf[0].__contains__('<') == True:
                    j = 0
                else:
                    j = 1
                while (j < len(temp_inf)):
                    temp1 = ''
                    j1 = 0
                    while (temp_inf[j][j1] != '<'):
                        temp1 += temp_inf[j][j1]
                        j1 += 1
                    l1_ent[-1].append(temp1)
                    l1_ent[-1].append([])
                    flag1g_1_i = False # for starting a bracket of grammar
                    flag1g_2_i = False # for indicating grammar within bracket
                    while (j1 < len(temp_inf[j])):
                        if temp_inf[j][j1] == '<':
                            temp1 = ''
                            if flag1g_1_i == False:
                                flag1g_1_i = True
                            else:
                                flag1g = False
                        elif temp_inf[j][j1] == '>':
                            l1_ent[-1][-1].append(temp1)
                            if flag1g_2_i == False:
                                flag1g = False
                            flag1g_1_i = False
                            flag1g_2_i = False
                        else:
                            temp1 += temp_inf[j][j1]
                            if flag1g_1_i == True:
                                flag1g_2_i = True
                        j1 += 1
                    j += 1

            else:
                # fetches -> root / original / translations
                left_limit = 0
                right_limit = len(i) - 1
                j = 0
                while (i[j].isspace()):
                    left_limit += 1
                    j += 1
                
                j = len(i) - 1
                while (i[j].isspace()):
                    right_limit -= 1
                    j -= 1

                temp1 = ''
                while (left_limit <= right_limit):
                    temp1 += i[left_limit]
                    left_limit += 1

                l1_ent[-1].append(temp1)

        else:
            l1_ent.append([])
    if flag1g == False:
        msg_rtn = 'Missing grammar types for '


    # delete unwanted blank lines

    i1 = 0
    while (l2_lines[i1] == '' or l2_lines[i1].isspace()):
        del l2_lines[i1]

    i1 = 0
    while (i1 < len(l2_lines) - 1):
        flag1 = False
        if l2_lines[i1] == '':
            if l2_lines[i1 + 1] == '':
                del l2_lines[i1 + 1]
                flag1 = True
            else:
                flag2 = False
                j1 = 0
                while (j1 < len(l2_lines[i1 + 1])):
                    if l2_lines[i1 + 1][j1].isspace():
                        j1 += 1
                    else:
                        flag2 = True
                        break
                if flag2 == False:
                    del l2_lines[i1 + 1]
                    flag1 = True
        else:
            flag2 = False
            j1 = 0
            while (j1 < len(l2_lines[i1])):
                if l2_lines[i1][j1].isspace():
                    j1 += 1
                else:
                    flag2 = True
                    break
            if flag2 == False:
                l2_lines[i1][j1] = ''
                if l2_lines[i1 + 1] == '':
                    del l2_lines[i1 + 1]
                    flag1 = True
                else:
                    flag2 = False
                    j1 = 0
                    while (j1 < len(l2_lines[i1 + 1])):
                        if l2_lines[i1 + 1][j1].isspace():
                            j1 += 1
                        else:
                            flag2 = True
                            break
                    if flag2 == False:
                        del l2_lines[i1 + 1]
                        flag1 = True

        if flag1 == False:
            i1 += 1

    i1 = len(l2_lines) - 1
    while (l2_lines[i1] == '' or l2_lines[i1].isspace()):
        del l2_lines[i1]
        i1 -= 1



    # store in l2_ent

    flag2g = True
    for i in l2_lines:
        if i != '':
            if i.__contains__('↤') == True:
                i1 = 0
                while (i[i1].isspace()): # detect empty
                    i1 += 1

                temp1 = ''
                while (i1 < len(i)): # root
                    if (i[i1].isspace() == False) and i[i1] == '↤':
                        break
                    temp1 += i[i1]
                    i1 += 1
                i1 += 1 

                right_limit = len(temp1) - 1
                for i2 in reversed(range(len(temp1))):
                    if temp1[i2].isspace() == False:
                        right_limit = i2
                        break
                temp2 = ''
                for i2 in range(right_limit + 1):
                    temp2 += temp1[i2]
                l2_ent[-1].append(temp2)

                temp1 = ''
                l2_ent[-1].append([])
                while (i1 < len(i)):
                    if i[i1].isspace() or i[i1] == '⋅':
                        if temp1 != '':
                            l2_ent[-1][-1].append(temp1)
                            temp1 = ''
                    else:
                        temp1 += i[i1]
                    i1 += 1
                if (i[-1].isspace() == False) or i[i1] != '⋅':
                    l2_ent[-1][-1].append(temp1)

            elif (i.__contains__('[') == True) and (i.__contains__(']') == True):
                l2_ent[-1].append([])
                temp1 = ''
                flag2g_i = False
                for j in i:
                    if j == '<' or j.isspace() or j == '[':
                        pass
                    elif j == '>' or j == ',' or j == '⋅' or j == ']':
                        l2_ent[-1][-1].append(temp1)
                        temp1 = ''
                    else:
                        temp1 += j
                        flag2g_i = True
                if flag2g == True and flag2g_i == False:
                    flag2g = False
                        
            elif (i.__contains__('<') == True) and (i.__contains__('>') == True) and (i.__contains__('<b/>') == False):
                temp_inf = i.split('/')
                if temp_inf[0].__contains__('<') == True:
                    j = 0
                else:
                    j = 1
                while (j < len(temp_inf)):
                    temp1 = ''
                    j1 = 0
                    while (temp_inf[j][j1] != '<'):
                        temp1 += temp_inf[j][j1]
                        j1 += 1
                    l2_ent[-1].append(temp1)
                    l2_ent[-1].append([])
                    flag2g_1_i = False # for starting a bracket of grammar
                    flag2g_2_i = False # for indicating grammar within bracket
                    while (j1 < len(temp_inf[j])):
                        if temp_inf[j][j1] == '<':
                            temp1 = ''
                            if flag2g_1_i == False:
                                flag2g_1_i = True
                            else:
                                flag2g = False
                        elif temp_inf[j][j1] == '>':
                            l2_ent[-1][-1].append(temp1)
                            if flag2g_2_i == False:
                                flag2g = False
                            flag2g_1_i = False
                            flag2g_2_i = False
                        else:
                            temp1 += temp_inf[j][j1]
                            if flag2g_1_i == True:
                                flag2g_2_i = True
                        #print(temp_inf[j][j1], flag2g_i, temp_inf[j])
                        j1 += 1
                    j += 1

            else:
                # fetches -> root / original / translations
                left_limit = 0
                right_limit = len(i) - 1
                j = 0
                while (i[j].isspace()):
                    left_limit += 1
                    j += 1
                
                j = len(i) - 1
                while (i[j].isspace()):
                    right_limit -= 1
                    j -= 1

                temp1 = ''
                while (left_limit <= right_limit):
                    temp1 += i[left_limit]
                    left_limit += 1

                l2_ent[-1].append(temp1)

        else:
            l2_ent.append([])
    
    if flag2g == False:
        if flag1g == False:
            msg_rtn += 'both languages'
        else:
            msg_rtn = 'Missing grammar types for language 2'
        c_entry_repeat = False
        return msg_rtn, 2
    elif flag1g == False:
        msg_rtn += 'language 1'
        c_entry_repeat = False
        return msg_rtn, 2
    
    if len(l1_ent) != len(l2_ent):
        msg_rtn = 'Total no. of entries should be same on both sides'
        c_entry_repeat = False
        return msg_rtn, 2
    
    """for j in l1_ent:
        print(j)
    print()
    for j in l2_ent:
        print(j)
    print()"""
    


    # detect type of each entry

    l1_ent_type = [] # 0 -> dix; 1 -> lsx
    l2_ent_type = [] # 0 -> dix; 1 -> lsx
    
    flag1,flag2 = True, True

    try:
        for j in l1_ent:
            if type(j[1]) == list:
                l1_ent_type.append(0)
            else:
                l1_ent_type.append(1)
    except:
        flag1 = False
    try:
        for j in l2_ent:
            if type(j[1]) == list:
                l2_ent_type.append(0)
            else:
                l2_ent_type.append(1)
    except:
        flag2 = False
    if flag1 == False and flag2 == False:
        msg_rtn = 'Wrong data entered for both languages'
        c_entry_repeat = False
        return msg_rtn, 2
    elif flag1 == False:
        msg_rtn = 'Wrong data entered for languagee 1'
        c_entry_repeat = False
        return msg_rtn, 2
    elif flag2 == False:
        msg_rtn = 'Wrong data entered for languagee 2'
        c_entry_repeat = False
        return msg_rtn, 2


    # check correctness of entries by counting no. of lines for each

    crt1 = True
    crt2 = True
    crt_gmr1 = True
    crt_gmr2 = True
    cn_l1_r_groups = [] # count length of groups denoting roots # (e.g. हो जा -> हो गयी)
    cn_l2_r_groups = []
    cn_l1_gr_i = [] # stores position of 1st group of a new entry in cn_l1_r_groups
    cn_l2_gr_i = [] # stores position of 1st group of a new entry in cn_l2_r_groups
    if lsx_type != 1:
        for i in range(len(l1_ent_type)):
            cn_l1_gr_i.append(len(cn_l1_r_groups))
            if l1_ent_type[i] == 0:
                if len(l1_ent[i]) % 2 != 0:
                    crt1 = False
                    break
            else:
                count1 = 0 # no. of words forming a group
                i1 = 0
                while (i1 < len(l1_ent[i][0]) - 1):
                    if l1_ent[i][0][i1].isspace() == False:
                        if l1_ent[i][0][i1 + 1].isspace():
                            count1 += 1
                        elif puncs.__contains__(l1_ent[i][0][i1 + 1]) == True:
                            count1 += 1
                        elif (i1 - 1 >= 0) and puncs.__contains__(l1_ent[i][0][i1 - 1]) == True:
                            count1 += 1
                    i1 += 1
                if l1_ent[i][0][i1].isspace() == False:
                    count1 += 1
                    #if puncs.__contains__(l1_ent[i][0][i1]) == True:
                    #    count1 += 1
                count2 = 0 # no. of words forming roots
                j1 = 2
                while (j1 < len(l1_ent[i]) - 1):
                    if len(l1_ent[i][j1]) == 1: # 'i', 't', 'c'
                        if l1_ent[i][j1][0].isspace() == False:
                            count2 += 1
                            cn_l1_r_groups.append(1)
                    else:
                        flag1 = False
                        i1 = 0
                        while (i1 < len(l1_ent[i][j1]) - 1):
                            if l1_ent[i][j1][i1].isspace() == False:
                                if (l1_ent[i][j1][i1 + 1].isspace()) or (i1 + 1 == len(l1_ent[i][j1]) - 1):
                                    count2 += 1
                                    if flag1 == False:
                                        cn_l1_r_groups.append(1)
                                        flag1 = True
                                    else:
                                        cn_l1_r_groups[-1] += 1
                            i1 += 1
                        if i1 > 1: # For words of length 1 placed at last
                            if l1_ent[i][j1][i1 - 1].isspace() and l1_ent[i][j1][i1].isspace() == False:
                                count2 += 1
                                cn_l1_r_groups[-1] += 1
                    j1 += 2
                #if len(l1_ent[i]) != (2 * count1) + 2:
                if count1 != count2:
                    crt1 = False
                    break
                
        for i in range(len(l2_ent_type)):
            cn_l2_gr_i.append(len(cn_l2_r_groups))
            if l2_ent_type[i] == 0:
                if len(l2_ent[i]) % 2 != 0:
                    crt2 = False
                    break
            else:
                count1 = 0 # no. of words forming a group
                i2 = 0
                while (i2 < len(l2_ent[i][0]) - 1):
                    if l2_ent[i][0][i2].isspace() == False:
                        if l2_ent[i][0][i2 + 1].isspace():
                            count1 += 1
                        elif puncs.__contains__(l2_ent[i][0][i2 + 1]) == True:
                            count1 += 1
                        elif (i2 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][i2 - 1]) == True:
                            count1 += 1
                    i2 += 1
                if l2_ent[i][0][i2].isspace() == False:
                    count1 += 1
                    #elif puncs.__contains__(l2_ent[i][0][i2]) == True:
                        #count1 += 1
                count2 = 0 # no. of words forming roots
                j1 = 2
                while (j1 < len(l2_ent[i]) - 1):
                    if len(l2_ent[i][j1]) == 1: # 'i', 't', 'c'
                        if l2_ent[i][j1][0].isspace() == False:
                            count2 += 1
                            cn_l2_r_groups.append(1)
                    else:
                        flag1 = False
                        i1 = 0
                        while (i1 < len(l2_ent[i][j1]) - 1):
                            if l2_ent[i][j1][i1].isspace() == False:
                                if (l2_ent[i][j1][i1 + 1].isspace()) or (i1 + 1 == len(l2_ent[i][j1]) - 1):
                                    count2 += 1
                                    if flag1 == False:
                                        cn_l2_r_groups.append(1)
                                        flag1 = True
                                    else:
                                        cn_l2_r_groups[-1] += 1
                            i1 += 1
                        if i1 > 1: # For words of length 1 placed at last
                            if l2_ent[i][j1][i1 - 1].isspace() and l2_ent[i][j1][i1].isspace() == False:
                                count2 += 1
                                cn_l2_r_groups[-1] += 1
                    j1 += 2
                if count1 != count2:
                    crt2 = False
                    break
    

    else:
        for i in range(len(l1_ent_type)):
            cn_l1_gr_i.append(len(cn_l1_r_groups))
            if l1_ent_type[i] == 0:
                if len(l1_ent[i]) % 2 != 0:
                    crt1 = False
                    break
            else:
                if crt_gmr1 == True:
                    if type(l1_ent[i][-1]) != list or type(l1_ent[i][-2]) != list:
                        crt_gmr1 = False

                count1 = 0 # no. of words forming a group
                i1 = 0
                while (i1 < len(l1_ent[i][0]) - 1):
                    if l1_ent[i][0][i1].isspace() == False:
                        if l1_ent[i][0][i1 + 1].isspace():
                            count1 += 1
                        elif puncs.__contains__(l1_ent[i][0][i1 + 1]) == True:
                            count1 += 1
                        elif (i1 - 1 >= 0) and puncs.__contains__(l1_ent[i][0][i1 - 1]) == True:
                            count1 += 1
                    i1 += 1
                if l1_ent[i][0][i1].isspace() == False:
                    count1 += 1
                elif puncs.__contains__(l1_ent[i][0][i1]) == True:
                    count1 += 1
                count2 = 0 # no. of words forming roots
                j1 = 2
                while (j1 < len(l1_ent[i]) - 1):
                    if len(l1_ent[i][j1]) == 1:
                        if l1_ent[i][j1][0].isspace() == False:
                            count2 += 1
                            cn_l1_r_groups.append(1)
                    else:
                        flag1 = False
                        i1 = 0
                        while (i1 < len(l1_ent[i][j1]) - 1):
                            if l1_ent[i][j1][i1].isspace() == False:
                                if (l1_ent[i][j1][i1 + 1].isspace()) or (i1 + 1 == len(l1_ent[i][j1]) - 1):
                                    count2 += 1
                                    if flag1 == False:
                                        cn_l1_r_groups.append(1)
                                        flag1 = True
                                    else:
                                        cn_l1_r_groups[-1] += 1
                            i1 += 1
                        if i1 > 1: # For words of length 1 placed at last
                            if l1_ent[i][j1][i1 - 1].isspace() and l1_ent[i][j1][i1].isspace() == False:
                                count2 += 1
                                cn_l1_r_groups[-1] += 1
                    j1 += 2
                #if len(l1_ent[i]) != (2 * count1) + 1 + 2:
                if (count1 != count2):
                    crt1 = False
                    break

        for i in range(len(l2_ent_type)):
            cn_l2_gr_i.append(len(cn_l2_r_groups))
            if l2_ent_type[i] == 0:
                if len(l2_ent[i]) % 2 != 0:
                    crt2 = False
                    break
            else:
                if crt_gmr2 == True:
                    if type(l2_ent[i][-1]) != list or type(l2_ent[i][-2]) != list:
                        crt_gmr2 = False

                count1 = 0 # no. of words forming a group
                i2 = 0
                while (i2 < len(l2_ent[i][0]) - 1):
                    if l2_ent[i][0][i2].isspace() == False:
                        if l2_ent[i][0][i2 + 1].isspace():
                            count1 += 1
                        elif puncs.__contains__(l2_ent[i][0][i2 + 1]) == True:
                            count1 += 1
                        elif (i2 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][i2 - 1]) == True:
                            count1 += 1
                    i2 += 1
                if l2_ent[i][0][i2].isspace() == False:
                    count1 += 1
                count2 = 0 # no. of words forming roots
                j1 = 2
                while (j1 < len(l2_ent[i]) - 1):
                    if len(l2_ent[i][j1]) == 1:
                        if l2_ent[i][j1][0].isspace() == False:
                            count2 += 1
                            cn_l2_r_groups.append(1)
                    else:
                        flag1 = False
                        i1 = 0
                        while (i1 < len(l2_ent[i][j1]) - 1):
                            if l2_ent[i][j1][i1].isspace() == False:
                                if (l2_ent[i][j1][i1 + 1].isspace()) or (i1 + 1 == len(l2_ent[i][j1]) - 1):
                                    count2 += 1
                                    if flag1 == False:
                                        cn_l2_r_groups.append(1)
                                        flag1 = True
                                    else:
                                        cn_l2_r_groups[-1] += 1
                            i1 += 1
                        if i1 > 1: # For words of length 1 placed at last
                            if l2_ent[i][j1][i1 - 1].isspace() and l2_ent[i][j1][i1].isspace() == False:
                                count2 += 1
                                cn_l2_r_groups[-1] += 1
                    j1 += 2
                if (count1 != count2):
                    crt2 = False
                    break

    if lsx_type == 1:
        if (crt_gmr1 == False) and (crt_gmr2 == False):
            msg_rtn = 'Missing new assigned grammar types for both languages'
            c_entry_repeat = False
            return msg_rtn, 2
        elif crt_gmr1 == False:
            msg_rtn = 'Missing new assigned grammar types for language 1'
            c_entry_repeat = False
            return msg_rtn, 2
        elif crt_gmr2 == False:
            msg_rtn = 'Missing new assigned grammar types for language 2'
            c_entry_repeat = False
            return msg_rtn, 2
          
    if (crt1 == False) and (crt2 == False):
        msg_rtn = 'Missing root word or grammar types for both languages'
        c_entry_repeat = False
        return msg_rtn, 2
    elif crt1 == False:
        msg_rtn = 'Missing root word or grammar types for language 1'
        c_entry_repeat = False
        return msg_rtn, 2
    elif crt2 == False:
        msg_rtn = 'Missing root word or grammar types for language 2'
        c_entry_repeat = False
        return msg_rtn, 2



    # generate entries for dictionary

    if lsx_type != 1:
        for i in range(len(l1_ent_type)):
            pdm_check = [['',''], ['','']] # [word/root, grammar types] # used to compare with paradigm entries
            
            if l1_ent_type[i] == 1:

                # enter in l1_l2_lsx

                gen_dix.append([])
                
                try:
                    temp1 = '<e lm="' + l1_ent[i][0] + '" c="' + l1_ent[i][1] + '">\n<p><l>'
                
                    j1 = 2
                    while (j1 < len(l1_ent[i])):
                        temp1 = temp1 + l1_ent[i][j1]
                        for j2 in l1_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + j2 + '"/>'
                        temp1 = temp1 + '<d/>'
                        j1 += 2
                
                    temp1 = temp1 + '</l>\n<r>'
                    
                    temp2 = ''
                    count1 = cn_l1_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                    count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                    j1 = 0
                    while (j1 < len(l1_ent[i][0]) - 1):
                        if l1_ent[i][0][j1].isspace():
                            if l1_ent[i][0][j1 + 1].isspace() == False:
                                if puncs.__contains__(l1_ent[i][0][j1 + 1]) == True:
                                    count2 = 1
                                elif count2 >= cn_l1_r_groups[count1]:
                                    temp2 += '<b/>'
                                    pdm_check[0][0] += '<b/>'
                                    count1 += 1
                                    count2 = 1
                                else:
                                    temp2 += ' '
                                    pdm_check[0][0] += ' '
                                    if count2 >= cn_l1_r_groups[count1]:
                                        count1 += 1
                                        count2 = 1
                                    else:
                                        count2 += 1
                        elif puncs.__contains__(l1_ent[i][0][j1]) == True:
                            temp2 += '<b/>'
                            temp2 += l1_ent[i][0][j1]
                            pdm_check[0][0] += '<b/>'
                            pdm_check[0][0] += l1_ent[i][0][j1]
                            count1 += 1
                            count2 = 1
                            if l1_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                                temp2 += '<b/>'
                                pdm_check[0][0] += '<b/>'
                        else:
                            if (j1 - 1 >= 0) and puncs.__contains__(l1_ent[i][0][j1 - 1]) == True:
                                count1 += 1
                            temp2 += l1_ent[i][0][j1]
                            pdm_check[0][0] += l1_ent[i][0][j1]
                        j1 += 1
                    if l1_ent[i][0][j1].isspace() == False:
                        if puncs.__contains__(l1_ent[i][0][j1]) == True:
                            temp2 += '<b/>'
                            temp2 += l1_ent[i][0][j1]
                            pdm_check[0][0] += '<b/>'
                            pdm_check[0][0] += l1_ent[i][0][j1]
                        else:
                            temp2 += l1_ent[i][0][j1]
                            pdm_check[0][0] += l1_ent[i][0][j1]

                    r_list = [] # list of repeated 1st grammar types
                    j1 = 3
                    while (j1 < len(l1_ent[i]) - 2):
                        if r_list.__contains__(j1) == False:
                            j2 = j1 + 2
                            while (j2 < len(l1_ent[i])):
                                if l1_ent[i][j1][0] == l1_ent[i][j2][0]:
                                    r_list.append(j2)
                                j2 += 2
                            temp2 = temp2 + '<s n="' + l1_ent[i][j1][0] + '"/>'
                            pdm_check[0][1] = pdm_check[0][1] + '<s n="' + l1_ent[i][j1][0] + '"/>'
                        j1 += 2
                    if r_list.__contains__(j1) == False:
                        temp2 = temp2 + '<s n="' + l1_ent[i][j1][0] + '"/>'
                        pdm_check[0][1] = pdm_check[0][1] + '<s n="' + l1_ent[i][j1][0] + '"/>'
                    
                    j1 = 1
                    while (j1 < len(l1_ent[i][3])):
                        j2 = 5
                        while (j2 < len(l1_ent[i])):
                            grm = 1
                            while (grm < len(l1_ent[i][j2])):
                                if l1_ent[i][j2][grm] == l1_ent[i][3][j1]:
                                    break # found
                                grm += 1
                            if grm == len(l1_ent[i][j2]):
                                break # do not check succeeding grammar types in the list
                            j2 += 2
                        if j2 >= len(l1_ent[i]):
                            temp2 = temp2 + '<s n="' + l1_ent[i][3][j1] + '"/>'
                            pdm_check[0][1] = pdm_check[0][1] + '<s n="' + l1_ent[i][3][j1] + '"/>'
                        j1 += 1
                        
                    temp1 = temp1 + temp2 + '</r></p>\n</e>'
                    l1_lsx.append(temp1)
                    msg_rtn = ''

                except:
                    msg_rtn = 'Possible error in grammar types for ' #language 1             
            
                if l2_ent_type[i] == 1:

                    # enter in l2_l1_lsx

                    try:
                        temp1 = '<e lm="' + l2_ent[i][0] + '" c="' + l2_ent[i][1] + '">\n<p><l>'
                        j1 = 2
                        while (j1 < len(l2_ent[i])):
                            temp1 = temp1 + l2_ent[i][j1]
                            for j2 in l2_ent[i][j1 + 1]:
                                temp1 = temp1 + '<s n="' + j2 + '"/>'
                            temp1 = temp1 + '<d/>'
                            j1 += 2
                        temp1 = temp1 + '</l>\n<r>'

                        temp3 = ''
                        count1 = cn_l2_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                        count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                        j1 = 0
                        while (j1 < len(l2_ent[i][0]) - 1):
                            if l2_ent[i][0][j1].isspace():
                                if l2_ent[i][0][j1 + 1].isspace() == False:
                                    if puncs.__contains__(l2_ent[i][0][j1 + 1]) == True:
                                        count2 = 1
                                    elif count2 >= cn_l2_r_groups[count1]:
                                        temp3 += '<b/>'
                                        pdm_check[1][0] += '<b/>'
                                        count1 += 1
                                        count2 = 1
                                    else:
                                        temp3 += ' '
                                        pdm_check[1][0] += ' '
                                        if count2 >= cn_l2_r_groups[count1]:
                                            count1 += 1
                                            count2 = 1
                                        else:
                                            count2 += 1
                            elif puncs.__contains__(l2_ent[i][0][j1]) == True:
                                temp3 += '<b/>'
                                temp3 += l2_ent[i][0][j1]
                                pdm_check[1][0] += '<b/>'
                                pdm_check[1][0] += l2_ent[i][0][j1]
                                count1 += 1
                                count2 = 1
                                if l2_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                                    temp3 += '<b/>'
                                    pdm_check[1][0] += '<b/>'
                            else:
                                if (j1 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][j1 - 1]) == True:
                                    count1 += 1
                                temp3 += l2_ent[i][0][j1]
                                pdm_check[1][0] += l2_ent[i][0][j1]
                            j1 += 1
                        if l2_ent[i][0][j1].isspace() == False:
                            if puncs.__contains__(l2_ent[i][0][j1]) == True:
                                temp3 += '<b/>'
                                temp3 += l2_ent[i][0][j1]
                                pdm_check[1][0] += '<b/>'
                                pdm_check[1][0] += l2_ent[i][0][j1]
                            else:
                                temp3 += l2_ent[i][0][j1]
                                pdm_check[1][0] += l2_ent[i][0][j1]

                        r_list = [] # list of repeated 1st grammar types
                        j1 = 3
                        while (j1 < len(l2_ent[i]) - 2):
                            if r_list.__contains__(j1) == False:
                                j2 = j1 + 2
                                while (j2 < len(l2_ent[i])):
                                    if l2_ent[i][j1][0] == l2_ent[i][j2][0]:
                                        r_list.append(j2)
                                    j2 += 2
                                temp3 = temp3 + '<s n="' + l2_ent[i][j1][0] + '"/>'
                                pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][j1][0] + '"/>'
                            j1 += 2
                        if r_list.__contains__(j1) == False:
                            temp3 = temp3 + '<s n="' + l2_ent[i][j1][0] + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][j1][0] + '"/>'
                        
                        j1 = 1
                        while (j1 < len(l2_ent[i][3])):
                            j2 = 5
                            while (j2 < len(l2_ent[i])):
                                grm = 1
                                while (grm < len(l2_ent[i][j2])):
                                    if l2_ent[i][j2][grm] == l2_ent[i][3][j1]:
                                        break # found
                                    grm += 1
                                if grm == len(l2_ent[i][j2]):
                                    break # do not check succeeding grammar types in the list
                                j2 += 2
                            if j2 >= len(l2_ent[i]):
                                temp3 = temp3 + '<s n="' + l2_ent[i][3][j1] + '"/>'
                                pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][3][j1] + '"/>'
                            j1 += 1
                            
                        temp1 = temp1 + temp3 + '</r></p>\n</e>'
                        l2_lsx.append(temp1)


                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j1 = 0
                            while (j1 < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j1][0] == pdm_check[0][1] and pdms[pdm_list][1][j1][1] == pdm_check[1][1]:
                                    break
                                j1 += 1
                            if j1 < len(pdms[pdm_list][1]):
                                # add new temp1 here
                                temp1 = '<e><p><l>' + pdm_check[0][0] + '</l><r>' + pdm_check[1][0] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        
                        if msg_rtn != '': # temp2 does not exist
                            msg_rtn = msg_rtn + 'language 1'
                            c_entry_repeat = False
                            return msg_rtn, 2
                        else:
                            if pdm_list == len(pdms) or len(pdms) == 0:
                                temp1 = '<e><p><l>' + str(temp2) + '</l><r>' + str(temp3) + '</r></p></e>'
                            gen_dix[-1].append(temp1)

                    except:
                        if msg_rtn != '':
                            msg_rtn = msg_rtn + 'both languages'
                            c_entry_repeat = False
                            return msg_rtn, 2
                        else:
                            msg_rtn = 'Possible error in grammar types for language 2'
                            c_entry_repeat = False
                            return msg_rtn, 2


                else:
                    if msg_rtn != '':
                        msg_rtn = msg_rtn + 'language 1'
                        c_entry_repeat = False
                        return msg_rtn, 2
                    
                    j1 = 0
                    while (j1 < len(l2_ent[i])):
                        temp1 = '<e><p><l>' + temp2 + '</l><r>' + l2_ent[i][j1]
                        pdm_check[1][1] = ''
                        for grm in l2_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + grm + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'
                        
                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j = 0
                            while (j < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                    break
                                j += 1
                            if j < len(pdms[pdm_list][1]):
                                # add new temp1 here
                                temp1 = '<e><p><l>' + pdm_check[0][0] + '</l><r>' + l2_ent[i][j1] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        if pdm_list == len(pdms) or len(pdms) == 0:
                            temp1 = temp1 + '</r></p></e>'
                        gen_dix[-1].append(temp1)
                        j1 += 2

            elif l2_ent_type[i] == 1:

                # enter in l2_l1_lsx

                gen_dix.append([])

                try:
                    temp1 = '<e lm="' + l2_ent[i][0] + '" c="' + l2_ent[i][1] + '">\n<p><l>'
                    j1 = 2
                    while (j1 < len(l2_ent[i])):
                        temp1 = temp1 + l2_ent[i][j1]
                        for j2 in l2_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + j2 + '"/>'
                        temp1 = temp1 + '<d/>'
                        j1 += 2
                    temp1 = temp1 + '</l>\n<r>'
                    
                    temp2 = ''
                    count1 = cn_l2_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                    count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                    j1 = 0
                    while (j1 < len(l2_ent[i][0]) - 1):
                        if l2_ent[i][0][j1].isspace():
                            if l2_ent[i][0][j1 + 1].isspace() == False:
                                if puncs.__contains__(l2_ent[i][0][j1 + 1]) == True:
                                    count2 = 1
                                elif count2 >= cn_l2_r_groups[count1]:
                                    temp2 += '<b/>'
                                    pdm_check[1][0] += '<b/>'
                                    count1 += 1
                                    count2 = 1
                                else:
                                    temp2 += ' '
                                    pdm_check[1][0] += ' '
                                    if count2 >= cn_l2_r_groups[count1]:
                                        count1 += 1
                                        count2 = 1
                                    else:
                                        count2 += 1
                        elif puncs.__contains__(l2_ent[i][0][j1]) == True:
                            temp2 += '<b/>'
                            temp2 += l2_ent[i][0][j1]
                            pdm_check[1][0] += '<b/>'
                            pdm_check[1][0] += l2_ent[i][0][j1]
                            count1 += 1
                            count2 = 1
                            if l2_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                                temp2 += '<b/>'
                                pdm_check[1][0] += '<b/>'
                        else:
                            if (j1 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][j1 - 1]) == True:
                                count1 += 1
                            temp2 += l2_ent[i][0][j1]
                            pdm_check[1][0] += l2_ent[i][0][j1]
                        j1 += 1
                    if l2_ent[i][0][j1].isspace() == False:
                        if puncs.__contains__(l2_ent[i][0][j1]) == True:
                            temp2 += '<b/>'
                            temp2 += l2_ent[i][0][j1]
                            pdm_check[1][0] += '<b/>'
                            pdm_check[1][0] += l2_ent[i][0][j1]
                        else:
                            temp2 += l2_ent[i][0][j1]
                            pdm_check[1][0] += l2_ent[i][0][j1]
                    
                    r_list = [] # list of repeated 1st grammar types
                    j1 = 3
                    while (j1 < len(l2_ent[i]) - 2):
                        if r_list.__contains__(j1) == False:
                            j2 = j1 + 2
                            while (j2 < len(l2_ent[i])):
                                if l2_ent[i][j1][0] == l2_ent[i][j2][0]:
                                    r_list.append(j2)
                                j2 += 2
                            temp2 = temp2 + '<s n="' + l2_ent[i][j1][0] + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][j1][0] + '"/>'
                        j1 += 2
                    if r_list.__contains__(j1) == False:
                        temp2 = temp2 + '<s n="' + l2_ent[i][j1][0] + '"/>'
                        pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][j1][0] + '"/>'
                    
                    j1 = 1
                    while (j1 < len(l2_ent[i][3])):
                        j2 = 5
                        while (j2 < len(l2_ent[i])):
                            grm = 1
                            while (grm < len(l2_ent[i][j2])):
                                if l2_ent[i][j2][grm] == l2_ent[i][3][j1]:
                                    break # found
                                grm += 1
                            if grm == len(l2_ent[i][j2]):
                                break # do not check succeeding grammar types in the list
                            j2 += 2
                        if j2 >= len(l2_ent[i]):
                            temp2 = temp2 + '<s n="' + l2_ent[i][3][j1] + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + l2_ent[i][3][j1] + '"/>'
                        j1 += 1
                        
                    temp1 = temp1 + temp2 + '</r></p>\n</e>'
                    l2_lsx.append(temp1)

                    j1 = 0
                    while (j1 < len(l1_ent[i])):
                        temp1 = '<e><p><l>' + l1_ent[i][j1]
                        pdm_check[0][1] = ''
                        for grm in l1_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + grm + '"/>'
                            pdm_check[0][1] = pdm_check[0][1] + '<s n="' + grm + '"/>'
                        
                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j = 0
                            while (j < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                    break
                                j += 1
                            if j < len(pdms[pdm_list][1]):
                                # add new temp1 here
                                temp1 = '<e><p><l>' + l1_ent[i][j1] + '</l><r>' + pdm_check[0][0] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        if pdm_list == len(pdms) or len(pdms) == 0:
                            temp1 = temp1 + '</l><r>' + temp2 + '</r></p></e>'
                        gen_dix[-1].append(temp1)
                        j1 += 2
                
                except:
                    msg_rtn = 'Possible error in grammar types for language 2'
                    c_entry_repeat = False
                    return msg_rtn, 2

            else:
                # usual dix entry

                gen_dix.append([])
                j1 = 0
                while (j1 < len(l1_ent[i])):
                    temp1 = '<e><p><l>' + l1_ent[i][j1]
                    pdm_check[0][1] = ''
                    for grm in l1_ent[i][j1 + 1]:
                        temp1 = temp1 + '<s n="' + grm + '"/>'
                        pdm_check[0][1] = pdm_check[0][1] + '<s n="' + grm + '"/>'
                    temp1 = temp1 + '</l><r>'
                    j2 = 0
                    while (j2 < len(l2_ent[i])):
                        temp2 = temp1 + l2_ent[i][j2]
                        pdm_check[1][1] = ''
                        for grm in l2_ent[i][j2 + 1]:
                            temp2 = temp2 + '<s n="' + grm + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'
                        
                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j = 0
                            while (j < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                    break
                                j += 1
                            if j < len(pdms[pdm_list][1]):
                                # add new temp2 here
                                temp2 = '<e><p><l>' + l1_ent[i][j1] + '</l><r>' + l2_ent[i][j2] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        if pdm_list == len(pdms) or len(pdms) == 0:
                            temp2 = temp2 + '</r></p></e>'
                        gen_dix[-1].append(temp2)
                        j2 += 2                
                    j1 += 2

    else:
        for i in range(len(l1_ent_type)):
            pdm_check = [['',''], ['','']] # [word/root, grammar types] # used to compare with paradigm entries

            if l1_ent_type[i] == 1:

                # enter in l1_l2_lsx

                gen_dix.append([])

                temp1 = '<e lm="' + l1_ent[i][0] + '" c="' + l1_ent[i][1] + '">\n<p><l>'
                j1 = 2
                while (j1 < len(l1_ent[i]) - 1):
                    temp1 = temp1 + l1_ent[i][j1]
                    for j2 in l1_ent[i][j1 + 1]:
                        temp1 = temp1 + '<s n="' + j2 + '"/>'
                    temp1 = temp1 + '<d/>'
                    j1 += 2
                temp1 = temp1 + '</l>\n<r>'
                
                temp2 = ''
                count1 = cn_l1_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                j1 = 0
                while (j1 < len(l1_ent[i][0]) - 1):
                    if l1_ent[i][0][j1].isspace():
                        if l1_ent[i][0][j1 + 1].isspace() == False:
                            if puncs.__contains__(l1_ent[i][0][j1 + 1]) == True:
                                count2 = 1
                            elif count2 >= cn_l1_r_groups[count1]:
                                temp2 += '<b/>'
                                pdm_check[0][0] += '<b/>'
                                count1 += 1
                                count2 = 1
                            else:
                                temp2 += ' '
                                pdm_check[0][0] += ' '
                                if count2 >= cn_l1_r_groups[count1]:
                                    count1 += 1
                                    count2 = 1
                                else:
                                    count2 += 1
                    elif puncs.__contains__(l1_ent[i][0][j1]) == True:
                        temp2 += '<b/>'
                        temp2 += l1_ent[i][0][j1]
                        pdm_check[0][0] += '<b/>'
                        pdm_check[0][0] += l1_ent[i][0][j1]
                        count1 += 1
                        count2 = 1
                        if l1_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                            temp2 += '<b/>'
                            pdm_check[0][0] += '<b/>'
                    else:
                        if (j1 - 1 >= 0) and puncs.__contains__(l1_ent[i][0][j1 - 1]) == True:
                            count1 += 1
                        temp2 += l1_ent[i][0][j1]
                        pdm_check[0][0] += l1_ent[i][0][j1]
                    j1 += 1
                if l1_ent[i][0][j1].isspace() == False:   
                    if puncs.__contains__(l1_ent[i][0][j1]) == True:
                        temp2 += '<b/>'
                        temp2 += l1_ent[i][0][j1]
                        pdm_check[0][0] += '<b/>'
                        pdm_check[0][0] += l1_ent[i][0][j1]
                    else:
                        temp2 += l1_ent[i][0][j1]
                        pdm_check[0][0] += l1_ent[i][0][j1]

                # new grammar types
                for grm in l1_ent[i][-1]:
                    temp2 = temp2 + '<s n="' + grm + '"/>'
                    pdm_check[0][1] = pdm_check[0][1] + '<s n="' + grm + '"/>'

                temp1 = temp1 + temp2 + '</r></p>\n</e>'
                l1_lsx.append(temp1)

                if l2_ent_type[i] == 1:

                    # enter in l2_l1_lsx

                    temp1 = '<e lm="' + l2_ent[i][0] + '" c="' + l2_ent[i][1] + '">\n<p><l>'
                    j1 = 2
                    while (j1 < len(l2_ent[i]) - 1):
                        temp1 = temp1 + l2_ent[i][j1]
                        for j2 in l2_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + j2 + '"/>'
                        temp1 = temp1 + '<d/>'
                        j1 += 2
                    temp1 = temp1 + '</l>\n<r>'

                    temp3 = ''
                    count1 = cn_l2_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                    count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                    j1 = 0
                    while (j1 < len(l2_ent[i][0]) - 1):
                        if l2_ent[i][0][j1].isspace():
                            if l2_ent[i][0][j1 + 1].isspace() == False:
                                if puncs.__contains__(l2_ent[i][0][j1 + 1]) == True:
                                    count2 = 1
                                elif count2 >= cn_l2_r_groups[count1]:
                                    temp3 += '<b/>'
                                    pdm_check[1][0] += '<b/>'
                                    count1 += 1
                                    count2 = 1
                                else:
                                    temp3 += ' '
                                    pdm_check[1][0] += ' '
                                    if count2 >= cn_l2_r_groups[count1]:
                                        count1 += 1
                                        count2 = 1
                                    else:
                                        count2 += 1
                        elif puncs.__contains__(l2_ent[i][0][j1]) == True:
                            temp3 += '<b/>'
                            temp3 += l2_ent[i][0][j1]
                            pdm_check[1][0] += '<b/>'
                            pdm_check[1][0] += l2_ent[i][0][j1]
                            count1 += 1
                            count2 = 1
                            if l2_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                                temp3 += '<b/>'
                                pdm_check[1][0] += '<b/>'
                        else:
                            if (j1 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][j1 - 1]) == True:
                                count1 += 1
                            temp3 += l2_ent[i][0][j1]
                            pdm_check[1][0] += l2_ent[i][0][j1]
                        j1 += 1
                    if l2_ent[i][0][j1].isspace() == False:
                        if puncs.__contains__(l2_ent[i][0][j1]) == True:
                            temp3 += '<b/>'
                            temp3 += l2_ent[i][0][j1]
                            pdm_check[1][0] += '<b/>'
                            pdm_check[1][0] += l2_ent[i][0][j1]
                        else:
                            temp3 += l2_ent[i][0][j1]
                            pdm_check[1][0] += l2_ent[i][0][j1]

                    # new grammar types
                    for grm in l2_ent[i][-1]:
                        temp3 = temp3 + '<s n="' + grm + '"/>'
                        pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'
                        
                    temp1 = temp1 + temp3 + '</r></p>\n</e>'
                    l2_lsx.append(temp1)


                    # compare pdm_check with entries in pdms

                    pdm_list = 0
                    while (pdm_list < len(pdms)):
                        j1 = 0
                        while (j1 < len(pdms[pdm_list][1])):
                            if pdms[pdm_list][1][j1][0] == pdm_check[0][1] and pdms[pdm_list][1][j1][1] == pdm_check[1][1]:
                                break
                            j1 += 1
                        if j1 < len(pdms[pdm_list][1]):
                            # add new temp1 here
                            temp1 = '<e><p><l>' + pdm_check[0][0] + '</l><r>' + pdm_check[1][0] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                            break
                        pdm_list += 1
                    if pdm_list == len(pdms) or len(pdms) == 0:
                        temp1 = '<e><p><l>' + temp2 + '</l><r>' + temp3 + '</r></p></e>'
                    gen_dix[-1].append(temp1)

                else:
                    j1 = 0
                    while (j1 < len(l2_ent[i])):
                        temp1 = '<e><p><l>' + temp2 + '</l><r>' + l2_ent[i][j1]
                        pdm_check[1][1] = ''
                        for grm in l2_ent[i][j1 + 1]:
                            temp1 = temp1 + '<s n="' + grm + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'
                        
                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j = 0
                            while (j < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                    break
                                j += 1
                            if j < len(pdms[pdm_list][1]):
                                # add new temp1 here
                                temp1 = '<e><p><l>' + pdm_check[0][0] + '</l><r>' + l2_ent[i][j1] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        if pdm_list == len(pdms) or len(pdms) == 0:    
                            temp1 = temp1 + '</r></p></e>'
                        gen_dix[-1].append(temp1)
                        j1 += 2

            elif l2_ent_type[i] == 1:

                # enter in l2_l1_lsx

                gen_dix.append([])

                temp1 = '<e lm="' + l2_ent[i][0] + '" c="' + l2_ent[i][1] + '">\n<p><l>'
                j1 = 2
                while (j1 < len(l2_ent[i]) - 1):
                    temp1 = temp1 + l2_ent[i][j1]
                    for j2 in l2_ent[i][j1 + 1]:
                        temp1 = temp1 + '<s n="' + j2 + '"/>'
                    temp1 = temp1 + '<d/>'
                    j1 += 2
                temp1 = temp1 + '</l>\n<r>'
                
                temp2 = ''
                count1 = cn_l2_gr_i[i] # iterate through integers in cn_l_r_groups # [[], [], []] -> len = 3
                count2 = 1 # iterate as per values of integers in cn_l_r_groups # ['give up' -> 'give' = 1, 'up' = 2]
                j1 = 0
                while (j1 < len(l2_ent[i][0]) - 1):
                    if l2_ent[i][0][j1].isspace():
                        if l2_ent[i][0][j1 + 1].isspace() == False:
                            if puncs.__contains__(l2_ent[i][0][j1 + 1]) == True:
                                count2 = 1
                            elif count2 >= cn_l2_r_groups[count1]:
                                temp2 += '<b/>'
                                pdm_check[1][0] += '<b/>'
                                count1 += 1
                                count2 = 1
                            else:
                                temp2 += ' '
                                pdm_check[1][0] += ' '
                                if count2 >= cn_l2_r_groups[count1]:
                                    count1 += 1
                                    count2 = 1
                                else:
                                    count2 += 1
                    elif puncs.__contains__(l2_ent[i][0][j1]) == True:
                        temp2 += '<b/>'
                        temp2 += l2_ent[i][0][j1]
                        pdm_check[1][0] += '<b/>'
                        pdm_check[1][0] += l2_ent[i][0][j1]
                        count1 += 1
                        count2 = 1
                        if l2_ent[i][0][j1 + 1].isspace() == False: # w1,w2
                            temp2 += '<b/>'
                            pdm_check[1][0] += '<b/>'
                    else:
                        if (j1 - 1 >= 0) and puncs.__contains__(l2_ent[i][0][j1 - 1]) == True:
                            count1 += 1
                        temp2 += l2_ent[i][0][j1]
                        pdm_check[1][0] += l2_ent[i][0][j1]
                    j1 += 1
                if l2_ent[i][0][j1].isspace() == False:
                    if puncs.__contains__(l2_ent[i][0][j1]) == True:
                        temp2 += '<b/>'
                        temp2 += l2_ent[i][0][j1]
                        pdm_check[1][0] += '<b/>'
                        pdm_check[1][0] += l2_ent[i][0][j1]
                    else:    
                        temp2 += l2_ent[i][0][j1]
                        pdm_check[1][0] += l2_ent[i][0][j1]
                
                # new grammar types

                for grm in l2_ent[i][-1]:
                    temp2 = temp2 + '<s n="' + grm + '"/>'
                    pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'
                    
                temp1 = temp1 + temp2 + '</r></p>\n</e>'
                l2_lsx.append(temp1)

                j1 = 0
                while (j1 < len(l1_ent[i])):
                    temp1 = '<e><p><l>' + l1_ent[i][j1]
                    pdm_check[0][1] = ''
                    for grm in l1_ent[i][j1 + 1]:
                        temp1 = temp1 + '<s n="' + grm + '"/>'
                        pdm_check[0][1] = pdm_check[0][1] + '<s n="' + grm + '"/>'
                    
                    # compare pdm_check with entries in pdms

                    pdm_list = 0
                    while (pdm_list < len(pdms)):
                        j = 0
                        while (j < len(pdms[pdm_list][1])):
                            if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                break
                            j += 1
                        if j < len(pdms[pdm_list][1]):
                            # add new temp1 here
                            temp1 = '<e><p><l>' + l1_ent[i][j1] + '</l><r>' + pdm_check[0][0] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                            break
                        pdm_list += 1
                    if pdm_list == len(pdms) or len(pdms) == 0:
                        temp1 = temp1 + '</l><r>' + temp2 + '</r></p></e>'
                    gen_dix[-1].append(temp1)
                    j1 += 2

            else:
                # usual dix entry

                gen_dix.append([])
                j1 = 0
                while (j1 < len(l1_ent[i])):
                    temp1 = '<e><p><l>' + l1_ent[i][j1]
                    pdm_check[0][1] = ''
                    for grm in l1_ent[i][j1 + 1]:
                        temp1 = temp1 + '<s n="' + grm + '"/>'
                        pdm_check[0][1] = pdm_check[0][1] + '<s n="' + grm + '"/>'
                    temp1 = temp1 + '</l><r>'
                    j2 = 0
                    while (j2 < len(l2_ent[i])):
                        temp2 = temp1 + l2_ent[i][j2]
                        pdm_check[1][1] = ''
                        for grm in l2_ent[i][j2 + 1]:
                            temp2 = temp2 + '<s n="' + grm + '"/>'
                            pdm_check[1][1] = pdm_check[1][1] + '<s n="' + grm + '"/>'

                        # compare pdm_check with entries in pdms

                        pdm_list = 0
                        while (pdm_list < len(pdms)):
                            j = 0
                            while (j < len(pdms[pdm_list][1])):
                                if pdms[pdm_list][1][j][0] == pdm_check[0][1] and pdms[pdm_list][1][j][1] == pdm_check[1][1]:
                                    break
                                j += 1
                            if j < len(pdms[pdm_list][1]):
                                # add new temp2 here
                                temp2 = '<e><p><l>' + l1_ent[i][j1] + '</l><r>' + l2_ent[i][j2] + '</r></p><par n="' + pdms[pdm_list][0] + '"/></e>'
                                break
                            pdm_list += 1
                        if pdm_list == len(pdms) or len(pdms) == 0:
                            temp2 = temp2 + '</r></p></e>'
                        gen_dix[-1].append(temp2)
                        j2 += 2                
                    j1 += 2



    # delete repeated entries from new list
    
    i1 = 0
    while (i1 < len(gen_dix) - 1):
        i2 = 0
        while (i2 < len(gen_dix[i1]) - 1):
            i3 = i2 + 1
            while (i3 < len(gen_dix[i1])):
                if gen_dix[i1][i2] == gen_dix[i1][i3]:
                    del gen_dix[i1][i3]
                else:
                    i3 += 1
            i2 += 1
        j1 = i1 + 1
        while (j1 < len(gen_dix)):
            i2 = 0
            while (i2 < len(gen_dix[i1])):
                j2 = 0
                while (j2 < len(gen_dix[j1])):
                    if gen_dix[i1][i2] == gen_dix[j1][j2]:
                        del gen_dix[j1][j2]
                    else:
                        j2 += 1
                i2 += 1
            j1 += 1
        i1 += 1
    i2 = 0
    while (i2 < len(gen_dix[i1]) - 1): # final list
        i3 = i2 + 1
        while (i3 < len(gen_dix[i1])):
            if gen_dix[i1][i2] == gen_dix[i1][i3]:
                del gen_dix[i1][i3]
            else:
                i3 += 1
        i2 += 1


    i1 = 0
    while (i1 < len(l1_lsx) - 1):
        i2 = i1 + 1
        while (i2 < len(l1_lsx)):
            if l1_lsx[i1] == l1_lsx[i2]:
                del l1_lsx[i2]
            else:
                i2 += 1
        i1 += 1

    i1 = 0
    while (i1 < len(l2_lsx) - 1):
        i2 = i1 + 1
        while (i2 < len(l2_lsx)):
            if l2_lsx[i1] == l2_lsx[i2]:
                del l2_lsx[i2]
            else:
                i2 += 1
        i1 += 1

    """print()
    for i in gen_dix:
        print(i)"""
    
    if output_type == 0: # append to existing files
        dix_file = open(addr + '/l1_l2_dix.txt', 'a+', newline='', encoding='utf-8')
        l1_lsx_file = open(addr + '/l1_l2_lsx.txt', 'a+', newline='', encoding='utf-8')
        l2_lsx_file = open(addr + '/l2_l1_lsx.txt', 'a+', newline='', encoding='utf-8')
    
    else: # create new files
        dix_file = open(addr + '/l1_l2_dix.txt', 'w', newline='', encoding='utf-8')
        l1_lsx_file = open(addr + '/l1_l2_lsx.txt', 'w', newline='', encoding='utf-8')
        l2_lsx_file = open(addr + '/l2_l1_lsx.txt', 'w', newline='', encoding='utf-8')
        
    for i1 in gen_dix:
        for i2 in i1:
            dix_file.write(i2)
            dix_file.write('\n')
        dix_file.write('\n')
    
    for i in l1_lsx:
        l1_lsx_file.write(i)
        l1_lsx_file.write('\n')
    
    for i in l2_lsx:
        l2_lsx_file.write(i)
        l2_lsx_file.write('\n')

    msg_rtn = 'Successfully generated Apertium entries'
    if c_entry_repeat == False:
        c_entry_repeat = True
        c_entry_color = 3
        return msg_rtn, 1
    else:
        if c_entry_color == 3:
            c_entry_color = 1
            return msg_rtn, 3
        else:
            c_entry_color = 3
            return msg_rtn, 1

def delete_duplicate(addr):
    global c_entry_repeat
    
    f_test = [1, 1, 1]# 0 if file does not exits    # dix, l1_lsx, l2_lsx
    
    try:
        dix_data = []
        dix_file = open(addr + '/l1_l2_dix.txt', 'r', encoding='utf-8')
        dix_readline = dix_file.readlines()
        for line in dix_readline:
            dix_data.append(line)
        dix_file.close()



        # check for duplicates

        i1 = 0
        while (i1 < len(dix_data) - 1):
            if ((len(dix_data[i1]) == 1) and (dix_data[i1] == '\n')):
                i1 += 1
            elif dix_data[i1] != '':
                i2 = i1 + 1
                temp1 = len(dix_data)
                while (i2 < len(dix_data)):
                    if dix_data[i1] == dix_data[i2]:
                        del dix_data[i2]
                    else:
                        i2 += 1
                if i2 == temp1:
                    i1 += 1
            else:
                i1 += 1



        # delete sequencial new / empty lines

        i1 = 0
        while (i1 < len(dix_data) - 1):
            i2 = i1 + 1
            if ((len(dix_data[i1]) == 1) and (dix_data[i1] == '\n')) or dix_data[i1] == '':
                while (i2 < len(dix_data)):
                    if ((len(dix_data[i2]) == 1) and (dix_data[i2] == '\n')) or dix_data[i2] == '':
                        del dix_data[i2]
                    else:
                        break
            i1 = i2

        dix_file = open(addr + '/l1_l2_dix.txt', 'w', newline='', encoding='utf-8')
        for i1 in dix_data:
            dix_file.write(i1)

    except:
        f_test[0] = 0

    try:
        l1_lsx_data = []
        l1_lsx_file = open(addr + '/l1_l2_lsx.txt', 'r', encoding='utf-8')
        l1_lsx_readline = l1_lsx_file.readlines()
        for line in l1_lsx_readline:
            if line.__contains__('<e ') == True:
                if line[-1] == '\n':
                    temp1 = ''
                    for i1 in range(len(line) - 1):
                        temp1 += line[i1]
                    l1_lsx_data.append([temp1])
                else:
                    l1_lsx_data.append([line])
            else:
                if ((len(line) == 1) and (line == '\n')) or line == '':
                    pass
                else:
                    if line[-1] == '\n':
                        temp1 = ''
                        for i1 in range(len(line) - 1):
                            temp1 += line[i1]
                        l1_lsx_data[-1].append(temp1)
                    else:
                        l1_lsx_data[-1].append(line)
        l1_lsx_file.close()



        # check for duplicates
        i1 = 0
        while (i1 < len(l1_lsx_data) - 1):
            i2 = i1 + 1
            temp1 = len(l1_lsx_data)
            while (i2 < len(l1_lsx_data)):
                if l1_lsx_data[i1] == l1_lsx_data[i2]:
                    del l1_lsx_data[i2]
                else:
                    i2 += 1
            if i2 == temp1:
                i1 += 1



        # write LSX file

        l1_lsx_file = open(addr + '/l1_l2_lsx.txt', 'w', newline='', encoding='utf-8')
        for i1 in l1_lsx_data:
            for i2 in i1:
                l1_lsx_file.write(i2)
                l1_lsx_file.write('\n')

    except:
        f_test[1] = 0

    try:
        l2_lsx_data = []
        l2_lsx_file = open(addr + '/l2_l1_lsx.txt', 'r', encoding='utf-8')
        l2_lsx_readline = l2_lsx_file.readlines()
        for line in l2_lsx_readline:
            if line.__contains__('<e ') == True:
                if line[-1] == '\n':
                    temp1 = ''
                    for i1 in range(len(line) - 1):
                        temp1 += line[i1]
                    l2_lsx_data.append([temp1])
                else:
                    l2_lsx_data.append([line])
            else:
                if ((len(line) == 1) and (line == '\n')) or line == '':
                    pass
                else:
                    if line[-1] == '\n':
                        temp1 = ''
                        for i1 in range(len(line) - 1):
                            temp1 += line[i1]
                        l2_lsx_data[-1].append(temp1)
                    else:
                        l2_lsx_data[-1].append(line)
        l2_lsx_file.close()



        # check for duplicates

        i1 = 0
        while (i1 < len(l2_lsx_data) - 1):
            i2 = i1 + 1
            temp1 = len(l2_lsx_data)
            while (i2 < len(l2_lsx_data)):
                if l2_lsx_data[i1] == l2_lsx_data[i2]:
                    del l2_lsx_data[i2]
                else:
                    i2 += 1
            if i2 == temp1:
                i1 += 1



        # write LSX file

        l2_lsx_file = open(addr + '/l2_l1_lsx.txt', 'w', newline='', encoding='utf-8')
        for i1 in l2_lsx_data:
            for i2 in i1:
                l2_lsx_file.write(i2)
                l2_lsx_file.write('\n')

    except:
        f_test[2] = 0
    


    if addr == '' or addr.isspace():
        msg_rtn = 'Output directory not specified'
        c_entry_repeat = False
        return msg_rtn, 0
    elif f_test[0] == 0 and f_test[1] == 0 and f_test[2] == 0:
        msg_rtn = 'No output files found'
        c_entry_repeat = False
        return msg_rtn, 0
    else:
        msg_rtn = 'Successfully deleted duplicate entries'
        c_entry_repeat = False
        return msg_rtn, 1
