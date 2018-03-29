# -*-coding: utf-8 -*-
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
import scipy.sparse
from scipy.sparse import diags


def normal_matrix(a):
    # 对于非对称的矩阵，我们的归一化的方式应该是按照行来进行归一化
    for number in range(0, np.size(a, 0)):
        if number % 10000 == 0:
            print "echo is %d" % number
        row_sum = a.getrow(number).sum()
        if row_sum == 0:
            continue
        else:
            for number_col in a.indices[a.indptr[number]:a.indptr[number+1]]:
                a[number, number_col] = a[number, number_col] / row_sum
    return a


def normal_matrix_new(a):
    # 对于对称的矩阵，我们可以使用矩阵相乘的方式来进行归一化，这样的话速度比较快。
    d = a.sum(0)
    d = np.array(d)
    d = d[0]
    dd = map(lambda x: 0 if x==0 else np.power(x, -0.5), d)
    D_matrix = diags(dd, 0)
    C = D_matrix.dot(a)
    C = C.dot(D_matrix)
    a = C
    return a


def motif_anchor(adjacency_matrix, a):
    # please write the corresponding formula in the paper to complete the computing anchor-motif
    # here we just give an example for anchor which computed by "U dot U^T element-wise product B".
    for i in range(a):
        print 'echo for motif is %d' % i
        adjacency_tran = np.transpose(adjacency_matrix)
        B_matrix_spare = adjacency_matrix.multiply(adjacency_tran)
        U_matrix = adjacency_matrix - B_matrix_spare
        U_matrix = np.abs(U_matrix)
        U_tran = np.transpose(U_matrix)
        result_1 = U_matrix.dot(U_tran)
        result_1 = result_1.multiply(B_matrix_spare)

        adjacency_matrix = result_1
        adjacency_tran = np.transpose(adjacency_matrix)
        adjacency_matrix = adjacency_matrix + adjacency_tran
        adjacency_matrix = normal_matrix_new(adjacency_matrix)

        if len(adjacency_matrix.data) > 0:
            print np.max(adjacency_matrix.data), adjacency_matrix.nnz
    return adjacency_matrix


def construct_motif(txt_name, time, alpha_value):
    entry = []
    f = open(txt_name)
    while True:
        line = f.readline()
        if line:
            temp = []
            line = line.replace('\n', '')
            line = line.split(';')
            for i in range(len(line)):
                temp.append(int(line[i]))
            entry.append(temp)
        else:
            break
    spare_array_row = []
    spare_array_col = []
    spare_array_data = []
    entry_all = []
    for i in range(len(entry)):
        spare_array_row.append(entry[i][0])
        spare_array_col.append(entry[i][1])
        spare_array_data.append(1)
        entry_all.append(entry[i][0])
        entry_all.append(entry[i][1])
    entry_unique = np.unique(entry_all)
    newspare_array_row = []
    newspare_array_col = []
    counttt = 0
    for nnn in range(len(spare_array_row)):
        if counttt % 100000 == 0:
            print 'echo is %d' % counttt
        counttt += 1
        id1 = spare_array_row[nnn]
        id2 = spare_array_col[nnn]
        id1new = np.where(entry_unique == id1)[0][0]
        id2new = np.where(entry_unique == id2)[0][0]
        newspare_array_row.append(id1new)
        newspare_array_col.append(id2new)
    maxnum = len(entry_unique)
    adjacency_matrix = csr_matrix((spare_array_data, (newspare_array_row, newspare_array_col)), shape=(maxnum, maxnum), dtype = np.float64)
    # 下面的三行代码主要是为了能够让得到的邻接矩阵为binary，如果希望是weighed，请注释
    data_array = adjacency_matrix.data
    lennn = data_array.shape[0]
    adjacency_matrix.data = np.ones((1, lennn), dtype=np.float64)[0]
    # print adjacency_matrix.shape
    print adjacency_matrix.nnz
    result_B = adjacency_matrix.copy()
    result_B = normal_matrix(result_B)
    result_C = motif_anchor(adjacency_matrix, time)

    result_temp1 = result_B.multiply(alpha_value).tolil()
    result_temp2 = result_C.multiply(1 - alpha_value).tolil()
    result_D = result_temp1 + result_temp2
    result_D = result_D.tocsr()
    print maxnum
    return result_D, entry_unique


def binary(a_original):
    a = a_original.copy()
    for number in range(0, np.size(a, 0)):
        if number % 10000 == 0:
            print "echo is %d" % number
        for number_col in a.indices[a.indptr[number]:a.indptr[number+1]]:
            a[number, number_col] = 1
    return a



