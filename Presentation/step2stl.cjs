const fs=require('fs');const occt=require('occt-import-js');
occt().then(o=>{const r=o.ReadStepFile(new Uint8Array(fs.readFileSync(process.argv[2])),null);
console.log('ok',r.success,'meshes',r.meshes.length);let mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9];
r.meshes.forEach((m,i)=>{const p=m.attributes.position.array;for(let k=0;k<p.length;k+=3)for(let j=0;j<3;j++){mn[j]=Math.min(mn[j],p[k+j]);mx[j]=Math.max(mx[j],p[k+j])}
console.log(i,m.name,m.color,p.length/3,'verts',m.index.array.length/3,'tris')});console.log(mn,mx);
fs.writeFileSync(process.argv[3],JSON.stringify(r.meshes.map(m=>({name:m.name,color:m.color,p:Array.from(m.attributes.position.array,x=>+x.toFixed(3)),i:Array.from(m.index.array)}))));});
