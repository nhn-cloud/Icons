# TODO

`alpha` 브랜치 재편 후 남은 작업. 기준 문서는 `docs/scheme.md`.
현황 수치는 `python tools/audit.py`로 언제든 다시 뽑을 수 있다.

**한 줄 요약**: Figma `03 Architecture icon` 페이지와 대조해 자산을 대거 확보했다.
서비스 아이콘 **117/119**, 일반 아이콘 **52개**. 남은 것은 **신규 제작 2건**과 **Identity 7건**, **Arrows 6종**이다.

| 구분 | 이전 | 현재 |
| --- | --- | --- |
| 서비스 아이콘 | 113 / 119 | **117 / 119** |
| 일반 아이콘 | 16 | **52** |
| 리소스 | IPSec VPN 없음 | **확보** |
| 카테고리 아이콘 | 10 / 22 | 범위에서 제외 (아래 참고) |

**카테고리 아이콘은 이번 작업 범위에서 제외한다.** Figma `03 Architecture icon` 페이지는
카테고리를 섹션 프레임과 텍스트 라벨로만 구분하고 카테고리 아이콘을 두지 않는다.
기존에 확보한 10개는 그대로 쓰고, 없는 12개는 추적하지 않는다.

---

## 1. 자산 확보

### 1-1. 우선순위 요약

| 순위 | 작업 | 수량 | 방법 | 막힘 |
| --- | --- | --- | --- | --- |
| 1 | 디자인팀 신규 제작 요청 | 2 | Database Migration Service, NHN Cloud Foundry | 디자인 리소스 |
| 2 | Identity 아이콘 확보 | 7 | Figma 에 라이트 버전이 없음 (아래 1-3) | 확인 필요 |
| 3 | Arrows 스펙 입력 | 6 | PPT 16쪽 (파일 아님) | 없음 |
| 4 | 산업·개념 보강 | 2 | Finance, Machine Learning (아래 1-6) | 정의 확인 필요 |

### 1-2. 일반 아이콘 — 확보 완료

Figma 의 `ic-General_Icons-*` 프레임 **49개를 추출**해 `icons/02-general/` 에 넣었다.
기존 16개와 합쳐 **52개**가 되었고, scheme.md 가 기대한 53개를 사실상 채웠다.

추출 경로: Figma 노드 내보내기(SVG) → `tools/figma_clean.py` 로 배경 제거 → `ic-general-<슬러그>.svg`.
브랜드 블루 `#125DE6`, 60×60 캔버스로 기존 자산과 형식이 같다.

- [ ] `ic-general-manager` 와 `ic-general-administrator` 는 **서로 다른 아이콘**으로 확인됐다(path 비교).
      둘 다 유지했으나 표시명이 겹칠 수 있어 `taxonomy.yaml` 에서 구분이 필요한지 확인

### 1-3. Identity 7개 — Figma 에 라이트 버전이 없음

`03 Architecture icon` 페이지에서 찾은 계정·역할 아이콘은 전부
`General Resources Icon/Dark Backgrounds/...` 즉 **어두운 배경용 변형**이다.
저장소는 컬러 한 가지만 관리하므로 그대로 쓸 수 없다.

- [ ] 라이트 버전이 `02 Service icon` 페이지나 다른 곳에 있는지 확인
- [ ] 없다면 디자인팀에 라이트 버전 요청

필요한 7종: NHN Cloud 계정 Owner / Admin / Member / Viewer, IAM 계정 Admin / Member / Viewer

> Figma 에는 Billing Viewer, Log Viewer 등 **문서에 없던 역할도 있다.** 포함할지 결정 필요.

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

### 1-5. 누락 서비스 아이콘 2개 — 전부 신규 제작

| 서비스 | 카테고리 | 상태 |
| --- | --- | --- |
| Database Migration Service | Database | Figma 에 전용 페이지(`260820 DMS`)가 있으나 **아키텍처 아이콘은 별개로 신규 요청 필요** |
| NHN Cloud Foundry | Machine Learning | 전용 페이지(`260731 Foundry`) 동일 |

**확보 완료된 것** (Figma 에서 추출)

| 서비스 | 결과 |
| --- | --- |
| Flow Log | `icons/08-network/services/ic-network-flow-log.svg` |
| Dooray! | `icons/25-collaboration/services/ic-collaboration-dooray.svg` |
| Contiple | 기존 `online-contact` 와 **path 가 완전히 일치**해 `ic-contact-center-contiple.svg` 로 개명 |
| IPSec VPN | `icons/14-security/resources/ic-security-network-firewall-ipsec-vpn.svg` |
| NHN Cloud Private Region | `icons/12-hybrid-private-cloud/services/ic-hybrid-private-cloud-nhn-cloud-private-region.svg` (2026-11-12 추가) |

### 1-6. 산업·개념 2개 — 정의 확인 필요

현재 3개 보유 (IoT, Manufacturing, Medical & Healthcare). scheme.md 는 5개를 기대한다.

- **Finance** — Figma 에서 이 이름으로 걸리는 것은 `ic-dooray_erp-finance`(Dooray! ERP 재무, Retired 대상)뿐이다.
  산업·개념으로서의 Finance 아이콘은 존재하지 않는 것으로 보인다. 분류표에서 뺄지 확인 필요
- **Machine Learning** — `ic-machine-learning` 을 `18-machine-learning/category/` 에 카테고리 아이콘으로 두었다.
  산업·개념에도 올릴지, 카테고리 아이콘만으로 둘지 결정 필요

### 1-7. 리소스 — 확보 완료

IPSec VPN 을 Figma 에서 추출해 넣었다. Security 리소스가 Firewall, IPSec VPN 2개로 분류표와 일치한다.

### 1-8. 카테고리 아이콘 — 범위 제외

이번 작업에서 제외한다. 보유한 10개는 그대로 쓰고, 없는 12개는 추적하지 않는다.

Figma `03 Architecture icon` 페이지는 카테고리를 **섹션 프레임 + 텍스트 라벨**로만 구분한다.
예를 들어 `Compute` 는 1958×650 프레임과 1942×29 텍스트이고, 아이콘 노드가 아니다.
필요해지면 `02 Service icon` 페이지를 따로 확인해야 한다.

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
- [ ] `nhn-private-cloud`(Retired)가 Private Station인지 Region인지 — **Figma 에서 Private Region 쪽으로 확인됐다.**
      `Groups` 변형(`4954:54491`)에서 "NHN Cloud Private Region" 셀의 박스가 `ic-hybrid_n_private_cloud-nhn_private_cloud-box` 이고,
      Private Station 셀은 `ic-hybrid_n_private_cloud-nhn_cloud_private_station-box` 로 따로 있다.
      이 결론을 반영해 `docs/scheme.md` § 주석(117행)과 388행 항목을 갱신할지 결정 필요
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
| `ic-contact-center-online-contact` | 1 | Contiple 로 개명 (Figma 대조로 동일 확인) |
