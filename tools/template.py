import json, os, numpy as np
from PIL import Image
res=json.load(open('data/img_class.json'))
ids=[k for k,v in res.items() if len(v)>1 and v[0]==1000 and v[1]==1000 and v[2]<12][:80]
stack=np.stack([np.array(Image.open('src_img/'+(os.path.basename(i)+'.webp' if i.startswith('/assets') else i)).convert('RGB')) for i in ids]).astype(np.uint8)
med=np.median(stack,axis=0).astype(np.uint8)
Image.fromarray(med).save('data/template_median.png')
# consistency: std small and not white
std=stack.astype(float).std(axis=0).mean(-1)
nonwhite=med.astype(int).sum(-1)<700
red=(stack[...,0]>150)&(stack[...,1]<90)&(stack[...,2]<90)
redfrac=red.mean(0)
np.save('data/redfrac.npy',redfrac); np.save('data/std.npy',std)
Image.fromarray((redfrac*255).astype(np.uint8)).save('data/redfrac.png')
print(len(ids))
