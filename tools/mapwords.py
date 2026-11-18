# Proyecta las palabras de la transcripción original (tiempo fuente) al video editado.
import json
segs = json.load(open('_work/segments.json'))['segments']
def to_out(t):
    for s in segs:
        if s['src_a'] - 1e-6 <= t < s['src_b']:
            return s['out_a'] + (t - s['src_a'])
    for s in segs:              # cae en un silencio quitado: va al inicio del siguiente tramo
        if t < s['src_a']:
            return s['out_a']
    return None
def mapped():
    w = json.load(open('_work/transcript.json', encoding='utf8'))
    w = w if isinstance(w, list) else w['words']
    out = []
    for i, x in enumerate(w):
        a = to_out(x['start']); b = to_out(max(x['start'] + 0.05, x['end'] - 0.01)) or (a + 0.3 if a is not None else None)
        if a is None: continue
        if any(s['src_a'] <= x['start'] < s['src_b'] for s in segs) or any(s['src_a'] <= x['end'] - 0.02 < s['src_b'] for s in segs):
            out.append({'i': i, 'text': x['text'], 'start': round(a, 3), 'end': round(max(b, a + 0.08), 3)})
    return out
if __name__ == '__main__':
    import sys
    m = mapped()
    sys.stdout.buffer.write((' '.join('%d:%s[%.2f]' % (x['i'], x['text'], x['start']) for x in m) + '\n').encode('utf8'))
