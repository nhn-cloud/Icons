# Presentation

제안서·소개 자료에서 구성도를 거들 때 쓰는 flat 아이콘입니다.
아키텍처 아이콘(02~28)과 달리 **서비스를 가리키지 않습니다.** 비용·규제·운영처럼
도형으로는 안 잡히는 개념을 장표에 얹을 때 씁니다.

## 출처

Figma `[공통] 디자인 리소스 프덥1팀 _2025~ - Copy` 파일(`nj6f8NZT7RNq6yz9wvdZpi`)의
`flat icon` 섹션(`2:5185`)입니다. 고유 아이콘 146종 중에서 골랐습니다.

고른 기준은 `NHN소개` 영업 장표(74쪽) 본문입니다. 장표를 관통하는 축이
보안·인증 / 비용 절감 / 클라우드 전환 / GPU·AI 데이터센터 / 24시간 운영지원 /
모니터링 / 규제 준수라서, 그 축에 쓰이는 것만 40개로 추렸습니다.

가져오기는 `tools/figma_flat_import.py` 입니다. 원본이 24x24~64x64 로 제각각이라
60x60 캔버스에 48px 상자로 맞춰 가운데 정렬합니다.

## 반영된 아이콘

| 슬러그 | Figma 노드 | 원본 이름 |
| --- | --- | --- |
| `ic-presentation-lock` | `2:5194` | 잠금(원) |
| `ic-presentation-shield-check` | `2:5444` | 방패(확인) |
| `ic-presentation-shield-ids` | `2:5458` | 방패(IDS) |
| `ic-presentation-shield-waf` | `2:5463` | 방패(WAF) |
| `ic-presentation-shield-ddos` | `2:5468` | 방패(DDos) |
| `ic-presentation-encryption-key` | `2:5664` | 암호키(원) |
| `ic-presentation-certification` | `2:5248` | 인증1 |
| `ic-presentation-attacker` | `2:15135` | 공격자 |
| `ic-presentation-fingerprint` | `2:15238` | 지문 |
| `ic-presentation-cloud` | `2:5415` | 클라우드 |
| `ic-presentation-server` | `2:5324` | 서버4 |
| `ic-presentation-internet` | `2:5298` | 인터넷 |

`Internet`·`Server` 는 02-general 에 같은 이름이 있어 `Web Globe`·`Server Rack` 으로
표시합니다. 팔레트를 나눠 적는 `팔레트/이름` 표기를 늘리지 않으려는 것입니다.

## 아직 안 들어온 28개

40개를 고르고 12개만 가져왔습니다. Figma MCP 월 한도(Starter·View 좌석 20회/월)를
소진해 나머지를 못 내려받았습니다. SVG 가 생기면 아래 한 줄로 끝납니다.

    python tools/figma_flat_import.py <svg디렉터리> icons/29-presentation
    python tools/make_drawio_libs.py && python tools/make_config_link.py --write-index

카탈로그 Subpage(`2:5186`) 를 통째로 내보내면 아래 14개가 한 번에 해결됩니다.

| 슬러그(예정) | 노드 | 원본 이름 | 장표에서의 쓰임 |
| --- | --- | --- | --- |
| `-global` | `2:5236` | 글로벌/인터넷 | 리전·글로벌 |
| `-link` | `2:5681` | 링크 | 연계·전용선 |
| `-24h` | `2:5269` | 24h | 24시간 운영센터 |
| `-cost` | `2:5551` | 달러(원) | 인프라 비용 |
| `-discount` | `2:5281` | 할인(%) | 비용 절감률 |
| `-scale-up` | `2:5590` | 상승(원) | 성능 향상·확장 |
| `-time` | `2:5544` | 시간(원) | 응답시간·소요기간 |
| `-data` | `2:5222` | 데이터2 | 데이터 |
| `-sql` | `2:5397` | SQL | DB |
| `-package` | `2:5377` | 박스 | 컨테이너·패키지 |
| `-analysis` | `2:5509` | 돋보기(원) | 진단·분석 |
| `-compliance` | `2:5261` | 법봉 | 금융 가이드라인·규제 |
| `-check` | `2:5532` | 확인(원) | 요건 충족 |
| `-settings` | `2:5502` | 설정(원) | 구성·운영 |

나머지 13개는 큰 Subpage(`2:5689`) 안에 흩어져 있어 개별로 내보내야 합니다.

| 슬러그(예정) | 노드 | 원본 이름 | 장표에서의 쓰임 |
| --- | --- | --- | --- |
| `-migration` | `2:15068` | 업데이트/전환 | 클라우드 전환 |
| `-data-center` | `2:13912` | 지붕 | 데이터센터 |
| `-dashboard` | `2:7324` | 모니터+원그래프 | 통합 대시보드 |
| `-bar-chart` | `2:7601` | 막대 그래프 | 수치 비교 |
| `-line-chart` | `2:7877` | 선그래프 | 추이 |
| `-health-check` | `2:15492` | 심박수 | 헬스체크·가용률 |
| `-warning` | `2:8196` | 경고 | 장애 알림 |
| `-recovery` | `2:8427` | 복구 | 백업·복구 |
| `-code` | `2:8572` | 코드 | 개발·CI/CD |
| `-api` | `2:12300` | API | API Gateway 연계 |
| `-guide` | `2:15263` | 책 | 보안백서·가이드 |
| `-users` | `2:13030` | 사용자(다수) | 고객사·기관 |
| `-support-chat` | `2:7145` | 대화 | 기술지원 |

## 쓰지 않기로 한 것

| 원본 | 노드 | 사유 |
| --- | --- | --- |
| 감시 | `2:8082` | 눈 흰자가 `fill="white"` 라 흰 배경에서 안 보임. 컬러 배경 전용 |
| SG, ES | `2:5654`, `2:5659` | 글자가 별도 레이어라 `svgAssets` 가 원만 내려줌. 그룹 박스는 05-groups 에 이미 있음 |
| WAF, VPN | `2:15648`, `2:13162` | 방패 위에 얹는 흰 글자 레이어. 단독 아이콘이 아님 |

## 가져올 때 주의

`download_assets` 의 두 산출물이 서로 다릅니다.

- `svgAssets` — 깨끗하지만 **텍스트 레이어를 뺍니다.**
- `export` — 글자를 패스로 담지만 조상 배경(페이지 프레임, Subpage 배경, 원형 장식)이 딸려 옵니다.

글자가 그림의 일부인 아이콘(`24h`, `SQL`, `방패(IDS/WAF/DDos)`)은 `export` 를 받아
`figma_flat_import.py` 로 정리해야 합니다. 나머지는 `svgAssets` 가 편합니다.
`서버4`처럼 `svgAssets` 가 여러 조각으로 쪼개져 오는 것도 `export` 쪽을 씁니다.
