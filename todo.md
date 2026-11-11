# TODO

`alpha` 브랜치 재편 후 남은 작업. 기준 문서는 `docs/scheme.md`.
현황 수치는 `python tools/audit.py`로 언제든 다시 뽑을 수 있다.

**한 줄 요약**: 저장소는 **컬러 SVG 211개**만 관리한다. 확보해야 할 아이콘은 **65개**다.

| 구분 | 수량 | 내역 |
| --- | --- | --- |
| PPT V2.2 에서 추출 | 62 | 일반 38, 카테고리 12, Identity 7, 산업 2, 리소스 1, Flow Log 1, Dooray! 1 |
| 디자인팀 신규 제작 | 2 | Database Migration Service, NHN Cloud Foundry |
| PPT 확인 후 결정 | 1 | NHN Cloud Private Region |

여기에 파일이 아닌 **Arrows 스펙 6종**(PPT 16쪽)과, 자산은 있으나 이름만 맞추면 되는
**Contiple 개명 1건**이 별도로 있다.

블랙 버전과 PNG 는 더 이상 관리하지 않는다. 흑백이 필요하면 draw.io 내보내기로 처리한다.

---

## 1. 자산 확보

### 1-1. 우선순위 요약

| 순위 | 작업 | 수량 | 방법 | 막힘 |
| --- | --- | --- | --- | --- |
| 1 | 일반 아이콘 추출 | 38 | PPT 18\~19쪽 | 없음 |
| 2 | 카테고리 아이콘 제작 | 12 | PPT 20쪽 또는 신규 | 디자인 리소스 |
| 3 | Identity 아이콘 추출 | 7 | PPT 17쪽 | 없음 |
| 4 | Arrows 스펙 입력 | 6 | PPT 16쪽 (파일 아님) | 없음 |
| 5 | 누락 서비스 아이콘 | 6 | 추출 2 / 신규 2 / 확인 2 | DMS·Foundry는 디자인팀 |
| 6 | 산업·개념 아이콘 | 2 | PPT | Machine Learning은 중복 확인 필요 |
| 7 | 리소스 1건 | 1 | PPT | 없음 |

### 1-2. 일반 아이콘 38개 — PPT 18~19쪽에서 추출

기대 53개 중 15개 확인(보유 파일은 16개이고 그중 `manager`는 기대 목록에 없음). 추출 시 60×60 캔버스, 브랜드 블루 `#125DE6` 기준.

| 묶음 | 없는 아이콘 |
| --- | --- |
| 사람 (3) | Administrator, Authenticated user, Users |
| 단말 (2) | Client, Mobile client |
| 범용 인프라 (9) | Disk, Internet, Globe, Server, Servers, Storage, Tape storage, Cold storage, Office building |
| 애플리케이션·개발 (10) | Application Service, Generic application, Git repository, Programming language, Source code, SDK, Toolkit, Dev Tools, JSON script, NHN Cloud Console |
| 데이터·문서 (9) | Data stream, Data table, Document, Documents, Folder, Folders, Logs, Metrics, Multimedia |
| 보안·알림 (5) | Credentials, SAML token, SSL padlock, Alert, Chat |

> 보유 16개: application-instance, desktop, desktop-phone, external-user, gateway, interface, internal-user, ip-acl, laptop, login-security-settings, manager, mobile-devices, peering, phone, private-network, subnet

- [ ] `manager`가 기대 목록의 **Administrator**와 같은 것인지 확인. 같으면 `ic-general-administrator`로 개명, 다르면 Administrator를 따로 추출

### 1-3. Identity 7개 — PPT 17쪽에서 추출

`icons/04-identity/`가 비어 있다. 파일명은 `ic-identity-<name>.svg`.

- NHN Cloud 계정: Owner, Admin, Member, Viewer
- IAM 계정: Admin, Member, Viewer

### 1-4. Arrows 6종 — PPT 16쪽, 파일이 아니라 엣지 스타일

`icons/01-arrows/styles.yaml`이 비어 있다. 선 두께는 모두 1pt.

| 항목 | 선 색 | 선 종류 |
| --- | --- | --- |
| Primary Path | `#555555` | 실선 |
| Secondary Path | `#555555` | 점선 |
| Primary Path (연한 배경용) | `#999999` | 실선 |
| Secondary Path (연한 배경용) | `#999999` | 점선 |
| Success Status | `#09C72C` | 실선 |
| Failure Status | `#EF0F0F` | 실선 |

- [ ] 점선의 실제 dash 패턴 값을 PPT에서 확인 (현재 표에 없음)
- [ ] `styles.yaml` 스키마를 정하고 `make_drawio_libs.py`가 엣지 스타일 엔트리를 생성하도록 추가

### 1-5. 누락 서비스 아이콘 6개

| 서비스 | 카테고리 | 상태 | 조치 |
| --- | --- | --- | --- |
| Flow Log | Network | SVG 없음. PNG 만 있었으나 PNG 관리를 중단해 삭제 | PPT 에서 추출 |
| Dooray! | Collaboration | 컬러 SVG 없음 (블랙만 있었으나 삭제) | 박스에서 추출하거나 PPT에서 |
| NHN Cloud Private Region | Hybrid & Private Cloud | 자산 전혀 없음 | PPT 확인 후 없으면 신규 제작 |
| Database Migration Service § | Database | 아이콘 자체 없음 | **디자인팀 신규 제작 요청** |
| NHN Cloud Foundry § | Machine Learning | 아이콘 자체 없음 | **디자인팀 신규 제작 요청** |
| Contiple | Contact Center | 파일은 `ic-contact-center-online-contact`로 존재 | 같은 상품인지 확인 후 개명 |

### 1-6. 산업·개념 2개

- Finance — PPT에서 추출
- Machine Learning — `ic-machine-learning`을 `18-machine-learning/category/`에 카테고리 아이콘으로 배치했는데, scheme.md는 산업·개념 목록에도 올려 두었다. **같은 아이콘인지 확인**하고, 같다면 어느 쪽에 둘지(또는 양쪽 모두) 결정

### 1-7. 리소스 1개

- IPSec VPN † (Security / Network Firewall) — PPT에서 추출. 현재 Security 리소스는 Firewall 1개뿐

### 1-8. 카테고리 아이콘 12개 — 자산 없음

PNG 로 임시 운용하던 것을 PNG 관리 중단과 함께 삭제했다. SVG 로 다시 확보해야 한다.
PNG 원본은 `git show d1915f1:files/category_icons/` 로 꺼내 참고할 수 있다.

`compute` · `container` · `network` · `monitoring` · `hybrid-private-cloud` · `game` · `search` · `management` · `bill` · `collaboration` · `contact-center` · `governance-audit`

> 나머지 10개(storage, database, security, ai-service, application-service, content-delivery, data-analytics, dev-tools, machine-learning, notification)는 SVG 보유.

---

## 2. 검증

- [x] **draw.io에서 라이브러리 렌더링 확인** (2026-11-11, app.diagrams.net)
  - [x] `05-groups` 19개 로드, 타이틀 19개 모두 정상 표기
  - [x] `06-compute` 로드 (당시 카테고리 PNG 포함 9개, 현재는 서비스 8개)
  - [x] 그룹 컨테이너 선 스타일 — VPC 회색 실선, Auto Scaling Group 파란 점선으로 구분됨
  - [x] 모서리 아이콘 24×24가 박스 좌상단에 표시됨
  - [x] 컨테이너 동작 — VPC 박스에 Instance를 떨어뜨린 뒤 박스를 이동하니 자식이 함께 따라옴
  - [ ] 나머지 팔레트 일괄 로드 확인 (2개만 표본 검증함)
- [ ] `docs/sample-3tier-architecture.drawio`를 새 라이브러리로 다시 그려 비교
- [ ] PPT V2.2 10\~13쪽 예시 구성도를 draw.io로 재현해 누락 아이콘 확인

---

## 3. 결정이 필요한 사항

- [ ] **`taxonomy.yaml`의 표시명 전수 검증** — 슬러그에서 기계적으로 유도한 초안이다. 공식 홈페이지 표기와 대조 필요
- [ ] `online-contact` = Contiple 인지 확인 (1-5 참고)
- [ ] `nhn-private-cloud`(Retired)가 Private Station인지 Region인지 — scheme.md Retired 목록은 "개명 전 NHN Private Cloud"로 보지만, § 주석은 미확인으로 남겨 둠
- [ ] Public/Private subnet 레이블 프리셋을 Groups 팔레트에 항목 2개로 넣을지, 한 항목에 레이블만 바꿔 쓸지
- [ ] 홈페이지 서비스 목록 변경 시 분류표를 다시 맞추는 주기 (예: 분기 1회)

---

## 4. 배포 준비

- [ ] **`alpha` 를 origin 에 푸시해야 `clibs` 링크가 동작한다**
- [ ] 링크 URL 이 2,660자다. 사내 브라우저·프록시에서 잘리지 않는지 확인하고,
      문제가 있으면 분할하거나 `defaultCustomLibraries` 방식으로 전환
- [ ] 저장소 `assets/pptx/` 사본을 포털 최신판(2026.4.8, 58쪽)으로 교체 — 현재 2026.1.29판(57쪽)
- [ ] PPT 다음 개정을 홈페이지 기준으로 갱신 요청 (Face Liveness 중복 표기, 단종 아이콘 포함, 신규 2개 누락)
- [ ] `tools/validate.py` 작성 — 블랙 누락, 슬러그 규칙 위반, taxonomy 미등록 검출을 CI로

---

## 5. 참고: 이번 재편에서 삭제한 것

되살리려면 `git show d1915f1:<경로>`.

| 삭제물 | 수량 | 사유 |
| --- | --- | --- |
| PNG | 596 | SVG에서 파생 가능. SVG와 어긋나 드리프트 중이었음 |
| 서비스 박스 | 127 | 레퍼런스 아키텍처 근거가 없음. 9개만 Groups 팔레트에 유지 |
| 구 draw.io 라이브러리 | 8 | `dist/`로 대체 |
| 구 카탈로그 md | 4 | `taxonomy.yaml`에서 생성 |
| 중복·잔재 SVG | 9 | `@2x`, `(dsr)` 중복, 위치 오류 리소스 등 |
| 블랙 SVG | 199 | 컬러만 제공하기로 결정 |
| 복구했던 PNG | 13 | PNG 관리 중단 (카테고리 12, Flow Log 1) |
