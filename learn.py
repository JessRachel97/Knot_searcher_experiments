import tensorflow as tf
from tensorflow import keras
import sys
import csv
import ast
import numpy as np

# invariant name options:
# 'arc_index', 'braid_index', 'braid_length', 'bridge_index', 'fd_clasp_number', 'crosscap_number', 'determinant', 'three_genus', 'morse_novikov_number',
# 'nakanishi_index', 'super_bridge_index', 'thurston_bennequin_number', 'tunnel_number', 'turaev_genus', 'unknotting_number', 'width', 'arf_invariant',
# 'td_clasp_number', 'smooth_4d_crosscap_number', 'topological_4d_crosscap_number', 'smooth_concordance_crosscap_number', 'topological_concordance_crosscap_number',
# 'smooth_concordance_order', 'algebraic_concordance_order', 'topological_concordance_order', 'smooth_concordance_genus', 'topological_concordance_genus', 'double_slice_genus',
# 'smooth_four_genus', 'topological_four_genus', 'signature', 'epsilon', 'l_space', 'ozsvath_szabo_tau_invariant', 'rasmussen_invariant', 'chern_simons_invariant',
# 'longitude_length', 'meridian_length', 'volume', 'alternating', 'fibered', 'almost_alternating', 'adequate', 'quasi_alternating', 'positive_braid', 'positive',
# 'strongly_quasipositive', 'quasipositive', 'l_space','alternating', 'fibered', 'almost_alternating', 'adequate', 'quasi_alternating', 'positive_braid', 'positive'

pols = ['alexander_polynomial_vector', 'conway_polynomial_vector','jones_polynomial_vector', 'kauffman_polynomial_vector',
'homfly_polynomial_vector']  # list of available indices that are polynomials
train_size = 0.8  # fraction of data used for training (0 -> 1)
nodes_per_layer = 100  # number of nodes in the hidden layers
epochs = 100  # number of training epochs (passes through training data)

try: # get number of inputs from command line arguments
    num_inputs = int(sys.argv[1])
except:
    print('\n First arg (num inputs) not a a valid integer\n')
    quit()

if len(sys.argv) > 3 + num_inputs:
    print('\n Incorrect number of args.\n')
    quit()

input_indices = []
knot_file = open('knotinfo_original.csv')
data_reader = csv.reader(knot_file, delimiter=';')  # reads the knotinfo dataset
titles = next(data_reader)  # list of column titles in knotinfo dataset
for i in range(2, 2 + num_inputs):  # get the column numbers of the inputs
    try:
        idx = titles.index(sys.argv[i])
        input_indices.append(idx)
    except:
        print(f'\n Input {i-1} invalid.\n')
        quit()

i += 1
try:  # get the column number of the output
    output_idx  = titles.index(sys.argv[i])
except:
    print(f'\n Output invalid. \n')
    quit()

# prepare data for learning
next(data_reader)
inputs = []  # all inputs for learning
outputs = []  # all outputs for learning
max_len = 0
for row in data_reader:  # loop through all knots
    ins = [row[i] for i in input_indices]
    out = row[output_idx]
    if sys.argv[2] in pols:  # different procedure for preparing polynomial input
        if num_inputs > 1:
            print(f'\n Multiple inputs for polynomials not supported.')
            quit()
        ins = ins[0]
        ins = ins.replace('{', '[')
        ins = ins.replace('}', ']')
        bcount = 0
        for i in range(len(ins)):
            if ins[i] == '[':
                bcount += 1
        if bcount > 1:
            ins = ast.literal_eval(ins)
            nins = []
            for element in ins:
                if type(element) is list:
                    for item in element:
                        nins.append(item)
                else:
                    nins.append(element)
            ins = nins
        elif bcount == 1:
            ins = ast.literal_eval(ins)
        else:
            ins = [int(ins)]
        if len(ins) > max_len:
            max_len = len(ins)

    else:  # processing for non polynomial inputs
        for i in range(len(ins)):
            if ins[i] == 'Y':
                ins[i] = 1
            elif ins[i] == 'N':
                ins[i] = 0
            elif ins[i] == 'Yes':
                ins[i] = 1
            elif ins[i] == 'No':
                ins[i] = 0
    if out == 'Y':
        out = 1
    elif out == 'N':
        out = 0
    elif out == 'Yes':
        out = 1
    elif out == 'No':
        out = 0
    try:
        for i in range(len(ins)):
            ins[i] = float(ins[i])
        out = float(out)
        inputs.append(ins)
        outputs.append(out)
    except:
        pass
knot_file.close()

if len(outputs) < 100:
    print(f'\n Not enough knots for learning. \n')
    quit()
z = 0
o = 0
for i in inputs:
    if i == 0:
        z += 1
    else:
        o += 1
flag = True
for x in outputs:  # check if task is regression or classification
    flag = flag and (int(x) == x)

if flag:
    task = 'c'
else:
    task = 'r'
    # remove zeros from output
    inputs = [inputs[i] for i in range(0, len(inputs)) if outputs[i] != 0]
    outputs = [outputs[i] for i in range(0, len(outputs)) if outputs[i] != 0]


if sys.argv[2] in pols: # if inputs are pols, normalize length
    for pol in inputs:
        while len(pol) < max_len:
            pol.append(0)
inputs = np.array(inputs)
outputs = np.array(outputs)

if task == 'c':
    mmin = min(outputs)
    for i in range(len(outputs)): # scale classes from 0 up to num classes
        outputs[i] -= mmin
    output_type = max(outputs) - min(outputs) + 1  # number of classes
    out_act = 'softmax'  # output later represents probabilities
    loss = 'sparse_categorical_crossentropy'  # appropriate loss function for class.
else:
    output_type = 1  # one output node for regression
    out_act = 'relu'
    loss = 'mean_squared_error'

num_trainers = int(np.floor(train_size*len(outputs)))  # length of training set
train_indices = []  # indices of training set
while len(train_indices) < num_trainers:
    n = np.random.randint(0, len(outputs))
    if n not in train_indices:
        train_indices.append(n)

test_indices = list(set(list(range(len(outputs)))) - set(train_indices))  #indices of test set

train_in = inputs[train_indices]
test_in = inputs[test_indices]
train_out = outputs[train_indices]
test_out = outputs[test_indices]

# structure of the model
model = keras.models.Sequential([
    keras.layers.Dense(nodes_per_layer, activation='relu', input_dim=len(inputs[0])),
    keras.layers.Dense(nodes_per_layer, activation='relu'),
    keras.layers.Dense(nodes_per_layer, activation='relu'),
    keras.layers.Dense(output_type, activation=out_act)
])

# train
model.compile(optimizer=tf.keras.optimizers.Adam(), loss=loss)
model.fit(train_in, train_out, epochs=epochs, verbose=1)
model.save(f'model.h5')
mmax = 10
acc = 0
# validation
predictions = model.predict(test_in)
if task == 'c':
    corr_count = 0
    # test accuracy by checking that the 'most probable' predicted class matches actual
    for i in range(len(predictions)):
        if np.argmax(predictions[i]) == test_out[i]:
            corr_count += 1
    acc = corr_count/len(predictions)
else:
    err = np.zeros(predictions.size)
    for i in range(0, predictions.size):
        err[i] = np.abs(predictions[i]-test_out[i])/test_out[i]
    acc = 1- np.sum(err)/len(predictions)

print(f'\n Accuracy is {acc*100}%\n')
