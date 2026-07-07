import pathlib, sys
p = pathlib.Path(r'c:/Users/parll/OneDrive/Desktop/Work/Games/AdventureGame/backend/app.py')
src = p.read_text(encoding='utf-8')
try:
    compile(src, str(p), 'exec')
except SyntaxError as e:
    print('line', e.lineno, 'offset', e.offset, 'msg', e.msg)
    lines = src.splitlines()
    start = max(1, e.lineno - 6)
    end = min(len(lines), e.lineno + 6)
    for i in range(start, end + 1):
        print(f'{i}: {lines[i-1]}')
    sys.exit(1)
