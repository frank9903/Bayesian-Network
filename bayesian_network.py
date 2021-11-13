import numpy as np
import copy

def restrict(factor, variable, value):
    restricted_factor = []
    labels = factor[0]
    if (variable not in labels):
        return None
    idx = labels.index(variable)
    restricted_factor.append(labels[:idx] + labels[idx+1:])
    print("Restrict f("+" ".join(labels[:-1])+") to "+variable+" = "+str(bool(1 - value))+" to produce f("+" ".join(restricted_factor[0][:-1])+")")
    print(",       ".join(restricted_factor[0]))
    for row in factor[1:]:
        if (row[idx] == value):
            temp = row[:idx] + row[idx+1:]
            restricted_factor.append(temp)
            print(",   ".join([str(bool(1 - i)) for i in temp[:-1]]+[str(temp[-1])]))
    return restricted_factor

# f1 = [['X', 'Y', 'Z', 'val'], [0,0,0,0.1], [0,0,1,0.9], [0,1,0,0.2], [0,1,1,0.8], [1,0,0,0.4], [1,0,1,0.6], [1,1,0,0.3], [1,1,1,0.7]]
# print(restrict(f1, 'X', 0))

def multiply(factora, factorb):
    product_factor = []
    labels_a = factora[0][:-1]
    labels_b = factorb[0][:-1]
    intersect = list(set.intersection(set(labels_a), set(labels_b)))
    if (len(intersect) == 0):
        product_factor.append(labels_a + labels_b + [factora[0][-1]])
        for i in range(1, len(factora)):
            for j in range(1, len(factorb)):
                    # print(factora[i][-1])
                    # print(factorb[j][-1])
                    # print(factora[i][-1]*factorb[j][-1])
                    product_factor.append(factora[i][:-1] + factorb[j][:-1] + [factora[i][-1]*factorb[j][-1]])
        return product_factor
    idx_a = []
    idx_b = []
    for item in intersect:
        idx_a.append(labels_a.index(item))
        idx_b.append(labels_b.index(item))
    # print(idx_a)
    # print(idx_b)
    product_factor.append(labels_a + [i for j, i in enumerate(labels_b) if j not in idx_b] + [factora[0][-1]])
    for i in range(1, len(factora)):
        for j in range(1, len(factorb)):
            if (np.array_equal(np.array(factora[i]).take(idx_a), np.array(factorb[j]).take(idx_b))):
                # print(factora[i][-1])
                # print(factorb[j][-1])
                # print(factora[i][-1]*factorb[j][-1])
                product_factor.append(factora[i][:-1] + [b for a, b in enumerate(factorb[j][:-1]) if a not in idx_b] + [factora[i][-1]*factorb[j][-1]])
    # product_factor = np.array(product_factor).T
    # product_factor = sorted(product_factor, key=lambda l:l[0])
    # product_factor = np.array(product_factor).T
    return product_factor

# f1 = [['X', 'Y', 'val'], [0, 0, 0.1], [0, 1, 0.9], [1, 0, 0.2], [1, 1, 0.8]]
# f2 = [['Y', 'Z', 'val'], [0, 0, 0.3], [0, 1, 0.7], [1, 0, 0.6], [1, 1, 0.4]]

# print(multiply(f1, f2))

def sumout(factor, variable):
    temp = copy.deepcopy(factor)
    result_factor = []
    labels = factor[0]
    if (variable not in labels):
        return None
    idx = labels.index(variable)
    for row in temp:
        del row[idx]
    result_factor.append(temp[0])
    print("Sum out "+variable+" from f("+" ".join(labels[:-1])+") to produce f("+" ".join(result_factor[0][:-1])+")")
    print(",       ".join(result_factor[0]))
    var = []
    val = []
    for row in temp[1:]:
        if (not row[:-1] in var):
            var.append(row[:-1])
            val.append(row[-1])
        else:
            val[var.index(row[:-1])] += row[-1]
    for i, j in zip(var, val):
        cur = i + [j]
        result_factor.append(cur)
        print(",   ".join([str(bool(1-i)) for i in cur[:-1]]+[str(cur[-1])]))
    return result_factor

# f1 = [['X', 'Y', 'Z', 'val'], [0,0,0,0.03], [0,0,1,0.07], [0,1,0,0.54], [0,1,1,0.36], [1,0,0,0.06], [1,0,1,0.14], [1,1,0,0.48], [1,1,1,0.32]]
# print(sumout(f1, 'Y'))

def normalize(factor):
    normalized_factor = copy.deepcopy(factor)
    print("Normalized f("+" ".join(factor[0][:-1])+") to produce f("+" ".join(factor[0][:-1])+")")
    print(",       ".join(factor[0]))
    total = 0
    for row in normalized_factor[1:]:
        total += row[-1]
    for row in normalized_factor[1:]:
        row[-1] = row[-1] / total
        print(",   ".join([str(bool(1-i)) for i in row[:-1]]+[str(row[-1])]))
    return normalized_factor

# f1 = [['Y','val'],[0,0.2],[1,0.6]]
# print(normalize(f1))

def contain_var(factor, variable):
    if variable in factor[0]:
        return True
    return False

def ve(factor_list, query_variables, ordered_list_hidden_variables, evidence_list):
    factors = copy.deepcopy(factor_list)
    for variable in evidence_list:
        for i, factor in enumerate(factors):
            restricted_factor = restrict(factor, variable[0], variable[1])
            if (restricted_factor):
                factors[i] = restricted_factor
    # print(factors)
    for variable in ordered_list_hidden_variables:
        cur = None
        idx_elim = []
        variable_elim = []
        for i, factor in enumerate(factors):
            if contain_var(factor, variable):
                idx_elim.append(i)
                variable_elim.append(factor[0][:-1])
                if cur:
                    cur = multiply(cur, factor)
                else:
                    cur = factor
        if len(variable_elim) > 1:
            prints = []
            for item in variable_elim:
                factor_str = "f( " + " ".join(item) + " )"
                prints.append(factor_str)
            print("Multiply " + " ".join(prints) + " to produce f( " + " ".join(cur[0][:-1]) + " )")
            print(",       ".join(cur[0]))
            for row in cur[1:]:
                print(",   ".join([str(bool(1-i)) for i in row[:-1]]+[str(row[-1])]))
        if cur:
            cur = sumout(cur, variable)
            factors.append(cur)
        for i in reversed(idx_elim):
            del factors[i]

    # print(factors)
    cur = None
    prints = []
    for factor in factors:
        # print("-------------")
        # print(factor)
        # print(cur)
        # print("-------------")
        factor_str = "f( " + " ".join(factor[0][:-1]) + " )"
        prints.append(factor_str)
        if cur:
            cur = multiply(cur, factor)
        else:
            cur = factor
    print("Multiply " + " ".join(prints) + " to produce f( " + " ".join(cur[0][:-1]) + " )")
    print(",       ".join(cur[0]))
    for row in cur[1:]:
        print(",   ".join([str(bool(1-i)) for i in row[:-1]]+[str(row[-1])]))

    cur = normalize(cur)
    return cur

# ================== TEST ==================
# print("================== TEST ==================")
# f1 = [['B', 'val'], [0, 0.3], [1, 0.7]]
# f2 = [['E', 'val'], [0, 0.1], [1, 0.9]]
# f3 = [['A','B','E', 'val'], [0, 0, 0, 0.8], [0,0,1, 0.7], [0,1,0,0.2],[0,1,1,0.1],[1,0,0,0.2],[1,0,1,0.3],[1,1,0,0.8],[1,1,1,0.9]]
# f4 = [['W', 'A', 'val'], [0,0,0.8], [0,1,0.4],[1,0,0.2],[1,1,0.6]]
# factor_list=[f1,f2,f3,f4]
# query_variable = 'B'
# olhv = ['W','E']
# observed = [['A', 1]]
# ve(factor_list, query_variable, olhv, observed)



# ================== A ==================
print("================== A ==================")
f1 = [['AB','AS','Prob'],[0,0,0.8000],[0,1,0.2000],[1,0,0.2000],[1,1,0.8000]]
f2 = [['AH','AS','M','NH','Prob'],[0,0,0,0,0.9500],[0,0,0,1,0.8500],[0,0,1,0,0.7000],[0,0,1,1,0.5500],[0,1,0,0,0.6500],[0,1,0,1,0.3000],[0,1,1,0,0.1500],[0,1,1,1,0.0000],[1,0,0,0,0.0500],[1,0,0,1,0.1500],[1,0,1,0,0.3000],[1,0,1,1,0.4500],[1,1,0,0,0.3500],[1,1,0,1,0.7000],[1,1,1,0,0.8500],[1,1,1,1,1.0000]]
f3 = [['AS','Prob'],[0,0.0500],[1,0.9500]]
f4 = [['M','Prob'],[0,0.0357],[1,0.9643]]
f5 = [['M','NA','NH','Prob'],[0,0,0,0.9000],[0,0,1,0.1000],[0,1,0,0.3000],[0,1,1,0.7000],[1,0,0,0.6000],[1,0,1,0.4000],[1,1,0,0.0000],[1,1,1,1.0000]]
f6 = [['NA', 'Prob'],[0,0.4000],[1,0.6000]]
factor_list = [f1,f2,f3,f4,f5,f6]
query_variable = ['AS']
hidden = ['M','NA','NH']
observed = [['AB',0],['AH',0]]
print("Computing P(AS | AB and AH)")
print("Define factors f(AB,AS) f(AH,AS,M,NH) f(AS) f(M) f(M,NA,NH) f(NA)")
result = ve(factor_list, query_variable, hidden, observed)
print("P(AS | AB and AH) is " + str(result[1][-1]))

# ================== B ==================
print("================== B ==================")
f1 = [['AB','AS','Prob'],[0,0,0.8000],[0,1,0.2000],[1,0,0.2000],[1,1,0.8000]]
f2 = [['AH','AS','M','NH','Prob'],[0,0,0,0,0.9500],[0,0,0,1,0.8500],[0,0,1,0,0.7000],[0,0,1,1,0.5500],[0,1,0,0,0.6500],[0,1,0,1,0.3000],[0,1,1,0,0.1500],[0,1,1,1,0.0000],[1,0,0,0,0.0500],[1,0,0,1,0.1500],[1,0,1,0,0.3000],[1,0,1,1,0.4500],[1,1,0,0,0.3500],[1,1,0,1,0.7000],[1,1,1,0,0.8500],[1,1,1,1,1.0000]]
f3 = [['AS','Prob'],[0,0.0500],[1,0.9500]]
f4 = [['M','Prob'],[0,0.0357],[1,0.9643]]
f5 = [['M','NA','NH','Prob'],[0,0,0,0.9000],[0,0,1,0.1000],[0,1,0,0.3000],[0,1,1,0.7000],[1,0,0,0.6000],[1,0,1,0.4000],[1,1,0,0.0000],[1,1,1,1.0000]]
f6 = [['NA', 'Prob'],[0,0.4000],[1,0.6000]]
factor_list = [f1,f2,f3,f4,f5,f6]
query_variable = ['AS']
hidden = ['NH']
observed = [['AB',0],['AH',0],['M',0],['NA',1]]
print("Computing P(AS | AB and AH and M and not NA)")
print("Define factors f(AB,AS) f(AH,AS,M,NH) f(AS) f(M) f(M,NA,NH) f(NA)")
result = ve(factor_list, query_variable, hidden, observed)
print("P(AS | AB and AH and M and not NA) is " + str(result[1][-1]))
