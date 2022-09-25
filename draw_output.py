import sys
import os

pols = ['alexander_polynomial_vector', 'conway_polynomial_vector','jones_polynomial_vector', 'kauffman_polynomial_vector',
    'homfly_polynomial_vector']
invariant_names = ['arc_index', 'braid_index', 'braid_length', 'bridge_index', 'fd_clasp_number', 'crosscap_number', 'determinant', 'three_genus', 'morse_novikov_number',
                    'nakanishi_index', 'super_bridge_index', 'thurston_bennequin_number', 'tunnel_number', 'turaev_genus', 'unknotting_number', 'width', 'arf_invariant',
                    'td_clasp_number', 'smooth_4d_crosscap_number', 'topological_4d_crosscap_number', 'smooth_concordance_crosscap_number', 'topological_concordance_crosscap_number',
                    'smooth_concordance_order', 'algebraic_concordance_order', 'topological_concordance_order', 'smooth_concordance_genus', 'topological_concordance_genus', 'double_slice_genus',
                    'smooth_four_genus', 'topological_four_genus', 'signature', 'epsilon', 'l_space', 'ozsvath_szabo_tau_invariant', 'rasmussen_invariant', 'chern_simons_invariant',
                    'longitude_length', 'meridian_length', 'volume', 'alternating', 'fibered', 'almost_alternating', 'adequate', 'quasi_alternating', 'positive_braid', 'positive',
                    'strongly_quasipositive', 'quasipositive', 'l_space','alternating', 'fibered', 'almost_alternating', 'adequate', 'quasi_alternating', 'positive_braid', 'positive',
                    'strongly_quasipositive', 'quasipositive', 'l_space', 'smooth_concordance_crosscap_number']

out_file_name = input("Output file name?\n")
num_ins = input("How many inputs per experiment?\n")
min_acc = input("Minimum accuracy?\n")
max_acc = input("Maximum accuracy?\n")
min_num = input("Minimum number of knots?\n")
max_num = input("Maximum number of knots?\n")
in_names = input("Comma separated list of inputs (i.e. volume,alternating,quasipositive) or type [ALL] or  [POLY]\n")
out_names = input("Comma separated list of outputs or type [ALL]\n")

try:
    num_ins = int(num_ins)
except:
    print("Number of inputs is not a valid integer.")
    quit()

if num_ins > 3 or num_ins < 1:
    print("Invalid number of inputs.")

try:
    min_acc = float(min_acc)
    max_acc = float(max_acc)
except:
    print("Accuracies not valid real numbers.")
    quit()

try:
    min_num = int(min_num)
    max_num = int(max_num)
except:
    print("Knot count not valid integers.")
    quit()

if min_acc < 0 or min_acc > 100 or max_acc < 0 or max_acc > 100 or min_acc > max_acc:
    print("Invalid range for accuracies.")
    quit()

ins = in_names.split(',')
outs = out_names.split(',')
must_in = []
must_out = []

pol = False

if len(ins) < num_ins:
    if ins[0] == 'ALL':
        ins = invariant_names
    elif ins[0] == 'POLY':
        ins = pols
    else:
        print("Invalid number of input invariants entered")
        quit()

if ins[0] == 'POLY':
    ins = pols

if outs[0] == 'ALL':
    outs = invariant_names

for name in ins:
    if name not in invariant_names and name not in pols:
        print(f"Invalid invariant name for input {name}")
        quit()
    if name in pols and num_ins > 1:
        print("Multi-input experiments not supported for polynomial inputs")
        quit()
    elif name in pols:
        pol = True
    inm = ''
    # while inm != 'Y' and inm != 'N':
    #     inm = input(f'Must {name} be included in every entry as an input (Y/N)?')
    # must_in.append(inm)
for name in outs:
    if name not in invariant_names:
        print(f"Invalid invariant name for output {name}")
        quit()
    inm = ''
    # while inm != 'Y' and inm != 'N':
    #     inm = input(f'Must {name} be included in every entry as an output (Y/N)?')
    # must_out.append(inm)

if num_ins == 1 and not pol:
    f = open('results_one_fin.txt', 'r')
elif pol:
    f = open('results_poly_fin.txt','r')
elif num_ins == 2:
    f = open('results_two_fin.txt', 'r')
else:
    f = open('results_three_fin.txt', 'r')

marked = []
for line in f:
    l = line.split(',')
    for name in ins:
        if num_ins == 1:
            if name == l[0] and float(l[2]) < max_acc and float(l[2]) > min_acc and int(l[-4]) > min_num and int(l[-4]) < max_num:
                for name2 in outs:
                    if name2 == l[1]:
                        marked.append(l)
        if num_ins == 2:
            if name == l[0] or name == l[1] and float(l[3]) < max_acc and float(l[3]) > min_acc and int(l[-4]) > min_num and int(l[-4]) < max_num:
                for name2 in outs:
                    if name2 == l[2]:
                        marked.append(l)
        if num_ins == 3:
            if name == l[0] or name == l[1] or name == l[2] and float(l[4]) < max_acc and float(l[4]) > min_acc and int(l[-4]) > min_num and int(l[-4]) < max_num:
                for name2 in outs:
                    if name2 == l[3]:
                        marked.append(l)

# todo = []
# for m in marked:
#     flag = True
#     if num_ins == 1:
#         for i in range(0, len(ins)):
#             if must_in[i] == 'Y' and ins[i] != m[0]:
#                 flag = False
#         for i in range(0, len(outs)):
#             if must_out[i] == 'Y' and outs[i] != m[1]:
#                 flag = False
#     elif num_ins == 2:
#         for i in range(0, len(ins)):
#             if must_in[i] == 'Y' and (ins[i] != m[0] and ins[i] != m[1]):
#                 flag = False
#         for i in range(0, len(outs)):
#             if must_out[i] == 'Y' and outs[i] != m[2]:
#                 flag = False
#     else:
#         for i in range(0, len(ins)):
#             if must_in[i] == 'Y' and (ins[i] != m[0] and ins[i] != m[1] and ins[i] != m[1]):
#                 flag = False
#         for i in range(0, len(outs)):
#             if must_out[i] == 'Y' and outs[i] != m[3]:
#                 flag = False
#     if flag:
#         todo.append(m)

# for m in todo:
#     print(m)

todo = marked

with open(f'{out_file_name}.tex', 'w') as f:
    f.write('\\documentclass{article}\n')
    f.write('\\usepackage[utf8]{inputenc}\n')
    f.write('\\title{' + out_file_name + '}\n')
    f.write('\\begin{document}')
    # create and print table
    f.write('\\begin{table}[t]\n')
    f.write('\\begin{center}\n')
    str_col = '\\begin{tabular}{|'
    str_title = ''
    for i in range(num_ins):
        str_col += 'c|'
        str_title += f'Input {i+1} &'
    str_col += 'c|c|c|c|}\n'
    str_title += 'Output & Accuracy & Mean/Mode & Number \\\\'
    f.write(str_col)
    f.write('\\hline\n')
    f.write(str_title)
    f.write('\\hline\n')
    f.write('\\hline\n')
    for m in todo:
        for i in range(num_ins+1):
            str = m[i]
            str = str.replace('_', ' ')
            f.write(str + '&')
        f.write(m[i+1] + '&' + m[i+2] + '&' + m[i+4] + '\\\\\n')
        f.write('\\hline\n')
    f.write('\\end{tabular}\\end{center}\\end{table}')
    f.write('\\end{document}')
    f.close()
os.system(f"pdflatex {out_file_name}.tex")
