# Transcribe assets/voz-limpia.wav por tramos (cortados en silencios) y une las palabras -> assets/transcript.json
import json, subprocess, os, soundfile as sf, numpy as np
x, sr = sf.read('assets/voz-limpia.wav'); x = x if x.ndim == 1 else x.mean(1)
hop = int(sr * 0.02); n = len(x) // hop
db = np.array([20*np.log10(np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2))+1e-9) for i in range(n)])
targets = [12.5, 24.0, 35.0, 46.0, 57.0, 67.0]
cuts = [0.0]
for t in targets:
    k0, k1 = int((t-0.8)/0.02), int((t+0.8)/0.02)
    cuts.append(round((k0 + int(np.argmin(db[k0:k1]))) * 0.02 + 0.01, 2))
cuts.append(round(len(x)/sr, 2))
words = []
for i in range(len(cuts)-1):
    a, b = cuts[i], cuts[i+1]; d = f'_work/tr/{i}'; os.makedirs(d, exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i','assets/voz-limpia.wav',f'{d}/s.wav'],check=True)
    subprocess.run('npx --yes hyperframes@0.8.186 transcribe s.wav --dir . --language es --json', shell=True, cwd=d, capture_output=True)
    w = json.load(open(f'{d}/transcript.json', encoding='utf8')); w = w if isinstance(w, list) else w['words']
    for x_ in w:
        words.append({'text': x_['text'], 'start': round(x_['start']+a, 3), 'end': round(x_['end']+a, 3)})
for i, w in enumerate(words): w['id'] = f'w{i}'
json.dump(words, open('assets/transcript.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
import sys
sys.stdout.buffer.write((('cuts %s\n' % cuts) + ' '.join('%d:%s[%.2f]' % (i, w['text'], w['start']) for i, w in enumerate(words)) + '\n').encode('utf8'))
