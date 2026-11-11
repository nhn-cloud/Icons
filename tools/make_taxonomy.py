# -*- coding: utf-8 -*-
"""icons/ 트리를 읽어 taxonomy.yaml 초안을 만든다.

표시명(name)은 슬러그에서 기계적으로 유도한 "초안"이다.
홈페이지 표기로 검증한 뒤 taxonomy.yaml 을 직접 고쳐 쓰는 것이 정상 운용이며,
이 스크립트는 최초 부트스트랩과 누락 점검용이다.

    python tools/make_taxonomy.py            # 표준출력으로 미리보기
    python tools/make_taxonomy.py --write    # taxonomy.yaml 에 기록 (기존 name 보존)
    python tools/make_taxonomy.py --write --reset   # name 을 슬러그에서 다시 유도
"""
import io
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / 'icons'

# 기존 taxonomy.yaml 의 slug -> name. 사람이 검증해 고친 표시명을 보존한다.
KEPT = {}


def load_kept():
    """기존 taxonomy.yaml 에서 slug 별 표시명을 읽어 둔다.

    --reset 을 주지 않는 한, 이미 등록된 슬러그의 name 은 그대로 유지하고
    새로 들어온 파일만 슬러그에서 이름을 유도한다.
    """
    p = ROOT / 'taxonomy.yaml'
    if '--reset' in sys.argv or not p.exists():
        return
    slug = None
    for line in io.open(p, encoding='utf-8'):
        s = line.strip()
        if s.startswith('- slug:') or s.startswith('slug:'):
            slug = s.split(':', 1)[1].strip()
        elif s.startswith('name:') and slug:
            KEPT[slug] = s.split(':', 1)[1].strip().strip('"')
            slug = None

TITLES = {
    '01-arrows': 'Arrows', '02-general': 'General Resources',
    '03-industry': 'Industry & Concepts', '04-identity': 'Identity',
    '05-groups': 'Groups', '28-retired': 'Retired',
}
# 슬러그 -> 표시명에서 대문자로 살려야 하는 토큰
ACRONYM = {
    'ai': 'AI', 'api': 'API', 'acl': 'ACL', 'cdn': 'CDN', 'cds': 'CDS', 'dns': 'DNS',
    'dsr': 'DSR', 'erp': 'ERP', 'gpu': 'GPU', 'gslb': 'GSLB', 'iap': 'IAP', 'ip': 'IP',
    'iot': 'IoT', 'nas': 'NAS', 'nat': 'NAT', 'ncc': 'NCC', 'ncr': 'NCR', 'ncs': 'NCS',
    'nhn': 'NHN', 'nks': 'NKS', 'ocr': 'OCR', 'rcs': 'RCS', 'rds': 'RDS', 'rtcs': 'RTCS',
    'siem': 'SIEM', 'sms': 'SMS', 'sql': 'SQL', 'vpc': 'VPC', 'vpn': 'VPN',
    'ms': 'MS', 'db': 'DB', 'mysql': 'MySQL', 'mariadb': 'MariaDB', 'postgresql': 'PostgreSQL',
    'cubrid': 'CUBRID', 'tibero': 'Tibero', 'redis': 'Redis', 'valkey': 'Valkey',
    'easycache': 'EasyCache', 'easymaker': 'EasyMaker', 'webtob': 'WebtoB', 'jeus': 'JEUS',
    'etax': 'eTax', 'shorturl': 'ShortURL', 'gameanvil': 'GameAnvil', 'gamebase': 'Gamebase',
}


def title_of(slug, strip_prefix):
    s = slug
    for pre in strip_prefix:
        if s.startswith(pre):
            s = s[len(pre):]
            break
    words = [w for w in s.split('-') if w]
    out = [ACRONYM.get(w, w.capitalize()) for w in words]
    for i, w in enumerate(words):
        if w == 'for' and i > 0:          # RDS for MySQL
            out[i] = 'for'
    t = ' '.join(out)
    return t.replace('MS SQL', 'MS-SQL').replace('Log N Crash', 'Log & Crash')


def entries(d, strip_prefix):
    """컬러 원본(.svg 우선, 없으면 .png)을 찾아 (slug, name, black, fmt) 로."""
    out = []
    if not d.exists():
        return out
    seen = set()
    for p in sorted(list(d.glob('*.svg')) + list(d.glob('*.png'))):
        if p.stem.endswith('.black'):
            continue
        slug = p.stem
        if slug in seen:
            continue        # 같은 슬러그의 .svg 를 이미 잡았으면 .png 는 건너뜀
        seen.add(slug)
        black = (p.with_name(slug + '.black.svg').exists()
                 or p.with_name(slug + '.black.png').exists())
        out.append((slug, KEPT.get(slug) or title_of(slug, strip_prefix),
                    black, p.suffix[1:]))
    return out


def emit(lines, items, indent):
    pad = ' ' * indent
    for slug, name, black, fmt in items:
        lines.append('%s- slug: %s' % (pad, slug))
        lines.append('%s  name: "%s"' % (pad, name))
        if fmt != 'svg':
            lines.append('%s  format: %s       # SVG 없음, 비트맵으로 관리' % (pad, fmt))
        if not black:
            lines.append('%s  black: false      # 블랙 버전 없음' % pad)


def main():
    load_kept()
    L = []
    L.append('# NHN Cloud 아이콘 분류 단일 원천')
    L.append('# 생성: tools/make_taxonomy.py (%s)' % date.today().isoformat())
    L.append('#')
    L.append('# name 값은 슬러그에서 기계적으로 유도한 초안이다.')
    L.append('# 공식 홈페이지 서비스 목록 표기로 검증해야 한다. docs/scheme.md 참고.')
    L.append('#')
    L.append('# 이미 등록된 슬러그의 name 은 재생성해도 보존된다(검증한 표시명 유지).')
    L.append('# 슬러그에서 다시 유도하려면 --reset 을 준다.')
    L.append('version: 1')
    L.append('palettes:')

    for d in sorted(ICONS.iterdir()):
        if not d.is_dir():
            continue
        pid = d.name
        cat = pid.split('-', 1)[1]
        L.append('  - id: "%s"' % pid)
        L.append('    title: "NHN Cloud / %s"' % TITLES.get(pid, title_of(cat, [])))

        if pid == '01-arrows':
            L.append('    kind: styles')
            L.append('    source: styles.yaml')
            continue
        if pid == '05-groups':
            L.append('    kind: groups')
            L.append('    containers:')
            emit(L, entries(d / 'containers', ['grp-']), 6)
            L.append('    service_boxes:')
            emit(L, entries(d / "service-boxes", ["box-container-", "box-database-", "box-dev-tools-", "box-machine-learning-", "box-security-", "box-storage-", "box-"]), 6)
            continue
        if pid in ('02-general', '03-industry', '04-identity', '28-retired'):
            L.append('    kind: flat')
            items = entries(d, ['ic-general-', 'ic-industry-', 'ic-'])
            if items:
                L.append('    icons:')
                emit(L, items, 6)
            continue

        L.append('    kind: category')
        L.append('    category: %s' % cat)
        ci = entries(d / 'category', ['ic-'])
        if ci:
            slug, _n, black, fmt = ci[0]
            L.append('    category_icon:')
            L.append('      slug: %s' % slug)
            L.append('      name: "%s"' % (KEPT.get(slug) or _n))
            if fmt != 'svg':
                L.append('      format: %s       # SVG 없음, 비트맵으로 관리' % fmt)
            if not black:
                L.append('      black: false      # 블랙 버전 없음')
        else:
            L.append('    category_icon: null   # 없음, 제작 필요')
        svc = entries(d / 'services', ['ic-%s-' % cat])
        if svc:
            L.append('    services:')
            emit(L, svc, 6)
        res = entries(d / 'resources', ['ic-%s-' % cat])
        if res:
            # 리소스 슬러그에서 상위 서비스 슬러그를 떼어내 parent 로 기록
            svc_slugs = sorted((s[0] for s in svc), key=len, reverse=True)
            L.append('    resources:')
            for slug, _name, black, fmt in res:
                parent = next((x for x in svc_slugs if slug.startswith(x + '-')), None)
                tail = slug[len(parent) + 1:] if parent else slug[len('ic-%s-' % cat):]
                L.append('      - slug: %s' % slug)
                L.append('        name: "%s"' % (KEPT.get(slug) or title_of(tail, [])))
                L.append('        parent: %s' % (parent or 'null   # 상위 서비스 확인 필요'))
                if fmt != 'svg':
                    L.append('        format: %s       # SVG 없음, 비트맵으로 관리' % fmt)
                if not black:
                    L.append('        black: false      # 블랙 버전 없음')

    text = '\n'.join(L) + '\n'
    if '--write' in sys.argv:
        io.open(ROOT / 'taxonomy.yaml', 'w', encoding='utf-8', newline='\n').write(text)
        print('taxonomy.yaml 기록: %d줄' % len(L))
    else:
        print(text)


if __name__ == '__main__':
    main()
