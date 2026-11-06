<h1 align="center">NHN Cloud 아이콘 라이브러리</h1>
<p align="center">
NHN Cloud 아키텍처 다이어그램을 그리는데 필요한 NHN Cloud 서비스 아이콘, 리소스 아이콘, 및 일반 아이콘을 제공합니다. 
아이콘은 2가지 형식(PNG와 SVG)와 2가지 버전(컬러와 블랙)으로 제공됩니다.
</p>

> [!Note]\
> SVG는 파일 크기가 더 작고 모든 최신 웹 브라우저에서 지원되며 인쇄 및 고해상도 화면에 적합한 형식입니다.

## 아이콘 유형

크게 서비스 아이콘, 리소스 아이콘, 일반 아이콘으로 구분됩니다. 리소스 아이콘은 서비스에 종속된 하위의 리소스를 지칭하며 일반 아이콘은 서비스에 종속되지않고 단독으로 사용 가능한 아이콘입니다.

* [서비스 아이콘](service_icons/service_icons.md)
* [리소스 아이콘](service_icons/resource_icons.md)
* [일반 아이콘](general_icons/general_icons.md)
* [박스 형태 아이콘](box_type/box_type.md)
> 박스 형태 아이콘은 아키텍처 다이어그램을 그릴 때 필요한 그룹을 그릴 때 사용합니다.

## 아이콘 명부 (icons.json)

리포지토리 루트의 `icons.json` 은 모든 아이콘을 한 곳에 모은 단일 명부입니다. 아이콘마다
식별자, 표시 이름, 분류, 검색 태그, color/black x PNG/SVG 파일 경로를 담고 있으며
`files/` 트리와 카탈로그 표에서 생성됩니다.

```bash
python scripts/build_manifest.py
```

카탈로그 표에 이름이 없어 파일명에서 유추한 항목과, 카탈로그 이름이 파일명과 어긋나는
항목은 `needs_review: true` 로 표시됩니다.

## 아키텍처 다이어그램

제공되는 아이콘을 활용하여 아키텍처 다이어그램을 그릴 수 있습니다. 다이어그램을 그리는 데 필요한 그룹, 선과 같은 요소는 아래의 PPT 파일을 참고하시기 바랍니다.
* [NHN Cloud Architecture Icons](files/pptx)

  
