import os, json
from huggingface_hub import list_repo_files, hf_hub_download
ROOT=r'E:\Repos\repo'
def sample(repo, prefix, ext, outname):
    out=os.path.join(ROOT,outname,'sample_200'); os.makedirs(out,exist_ok=True)
    fs=[f for f in list_repo_files(repo,repo_type='dataset') if f.startswith(prefix) and f.lower().endswith(ext)][:200]
    with open(os.path.join(out,'metadata.jsonl'),'w',encoding='utf8') as m:
        for i,f in enumerate(fs):
            p=hf_hub_download(repo,f,repo_type='dataset',local_dir=out)
            target=os.path.join(out,f'{i+1:04d}'+os.path.splitext(f)[1]); os.replace(p,target)
            m.write(json.dumps({'dataset':repo,'source_file':f,'file':os.path.basename(target)},ensure_ascii=False)+'\n')
    print(outname,len(fs))
sample('AgamiAI/Indian-Bank-Statements','train/','.pdf','Indian-Bank-Statements')
sample('theatticusproject/maud','MAUD_v1/contracts/','.txt','MAUD')
