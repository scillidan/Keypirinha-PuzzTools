import re
from typing import Callable, Iterable

Grid = Iterable[Iterable[str]]
GridTransform = Callable[[Grid], Grid]


def make_grid_transform(grid_transform: GridTransform) -> Callable[[str], str]:
    """Returns a transform that applies the given grid transform to the input text."""
    def transform(data: str) -> str:
        has_tab = '\t' in data
        new_line = '\r\n' if '\r\n' in data else '\n'
        grid = [l.split('\t') if has_tab else list(l) for l in data.split(new_line)]
        new_grid = grid_transform(grid)
        return new_line.join(('\t' if has_tab else '').join(line) for line in new_grid)
    return transform

_CASES = {
    'lowercase': str.lower,
    'uppercase': str.upper,
    'titlecase': lambda x: x.title(),
    'kebabcase': lambda x: re.sub(r'\s|(\B)([A-Z])', r'-\2', x).lower(),
    'snakecase': lambda x: re.sub(r'\s|(\B)([A-Z])', r'_\2', x).lower(),
    'camelcase': lambda x: x[0].lower() + re.sub(r'\s|(\B)([A-Z])', r'\2', x)[1:],
    'pascalcase': lambda x: re.sub(r'\s|(\B)([A-Z])', r'\2', x),
}

_NUTRIMATICS = {
    'from ANSWERIZE': lambda x: x.lower().replace('?', 'A'),
    'add A* between': lambda x: 'A*' + 'A*'.join(x) + 'A*',
    'add ?': lambda x: ''.join(f'{c}?' for c in x),
    'from enumeration': lambda x: ' '.join(f'A{{{n}}}' for n in re.findall(r'\d+', x)),
}

_SORTS = {
    'alphabetical': lambda x: '\n'.join(sorted(x.split('\n'))),
    'by length': lambda x: '\n'.join(sorted(x.split('\n'), key=len)),
    'reverse': lambda x: '\n'.join(reversed(x.split('\n'))),
}

_TOOLS = {
    # 'lobechat assistants': lambda x: re.sub(r'https://lobehub.com/assistants/(.*)', r'https://lobechat.com/discover/assistant/\1', x),
    '2github api': lambda x: x.replace('https://github.com/', 'https://api.github.com/repos/'),
    '2github commits atom': lambda x: re.sub(r'https://github.com/([^/]+)/([^/]+)(?:/.*)?', r'https://github.com/\1/\2/commits.atom', x),
    '2github raw url': lambda x: re.sub(r'https://github.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)', r'https://raw.githubusercontent.com/\1/\2/refs/heads/\3/\4', x),
    '2github releases atom': lambda x: re.sub(r'https://github.com/([^/]+)/([^/]+)(?:/.*)?', r'https://github.com/\1/\2/releases.atom', x),
    '2ghcli url': lambda x: re.sub(r'https://github.com/([^/]+)/([^/]+)(?:/.*)?', r'\1/\2', x),
    '2unix url': lambda x: x.replace('\\', '/'),
    '2unix 2xurl': lambda x: x.replace('\\\\', '/'),
    '2windows url': lambda x: x.replace('/', '\\'),
    '2windows urlx2': lambda x: x.replace('\\', '\\\\'),
    'typst commit': lambda x: re.sub(r'packages/preview/(.+?)/.*', r'https://typst.app/universe/search/?q=\1', x),
    'vscode marketplace': lambda x: re.sub(r'https://marketplace.visualstudio.com/items\?itemName=([^\.]+)\.(.+)', r'https://marketplace.visualstudio.com/_apis/public/gallery/publishers/\1/vsextensions/\2/latest/vspackage', x),
    'delete space': lambda x: re.sub(r'[\s\xA0]+', '', x),
    'linebreak 2comma': lambda x: ','.join(sorted(set(x.split()), key=int)),
}

TRANSFORMS = {
    'case': _CASES,
    'nutrimatic': _NUTRIMATICS,
    'sort': _SORTS,
    'tool': _TOOLS,
    'alphabet': lambda _: 'abcdefghijklmnopqrstuvwxyz',
    'answerize': lambda x: re.sub('[^A-Z0-9]', '', x.upper()),
    'length': len,
    'reverse': lambda x: x[::-1],
    'rotate': make_grid_transform(lambda x: zip(*reversed(x))),
    'transpose': make_grid_transform(lambda x: zip(*x)),
    'unique': lambda x: ''.join(set(x)),
}
