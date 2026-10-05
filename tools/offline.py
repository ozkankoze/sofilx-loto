"""dist/ -> onizleme/ : sunucusuz (çift tıklayarak) açılabilen önizleme kopyası.
HTML dosyaları onizleme/ içine yazılır, görseller/CSS/JS dist/assets'ten kullanılır."""
import os, re, glob, shutil
ROOT = '/home/claude/sofilx/'
SRC, OUT = ROOT + 'dist/', ROOT + 'onizleme/'
shutil.rmtree(OUT, ignore_errors=True)
for f in glob.glob(SRC + '**/*.html', recursive=True):
    rel = os.path.relpath(f, SRC)
    depth = rel.count('/')
    up = '../' * depth
    assets = '../' * (depth + 1) + 'dist/assets/'

    def fix(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith('/assets/'):
            return f'{attr}="{assets}{url[len("/assets/"):]}"'
        if url.startswith('/') and not url.startswith('//'):
            path, sep, rest = re.match(r'([^?#]*)([?#]?)(.*)', url).groups()
            target = 'index' if path in ('', '/') else path.strip('/')
            if path.endswith(('.xml', '.txt', '.webmanifest', '.png', '.svg', '.ico')):
                return f'{attr}="{"../" * (depth + 1)}dist{path}"'
            return f'{attr}="{up}{target}.html{sep}{rest}"'
        return m.group(0)

    h = open(f).read()
    h = re.sub(r'<link rel="preload"[^>]*>\n?', '', h)
    h = re.sub(r'\b(href|src|data-full|action)="([^"]*)"', fix, h)
    h = h.replace('<head>', f'<head>\n<script>window.__ROOT__="{up}";window.__ASSETS__="{assets}"</script>', 1)
    # form action için .html
    os.makedirs(os.path.dirname(OUT + rel), exist_ok=True)
    open(OUT + rel, 'w').write(h)
print('önizleme hazır:', len(glob.glob(OUT + '**/*.html', recursive=True)), 'sayfa')
