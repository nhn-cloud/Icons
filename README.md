<h1 align="center">NHN Cloud 아이콘 라이브러리</h1>
<p align="center">
NHN Cloud 아키텍처 다이어그램을 그리는 데 필요한 서비스 아이콘, 리소스 아이콘, 일반 아이콘을 제공합니다.
원본은 컬러 SVG 로만 관리합니다.
</p>

> [!Note]\
> 이 브랜치(`alpha`)는 `docs/scheme.md`의 분류 체계에 맞춰 저장소를 재편하는 중입니다.
> 디렉터리 번호가 draw.io 팔레트 번호와 같습니다. 구 경로(`files/…`)는 더 이상 쓰지 않습니다.

## 디렉터리

| 경로 | 내용 |
| --- | --- |
| `icons/` | 원본 SVG. 팔레트 28개와 1:1 |
| `taxonomy.yaml` | 분류·표시명의 단일 원천. 라이브러리는 여기서 생성 |
| `dist/` | 생성된 draw.io 라이브러리 28개 |
| `tools/` | 생성·검증 스크립트 |
| `docs/` | 분류 체계 문서와 샘플 구성도 |
| `assets/pptx/` | 아키텍처 아이콘 PPT |

### 팔레트 구성

팔레트는 **`main` 브랜치의 아이콘 유형 체계**를 따릅니다. 사내 배포 라이브러리
(`NHNCloud-*.xml`)와 같은 구성입니다.

| # | 팔레트 | 담긴 것 | 개수 | 배포본 |
| --- | --- | --- | --- | --- |
| 01 | Box Type | 그룹 컨테이너 + 서비스마다의 박스 | 134 | 154 |
| 02 | Services | 서비스 아이콘 | 119 | 136 |
| 03 | Resources | 서비스에 딸린 리소스 아이콘 | 35 | 34 |
| 04 | General | 일반 아이콘 (`main` 의 general_icons 30종) | 30 | 30 ✓ |
| 05 | Arrows | 연결선 스타일 (4색 x 6변형) | 24 | 24 ✓ |
| 06 | Annotations | 단계·문제·개선 번호, 말풍선·메모·제목·범례 | 22 | 22 ✓ |
| 07 | Extra | 계정·장비·문서 등 + 카테고리 아이콘 | 68 | 71 |
| 08 | Templates | 예시 구성도 (끌어다 놓으면 통째로 들어감) | 10 | 10 ✓ |
| 09 | Presentation | 제안서 보조용 flat 아이콘 | 12 | — |
| 10 | Retired | 홈페이지에서 빠지거나 개명된 아이콘 | 15 | — |

`Arrows` · `Annotations` · `Templates` 는 배포 라이브러리와 **내용이 한 글자까지 같습니다**
(엔트리의 이름·크기·태그·도형 XML 전부 대조 확인). 아이콘이 아니라 draw.io 도형이라
SVG 에서 만들 수 없어, 배포본에서 풀어 `icons/annotations` · `icons/templates` 에
XML 로 두고 `kind: raw` 로 다시 압축합니다.

### icons/ 구성

`icons/` 는 **자산 원본 트리**이고 팔레트와 1:1 이 아닙니다. 서비스 카테고리로 묶여
있어 홈페이지 메뉴와 대조하기 쉽고, 어느 파일이 어느 팔레트에 들어가는지는
`taxonomy.yaml` 각 항목의 `src` 가 정합니다. 카테고리 아이콘처럼 **한 파일이 두
팔레트에 들어가는 경우**(General 과 Extra)가 있어 디렉터리로는 표현할 수 없습니다.

```
01-arrows        엣지 스타일 24종 (SVG 없음, styles.yaml)   -> Arrows
annotations      주석 도형 22종 (SVG 없음, mxGraphModel XML)  -> Annotations
templates        예시 구성도 10종 (SVG 없음, mxGraphModel XML) -> Templates
02-general       일반 리소스          03-industry   산업·개념   -> General · Extra
04-identity      계정·역할                                      -> Extra
05-groups        그룹 컨테이너                                  -> Box Type
06-architecture  구성도 명세 4건 (생성기용 YAML. 팔레트에는 안 들어감)
07-compute … 28-governance-audit      서비스 카테고리 22개       -> Services · Resources
                 (각 디렉터리의 category/ 는 Extra 와 General 양쪽으로)
29-presentation  제안서·구성도 보조용 flat 아이콘 (Figma 출처)   -> Presentation
30-retired       홈페이지에서 빠지거나 개명된 아이콘             -> Retired
```

각 카테고리 디렉터리는 `category/`, `services/`, `resources/`로 나뉩니다. 리소스는 해당되는 8개 카테고리에만 있습니다.

## 파일명 규칙

| 유형 | 규칙 | 예 |
| --- | --- | --- |
| 카테고리 | `ic-<category>` | `ic-database` |
| 서비스 | `ic-<category>-<service>` | `ic-database-rds-for-mysql` |
| 리소스 | `ic-<category>-<service>-<resource>` | `ic-database-rds-for-mysql-rds-instance` |
| 그룹 컨테이너 | `grp-<name>` | `grp-subnet` |
| 서비스 박스 | `box-<category>-<service>` | `box-container-nks` |

전부 소문자 kebab-case입니다. 파일명은 슬러그일 뿐이고, 표시명은 `taxonomy.yaml`에만 둡니다.

## 파일 형식

**컬러 SVG 한 가지만** 관리합니다. PNG 와 블랙 버전은 저장소에 두지 않습니다.

PNG 가 필요하면 draw.io 에서 바로 얻습니다.

- `File > Export as > PNG` — 확대율·DPI·여백·투명 배경·선택 영역 지정 가능
- 선택 후 우클릭 `Copy as Image` (`Ctrl+Alt+X`) — PPT·Word 에 바로 붙여넣기

> [!Warning]\
> `Copy as Image` 로 붙여넣으면 배경이 검게 나오는 사례가 있습니다. 문서 배경을 흰색으로 두거나 내보내기에서 투명 배경을 끄세요.

## 라이브러리 링크

draw.io 배포 링크는 **하나**입니다: <https://nhn-cloud.github.io/Icons/>

이 페이지는 공식 draw.io(app.diagrams.net)의 **설정 링크**(`#_CONFIG_`)로 팔레트를 등록합니다.

| 조건 | 충족 방법 |
| --- | --- |
| 단일 URL | `index.html` 배포 페이지 1개 |
| 어떤 아이콘이 있는지 훑어보기 | `gallery.html` 카탈로그 — 설정이 끝난 사람은 배포 주소가 여기로 들어감 |
| 다시 열어도 팔레트 접힘 | 설정 `expandLibraries: false` (URL 파라미터로는 줄 수 없는 값) |
| 내보내기·클라우드 저장 유지 | 공식 app.diagrams.net 을 그대로 사용 |
| GitHub 원본 | 라이브러리는 `dist/*.xml` 을 raw URL 로 직접 읽음 |
| '그 외 도형' 목록 | 설정 `libraries` 로 'NHN Cloud' 항목 등록 (AWS 처럼 체크 하나로 켜고 끔) |
| 도형 검색 | `libraries` 로 등록한 아이콘은 검색 색인에 들어감 |
| 팔레트 이름 표시 | 설정 `sidebarTitles: true` — 팔레트를 펼치면 도형 아래에 이름이 보임 |
| 탭 제목 고정 | `?title=NHN%20Cloud%20Icons` — 열린 파일 이름 대신 이 제목을 씀 |

```
python tools/make_config_link.py --write-index                 # index.html 생성 (draft 브랜치)
python tools/make_config_link.py --write-index --branch main   # 브랜치 지정
python tools/make_config_link.py                               # 설정 JSON 과 링크만 출력
python tools/make_gallery.py                                   # gallery.html 생성
```

### 아이콘 카탈로그 (`gallery.html`)

팔레트를 설치해도 **어떤 아이콘이 있는지는 안 보입니다.** draw.io 의 도형 검색은
이름을 이미 알 때만 쓸모가 있어서, Figma 의 `flat icon` 페이지처럼 전부 펼쳐 놓은
화면을 따로 둡니다. 도형 1개가 타일 1개이고 셋을 할 수 있습니다.

타일 하나만 쓸 때는 타일 안의 버튼을 씁니다.

| 동작 | 결과 | 언제 쓰나 |
| --- | --- | --- |
| 열기 | draw.io 새 탭에 그 도형 하나를 올린 새 그림이 열림 | 아이콘 하나로 그림을 시작할 때 |
| 복사 | `mxGraphModel` XML 을 클립보드에 넣음 | **편집 중인 그림에 Ctrl+V** — 실제로 제일 많이 씀 |
| SVG | 원본 SVG 내려받기 | PPT·문서에 넣을 때 |

**타일을 누르면 화면 아래 담는 자리에 쌓입니다.** 무엇을 담았는지 아이콘으로 바로 보이고,
담긴 것을 누르면 빠집니다. 다 고른 뒤 한꺼번에 처리합니다.

| 동작 | 결과 |
| --- | --- |
| draw.io 에서 열기 | 고른 도형을 격자로 배치한 그림 하나를 새 탭에 엶 |
| 라이브러리(.xml) 받기 | 고른 것만 담은 `mxlibrary` 파일을 내려받음. draw.io 의 **파일 > 라이브러리 열기 > 디바이스** 로 열면 라이브러리 편집 창이 뜨고 왼쪽 패널에도 붙음 |
| 모두 복사 | 고른 도형 전부를 한 번에 클립보드로 |

클릭이 열리는 원리는 `drawio_open.py` 와 같습니다. draw.io 는 URL 조각 `#R<데이터>` 에
담긴 도형을 그대로 읽고, 조각은 서버로 가지 않아 사내 프록시를 타지 않습니다.
SVG 가 base64 로 박혀 있어 **팔레트를 설치하지 않은 브라우저에서도 그려집니다.**
`dist/` 를 고치면 `make_gallery.py` 를 다시 돌려야 카탈로그가 따라옵니다.

머리 배너는 `images/nhn-cloud-header.png` 입니다. 파일을 바꾸면 그대로 바뀌고,
지우면 배너 없이 생성됩니다. 원본이 3840x248(15.5:1)이라 폭에 맞추면 넓은 화면에서
너무 두꺼워지므로 높이를 `clamp(52px, 6.5vw, 92px)` 로 묶고 로고가 있는 오른쪽을
남기며 잘라 냅니다.

> [!Note]> **라이브러리를 URL 로 띄우는 방법은 없습니다.** `#R` 에 `<mxlibrary>` 를 넣으면
> draw.io 가 "다이어그램 파일이 아닙니다" 로 거부하고, `?clibs=U<data: URI>` 도 붙지
> 않습니다. 라이브러리로 쓰려면 파일을 받아 draw.io 에서 여는 수밖에 없습니다.
>
> 라이브러리 항목의 `xml` 은 **반드시 압축**해야 합니다. `Graph.decompress` 가 평문을
> 거부합니다(그림 쪽 `#R` 은 평문도 받습니다). 카탈로그는 `CompressionStream('deflate-raw')`
> 로 그 자리에서 압축합니다. 이 API 가 없는 낡은 브라우저에서는 라이브러리 받기만
> 막히고 나머지는 그대로 동작합니다.

### 사용자 동작

- **처음 열 때** draw.io 가 설정 적용 여부를 **두 번** 묻습니다. 두 번 모두 확인을 누르면 새로고침되고 팔레트 28개가 접힌 상태로 붙습니다.
- 팔레트는 **+ 그 외 도형** 창 맨 위 'NHN Cloud' 항목으로 켜고 끕니다. 내장 팔레트(AWS 등)도 같은 창에서 켜고 끕니다.
- 검색창에 아이콘 이름(예: `Gamebase`, `Auto Scale`)을 넣으면 NHN Cloud 아이콘도 검색됩니다. `Instance`, `Load Balancer` 처럼 흔한 단어는 draw.io 내장 도형·타사 클라우드 아이콘이 먼저 나옵니다.
- **NHN Cloud 아이콘만 보려면 검색어 앞에 `nhn` 을 붙이세요.** 예: `nhn load balancer`, `nhn instance`. 모든 NHN Cloud 아이콘에 `nhn` 검색 태그가 들어 있습니다.
- **다음부터는** 같은 주소를 열면 확인 없이 바로 아이콘 카탈로그로 들어갑니다. 아무 파라미터 없는 app.diagrams.net 을 열어도 팔레트가 그대로 있습니다.
- 팔레트가 보이지 않으면 `https://nhn-cloud.github.io/Icons/?setup` 으로 다시 설정합니다.

### 동작 원리

- 배포 페이지는 적용한 설정 `version` 을 자기 도메인 localStorage 에 기억해, 처음이거나 version 이 바뀐 경우에만 설정 링크로 보냅니다.
- `version` 은 `dist/` 내용의 해시입니다. 팔레트를 고치고 `index.html` 을 다시 생성하면 version 이 바뀌어, 사용자는 다음 방문 때 한 번만 다시 확인을 누르면 됩니다.
- 설정은 `{"merge": {...}}` 형식이라 사용자가 따로 가진 draw.io 설정은 지우지 않습니다. 단, version 이 바뀌면 draw.io 의 패널 구성(열어 둔 팔레트, 최근 색 등)은 초기화됩니다.
- 라이브러리 호스트는 `raw.githubusercontent.com` 입니다. draw.io 가 프록시 없이 직접 읽는 호스트이기 때문입니다.

> [!Note]\
> 라이브러리를 읽지 못하면(네트워크 차단, 브랜치 미푸시 등) 해당 팔레트에 오류가 표시됩니다. 네트워크가 복구되면 새로고침으로 다시 읽습니다.

### 이전 방식 (참고)

`clibs` 링크는 설정 없이 바로 열리지만 팔레트가 매번 펼쳐진 채로 열립니다.
임베드 방식은 팔레트를 접을 수 있지만 클라우드 저장을 쓸 수 없습니다.
둘 다 쓰지 않기로 했고, 생성기와 시험판은 2026-11-16 에 지웠습니다(git 히스토리에 남아 있습니다).

## 분류 체계

`docs/scheme.md`가 기준입니다. 카테고리·서비스 구성과 표시명은 [NHN Cloud 공식 홈페이지 서비스 목록](https://www.nhncloud.com/kr/service)을, 아이콘 유형·그룹·화살표 규칙은 [NHN Cloud Architecture Icons V2.2 PPT](https://static.toastoven.net/portal/public/resources/reference-architecture/NHN_Cloud_Architecture_Icons_2026.pptx)를 따릅니다.
