# draw.io 도형 라이브러리

이 리포지토리의 SVG 아이콘을 draw.io(diagrams.net) **도형 라이브러리(Shape Library)** 로 변환한 파일입니다.
SVG가 파일 안에 base64로 임베드되어 있어 네트워크 연결 없이 동작하고, PNG/PDF로 내보낼 때도 아이콘이 그대로 렌더링됩니다.

## 파일

| 파일 | 아이콘 수 | 내용 |
| --- | --- | --- |
| `NHNCloud-Services-color.xml` | 133 | 서비스 아이콘 (컬러) |
| `NHNCloud-Resources-color.xml` | 34 | 리소스 아이콘 (컬러) |
| `NHNCloud-General-color.xml` | 30 | 일반 아이콘 (컬러) |
| `NHNCloud-BoxType-color.xml` | 147 | 박스(그룹) 아이콘 (컬러) |
| `black/NHNCloud-*-black.xml` | 200 | 위와 동일한 구성의 블랙 버전 |

`sample-3tier-architecture.drawio` — 아이콘 사용법을 보여 주는 3계층 웹 서비스 예시 구성도.

## 불러오기

### 방법 1. 파일로 불러오기 (권장)

draw.io 웹/데스크톱 모두 동일합니다.

1. **파일 > 라이브러리 열기…** (File > Open Library…)
2. `drawio/NHNCloud-Services-color.xml` 선택
3. 왼쪽 도형 패널 위쪽에 `NHNCloud-Services-color` 섹션이 추가됩니다

필요한 라이브러리를 여러 개 열어 두면 섹션이 각각 쌓입니다. 한 번 열어 두면 브라우저/앱에 기억되므로 다음에 다시 열 필요가 없습니다.

### 방법 2. GitHub URL로 불러오기

아래 주소로 접속하면 draw.io가 열리면서 라이브러리가 자동으로 추가됩니다. 북마크해 두고 쓰면 편합니다.

**서비스 아이콘만**

```
https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fnhn-cloud%2FIcons%2Fmain%2Fdrawio%2FNHNCloud-Services-color.xml
```

**4종 전체 (서비스 + 리소스 + 일반 + 박스)**

```
https://app.diagrams.net/?clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fnhn-cloud%2FIcons%2Fmain%2Fdrawio%2FNHNCloud-Services-color.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fnhn-cloud%2FIcons%2Fmain%2Fdrawio%2FNHNCloud-Resources-color.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fnhn-cloud%2FIcons%2Fmain%2Fdrawio%2FNHNCloud-General-color.xml;Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fnhn-cloud%2FIcons%2Fmain%2Fdrawio%2FNHNCloud-BoxType-color.xml
```

`clibs` 파라미터는 `U` + URL 인코딩한 raw 주소 형식이며, 여러 개는 `;` 로 구분합니다.
블랙 버전은 경로의 `drawio%2F` 를 `drawio%2Fblack%2F` 로, 파일명을 `-black.xml` 로 바꾸면 됩니다.

## 사용법

* **검색** — 도형 패널 상단 검색창에 `Load Balancer`, `RDS`, `VPC` 처럼 입력하면 바로 찾을 수 있습니다.
  각 항목에는 표시 이름 외에 **검색용 태그**가 붙어 있어 카테고리(`network`, `storage`), 약어(`dsr`, `nks`, `ncr`),
  파일명(`ic-network-vpc`) 중 아무것으로나 찾을 수 있습니다. 아이콘 위에 마우스를 올리면 이름이 표시됩니다.
* **레이블** — 아이콘을 캔버스에 끌어다 놓으면 아이콘 아래에 이름이 함께 붙습니다. 더블클릭해서 수정하세요.
* **박스(그룹) 아이콘** — `BoxType` 라이브러리 항목은 컨테이너로 만들어져 있습니다. VPC·서브넷처럼 다른 아이콘을 안에 끌어다 넣으면 함께 움직입니다. 썸네일은 모두 비슷해 보이므로 검색으로 찾는 것이 빠릅니다.
* **색상 변경** — 아이콘은 이미지라 draw.io에서 색을 바꿀 수 없습니다. 블랙 버전이 필요하면 `black/` 라이브러리를 사용하세요.

## 라이브러리 재생성

원본 아이콘이 갱신되면 리포지토리 루트에서 **순서대로** 실행합니다.

```bash
python scripts/build_manifest.py        # files/ + 카탈로그 -> icons.json
python drawio/make_drawio_libs.py . drawio
```

이름과 검색 태그는 `icons.json` 한 곳에서만 옵니다. 생성기는 카탈로그 md 를 다시 읽지
않으므로 출처가 둘로 갈릴 일이 없습니다. 카탈로그 표에 없는 아이콘은 파일명에서 이름을
유추하고 `icons.json` 에 `needs_review: true` 로 표시됩니다.
