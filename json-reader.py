#!/usr/bin/python3
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import keras.preprocessing.text as kr_txt


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


if __name__ == '__main__':
    bugs = {}

    parser = argparse.ArgumentParser(description='Read in json.')
    parser.add_argument('--bugs',dest='bugs_file_name',default='bugs.txt',help='filename of bugs on json format')
    parser.add_argument('--mwords',dest='mwords',default=1000,type=int)

    args = parser.parse_args()

    try: 
        bugs = json.load(open(args.bugs_file_name))
    except:
        print("Could not read %s" % args.bugs_file_name)

    print("Loaded %i bugs" % (len(bugs)))

    bugs_keys = [] 
    bugs_text = []
    bugs_count = [] 
    bugs_duration = []
    bugs_summary = []


    for key,value in bugs.items():
        bugs_keys.append(key)
        bugs_text.append(value['Summary'] + ' ' + value['Text'][:3000])
        bugs_count.append(value['Count'])
        bugs_duration.append(value['etime'] - value['ctime'])
        bugs_summary.append(value['Summary'])

    #plot_sample_length_distribution(bugs_text)
    #plot_sample_distribution(bugs_count)
    #plt.plot([len(s) for s in bugs_text],bugs_duration,linestyle='None',marker='+')
    #plt.plot(bugs_count,bugs_duration,linestyle='None',marker='+')
    #plt.xlabel('Length of text')
    #plt.ylabel('Count')
    #plt.show()
    #plot_xy(bugs_count,bugs_duration)
    # Initialize tokenizer and tokenize bug report
    tok = kr_txt.Tokenizer(num_words=args.mwords)
    tok.fit_on_texts(bugs_text)
    bugs_seq = tok.texts_to_sequences(bugs_text)
    print("First bug report as sequence: ",bugs_seq[0])
    back_seq = tok.sequences_to_texts(bugs_seq)
    print("First bug translated back: ", back_seq[0])

    #print("Word count: ", tok.word_counts)
