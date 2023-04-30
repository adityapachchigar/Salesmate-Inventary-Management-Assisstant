from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import numpy as np
from collections import Counter
import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template,redirect,request,url_for
import pandas as pd
from flask_mysqldb import MySQL
# import mysql
import pymysql,csv

app=Flask(__name__)

@app.route('/vend')
def vend():
    df = pd.read_csv("hackathon_vendor.csv")
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
        
    name = 'anuj shah'
    # domain=str(input('Enter user domain: '))
    domain = 'gaming'
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

    comb=[]
    for i in range(len(vendors)):
        tot=[]
        for j in range(len(vendors[i])):
            tot.append(vendors[i][j][0])
        new = ",".join(tot) 
        l=[df['name'][i],new]
        comb.append(l)
    comb=pd.DataFrame(comb)

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

    sorted_similar_game = sorted(sim, key=lambda x:x[1], reverse=True)
    sorted_similar_game.pop(0)

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
    slis=[]
    for i in range(len(sim_name)):
        slis.append(sim_name[i][0])

    fams={}
    for i in range(len(vendors)):
        if i in slis:
            for j in range(len(vendors[i])):
                if vendors[i][j][0] in fams.keys():
                    fams[vendors[i][j][0]]+=vendors[i][j][1]
                else:
                    fams.update({vendors[i][j][0]:vendors[i][j][1]})
    #             fams.append(vendors[i][j])
            
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
    return rec
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']=''
# app.config['MYSQL_DB']='test'
mysql=MySQL(app)
@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/inventory')
def Inventory():
    return render_template('inventory.html')

@app.route('/upload',methods=['POST'])
def Upload():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cursor = conn.cursor()
    name=request.form['name']
    domain=request.form['domain']

    print(name,domain)

    # csv_file = request.files['file']
    # # csv_r=csv.reader(csv_file)
    # df = pd.read_csv(csv_file)
    # tb=csv_file.filename

    # # insert the data into the database
    
    # a=0
    # for index, row in df.iterrows():
    #     sql = "INSERT INTO vendor (name, domain) VALUES ( %s, %s)"
    #     cursor.execute(sql, (row['name'], row['domain']))
    #     a=1

    # # commit the changes and close the database connection
    # conn.commit()
    # cursor.close()
    # conn.close()
    # if a==1:
        # return 'File Uploaded Successfully!!'
    return redirect(url_for('Inventory'))

@app.route('/print')
def Print():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    cur=conn.cursor()
    cur.execute("SELECT *FROM aryan_mehta")
    tab = cur.fetchall()
    tb_html="<table style='font-size:50px;'><tr><th>ID</th><th>Name</th><th>Domain</th></tr>"
    for column in tab:
        tb_html += "<tr>"
        for field in column:
            tb_html += "<td>{}</td>".format(field)
        tb_html += "</tr>"
    tb_html += "</table>"

    cur.close()
    conn.close()    
    return tb_html

@app.route('/virtual')
def Virtual():
    return render_template('virtual.html')

@app.route('/retention')
def Retension():
    return render_template('retention1.html')


def rec():
    query='xbox games'
    l1=query.split(' ')
    stri=""
    for i in range(0,len(l1)):
        stri=stri+l1[i]
        if(i!=len(l1)-1):
            stri=stri+'+'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }
    url='https://www.google.com//search?q='+'best+'+stri
    req=requests.get(url,headers=headers)
    content=req.text
    bs=BeautifulSoup(content)
    queue=[]
    setq=[]
    cou=0
    #print('1')
    possible_links = bs.find_all('a')
    for link in possible_links:
        if link.has_attr('href'):
            #print(link.attrs['href'])
            if(len(queue)<=100 and not(link.attrs['href'].startswith('https://www.google.com')) and (link.attrs['href'].find('google'))==-1):
                if(link.attrs['href'].find('/url')!=-1 and link.attrs['href'].find('youtube')==-1):
                    x=link.attrs['href'].split('.com')[0]
                    if x not in setq:
                        setq.append(x)
                        setq=list(set(setq))
                    
                        queue.append(link.attrs['href'])
    #print('2')
    nqueue=[]
    for i in queue:
        x=i.split('url=')[1]
        nqueue.append(x)
    n2queue=[]
    for i in nqueue:
        x=i.split('&')[0]
        n2queue.append(x)
    lmain=[]
    docsno=[]
    cou=0
    #print('3')
    for i in n2queue:
        
    #url='https://in.ign.com/feature/152649/the-best-ps5-games'
        url=i
        try:
            req=requests.get(url)
        except:
            continue
        content=req.text
        con2=req.content.decode('utf-8')
        bs=BeautifulSoup(content)
        h2_tags = bs.find_all("h2")
        h3_tags = bs.find_all("h3")
        #a_tags=bs.find_all("a")
        #for j in h2_tags:
            #lmain.append(j.text)
        for k in h3_tags:
            lmain.append(k.text)
            docsno.append(cou)
        for l in h2_tags:
            lmain.append(l.text)
            docsno.append(cou)
        cou=cou+1
    lmainp=[]
    #print('4')
    for i in lmain:
        s_stripped = i.strip()
        lmainp.append(s_stripped)
    lmainp1=[]
    for i in lmain:
        s_stripped = i.strip()
        lmainp1.append(s_stripped)
    lmainp1 = list(filter(lambda string: string != "", lmainp1))
    lmainp2=[]
    for i in lmainp1:
        if(i.find('. ')!=-1):
            ltemp2=i.split('.')[1]
            #print(ltemp2)
            ltemp2=ltemp2.strip()
            lmainp2.append(ltemp2)
        else:
            lmainp2.append(i)
    lfgame=[]
    for i in lmainp2:
        if (i.lower().find('youtube')==-1 and i.lower().find('guide')==-1):
            lfgame.append(i)

    #print('5')
    counter = Counter(lfgame)
    countsv = list(counter.values())
    countsl = list(counter.keys())
    dict1={}
    ldictm=[]
    for j in countsl:
        #print(j)
        temp=[]
        indexes = [i for i, x in enumerate(lmainp) if x == j]
        #print(indexes)
        for k in indexes:
            temp.append(docsno[k])
        temp=list(set(temp)) 
        ldictm.append(temp)
    dictm=[]
    for i in ldictm:
        dictm.append(len(i))
    x=np.array(countsv)
    y=np.array(dictm)

    finalwt=x*(20+np.log10(y))
    zipped_lists = list(zip(finalwt,countsl))

    # Sort the zipped list in descending order based on the values of list1
    sorted_lists = sorted(zipped_lists, reverse=True)
    ary=[]
    for i in range(5):
        ary.append(sorted_lists[i][1])
    #ary has all recomm
    return ary


def price():
    #df1=pd.read_csv('electroapri.csv')
    data = {
        'customer_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'products': ['Smartphone,Headphones,Charger,Screen protector', 'Laptop,Charger,Mouse,Backpack',
                    'Smartwatch,Headphones,Charger,Screen protector', 'Smartphone,Charger,Screen protector,Case',
                    'Laptop,Mouse,Keyboard,Screen protector', 'Smartphone,Headphones,Charger,Case',
                    'Laptop,Charger,Backpack', 'Smartwatch,Charger,Screen protector,Case',
                    'Smartphone,Headphones,Charger,Screen protector', 'Laptop,Charger,Mouse,Screen protector'],
        'price': [200000, 300000, 50000, 70000, 100000, 80000, 40000, 20000, 30000, 85000]
    }

    df1 = pd.DataFrame(data)
    df2=df1['products']
    list_ = list(df2) 
    list2_ = []
    for i in list_:
        list2_.append(i.split(','))
        
    te = TransactionEncoder()
    te_ary = te.fit(list2_).transform(list2_)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.4, use_colnames=True)

    # Apply the Association Rules algorithm to find rules
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.8)

    # Print the results
    #print("Frequent Itemsets:")
    #print(frequent_itemsets)
    #
    #print("\nAssociation Rules:")
    #print(rules)
    la=[]
    for i in rules['antecedents']:
        s=set(i)
        la.append(s)
    lc=[]
    for i in rules['consequents']:
        s=set(i)
        lc.append(s)
    
    return la,lc;



@app.route('/recvirt')
def recvirt():
    return render_template('recvirt.html')

@app.route('/recom')
def recom():
    return render_template('recom.html')

@app.route('/globaly')
def globaly():
    my_list = rec()
    print(my_list)
    return render_template('globaly.html',my_list = my_list)

@app.route('/vendor')
def vendor():
    my_list = vend()
    return render_template('vendor.html',my_list = my_list)

@app.route('/adjust')
def adjust():
    l1,l2 = price()
    comb = zip(l1,l2)
    return render_template('adjust.html',comb=comb)

if __name__=="__main__":
    app.run(debug=True)