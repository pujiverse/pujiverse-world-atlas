import json,collections,csv
exec(open('build1.py').read().split('# geonames cities')[0])
states=json.load(open('states_m.json'))
ne=json.load(open('admin1_full.geojson'))
iso2to3={v:k for k,v in iso3to2.items()}
cont={c['iso_code']:c['continent'] for c in countries}
featcountry={}
for s in states:
    for f in s['_f']: featcountry[f]=name2iso3[s['country']]
out=[]
for i,ft in enumerate(ne['features']):
    iso3=featcountry.get(i) or iso2to3.get(ft['properties']['iso_a2'])
    if not iso3 or not ft['geometry']: continue
    out.append({'type':'Feature','properties':{'id':i,'c':iso3,'ct':cont[iso3].replace(' ','_')},'geometry':ft['geometry']})
json.dump({'type':'FeatureCollection','features':out},open('admin1_tag.geojson','w'))
print(len(out))
