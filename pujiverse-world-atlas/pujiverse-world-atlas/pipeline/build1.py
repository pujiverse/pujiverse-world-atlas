import csv,json,collections,unicodedata,re
def norm(s):
    s=unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().lower()
    s=re.sub(r"\b(province|provincia|region|state|district|governorate|county|department|of|de|du|la|le|the|oblast|prefecture|municipality|city|autonomous)\b",' ',s)
    return re.sub(r'[^a-z0-9]','',s)
ci3={};ci2={};num={}
for l in open('countryInfo.txt',encoding='utf8'):
    if l.startswith('#'):continue
    f=l.rstrip('\n').split('\t'); ci3[f[1]]=f[0]; num[f[1]]=f[2]
countries=list(csv.DictReader(open('countries.csv',encoding='utf8')))
name2iso3={c['country']:c['iso_code'] for c in countries}
iso3to2={c['iso_code']:ci3.get(c['iso_code']) for c in countries}
print('missing iso2',[k for k,v in iso3to2.items() if not v])
# geonames cities
gn=collections.defaultdict(list)
for l in open('cities15000.txt',encoding='utf8'):
    f=l.rstrip('\n').split('\t')
    gn[f[8]].append(dict(id=int(f[0]),name=f[1],ascii=f[2],alt=f[3],lat=float(f[4]),lon=float(f[5]),a1=f[10],pop=int(f[14] or 0)))
idx={}
for cc,L in gn.items():
    d=collections.defaultdict(list)
    for r in L:
        d[r['name']].append(r); d[norm(r['ascii'])].append(r)
    idx[cc]=d
cities=list(csv.DictReader(open('cities.csv',encoding='utf8')))
hit=0; miss=[]
for c in cities:
    cc=iso3to2[name2iso3[c['country']]]; p=int(c['total_population'])
    cand=idx.get(cc,{}).get(c['city'],[]) or idx.get(cc,{}).get(norm(c['city']),[])
    if not cand:
        cand=[r for r in gn.get(cc,[]) if r['pop']==p]
    if cand:
        r=min(cand,key=lambda r:abs(r['pop']-p)); c['_g']=r; hit+=1
    else: miss.append((c['country'],c['city']))
print('cities matched',hit,len(cities),miss[:10])
json.dump([ {k:v for k,v in c.items()} for c in cities],open('cities_m.json','w'))
