# Yağ ve Kimyasal Emici Kitler kategorisini ve 61 ürünü ekler (tekrar çalıştırılabilir)
#   görseller: src_emici/<i>-<k>.* -> out_emici (Sofilx çerçevesi) -> dist/assets/urunler
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from elektrik_img import compose
from elektrik_ekle import slugify, export_img
ROOT = '/home/claude/sofilx/'
CAT = ['emici', 'Yağ ve Kimyasal Emici Kitler', 'Yağ ve Kimyasal Emici Kitler', 'yag-ve-kimyasal-emici-kitler',
       'Yağ, kimyasal ve genel amaçlı emici ped, rulo, sosis, yastık ve çantalı / tekerlekli döküntü kitleri.']

if __name__ == '__main__':
    src = {o['i']: o for o in json.load(open(ROOT + 'data/emici_kaynak.json'))}
    P = []
    for a in (1, 21, 42):
        P += json.load(open(ROOT + f'data/emici_out_{a}.json'))
    D = json.load(open(ROOT + 'data/urunler.json'))
    D['cats'] = [c for c in D['cats'] if c[0] != 'emici'] + [CAT]
    D['products'] = [p for p in D['products'] if p['cat'] != 'emici']
    os.makedirs(ROOT + 'out_emici', exist_ok=True)
    for n in P:
        stem = slugify(n['code'] + '-' + n['name'])
        imgs = []
        for k, f in enumerate(src[n['i']]['files'], 1):
            framed = ROOT + f'out_emici/{n["code"].lower()}-{k}.png'
            if not os.path.exists(framed):
                compose(ROOT + 'src_emici/' + os.path.basename(f), framed, n['code'])
            imgs.append(export_img(framed, f'{stem}-{k}'))
        D['products'].append(dict(code=n['code'], name=n['name'], path='/' + stem, ls_path=None, cat='emici', images=imgs, variant=None,
                                  summary=n['summary'], intro=n['intro'], feats=n['feats'], specs=n['specs'], pack=n.get('pack', []), notes=[],
                                  usage=n['usage']))
    json.dump(D, open(ROOT + 'data/urunler.json', 'w'), ensure_ascii=False, indent=1)
    K = json.load(open(ROOT + 'data/kat/kategori_icerik.json'))
    K['emici'] = json.load(open(ROOT + 'data/emici_kat.json'))
    json.dump(K, open(ROOT + 'data/kat/kategori_icerik.json', 'w'), ensure_ascii=False, indent=1)
    print(len(D['products']), 'ürün')
