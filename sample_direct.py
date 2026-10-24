import os, json
from huggingface_hub import list_repo_files, hf_hub_download
ROOT=r'E:\Repos\repo'
out=os.path.join(ROOT,'NutriGreen','sample_200'); os.makedirs(out,exist_ok=True)
files=[f for f in list_repo_files('Voxel51/NutriGreen',repo_type='dataset') if f.lower().endswith(('.jpg','.jpeg','.png'))][:200]
with open(os.path.join(out,'metadata.jsonl'),'w',encoding='utf8') as mf:
  for i,f in enumerate(files):
    p=hf_hub_download('Voxel51/NutriGreen',f,repo_type='dataset',local_dir=out)
    target=os.path.join(out,f'{i+1:04d}'+os.path.splitext(f)[1]); os.replace(p,target)
    mf.write(json.dumps({'dataset':'Voxel51/NutriGreen','source_file':f,'file':os.path.basename(target)},ensure_ascii=False)+'\n')
print('NutriGreen',len(files))
import pyarrow.parquet as pq
out=os.path.join(ROOT,'IDSpace','sample_200'); os.makedirs(out,exist_ok=True)
p=hf_hub_download('cactuslab/IDSpace','preview/mobile/mobile.parquet',repo_type='dataset',local_dir=out)
t=pq.read_table(p); col=t.column('image'); n=min(200,t.num_rows)
with open(os.path.join(out,'metadata.jsonl'),'w',encoding='utf8') as mf:
  for i in range(n):
    b=col[i].as_py(); raw=b.get('bytes') if isinstance(b,dict) else None
    if raw:
      fn=f'{i+1:04d}.jpg'; open(os.path.join(out,fn),'wb').write(raw)
      row={k:t.column(k)[i].as_py() for k in t.column_names if k!='image'}; row.update({'dataset':'cactuslab/IDSpace','file':fn}); mf.write(json.dumps(row,default=str,ensure_ascii=False)+'\n')
print('IDSpace',n)
