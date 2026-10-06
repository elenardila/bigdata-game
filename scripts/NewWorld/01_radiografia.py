from pathlib import Path

import pandas as pd


DATASET = Path(
    'data/raw/nevworld_599510517943134969_20261005_183045.jsonl'
)

if not DATASET.exists():
    raise FileNotFoundError(
        f'No se encuentra: {DATASET.resolve()}'
    )

df = pd.read_json(DATASET, lines=True)


required = ['run_id', 'event_index', 'tick', 'type']

assert not df.empty, 'El dataset está vacío'
assert all(column in df.columns for column in required), \
    'Faltan columnas principales'
assert not df.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados (run_id + event_index)'

ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, \
    'Los ticks retroceden al ordenar por event_index'

print('VALIDACIÓN BÁSICA: OK')


print('\nPRIMEROS EVENTOS')
print(df.head())

filas, columnas = df.shape
conteo = df['type'].value_counts()

print('Nombre del archivo:', DATASET.name)
print('Número total de eventos:', filas)
print('Número de columnas:', columnas)
print('Nombres de las columnas:', df.columns.tolist())
print('Tipo del primer evento:', df['type'].iloc[0])
print(
    'Tipo más frecuente:',
    conteo.idxmax(), '->', conteo.max(), 'eventos'
)

print('\nRecuento de todos los tipos:')
print(conteo)

print('\nPrimera fila:')
print('run_id:', df['run_id'].iloc[0])
print('semilla:', df['seed'].iloc[0])
print('esquema:', df['schema_version'].iloc[0])

print('\nTick mínimo:', df['tick'].min())
print('Tick máximo:', df['tick'].max())