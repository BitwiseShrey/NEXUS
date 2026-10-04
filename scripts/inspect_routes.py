import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.main import app

routes = []
for r in app.routes:
    methods = getattr(r, 'methods', None)
    path = getattr(r, 'path', None)
    if path:
        routes.append((list(methods) if methods else [], path))

print(f"Total endpoints registered: {len(routes)}")
for m, p in sorted(routes, key=lambda x: x[1]):
    clean_m = [x for x in m if x != 'HEAD'] if m else ['MOUNT']
    print(f"  {clean_m}: {p}")
