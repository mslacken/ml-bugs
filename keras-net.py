#!/usr/bin/python3
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import keras as kr
import sklearn.model_selection as sk
import tensorflow as tf
import sys


def plot_sample_length_distribution(sample_texts):
    """Plots the sample length distribution.

    # Arguments
        samples_texts: list, sample texts.
    """
    plt.hist([len(s) for s in sample_texts], 50)
    plt.xlabel('Length of a sample')
    plt.ylabel('Number of samples')
    plt.title('Sample length distribution')
    plt.show()

def plot_sample_distribution(samples):
    """Plots the sample distribution.

    # Arguments
        samples_texts: list, sample texts.
    """
    plt.hist(samples, 50)
    plt.xlabel('Value of a sample')
    plt.ylabel('Number of samples')
    plt.title('Sample distribution')
    plt.show()

def plot_xy(data1,data2):
    plt.plot(data1,data2,linestyle='None',marker='+')
    plt.title('Values')
    plt.show()

def plot_hist(history):
    history_dict = history.history

    acc = history_dict['acc']
    val_acc = history_dict['val_acc']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()



if __name__ == '__main__':
    bugs = {}

    parser = argparse.ArgumentParser(description='Read in json.')
    parser.add_argument('--bugs',dest='bugs_file_name',default='bugs.txt',help='filename of bugs on json format')
    parser.add_argument('--mwords',dest='mwords',default=1000,type=int)
    parser.add_argument('--max_len',dest='max_len',default=7000,type=int)
    parser.add_argument('--max_count',dest='max_count',default=20,type=int)
    parser.add_argument('--epochs',dest='epochs',default=10,type=int)
    parser.add_argument('--nr_units',dest='nr_units',default=32,type=int)
    parser.add_argument('--nr_layers',dest='nr_layers',default=1,type=int)

    args = parser.parse_args()

    try: 
        bugs = json.load(open(args.bugs_file_name))
    except Exception as excep_reader:
        print("Could not read %s" % args.bugs_file_name)
        print(excep_reader)
        sys.exit(1)

    print("Loaded %i bugs" % (len(bugs)))

    bugs_keys = [] 
    bugs_text = []
    bugs_count = [] 
    bugs_duration = []
    bugs_summary = []
    bugs_id1 = []
    bugs_id2 = []


    for key,value in bugs.items():
        bugs_keys.append(key)
        bugs_text.append(value['summary'] + ' ' + value['text'][:args.max_len])
        bugs_count.append(value['count'])
        bugs_duration.append(value['etime'] - value['ctime'])
        bugs_summary.append(value['summary'])

    #plot_sample_length_distribution(bugs_text)
    #plot_sample_distribution(bugs_count)
    #plt.plot([len(s) for s in bugs_text],bugs_duration,linestyle='None',marker='+')
    #plt.plot(bugs_count,bugs_duration,linestyle='None',marker='+')
    #plt.xlabel('Length of text')
    #plt.ylabel('Count')
    #plt.show()
    #plot_xy(bugs_count,bugs_duration)
    # Initialize tokenizer and tokenize bug report
    tok = kr.preprocessing.text.Tokenizer(num_words=args.mwords)
    tok.fit_on_texts(bugs_text)
    bugs_seq = tok.texts_to_sequences(bugs_text)
    #print("First bug report as sequence: ",bugs_seq[0])
    #back_seq = tok.sequences_to_texts(bugs_seq)
    #print("First bug translated back: ", back_seq[0])
    # Pad the input data
    bugs_seq = kr.preprocessing.sequence.pad_sequences(bugs_seq,
            padding='post',maxlen=args.max_len)
    bug_seq_train, bug_seq_test, bug_cnt_train, bug_cnt_test, bug_dur_train, bug_dur_test = sk.train_test_split(bugs_seq,bugs_count,bugs_duration,test_size=0.2)
    # model creation
    model = kr.Sequential()
    model.add(kr.layers.Embedding(args.max_len+1, args.nr_units))
    model.add(kr.layers.GlobalAveragePooling1D())
    for n in range(0,args.nr_layers):
        model.add(kr.layers.Dense(args.nr_units, activation=tf.nn.relu))
    model.add(kr.layers.Dense(1))

    model.summary()
    
    optimizer =  kr.optimizers.Adam()

    model.compile(optimizer, loss='mean_squared_error', metrics=['acc'])
    
    history = model.fit(bug_seq_train,bug_dur_train,
                    epochs=args.epochs,
                    batch_size=512,
                    validation_split = 0.5,
                    verbose=1)

    results = model.evaluate(bug_seq_test, bug_dur_test)
    print(results)
    
    plot_hist(history)


    #print("Word count: ", tok.word_counts)
