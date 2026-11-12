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
| `dist/` | 생성된 draw.io 라이브러리 26개 |
| `tools/` | 생성·검증 스크립트 |
| `docs/` | 분류 체계 문서와 샘플 구성도 |
| `assets/pptx/` | 아키텍처 아이콘 PPT |

### icons/ 구성

```
01-arrows        엣지 스타일 (SVG 없음)
02-general       일반 리소스          03-industry   산업·개념
04-identity      계정·역할            05-groups     그룹 컨테이너 + 서비스 박스
06-compute … 27-governance-audit      서비스 카테고리 22개 (홈페이지 메뉴 순)
28-retired       홈페이지에서 빠지거나 개명된 아이콘
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
| 다시 열어도 팔레트 접힘 | 설정 `expandLibraries: false` (URL 파라미터로는 줄 수 없는 값) |
| 내보내기·클라우드 저장 유지 | 공식 app.diagrams.net 을 그대로 사용 |
| GitHub 원본 | 라이브러리는 `dist/*.xml` 을 raw URL 로 직접 읽음 |
| '그 외 도형' 목록 | 설정 `libraries` 로 'NHN Cloud' 항목 등록 (AWS 처럼 체크 하나로 켜고 끔) |
| 도형 검색 | `libraries` 로 등록한 아이콘은 검색 색인에 들어감 |

```
python tools/make_config_link.py --write-index                 # index.html 생성 (main 브랜치)
python tools/make_config_link.py --write-index --branch draft  # 브랜치 지정
python tools/make_config_link.py                               # 설정 JSON 과 링크만 출력
```

### 사용자 동작

- **처음 열 때** draw.io 가 설정 적용 여부를 **두 번** 묻습니다. 두 번 모두 확인을 누르면 새로고침되고 팔레트 26개가 접힌 상태로 붙습니다.
- 팔레트는 **+ 그 외 도형** 창 맨 위 'NHN Cloud' 항목으로 켜고 끕니다. 내장 팔레트(AWS 등)도 같은 창에서 켜고 끕니다.
- 검색창에 아이콘 이름(예: `Gamebase`, `Auto Scale`)을 넣으면 NHN Cloud 아이콘도 검색됩니다. `Instance`, `Load Balancer` 처럼 흔한 단어는 draw.io 내장 도형·타사 클라우드 아이콘이 먼저 나옵니다.
- **NHN Cloud 아이콘만 보려면 검색어 앞에 `nhn` 을 붙이세요.** 예: `nhn load balancer`, `nhn instance`. 모든 NHN Cloud 아이콘에 `nhn` 검색 태그가 들어 있습니다.
- **다음부터는** 같은 주소를 열면 확인 없이 바로 draw.io 로 이동합니다. 아무 파라미터 없는 app.diagrams.net 을 열어도 팔레트가 그대로 있습니다.
- 팔레트가 보이지 않으면 `https://nhn-cloud.github.io/Icons/?setup` 으로 다시 설정합니다.

### 동작 원리

- 배포 페이지는 적용한 설정 `version` 을 자기 도메인 localStorage 에 기억해, 처음이거나 version 이 바뀐 경우에만 설정 링크로 보냅니다.
- `version` 은 `dist/` 내용의 해시입니다. 팔레트를 고치고 `index.html` 을 다시 생성하면 version 이 바뀌어, 사용자는 다음 방문 때 한 번만 다시 확인을 누르면 됩니다.
- 설정은 `{"merge": {...}}` 형식이라 사용자가 따로 가진 draw.io 설정은 지우지 않습니다. 단, version 이 바뀌면 draw.io 의 패널 구성(열어 둔 팔레트, 최근 색 등)은 초기화됩니다.
- 라이브러리 호스트는 `raw.githubusercontent.com` 입니다. draw.io 가 프록시 없이 직접 읽는 호스트이기 때문입니다.

> [!Note]\
> 라이브러리를 읽지 못하면(네트워크 차단, 브랜치 미푸시 등) 해당 팔레트에 오류가 표시됩니다. 네트워크가 복구되면 새로고침으로 다시 읽습니다.

### 이전 방식 (참고)

`tools/make_links.py` 의 `clibs` 링크는 설정 없이 바로 열리지만 팔레트가 매번 펼쳐진 채로 열립니다.
`embed/` 는 팔레트를 접을 수 있지만 클라우드 저장을 쓸 수 없습니다.

## 분류 체계

`docs/scheme.md`가 기준입니다. 카테고리·서비스 구성과 표시명은 [NHN Cloud 공식 홈페이지 서비스 목록](https://www.nhncloud.com/kr/service)을, 아이콘 유형·그룹·화살표 규칙은 [NHN Cloud Architecture Icons V2.2 PPT](https://static.toastoven.net/portal/public/resources/reference-architecture/NHN_Cloud_Architecture_Icons_2026.pptx)를 따릅니다.
