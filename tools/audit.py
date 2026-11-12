# -*- coding: utf-8 -*-
"""docs/scheme.md 분류표와 icons/ 실제 파일을 대조해 누락 자산을 보고한다.

    python tools/audit.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / 'icons'
SCHEME = ROOT / 'docs' / 'scheme.md'

CATS = ['compute', 'container', 'network', 'storage', 'database', 'monitoring',
        'hybrid-private-cloud', 'game', 'security', 'content-delivery', 'notification',
        'ai-service', 'machine-learning', 'application-service', 'search', 'data-analytics',
        'dev-tools', 'management', 'bill', 'collaboration', 'contact-center', 'governance-audit']
CATDIR = {c: '%02d-%s' % (i + 6, c) for i, c in enumerate(CATS)}
TITLE2CAT = {
    'Compute': 'compute', 'Container': 'container', 'Network': 'network', 'Storage': 'storage',
    'Database': 'database', 'Monitoring': 'monitoring', 'Hybrid & Private Cloud': 'hybrid-private-cloud',
    'Game': 'game', 'Security': 'security', 'Content Delivery': 'content-delivery',
    'Notification': 'notification', 'AI Service': 'ai-service', 'Machine Learning': 'machine-learning',
    'Application Service': 'application-service', 'Search': 'search', 'Data & Analytics': 'data-analytics',
    'Dev Tools': 'dev-tools', 'Management': 'management', 'Bill': 'bill',
    'Collaboration': 'collaboration', 'Contact Center': 'contact-center',
    'Governance & Audit': 'governance-audit',
}
# 표시명 -> 실제 슬러그 (괄호 등 기계 변환이 안 되는 것만)
ALIAS = {
    'NHN Kubernetes Service (NKS)': 'nks', 'NHN Container Registry (NCR)': 'ncr',
    'NHN Container Service (NCS)': 'ncs', 'Load Balancer (DSR)': 'load-balancer-dsr',
    'NAS (offline)': 'nas-offline', 'VPN Gateway (Site-to-Site VPN)': 'vpn-gateway',
    'Native Deck': 'nhn-native-deck', 'Dooray!': 'dooray', 'Log & Crash Search': 'log-n-crash-search',
    'File-Crafter': 'file-crafter', 'RDS for MS-SQL': 'rds-for-ms-sql',
    'MS-SQL Instance': 'ms-sql-instance', 'Security Compliance': 'security-compliance',
    'NHN Cloud Private Station': 'nhn-cloud-private-station',
    'NHN Cloud Private Deck': 'nhn-cloud-private-deck',
    'NHN Cloud Private Region': 'nhn-cloud-private-region',
    'NHN Hybrid Cloud': 'nhn-hybrid-cloud', 'GameStarter': 'game-starter',
    'NAS for BigData': 'nas-for-bigdata', 'Data Transporter': 'data-transporter',
}


def to_slug(name):
    if name in ALIAS:
        return ALIAS[name]
    s = name.lower().replace('&', 'n').replace('!', '')
    s = re.sub(r'\(.*?\)', '', s)
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


rows = []
for line in io.open(SCHEME, encoding='utf-8'):
    m = re.match(r'^\| ([A-Z][^|(]*?) \((\d+)\) \| (.+?) \| (.+?) \|\s*$', line)
    if m:
        rows.append((m.group(1).strip(), int(m.group(2)), m.group(3), m.group(4)))

print('=' * 64)
print('서비스 아이콘 감사 (scheme.md 분류표 기준)')
print('=' * 64)
total_exp = total_have = 0
missing_all = []
for title, cnt, svc_cell, _res in rows:
    cat = TITLE2CAT.get(title)
    if not cat:
        print('  ?? 미지의 카테고리: %s' % title)
        continue
    expected = [s.strip() for s in svc_cell.split(',')]
    d = ICONS / CATDIR[cat] / 'services'
    have = {p.stem[len('ic-%s-' % cat):] for p in list(d.glob('*.svg')) + list(d.glob('*.png'))
            if not p.stem.endswith('.black')}
    miss = []
    for e in expected:
        mark = ''
        for ch in '†‡§':
            if ch in e:
                mark = ch
                e = e.replace(ch, '')
        e = e.strip()
        if to_slug(e) not in have:
            miss.append((e, mark))
    total_exp += len(expected)
    total_have += len(expected) - len(miss)
    extra = have - {to_slug(e.replace('†', '').replace('‡', '').replace('§', '').strip())
                    for e in expected}
    if miss or extra:
        print('\n[%s] 기대 %d · 보유 %d' % (title, len(expected), len(expected) - len(miss)))
        for e, mark in miss:
            tag = {'†': '† 박스만 있음', '‡': '‡', '§': '§ 아이콘 자체 없음'}.get(mark, '')
            print('   없음: %-34s %s' % (e, tag))
            missing_all.append((title, e, tag))
        for x in sorted(extra):
            print('   분류표에 없는 파일: %s' % x)

print('\n서비스 합계: 기대 %d · 보유 %d · 누락 %d' % (total_exp, total_have, total_exp - total_have))

print('\n' + '=' * 64)
print('기타 팔레트')
print('=' * 64)
for pid, label, expect in [('01-arrows', '화살표', 18), ('02-general', '일반 리소스', None),
                           ('03-industry', '산업·개념', None), ('04-identity', '계정·역할', 9),
                           ('05-groups/containers', '그룹 컨테이너', 11)]:
    d = ICONS / pid
    if pid == '01-arrows':
        # 화살표는 SVG 가 아니라 styles.yaml 의 엣지 스타일이라 파일 수로 셀 수 없다.
        import yaml
        f = d / 'styles.yaml'
        n = len((yaml.safe_load(f.read_text(encoding='utf-8')) or {}).get('arrows') or [])             if f.exists() else 0
    else:
        n = len([p for p in list(d.glob('*.svg')) + list(d.glob('*.png'))
                 if not p.stem.endswith('.black')]) if d.exists() else 0
    note = '' if expect is None else ('  <- %d개 기대, %d개 부족' % (expect, expect - n) if n < expect else '')
    print('  %-22s %3d개%s' % (label, n, note))

print('\n카테고리 아이콘:')
no_ci = [c for c in CATS if not (ICONS / CATDIR[c] / 'category').exists()
         or not (list((ICONS / CATDIR[c] / 'category').glob('*.svg'))
                 + list((ICONS / CATDIR[c] / 'category').glob('*.png')))]
print('  보유 %d / 22, 없음 %d개: %s' % (22 - len(no_ci), len(no_ci), ', '.join(no_ci)))
