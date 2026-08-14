"""Dataset analysis script for cyberbullying_dataset.csv"""
import json
from collections import Counter

with open('dataset/cyberbullying_dataset.csv', 'r', encoding='utf-8') as f:
    content = f.read()

data = json.loads(content)
print(f'Total records: {len(data)}')
print(f'Keys in first record: {list(data[0].keys())}')

labels = [d.get('output', '') for d in data]
label_counts = Counter(labels)
print('\nLabel distribution (output field):')
for k, v in sorted(label_counts.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v} ({100*v/len(data):.1f}%)')

texts = [d.get('instruction', '') for d in data]
empty = sum(1 for t in texts if not t.strip())
duplicates = len(texts) - len(set(texts))
short = sum(1 for t in texts if 0 < len(t.strip()) < 10)
long_count = sum(1 for t in texts if len(t) > 1000)

print(f'\nInstruction (actual text) stats:')
print(f'  Empty: {empty}')
print(f'  Duplicates: {duplicates}')
print(f'  Very short (<10 chars): {short}')
print(f'  Very long (>1000 chars): {long_count}')

static_texts = Counter([d.get('text', '') for d in data])
print(f'\nUnique "text" (prompt) values: {len(static_texts)}')
print(f'Constant "text" field? {"YES" if len(static_texts) == 1 else "NO"}')
