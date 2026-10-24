import json, os, io
from datasets import load_dataset
from PIL import Image

ROOT = r'E:\Repos\repo'
TARGETS = {
    'SROIE': 'mychen76/ds_receipts_v2_train',
    'CORD': 'naver-clova-ix/cord-v2',
    'WildReceipt': 'kaydee/wildreceipt',
    'NutriGreen': 'Voxel51/NutriGreen',
    'IDSpace': 'cactuslab/IDSpace',
}

for name, repo in TARGETS.items():
    out = os.path.join(ROOT, name, 'sample_200')
    os.makedirs(out, exist_ok=True)
    meta_path = os.path.join(out, 'metadata.jsonl')
    count = 0
    try:
        ds = load_dataset(repo, split='train', streaming=True)
    except Exception as e:
        print(f'{name}: load failed: {e}')
        continue
    with open(meta_path, 'w', encoding='utf-8') as mf:
        for row in ds:
            if count >= 200: break
            image = row.get('image')
            if image is None: continue
            if isinstance(image, dict) and 'bytes' in image and image['bytes']:
                im = Image.open(io.BytesIO(image['bytes']))
            elif isinstance(image, Image.Image):
                im = image
            else: continue
            path = os.path.join(out, f'{count+1:04d}.jpg')
            im.convert('RGB').save(path, quality=95)
            clean = {k: (v if isinstance(v, (str,int,float,bool,type(None),list,dict)) else str(v)) for k,v in row.items() if k != 'image'}
            clean.update({'dataset': repo, 'sample_index': count, 'file': os.path.basename(path)})
            mf.write(json.dumps(clean, ensure_ascii=False, default=str) + '\n')
            count += 1
    print(f'{name}: {count} samples')
