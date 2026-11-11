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
| `dist/` | 생성된 draw.io 라이브러리 25개 |
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

draw.io 배포 링크는 **하나**입니다. 팔레트 25개를 한 링크에 담습니다.

```
python tools/make_links.py                  # GitHub Pages 기준, 약 1,500자 (권장)
python tools/make_links.py --host raw --branch <브랜치>   # raw, 약 2,150자
```

`clibs` 링크는 draw.io 가 XML 을 직접 읽어가는 방식이라 해당 브랜치가 origin 에 푸시되어 있어야 하고,
호스트가 `Access-Control-Allow-Origin: *` 을 보내야 합니다. GitHub raw 와 GitHub Pages 모두 보냅니다.

링크에는 라이브러리 1개마다 URL 이 하나씩 들어갑니다. 그래서 `dist/` 파일명을 팔레트 번호
두 자리(`02.xml`)로 줄였습니다. 패널에 보이는 이름은 파일명이 아니라 XML 의 `title` 속성이 정합니다.

로컬에서 바로 쓰려면 draw.io 에서 `도형 > 라이브러리 열기 > 기기` 로 `dist/*.xml` 을 올리면 됩니다.

## 분류 체계

`docs/scheme.md`가 기준입니다. 카테고리·서비스 구성과 표시명은 [NHN Cloud 공식 홈페이지 서비스 목록](https://www.nhncloud.com/kr/service)을, 아이콘 유형·그룹·화살표 규칙은 [NHN Cloud Architecture Icons V2.2 PPT](https://static.toastoven.net/portal/public/resources/reference-architecture/NHN_Cloud_Architecture_Icons_2026.pptx)를 따릅니다.
