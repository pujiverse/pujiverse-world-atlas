import json,csv,collections
exec(open('build1.py').read().split('# geonames cities')[0])
YEARS=list(range(2015,2026))
wb={}
for ind,key in [('SP.POP.TOTL','p'),('SP.POP.TOTL.MA.IN','m'),('SP.POP.TOTL.FE.IN','f'),('SP.DYN.CBRT.IN','br'),('SP.DYN.CDRT.IN','dr')]:
    for r in json.load(open(f'wb_{ind}.json'))[1]:
        if r['value'] is not None: wb[(r['countryiso3code'],int(r['date']),key)]=r['value']
def I(x): return int(x) if x not in ('',None) else None
def F(x): return float(x) if x not in ('',None) else None
C=[];nohist=[]
for c in countries:
    i3=c['iso_code']; P=I(c['total_population']); M=I(c['male_population']); Fe=I(c['female_population'])
    br=F(c['birth_rate_per_1000']); dr=F(c['death_rate_per_1000'])
    ms=M/P if M else None
    h={'p':[],'m':[],'f':[],'b':[],'d':[]}
    has=any((i3,y,'p') in wb for y in range(2015,2025))
    if not has: nohist.append(c['country'])
    for y in YEARS:
        if y==2025:
            p,m,f,b,d=P,M,Fe,I(c['avg_births_per_year']),I(c['avg_deaths_per_year'])
        else:
            p=wb.get((i3,y,'p'))
            if p is None:
                ks=[yy for yy in range(2015,2025) if (i3,yy,'p') in wb]
                p=wb[(i3,min(ks,key=lambda k:abs(k-y)),'p')] if ks else P
            p=int(p)
            m=wb.get((i3,y,'m')); f=wb.get((i3,y,'f'))
            if M is None: m=f=None
            elif m is None or f is None: m=round(p*ms); f=p-m
            else: m,f=int(m),int(f)
            b_=wb.get((i3,y,'br'),br); d_=wb.get((i3,y,'dr'),dr)
            b=round(p*b_/1000) if b_ is not None and br is not None else None
            d=round(p*d_/1000) if d_ is not None and dr is not None else None
        for k,v in zip('pmfbd',(p,m,f,b,d)): h[k].append(v)
    AF=json.load(open('area_final.json')); sa,la=AF['cw'].get(c['country'],(None,None))
    C.append(dict(sa=sa,la=la,c=i3,n=c['country'],ct=c['continent'],cap=c['capital'].strip(),lang=c['popular_language'],ol=c['other_languages'],br=br,dr=dr,src=c['source'],hist=has,h=h))
print('no history:',len(nohist),nohist[:40])
CT=[]
for r in csv.DictReader(open('continents.csv')):
    cs=[c for c in C if c['ct']==r['continent']]
    h={k:[sum(c['h'][k][i] or 0 for c in cs) for i in range(len(YEARS))] for k in 'pmfbd'}
    assert h['p'][-1]==int(r['total_population']),(r['continent'],h['p'][-1])
    # use the file's own 2025 values
    h['m'][-1]=int(r['male_population']);h['f'][-1]=int(r['female_population']);h['b'][-1]=int(r['avg_births_per_year']);h['d'][-1]=int(r['avg_deaths_per_year'])
    cs_=[c for c in C if c['ct']==r['continent']]
    CT.append(dict(sa=round(sum(c['sa'] or 0 for c in cs_),1),la=round(sum(c['la'] or 0 for c in cs_),1),n=r['continent'],nc=int(r['countries']),cities=int(r['cities_15k_listed']),h=h))
# country geometry ids -> iso3
numto3={v:k for k,v in num.items()}
fix={'Somaliland':'SOM','Kosovo':'XKX','N. Cyprus':'CYP','Indian Ocean Ter.':'CXR','Siachen Glacier':'IND'}
have={c['c'] for c in C}
for fn,out in [('countries50.json','world50.json'),('countries110.json','world110.json')]:
    t=json.load(open(fn)); miss=[]
    for g in t['objects']['countries']['geometries']:
        i3=numto3.get(g.get('id')) or fix.get(g['properties']['name'])
        if i3=='SRB' and 0: pass
        g['id']=i3 if i3 in have else None
        if g['id'] is None: miss.append(g['properties']['name'])
        g['properties']={'n':g['properties']['name']}
    print(fn,'unmatched geoms',miss)
    json.dump(t,open('site/data/'+out,'w'),separators=(',',':'))
json.dump(dict(years=YEARS,continents=CT,countries=C),open('site/data/core.json','w'),separators=(',',':'))
# geo
states=json.load(open('states_m.json')); cities=json.load(open('cities_m.json'))
S=collections.defaultdict(list); sidx={}
for s in states:
    i3=name2iso3[s['country']]; sidx[(s['country'],s['state_province'])]=len(S[i3])
    S[i3].append([s['state_province'],s['subdivision_type'],I(s['cities_listed_15k']),I(s['population_in_listed_cities']),I(s['male_est']),I(s['female_est']),I(s['avg_births_per_year_est']),I(s['avg_deaths_per_year_est']),s['largest_city'],s['_f'],AF['sarea'].get(s['country']+'|'+s['state_province'],[None])[0]])
CI=collections.defaultdict(list); langdiff=0
clang={c['n']:c['lang'] for c in C}
for ci,c in enumerate(cities):
    i3=name2iso3[c['country']]; g=c['_g']
    row=[sidx[(c['country'],c['state_province'])],c['city'],I(c['total_population']),I(c['male_population_est']),I(c['female_population_est']),I(c['avg_births_per_year_est']),I(c['avg_deaths_per_year_est']),round(g['lat'],3),round(g['lon'],3),1 if c['capital']=='True' else 0, AF['carea'].get(str(ci))]
    if c['popular_language']!=clang[c['country']]: row.append(c['popular_language']); langdiff+=1
    CI[i3].append(row)
print('lang diff',langdiff)
json.dump(dict(states=S,cities=CI),open('site/data/places.json','w'),separators=(',',':'),ensure_ascii=False)
