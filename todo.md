# TODO

`alpha` 브랜치 재편 후 남은 작업. 기준 문서는 `docs/scheme.md`.
현황 수치는 `python tools/audit.py`로 언제든 다시 뽑을 수 있다.

**한 줄 요약**: Figma `03 Architecture icon` 페이지와 대조해 자산을 대거 확보했다.
서비스 아이콘 **117/119**, 일반 아이콘 **52개**, 산업·개념 **5개(완료)**.
**SVG 가 없는 아이콘은 2개**로 줄었다 — 둘 다 디자인팀 신규 제작 건이다. 목록은 **1-1** 에 모아 두었다.
계정·역할 7개는 Figma Identity & Governance 표에서 **9개로 확보해 팔레트까지 반영**했다(1-3).
Arrows 는 이미지가 아니라 엣지 스타일이라 따로 센다. **18종 배포까지 확인 완료**(1-4).

| 구분 | 이전 | 현재 |
| --- | --- | --- |
| 서비스 아이콘 | 113 / 119 | **117 / 119** |
| 일반 아이콘 | 16 | **52** |
| 리소스 | IPSec VPN 없음 | **확보** |
| 계정·역할 | 0 / 7 | **9개(완료)** |
| 카테고리 아이콘 | 10 / 22 | 범위에서 제외 (아래 참고) |

**카테고리 아이콘은 이번 작업 범위에서 제외한다.** Figma `03 Architecture icon` 페이지는
카테고리를 섹션 프레임과 텍스트 라벨로만 구분하고 카테고리 아이콘을 두지 않는다.
기존에 확보한 10개는 그대로 쓰고, 없는 12개는 추적하지 않는다.

---

## 1. 자산 확보

### 1-1. 아직 SVG가 없는 아이콘 — 한눈에

**남은 것은 디자인팀 신규 제작 2개뿐이다.** 계정·역할 7개는 2026-11-12 에 확보해 (나)로 옮겼다.
수치는 `python tools/audit.py` 로 언제든 다시 센다.

#### (가) 디자인팀에 신규 제작 요청 — 2개

아키텍처 아이콘이 어디에도 없다. Figma 에 서비스 전용 페이지는 있지만 그건 서비스 소개용이라
아키텍처 아이콘과 별개다.

| 서비스 | 넣을 파일 | 확인한 곳 |
| --- | --- | --- |
| Database Migration Service | `icons/10-database/services/ic-database-database-migration-service.svg` | Figma `260820 DMS` 페이지는 있으나 아키텍처 아이콘 아님 |
| NHN Cloud Foundry | `icons/18-machine-learning/services/ic-machine-learning-nhn-cloud-foundry.svg` | Figma `260731 Foundry` 페이지, 위와 같음 |

→ 이 2개를 채우면 서비스 아이콘이 **117/119 → 119/119** 가 된다.

#### (나) 확보 완료 — Identity 계정·역할 9개 (2026-11-12)

`icons/04-identity/` 를 채웠다. 아래 슬러그로 확정했고 팔레트 `dist/04.xml` 까지 생성된다.
자세한 경위는 1-3.

| 계열 | 아이콘 | 파일 이름 |
| --- | --- | --- |
| NHN Cloud 계정 | 계열 상위 | `ic-identity-nhn-cloud.svg` |
| NHN Cloud 계정 | Owner | `ic-identity-nhn-cloud-owner.svg` |
| NHN Cloud 계정 | Admin | `ic-identity-nhn-cloud-admin.svg` |
| NHN Cloud 계정 | Member | `ic-identity-nhn-cloud-member.svg` |
| NHN Cloud 계정 | Viewer | `ic-identity-nhn-cloud-viewer.svg` |
| IAM 계정 | 계열 상위 | `ic-identity-iam.svg` |
| IAM 계정 | Admin | `ic-identity-iam-admin.svg` |
| IAM 계정 | Member | `ic-identity-iam-member.svg` |
| IAM 계정 | Viewer | `ic-identity-iam-viewer.svg` |

#### (다) SVG 가 필요 없는 것 — Arrows (완료)

화살표는 **이미지 파일이 아니라 draw.io 엣지 스타일**이다. 2026-11-12 에 PPT 16쪽 값을
`icons/01-arrows/styles.yaml` 에 옮기고 `dist/01.xml` 을 만들었다. 자세한 내용은 1-4.

#### (라) 추적하지 않는 것 — 카테고리 아이콘 12종

이번 작업 범위에서 제외했다(문서 맨 위 참고). 보유한 10개는 그대로 쓴다.
없는 12개: compute, container, network, monitoring, hybrid-private-cloud, game, search,
management, bill, collaboration, contact-center, governance-audit.

#### 확보 완료 (참고)

| 항목 | 결과 |
| --- | --- |
| 일반 아이콘 | 16 → **52개** (1-2) |
| 산업·개념 | 3 → **5개** (1-6, 2026-11-12) |
| 리소스 IPSec VPN | **확보** (1-7) |
| 그룹 박스 | PPT 15쪽 **15종** 전부 (2026-11-12) |
| 화살표 | PPT 16쪽 **18종** 전부, 엣지 스타일. 배포 확인 완료 (1-4, 2026-11-12) |
| 계정·역할 | Figma Identity & Governance 표에서 **9개** (1-3, 2026-11-12) |

### 1-2. 일반 아이콘 — 확보 완료

Figma 의 `ic-General_Icons-*` 프레임 **49개를 추출**해 `icons/02-general/` 에 넣었다.
기존 16개와 합쳐 **52개**가 되었고, scheme.md 가 기대한 53개를 사실상 채웠다.

추출 경로: Figma 노드 내보내기(SVG) → `tools/figma_clean.py` 로 배경 제거 → `ic-general-<슬러그>.svg`.
브랜드 블루 `#125DE6`, 60×60 캔버스로 기존 자산과 형식이 같다.

- [ ] `ic-general-manager` 와 `ic-general-administrator` 는 **서로 다른 아이콘**으로 확인됐다(path 비교).
      둘 다 유지했으나 표시명이 겹칠 수 있어 `taxonomy.yaml` 에서 구분이 필요한지 확인

### 1-3. Identity 9개 — 확보 완료 (2026-11-12)

**앞서 '막혔다'고 적은 것은 찾은 곳이 틀렸기 때문이었다.** 계정·역할 아이콘은
`General Resources Icon/Dark Backgrounds/...` 컴포넌트가 아니라, `03 Architecture icon` 페이지
**Identity & Governance 표**(`[NHNCloud]_architecture_icon_Color` > `4597:218941`)에 있다.
60x60 노드를 그대로 받아 넣었고 보정은 하지 않았다.

- PPT V2.2 17쪽의 9개와 그림을 1:1로 대조해 **전부 같은 것을 확인**했다.
- 색은 브랜드 블루가 아니라 **`#555555` 단색**이다. PPT·Figma 양쪽이 그렇다.
- PPT 17쪽이 표시명의 근거다. Figma 표 머리글은 `Subnet`, `Internet Gateway`, `Interface` 처럼
  **다른 표에서 복사된 값**이라 역할명을 알 수 없다.

- [ ] 패널 표시명이 `NHN Cl…` 로 잘려 NHN Cloud 계열 5종이 구분되지 않는다. Arrows 와 같은 건이라 1-4 에 함께 적었다
- [ ] **Figma 에만 있는 `C` + `$` 아이콘 1개**: PPT 17쪽에 없고 Figma 쪽 이름도 역할명이 아니라
      무엇인지 확정할 수 없어 넣지 않았다. 역할명을 알면 10번째로 추가. 디자인팀 확인 필요

> Figma 에는 Billing Viewer, Log Viewer 등 **문서에 없던 역할도 있다.** 포함할지 결정 필요.

### 1-4. Arrows 18종 — 배포 확인 완료 (2026-11-12)

PPT 16쪽 연결선 도형을 XML 에서 직접 읽어 `icons/01-arrows/styles.yaml` 에 옮겼다.
`make_drawio_libs.py` 에 엣지 엔트리 생성을 넣어 `dist/01.xml`(18종)이 생성된다.

**반영 확인 (2026-11-12)**: `draft` 푸시(`9a11144`) 후 배포 주소에서 끝까지 확인했다.
GitHub Pages 가 `draft` 를 서빙하므로 사용자도 지금 바로 쓸 수 있다.

| 확인 항목 | 결과 |
| --- | --- |
| `nhn-cloud.github.io/Icons/dist/01.xml` | 200, 8,881 bytes |
| 배포 페이지 version | `nhncloud-icons-7d9674d58e` · 팔레트 27개 |
| draw.io 도형 패널 | `NHN Cloud / Arrows` 맨 위, 18종 렌더링 정상 |
| 캔버스 드롭 | 연결선으로 생성됨 (색·점선·화살촉 유지) |

기존 사용자는 version 이 바뀌어 다음 방문 때 확인 2회를 한 번 더 눌러야 한다.

**이전 표가 실물과 달랐다.** 6종이 아니라 18종이고, `#999999` 열의 제목은
"Primary Path (연한 배경용)" 이 아니라 **Secondary Path** 다.

| 항목 | 선 색 | 화살촉 | 선 종류 | 종수 |
| --- | --- | --- | --- | --- |
| Primary Path | `#555555` | 끝 / 양쪽 / 없음 | 각 실선·점선 | 6 |
| Secondary Path | `#999999` | 끝 / 양쪽 / 없음 | 각 실선·점선 | 6 |
| Success Status | `#09C72C` | 끝 / 양쪽 / 없음 | 실선만 | 3 |
| Failure Status | `#EF0F0F` | 끝 / 양쪽 / 없음 | 실선만 | 3 |

dash 패턴은 OOXML 프리셋 그대로다. `dash` = `4 3`, `sysDash` = `3 1` (선 두께 배수).

- [ ] **디자인팀 확인 1건**: Primary Path 점선(끝 화살촉) 한 줄만 PPT 에서 `sysDash` 이고
      나머지 점선은 모두 `dash` 다. 작성상 흔들림으로 보이나 실물대로 두었다. 통일할지 확인
- [ ] **표시명이 패널에서 잘린다 (Arrows·Identity 공통)**: 도형 아래 이름이 8자쯤에서 끊긴다.
      Arrows 는 같은 계열 6종이 모두 `Primary…` `Second…` 로, Identity 는 NHN Cloud 계열 5종이
      모두 `NHN Cl…` 로 보여 **이름으로 구분이 안 된다**. 모양과 마우스오버로는 구분된다.
      변별 부분을 앞에 두면(`점선 Primary Path`, `Owner · NHN Cloud 계정`) 잘려도 구분되지만
      PPT 표기에서 벗어난다. 두 팔레트를 같은 규칙으로 정해야 한다. 결정 필요

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

### 1-6. 산업·개념 2개 — 확보 완료 (2026-11-12)

**5개 전부 확보했다** (Finance, IoT, Machine Learning, Manufacturing, Medical & Healthcare).
scheme.md 179행이 기대한 구성과 같다.

근거는 Figma `03 Architecture icon` 페이지의 **`[NHNCloud]_architecture_icon_Black` 변형**이다.
이 변형 안에 산업·개념 5칸이 한 줄로 나란히 있다(Medical & Healthcare, Manufacturing,
Finance, Machine Learning, IoT). Color 변형에는 이 줄이 없다.

| 셀 | Figma 인스턴스 | 쓴 파일 |
| --- | --- | --- |
| Finance | `ic-dooray_erp-finance-black` (`4938:66008`) | `icons/03-industry/ic-industry-finance.svg` |
| Machine Learning | `ic-machine_learning-black` (`4938:66013`) | `icons/03-industry/ic-industry-machine-learning.svg` |

**Black 변형이지만 그대로 쓴다.** 산업·개념 아이콘은 원래 `#222222` 단색이다. 기존 3개
(IoT, Manufacturing, Medical & Healthcare)도 모두 `#222222` 라 색이 어긋나지 않는다.
Identity 7종의 'Dark Backgrounds 변형이라 못 쓴다'(1-3)와는 다른 사안이다.

- **Finance 아트워크는 Dooray! ERP 재무 아이콘과 같은 그림이다.** Figma 에서 내보낸
  `ic-dooray_erp-finance-black` 의 path 4개가 `icons/28-retired/ic-collaboration-dooray-erp-finance.svg`
  와 완전히 일치했다. Figma 가 Finance 칸에 그 아이콘을 쓰고 있으므로 같은 그림을 복사해 넣었다.
  파일 2개가 내용이 같은 것은 의도한 것이다(Retired 슬롯 1개, 산업·개념 슬롯 1개)
- **Machine Learning 은 `18-machine-learning/category/ic-machine-learning.svg` 를 복사했다.**
  카테고리 아이콘으로도 계속 쓴다

- [ ] Machine Learning 은 Figma 내보내기와 path 대조를 하지 못했다(Figma MCP 호출 한도).
      이름 규칙(`ic-machine_learning-black` ↔ `ic-machine-learning`)과 색(`#222222`)만 맞춰
      기존 저장소 파일을 복사했다. 한도가 풀리면 `4938:66013` 을 내보내 대조할 것

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
  - [ ] **재확인 필요 (2026-11-12)**: Groups 팔레트를 PPT 15쪽 그룹 박스 15종으로 교체했다.
        서비스 박스 8종을 뺐고, 모서리 아이콘이 없는 4종(Security Groups, Availability Zone,
        Generic Group 2종)을 넣었다. 위 19개 기준 체크는 이 교체 이전 것이다
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
- [x] 저장소 `assets/pptx/` 사본을 포털 최신판(2026.4.8, 58쪽)으로 교체 (2026-11-12). `NHN_Cloud_Architecture_Icons_20260129.pptx`(57쪽) 삭제, `NHN_Cloud_Architecture_Icons_2026.pptx` 추가
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
