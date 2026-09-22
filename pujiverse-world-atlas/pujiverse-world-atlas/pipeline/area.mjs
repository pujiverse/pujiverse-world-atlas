import {geoArea} from 'd3-geo'; import fs from 'fs';
const R=6371.0088;
function ringA(r){ let a=geoArea({type:'Polygon',coordinates:[r]}); return Math.min(a,4*Math.PI-a); }
function area(f){ const g=f.geometry; const polys=g.type==='Polygon'?[g.coordinates]:g.type==='MultiPolygon'?g.coordinates:[]; let a=0;
  for(const p of polys){ p.forEach((r,i)=>{ a+= (i===0?1:-1)*ringA(r); }); } return Math.max(0,a)*R*R; }
const out={};
for(const [name,file] of [['admin1','admin1_full.geojson'],['marine','phys/geography_marine_polys.json'],['lakes','phys/lakes.json'],['regions','phys/geography_regions_polys.json']]){
  const d=JSON.parse(fs.readFileSync(file)); out[name]=d.features.map(f=>f.geometry?Math.round(area(f)*10)/10:null);
}
fs.writeFileSync('areas.json',JSON.stringify(out));
console.log(out.admin1.slice(0,3), out.lakes.slice(0,3), Math.max(...out.marine));
