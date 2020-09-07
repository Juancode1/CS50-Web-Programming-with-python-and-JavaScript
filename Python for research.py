# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:51:32 2020

@author: ACER-59SX
"""

import matplotlib.pyplot as plt
import numpy as np
import string
import random
import math
# funcion que cuenta cuantas veces esta cada letra en una frase 
# Tasks 1 week
def countl(s):
    alphabet=string.ascii_letters
    letters=set(s)
    countletters=dict()
    for i in alphabet:
        if i in letters:
            countletters[i]=1
    for l in countletters.keys():
        countletters[l]=s.count(l)
    return countletters
    
def rand():
    num=random.uniform(-1,1)
    return num

def in_circle(x,origin):
    distance=[]
    for i in range(2):
        distance.append(x[i]-origin[i])
    dist=math.sqrt((distance[0])**2+(distance[1])**2)
    if dist<=1:
        return True
    else:
        return False

def inside():
    inside=[]
    random.seed(1)
    for i in range(10000):
        inside.append(in_circle((rand(),rand()),(0,0)))
    per=inside.count(True)/10000
    return per
def smooth():    
    x=[]
    y=[]
    rang=[]
    sen=0
    n_neigh=5
    random.seed(1)
    for i in range(1000):
        x.append(random.uniform(0,1))
    for t in range(0,1000,n_neigh):  
        for i in range(n_neigh):
            if i==0:
                minn=x[t+i]
                maxx=x[t+i]
            else:
                if x[t+i]<minn:
                    minn=x[t+i]
                elif x[t+i]>maxx:
                    maxx=x[t+i]    
        sen=maxx-minn
        rang.append([minn,maxx])
        y.append(sen)
    sen=0
    return [y,rang]
# tasks 2 week
def create_board():   
    global board
    board=np.zeros((3,3),dtype=int)
    return board
def place(board, player,position):
    if player==1:
        if board[position]==0:
            board[position]=1
        else:
            print("casilla llena")
    elif player==2:
        if board[position]==0:
            board[position]=2
        else:
            print("casilla llena")
    else:
        print("choose betewwen player 1 or 2")
    return board

def possibilities(board):
    free_spaces=[]
    for i in range(3):
        for t in range(3):
            if board[i,t]==0:
                free_spaces.append((i,t))
    return free_spaces
def random_place(board, player):
    selection=possibilities(board)
    rand_selec=random.choice(selection)
    place(board,player,rand_selec)

def row_win(board):
    if True in np.all(board==1,axis=1):
        return (1)
    elif True in np.all(board==2,axis=1):
        return(2)
    else:
        return(0)
    
def col_win(board):
    boarde=np.transpose(board)
    if True in np.all(boarde==1,axis=1):
        return (1)
    elif True in np.all(boarde==2,axis=1):
        return(2)
    else:
        return(0)

def diag_win(board):
    sen=[]
    for mark in range(3):
        sen.append(board[mark,mark])
    sen1=[board[2,0],board[1,1],board[0,2]]
    if sen==[1,1,1] or sen1==[1,1,1]:
        return (1)
    elif sen==[2,2,2] or sen1==[2,2,2]:
        return (2)
    else:
        return (0)
    
def evaluate(board):
    if row_win(board)>0:
        return(row_win(board))
    elif col_win(board)>0:
        return(col_win(board))
    elif diag_win(board)>0:
        return(diag_win(board))
    else:
        return(0)
        
        
def play_game():
     Games=[]
     random.seed(1)
     for times in range(1000):
         win=0
         turns=0
         board=create_board()
         while win==0:
             if turns%2==0:
                 random_place(board,1)
             else:
                 random_place(board,2)
             game=evaluate(board)
             if game>0:
                 Games.append(game)
                 win=1
             else:
                 if possibilities(board)==[]:
                     Games.append(game)
                     win=1
                     #board=create_board()
             turns=turns+1
     return Games
 
def play_stratgame():
     Games=[]
     random.seed(1)
     for times in range(1000):
         win=0
         turns=0
         strat=0
         board=create_board()
         while win==0:
             if strat==0:
                 place(board,1,(1,1))
                 strat=1
                 turns=1
             if turns%2==0 and strat==1:
                 random_place(board,1)
             else:
                 random_place(board,2)
             game=evaluate(board)
             if game>0:
                 Games.append(game)
                 win=1
             else:
                 if possibilities(board)==[]:
                     Games.append(game)
                     win=1
                     # board=create_board()
                     # strat=0
             turns=turns+1
     return Games

def DNA_Trans():
    inputfile="DNA.txt"
    f=open(inputfile,"r")
    adnseq=f.read()
    adnseq=adnseq.replace("\n","")
    adnseq=adnseq.replace("\r","")
    adnseq=adnseq.replace(" ","")
    table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    Protseq=""
    if len(adnseq)%3==0:
        for trip in range(0,len(adnseq),3):
            Protseq+=table[adnseq[trip:trip+3]]
    else:
        for trip in range(20,938,3):
            Protseq+=table[adnseq[trip:trip+3]]
    return Protseq[:-1]

def cypher(message="klcpacqdphclvcfdhvdu",key=-3):
    alphabet=" "+string.ascii_lowercase
    pos=dict()
    i=0
    for char in alphabet:
        pos[char]=i
        i+=1
    k=list(pos.keys())
    v=list(pos.values())
    enco=""
    for let in message:
        if v.index(pos[let])+key>=len(pos):
            enco+=k[0+(v.index(pos[let])+key-len(pos))]
        else:
            enco+=k[v.index(pos[let])+key]
    return enco

def count_words(text):
    text=text.lower()
    skips=[".", ",", ":", ";", "'", '"', "(", ")", "!", "?"]
    for punct in skips:
        text=text.replace(punct,"")
    wordcounts=dict()
    
    for word in text.split(" "):
        if word in wordcounts.keys():
            wordcounts[word]+=1
        else:
            wordcounts[word]=1
    return wordcounts

def fast_wordsC(text):
    from collections import Counter
    text=text.lower()
    skips=[".", ",", ":", ";", "'", '"', "(", ")", "!", "?", "\n", "\r"]
    for punct in skips:
        text=text.replace(punct,"")
    wordcounts=Counter(text.split(" "))
    return wordcounts
def readbook(title_path=".\Books\German\shakespeare\Romeo und Julia.txt"):
    with open(title_path,"r",encoding="utf8") as current:
        text=current.read()
        text=text.replace("\n","").replace("\r","")
    return text
def words_stats(wordcounts):
    nu_u=len(wordcounts)
    counts=wordcounts.values()
    return (nu_u,sum(counts))

def tabBooks():
    import os
    import pandas as pd
    # pwd =it checks for the path directory wich spider is working at
    # cd =change the directory if neccesary with this command
    bookdir=".\Books"
    table=pd.DataFrame(columns=("language","author","tittle","lenght","unique"))
    i=0
    for language in os.listdir(bookdir):
        if not ".csv" in language:
            for author in os.listdir(bookdir+"/"+language):
                for title in os.listdir(bookdir+"/"+language+"/"+author):
                    i+=1
                    infile=bookdir+"/"+language+"/"+author+"/"+title
                    text=readbook(infile)
                    (u,l)=words_stats(count_words(text))
                    table.loc[i]=language,author.capitalize(),title[:-4],l,u
    plt.figure(figsize=(10,10))
    subset=table[table.language=="English"] 
    plt.loglog(subset.lenght,subset.unique,"o",color="forestgreen",label="English")
    subset=table[table.language=="French"] 
    plt.loglog(subset.lenght,subset.unique,"x",color="crimson",label="French")
    return table
    #table[table.language=="English"] 

def readcsv(title_path=".\Books\hamlets.csv"):
    import pandas as pd
    table=pd.read_csv(title_path,index_col=1)
    counted_text=(fast_wordsC(table.text[0]))
    data=pd.DataFrame(columns=("words","times","length","frequency"))
    i=0
    for word in counted_text.keys():
        i+=1
        if counted_text[word]>10:
            freq="Frequent"
        elif 1 < counted_text[word] <= 10:
            freq="Infrequent"
        else:
            freq="unique"
        data.loc[i]=word,counted_text[word],len(word),freq
        unique=len(data[data.frequency=="unique"])
    return data
def summarize_text():
    import pandas as pd
    title_path=".\Books\hamlets.csv"
    table=pd.read_csv(title_path)
    grouped_data=pd.DataFrame(columns=("language","frequency","mean_word_length","num_words"))
    # grouped_data=list()
    languages=["English","German","Portuguese"]
    i=0
    for language in languages:
        text=table[table.language==language].text[i]
        counted_text =fast_wordsC(text)
        # pd.DataFrame.iloc()
        data = pd.DataFrame({
            "word": list(counted_text.keys()),
            "count": list(counted_text.values())
        })
        
        data.loc[data["count"] > 10,  "frequency"] = "frequent"
        data.loc[data["count"] <= 10, "frequency"] = "infrequent"
        data.loc[data["count"] == 1,  "frequency"] = "unique"
        
        data["length"] = data["word"].apply(len)
        
        sub_data = pd.DataFrame({
            "language": language,
            "frequency": ["frequent","infrequent","unique"],
            "mean_word_length": data.groupby(by = "frequency")["length"].mean(),
            "num_words": data.groupby(by = "frequency").size()
        })
        for j in range(3):
            grouped_data.loc[j+3*i]=sub_data.iloc[j]
        i+=1
    return (grouped_data)
def plotting(grouped_data):
    colors = {"Portuguese": "green", "English": "blue", "German": "red"}
    markers = {"frequent": "o","infrequent": "s", "unique": "^"}
    import matplotlib.pyplot as plt
    print(grouped_data.mean_word_length)
    print(grouped_data.num_words)
    for i in range(grouped_data.shape[0]):
        row = grouped_data.iloc[i]
        plt.plot(row.mean_word_length, row.num_words,
            marker=markers[row.frequency],
            color = colors[row.language],
            markersize = 10
        )
    
    color_legend = []
    marker_legend = []
    for color in colors:
        color_legend.append(
            plt.plot([], [],
            color=colors[color],
            marker="o",
            label = color, markersize = 10, linestyle="None")
        )
    for marker in markers:
        marker_legend.append(
            plt.plot([], [],
            color="k",
            marker=markers[marker],
            label = marker, markersize = 10, linestyle="None")
        )
    plt.legend(numpoints=1, loc = "upper left")
    
    plt.xlabel("Mean Word Length")
    plt.ylabel("Number of Words")
    

def majority_vote_fast(votes):
    import scipy.stats as ss
    mode, count = ss.mstats.mode(votes)
    return mode

def distance(p1, p2):
    return np.sqrt(np.sum(np.power(p2 - p1, 2)))

def find_nearest_neighbors(p, points, k=5):
    """find de k nearest neighbors of point p and returns their indices"""
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]

def knn_predict(p, points, outcomes, k=5):
    ind = find_nearest_neighbors(p, points, k)
    return majority_vote_fast(outcomes[ind])[0]
    
def plot_prediction_grid (xx, yy, prediction_grid, filename,predictors, outcomes):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    
    background_colormap = ListedColormap (["hotpink","lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red","blue","green"])
    plt.figure(figsize =(10,10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:,0], predictors [:,1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)

# import pandas as pd
# from sklearn import preprocessing
# from sklearn import decomposition
# data=pd.read_csv("block@wine.csv")
# numeric_data=pd.DataFrame(data)
# numeric_data.drop("quality",axis=1,inplace=True)
# numeric_data.drop("high_quality",axis=1,inplace=True)
# t=0
# for col in numeric_data.color:
#     if col=="red":    
#         numeric_data.loc[t,"is_red"]=1 
#     else:
#         numeric_data.loc[t,"is_red"]=0
#     t+=1
# numeric_data.drop("color",axis=1,inplace=True)
# numeric_data=pd.DataFrame(preprocessing.scale(numeric_data,axis=1),columns=numeric_data.columns)
# # numeric_data.drop("Unnamed: 0",axis=1,inplace=True)
# pca=decomposition.PCA()
# ppal_comp=pca.fit_transform(numeric_data)

# from matplotlib.colors import ListedColormap
# from matplotlib.backends.backend_pdf import PdfPages
# observation_colormap = ListedColormap(['red', 'blue'])
# x = ppal_comp[:,0]# Enter your code here!
# y = ppal_comp[:,1]# Enter your code here!

# plt.title("Principal Components of Wine")
# plt.scatter(x, y, alpha = 0.2,c = data['high_quality'], cmap = observation_colormap, edgecolors = 'none')
# plt.xlim(-8, 8); plt.ylim(-8, 8)
# plt.xlabel("Principal Component 1")
# plt.ylabel("Principal Component 2")
# plt.show()

# np.random.seed(1) # do not change this!

# x = np.random.randint(0, 2, 1000)
# y = np.random.randint(0 ,2, 1000)

# def accuracy(predictions, outcomes):
#     accu=[]
#     for ele in range(len(outcomes)):
#         if outcomes[ele]==predictions[ele]:
#             accu.append(1)
#         else:
#             accu.append(0)
#     resp=accu.count(1)/len(accu)
#     resp=resp*100
#     return resp

# from sklearn.neighbors import KNeighborsClassifier
# knn = KNeighborsClassifier(n_neighbors = 5)
# knn.fit(numeric_data, data['high_quality'])
# lib_pre=knn.predict(numeric_data)
# accuracy(lib_pre,data["high_quality"])

# random.seed(123)
# n_rows = data.shape[0]
# random.sample(range(n_rows), 10)
