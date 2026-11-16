---
name: nhn-cloud-drawio
description: 사용자가 말이나 글로 설명한 NHN Cloud 아키텍처 구성도를 draw.io 파일(.drawio)로 그려 브라우저 draw.io 편집기로 열어 준다. "구성도 그려줘", "아키텍처 다이어그램", "3-tier 구성도", "이 구성 그림으로", "drawio로 만들어줘" 같은 요청에 사용한다. 도형은 NHN Cloud 아이콘 라이브러리(https://nhn-cloud.github.io/Icons/)의 실제 팔레트에서만 가져오며, 라이브러리에 없는 아이콘은 지어내지 않는다.
---

# NHN Cloud 아키텍처 구성도 생성

> **사내 배포본은 <https://github.com/TOAST-DOCS/Icons> 입니다.**
> 저장소 밖에서도 쓰려면 그쪽을 설치하세요. 이 사본은 Icons 저장소 안에서 작업할 때 쓰입니다.
> 둘 중 하나를 고치면 다른 쪽도 맞춰야 합니다.

사용자의 자연어 설명 → YAML 명세 → `.drawio` → 브라우저 draw.io 편집기.
생성물은 **초안**이다. 세밀한 배치는 draw.io 에서 사용자가 직접 손본다.

## 도구

클론한 **저장소 루트**(`dist/` 와 `tools/` 가 보이는 폴더)에서 실행한다.
Python 3.9 이상과 PyYAML 이 필요하다.

| 도구 | 용도 |
| --- | --- |
| `python tools/nhn_diagram.py --list [검색어]` | 라이브러리의 실제 도형 이름 조회 (276개) |
| `python tools/nhn_diagram.py spec.yaml out.drawio` | 명세 → .drawio **최초 생성** |
| `python tools/drawio_edit.py out.drawio ...` | 이미 있는 .drawio **제자리 수정** |
| `python tools/drawio_open.py out.drawio` | 브라우저 draw.io 로 열기 |

`dist/` 가 없으면 `https://raw.githubusercontent.com/nhn-cloud/Icons/draft/dist` 에서
자동으로 받아 쓴다. PyYAML 이 필요하다.

## 절차

### 1. 구조 파악

사용자 설명에서 다음을 뽑는다. 애매하면 **지어내지 말고 묻는다**.

- 담을 것(노드): 서비스·리소스 아이콘
- 감쌀 것(그룹): NHN Cloud / Region / VPC / Subnet / Auto Scaling Group 등 중첩 관계
- 이을 것(엣지): 무엇에서 무엇으로, 어떤 선으로

### 2. 아이콘 이름 조회 — 건너뛰지 않는다

**기억으로 아이콘 이름을 쓰지 않는다.** 반드시 `--list` 로 실제 이름을 확인한다.

```bash
python tools/nhn_diagram.py --list 로드밸런      # 한글/영문 부분 일치, 대소문자·공백·하이픈 무시
python tools/nhn_diagram.py --list groups        # 그룹 박스 15종
python tools/nhn_diagram.py --list arrows        # 연결선 18종
```

- 못 찾으면 생성기가 비슷한 이름을 알려 준다. 그래도 없으면 **임의로 다른 아이콘을 대체하지 말고**
  사용자에게 "라이브러리에 없다. 무엇으로 대체할까" 하고 묻는다.
- 같은 이름이 여러 팔레트에 있으면 `"Network/Security Groups"` 처럼 `팔레트/이름` 으로 적는다.
  (실제 충돌 예: `Security Groups` 는 Groups 와 Network 양쪽에 있다)

### 3. 명세 작성 → 사용자 확인

YAML 을 작성해 **사용자에게 먼저 보여주고 확정**한 뒤 생성한다. 구조 오해를 그림까지 가서 발견하면 손해다.

### 4. 생성과 열기

```bash
python tools/nhn_diagram.py spec.yaml out.drawio   # 최초 1회만. 이미 있으면 아래 '수정 요청' 으로
python tools/drawio_open.py out.drawio
```

`drawio_open.py` 는 `out.open.html` 리다이렉트 파일을 만들고 기본 브라우저로 draw.io 를 띄운다
(URL 조각 방식이라 사내 프록시를 타지 않는다). 사용자 브라우저에는 NHN Cloud 팔레트 28개가
이미 붙어 있어 그 자리에서 아이콘을 더 끌어다 쓸 수 있다.

**편집 결과 저장**: draw.io 웹의 Ctrl+S 는 다운로드다. 제자리 저장을 원하면
draw.io 에서 `파일 > 열기 > 디바이스` 로 `.drawio` 를 직접 열라고 안내한다.

## 수정 요청 — 명세에서 다시 그리지 않는다

**`.drawio` 파일이 한 번이라도 존재하면 그 파일이 원본이다.** 사용자가 draw.io 에서 도형을
옮겼을 수 있고, 명세에서 다시 그리면 그 손질이 전부 사라진다. "DB 하나 더", "이 선 지워 줘"
같은 요청은 **반드시 `drawio_edit.py` 로 그 파일을 고친다.**

```bash
python tools/drawio_edit.py out.drawio list              # 먼저 현재 id 를 본다
python tools/drawio_edit.py out.drawio add --icon "RDS Instance" --id db3 --label "Replica 2" --below db2
python tools/drawio_edit.py out.drawio edge --from db1 --to db3 --style "Secondary Path · 점선"
python tools/drawio_edit.py out.drawio relabel db2 "Replica (읽기)"
python tools/drawio_edit.py out.drawio remove db3        # 딸린 연결선도 함께
```

- `list` 를 먼저 돌려 **실제 id 를 확인**한다. 자동 생성 id 는 `n2`, `n19` 처럼 순번이라 기억에 의존하면 틀린다.
- 위치는 `--below` / `--right-of` / `--into` 로 기존 도형을 기준 삼아 정한다. 부모 그룹이 좁으면 자동으로 넓어진다.
- 이 도구는 다른 도형의 좌표를 **건드리지 않는다.** 사용자가 draw.io 에서 추가한 도형도 그대로 남는다.
- XML 을 직접 편집하지 않는다. 압축 저장·id 중복·이스케이프 때문에 손으로 고치면 깨진다.

**명세에서 다시 그려도 되는 때는 하나뿐이다**: 구조를 통째로 바꿔야 해서 재배치가 더 나을 때.
이때는 "draw.io 에서 손보신 배치가 사라집니다" 라고 먼저 알리고 **승인을 받은 뒤** 다시 그린다.

명세 파일은 `<이름>.spec.yaml` 로 옆에 남겨 두되, 최초 생성 기록일 뿐 원본이 아니다.

## 명세 형식

```yaml
title: 3-Tier Web Service on NHN Cloud   # 선택. 왼쪽 위 제목
dir: row                                  # 최상위 배치 방향 row | col (기본·권장 row — 가로형)
items:
  - {id: users, icon: Users, label: 사용자}
  - group: Region                         # Groups 팔레트 이름
    label: KR1 (판교)                      # 생략 시 그룹 이름이 레이블
    dir: row
    items:
      - group: VPC
        items:
          - {id: lb, icon: Load Balancer}
edges:
  - [users, lb]                                   # 기본 Primary Path
  - [lb, web1, Secondary Path · 점선]
  - {from: web1, to: db, style: Primary Path, label: "3306"}
  - {from: asg, to: obs, exit: bottom, entry: top}
```

| 항목 | 옵션 |
| --- | --- |
| 노드 | `id`, `icon`(필수), `label`, `w`/`h` |
| 그룹 | `id`, `group`(필수), `label`, `dir`, `gap`, `pad`, `align`(center/start), `min_w`, `min_h` |
| 엣지 | `from`, `to`, `style`(Arrows 이름, 기본 Primary Path), `label`, `exit`/`entry`(left/right/top/bottom), `extra` |
| 빈 칸 | `{spacer: 60}` |

연결선은 이미지가 아니라 **엣지 스타일**이다. 18종: Primary Path / Secondary Path
(각각 기본·점선·양방향·양방향 점선·화살촉 없음·점선+화살촉 없음), Success Status /
Failure Status (각각 기본·양방향·화살촉 없음).

## 배치 요령

**구성도는 가로형이 기본이다.** 사용자가 세로형을 명시적으로 요청하지 않는 한
전체 흐름을 왼쪽 → 오른쪽으로 두고, 최상위와 바깥 그룹은 `dir: row` 로 쓴다.

자동 배치는 `row`/`col` 중첩 패킹이라 단순하다. 다음을 지키면 결과가 훨씬 낫다.

- **흐름은 가로로**: 외부 → 게이트웨이 → LB → 앱 → DB 를 `dir: row` 로 둔다.
  Region·VPC·Subnet 같은 바깥 그룹도 기본은 `dir: row` 다.
- **짝만 세로로**: 웹 서버 2대, DB Master/Replica 처럼 **같은 역할의 짝**만 `dir: col` 로 묶는다.
- **한 층에 3개 이상 쌓이면 열로 쪼갠다**: `Generic Group (점선)` 으로 묶어 가로로 세운다.
  (예: Private Subnet 안에 Web 열, DB 열) 그대로 `col` 로 쌓으면 그림이 세로로 길어진다.
- **엣지는 꼭 필요한 것만**: 선이 많을수록 겹침이 심해진다. 교차가 생기면 `exit`/`entry` 로 방향을 고정한다.
- 그룹이 너무 좁으면 `min_w` / `min_h` 로 넓힌다.

## 한계 — 미리 알린다

- 엣지 라우팅이 거칠어 **선이 그룹 경계를 지나거나 겹칠 수 있다.** draw.io 에서 선만 손보면 된다.
- 레이아웃 엔진이 격자 패킹이라 PPT 예시처럼 정교한 배치는 안 된다.
- 아이콘 패널 표시명은 8자쯤에서 잘린다(라이브러리 쪽 기존 이슈, `todo.md` 1-4 참고).

## 하지 말 것

- 라이브러리에 없는 아이콘 이름을 지어내기. `--list` 결과가 유일한 근거다.
- 비슷해 보인다고 임의 대체하기. 사용자에게 물어본다.
- `dist/*.xml` 을 직접 고치기. 팔레트는 `make_drawio_libs.py` 산출물이다.
