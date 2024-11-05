import math
import pandas as pd
from functools import reduce
d = {
    "Погода":["ясно","ясно","облачно","дождь","дождь","дождь","облачно","ясно","ясно","дождь","ясно","облачно","облачно","дождь"],
    "Температура":["Жарко","Жарко","Жарко","Тепло","Холодно","Холодно","Холодно","Тепло","Холодно","Тепло","Тепло","Тепло","Жарко","Тепло"], 
    "Влажность":["Высокая","Высокая","Высокая","Высокая","Норм","Норм","Норм","Высокая","Норм","Норм","Норм","Высокая","Норм","Высокая"],
    "Ветер":["Нет","Есть","Нет","Нет","Нет","Есть","Есть","Нет","Нет","Нет","Есть","Есть","Нет","Есть"],
   
    "Гольф":["×","×","○","○","○","×","○","×","○","○","○","○","○","×"],
}
df0 = pd.DataFrame(d)
cstr = lambda s:[k+":"+str(v) for k,v in sorted(s.value_counts().items())]
tree = {
    
    "name":"decision tree "+df0.columns[-1]+" "+str(cstr(df0.iloc[:,-1])),
  
    "df":df0,
    
    "edges":[],
}

open = [tree]
entropy = lambda s:-reduce(lambda x,y:x+y,map(lambda x:(x/len(s))*math.log2(x/len(s)),s.value_counts()))
while(len(open)!=0):
  
    n = open.pop(0)
    df_n = n["df"]

    if 0==entropy(df_n.iloc[:,-1]):
        continue

    attrs = {}
  
    for attr in df_n.columns[:-1]:
      
        attrs[attr] = {"entropy":0,"dfs":[],"values":[]}
      
        for value in sorted(set(df_n[attr])):
            
            df_m = df_n.query(attr+"=='"+value+"'")
         
            attrs[attr]["entropy"] += entropy(df_m.iloc[:,-1])*df_m.shape[0]/df_n.shape[0]
            attrs[attr]["dfs"] += [df_m]
            attrs[attr]["values"] += [value]
            pass
        pass
    
    if len(attrs)==0:
        continue
 
    attr = min(attrs,key=lambda x:attrs[x]["entropy"])

    for d,v in zip(attrs[attr]["dfs"],attrs[attr]["values"]):
        m = {"name":attr+"="+v,"edges":[],"df":d.drop(columns=attr)}
        n["edges"].append(m)
        open.append(m)
    pass

print(df0,"\n-------------")

def tstr(tree,indent=""):
   
    s = indent+tree["name"]+str(cstr(tree["df"].iloc[:,-1]) if len(tree["edges"])==0 else "")+"\n"

    for e in tree["edges"]:
        
        s += tstr(e,indent+"  ")
        pass
    return s

print(tstr(tree))