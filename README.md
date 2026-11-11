<h1 align="center">NHN Cloud 아이콘 라이브러리</h1>
<p align="center">
NHN Cloud 아키텍처 다이어그램을 그리는 데 필요한 서비스 아이콘, 리소스 아이콘, 일반 아이콘을 제공합니다.
원본은 SVG 컬러·블랙 두 버전으로 관리합니다.
</p>

> [!Note]\
> 이 브랜치(`alpha`)는 `docs/scheme.md`의 분류 체계에 맞춰 저장소를 재편하는 중입니다.
> 디렉터리 번호가 draw.io 팔레트 번호와 같습니다. 구 경로(`files/…`)는 더 이상 쓰지 않습니다.

## 디렉터리

| 경로 | 내용 |
| --- | --- |
| `icons/` | 원본 SVG. 팔레트 28개와 1:1 |
| `taxonomy.yaml` | 분류·표시명의 단일 원천. 라이브러리는 여기서 생성 |
| `dist/` | 생성된 draw.io 라이브러리 (`color/`, `black/`) |
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
| 블랙 버전 | 위 이름 + `.black.svg` | `ic-database.black.svg` |

전부 소문자 kebab-case입니다. 파일명은 슬러그일 뿐이고, 표시명은 `taxonomy.yaml`에만 둡니다.

## PNG

저장소는 PNG를 보관하지 않습니다. 필요하면 draw.io에서 바로 얻습니다.

- `File > Export as > PNG` — 확대율·DPI·여백·투명 배경·선택 영역 지정 가능
- 선택 후 우클릭 `Copy as Image` (`Ctrl+Alt+X`) — PPT·Word에 바로 붙여넣기

> [!Warning]\
> `Copy as Image`로 붙여넣으면 배경이 검게 나오는 사례가 있습니다. 문서 배경을 흰색으로 두거나 내보내기에서 투명 배경을 끄세요.

## 분류 체계

`docs/scheme.md`가 기준입니다. 카테고리·서비스 구성과 표시명은 [NHN Cloud 공식 홈페이지 서비스 목록](https://www.nhncloud.com/kr/service)을, 아이콘 유형·그룹·화살표 규칙은 [NHN Cloud Architecture Icons V2.2 PPT](https://static.toastoven.net/portal/public/resources/reference-architecture/NHN_Cloud_Architecture_Icons_2026.pptx)를 따릅니다.
