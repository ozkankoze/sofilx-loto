# Çeviri parçalarını doğrular ve birleştirir:  python3 tools/i18n_check.py <dil> [--merge]
import json, re, sys, glob, os
ROOT = '/home/claude/sofilx/data/i18n/'
PH = re.compile(r'</?[tx]\d+/?>')


def check_pair(src, tr):
    a = sorted(PH.findall(src)); b = sorted(PH.findall(tr))
    if a != b:
        return 'yer tutucu farklı'
    # iç içe yapı dengeli mi
    st = []
    for m in PH.findall(tr):
        if m.endswith('/>'):
            continue
        if m.startswith('</'):
            if not st or st[-1] != m[2:-1]:
                return 'denge bozuk'
            st.pop()
        else:
            st.append(m[1:-1])
    return None if not st else 'kapanmamış etiket'


def main(lang, merge=False):
    bad = {}; out = {}
    for f in sorted(glob.glob(ROOT + 'src/part-*.json')):
        name = os.path.basename(f)
        src = json.load(open(f))
        of = ROOT + f'out/{lang}/{name}'
        if not os.path.exists(of):
            bad[name] = 'dosya yok'; continue
        try:
            tr = json.load(open(of))
        except Exception as e:
            bad[name] = f'JSON hatası: {e}'; continue
        miss = [k for k in src if k not in tr or not str(tr[k]).strip()]
        errs = {k: check_pair(src[k], tr[k]) for k in src if k in tr and check_pair(src[k], str(tr[k]))}
        if miss or errs:
            bad[name] = {'eksik': miss[:20], 'eksik_sayi': len(miss), 'hata': dict(list(errs.items())[:20]), 'hata_sayi': len(errs)}
        for k in src:
            if k in tr and k not in errs and str(tr[k]).strip():
                out[k] = tr[k]
    print(lang, 'tamam' if not bad else json.dumps(bad, ensure_ascii=False)[:3000], '| birim:', len(out))
    if merge:
        json.dump(out, open(ROOT + f'{lang}.json', 'w'), ensure_ascii=False, indent=0)
    return bad


if __name__ == '__main__':
    main(sys.argv[1], '--merge' in sys.argv)
