import csv,json,collections,unicodedata,re
exec(open('build1.py').read().split('# geonames cities')[0])
cities=json.load(open('cities_m.json'))
a1names={}
for l in open('admin1codes.txt',encoding='utf8'):
    f=l.rstrip('\n').split('\t'); a1names[f[0]]=f[1]
ne=json.load(open('admin1_full.geojson'))
bycode=collections.defaultdict(list); byname=collections.defaultdict(list)
for i,ft in enumerate(ne['features']):
    p=ft['properties']
    if p.get('gn_a1_code'): bycode[p['gn_a1_code']].append(i)
    for n in [p.get('name'),p.get('gn_name'),p.get('woe_name')]+(p.get('name_alt') or '').split('|'):
        if n: byname[(p['iso_a2'],norm(n))].append(i)
states=list(csv.DictReader(open('states.csv',encoding='utf8')))
cmap=collections.defaultdict(list)
for c in cities: cmap[(c['country'],c['state_province'])].append(c)
stats=collections.Counter(); assigned=set()
for s in states:
    cc=iso3to2[name2iso3[s['country']]]
    cs=cmap[(s['country'],s['state_province'])]
    code=None
    if cs:
        a=collections.Counter(c['_g']['a1'] for c in cs).most_common(1)[0][0]; code=cc+'.'+a
    feats=bycode.get(code) if code else None
    how='code'
    if not feats:
        feats=byname.get((cc,norm(s['state_province']))); how='name'
    if not feats: how='none'; feats=[]
    s['_f']=feats; stats[how]+=1
print(stats)
unm=[(s['country'],s['state_province']) for s in states if not s['_f']]
print(collections.Counter(u[0] for u in unm).most_common(25))
json.dump(states,open('states_m.json','w'))
