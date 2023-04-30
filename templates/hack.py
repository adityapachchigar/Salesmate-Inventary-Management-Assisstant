import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv(r"hackathon_vendor.csv")
df
# Working\hackathon_vendor.csv
features = ['name','domain']
for feature in features:
    df[feature] = df[feature].fillna('')
    
vendors=[]
for details in df['name']:
    s=details+'.csv'
    v=pd.read_csv(s)
    v=v[['game','quantity']]
    vendors.append(v.values.tolist())

name=str(input('Enter user name: '))
domain=str(input('Enter user domain: '))
sx=df['name'].tolist()
if name not in sx:
    co=len(df)
    co=str(co)
    new_data = {'index': co, 'name': name, 'domain': domain}
    df = df.append(new_data,ignore_index=True)
#     df.to_csv('hackathon_vendor.csv', index=False)
# print(df)
# print(vendors)

sd=[]
for i in range(len(vendors)):
    for j in range(len(vendors[i])):
        sd.append(vendors[i][j])
        
sd=pd.DataFrame(sd)
sd

comb=[]
for i in range(len(vendors)):
    tot=[]
    for j in range(len(vendors[i])):
        tot.append(vendors[i][j][0])
    new = ",".join(tot) 
    l=[df['name'][i],new]
    comb.append(l)
comb=pd.DataFrame(comb)
comb

# cosine_sim = cosine_similarity(count_matrix)

game=name
import difflib
sim=[]
for i in range(len(comb)):
    sm = difflib.SequenceMatcher(None,game,comb[1][i])
    smo=[]
    smo.append(i)
    smo.append(sm.ratio())
#     print(smo)
    sim.append(smo)
sim

sorted_similar_game = sorted(sim, key=lambda x:x[1], reverse=True)
sorted_similar_game.pop(0)
sorted_similar_game

i=0
sim_name=[]
for i in range(len(sorted_similar_game)):
    if i>1:
        break
    else:
        p=[]
        p.append(i)
        p.append(comb[0][i])
#         print(comb[0][i])
        sim_name.append(p)
sim_name
slis=[]
for i in range(len(sim_name)):
    slis.append(sim_name[i][0])
slis

fams={}
for i in range(len(vendors)):
    if i in slis:
        for j in range(len(vendors[i])):
            if vendors[i][j][0] in fams.keys():
                fams[vendors[i][j][0]]+=vendors[i][j][1]
            else:
                fams.update({vendors[i][j][0]:vendors[i][j][1]})
#             fams.append(vendors[i][j])
        
fams

fm=(sorted(fams.items(),key=lambda x:x[1],reverse=True))
n=0
rec=[]
for i in range(len(fm)):
    if n>2:
        break
    else:
        p=[]
        p.append(fm[i][0])
#         print(fm[i][1])
        rec.append(p)
    n=n+1
print(rec)