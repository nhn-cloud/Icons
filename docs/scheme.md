# NHN Cloud 아키텍처 아이콘 draw.io 분류 체계

Nov 10, 2026 · @NHN Cloud\_박정현

## 개요

NHN Cloud 아이콘을 AWS draw.io 라이브러리처럼 **공통 팔레트 5개 + 서비스 카테고리 팔레트 22개**로 재편하고, 각 카테고리 안에서 서비스 아이콘(64px) 다음에 리소스 아이콘(48px)을 두는 체계를 제안합니다. 지금 저장소의 draw.io 라이브러리는 아이콘 유형별 4개 파일(서비스 133, 리소스 34, 일반 30, 박스 149)로만 나뉘어 있어서, 카테고리로 찾을 수 없고 그룹 박스가 149개 서비스 박스 사이에 묻혀 있습니다.

기준 자료는 두 가지입니다.

- **[NHN Cloud 공식 홈페이지 서비스 목록](https://www.nhncloud.com/kr/service) (최종 기준)**: 카테고리 22개, 서비스 119개. 카테고리·서비스 구성, 표시명, 순서는 모두 이 목록을 따름
- **[NHN Cloud Architecture Icons V2.2 (2026.4.8, PPT)](https://static.toastoven.net/portal/public/resources/reference-architecture/NHN_Cloud_Architecture_Icons_2026.pptx)**: 아이콘 유형, 그룹, 화살표 가이드의 기준. 저장소 사본 `assets/pptx/NHN_Cloud_Architecture_Icons_2026.pptx` 가 이 포털 최신판(58쪽)입니다(2026-11-12 교체, 이전 사본은 2026.1.29판 57쪽). 포털판은 Data Lake Storage 슬라이드와 개편된 Arrows 슬라이드가 추가되고 AI Fashion이 빠졌으며, "NHN Cloud 계정 용어 변경 논의중" 메모 슬라이드가 삭제돼 용어가 확정됐음을 보여줍니다

- **[Figma `NHN Cloud Service icon`](https://www.figma.com/design/i2vBIR2Fd8YwGlziRQqyAy/NHN-Cloud-Service-icon?node-id=4487-14877)**: `03 Architecture icon` 페이지. 아이콘 원본과 그룹 박스 배치의 디자인 원본입니다. 그룹 15종 표는 `4597:219944`, 서비스 박스 변형은 `[NHNCloud]_architecture_icon_Groups`(`4954:54169`) 입니다.

두 자료가 다를 때는 홈페이지 > PPT 순으로 따릅니다. 홈페이지에 없는 아이콘은 PPT에 있어도 Retired 팔레트로 보냅니다.

저장소([github.com/nhn-cloud/Icons](https://github.com/nhn-cloud/Icons))는 **전면 개편 대상이므로 기준으로 삼지 않습니다.** 이 문서에서 저장소를 언급하는 부분은 보유한 SVG 자산의 유무와 파일명을 확인하기 위한 현황 정보이며, 분류·표시명·순서의 근거가 아닙니다.

V2.1(2025.3.25) 대비 V2.2의 주요 변경은 다음과 같습니다. 그룹 16종과 화살표 스펙은 바뀌지 않았습니다.

- 카테고리 개편: Dooray!, Dooray! | ERP, Dooray! | Groupware가 **Collaboration** 하나(Dooray! 아이콘 1개)로 통합되고, **IDC** 카테고리가 빠져 24개 → 23개
- 추가: Cloud Functions, Load Balancer (DSR), NAS for BigData, Valkey Instance, EasyQueue, Data Lake Storage, Private CA, Cloud Access
- 개명: Hybrid & Private Cloud가 NHN Cloud Private Region, NHN Cloud Private Station, NHN Cloud Private Deck, NHN Hybrid Cloud 체계로 변경
- 삭제: AI Fashion, Contact Center의 Mobile Contact (Contiple만 남음)
- 용어 확정: 계정 아이콘의 "NHN Cloud Member → NHN Cloud 계정", "IAM Member → IAM 계정" 논의 메모가 사라지고 확정 용어로 표기

| AWS 기준 | 반영 여부 | NHN Cloud 적용 |
| --- | --- | --- |
| 공통 팔레트를 맨 위에, 서비스 카테고리를 그 아래 알파벳 순으로 | 반영 | Arrows, General Resources, Industry & Concepts, Identity, Groups 다음에 22개 카테고리. 카테고리 순서는 알파벳 대신 공식 홈페이지 서비스 메뉴 순 |
| 카테고리 팔레트 첫 항목은 카테고리 아이콘 | 반영 | 저장소 `category_icons/`의 아이콘을 각 팔레트 맨 앞에 배치 |
| 서비스 아이콘 → 리소스 아이콘 순서, 크기로 위계 표현 | 반영 | 서비스 64×64, 리소스 48×48 |
| 그룹은 선 색·선 종류·모서리 아이콘으로 구분하는 컨테이너 | 반영 | PPT의 그룹 16종 스펙을 draw.io 컨테이너 스타일로 정의 |
| 모든 항목에 검색 태그 | 반영 | 영문 + 한글 + 약어 + 카테고리명 |
| 단종 아이콘은 Retired 팔레트로 보존 | 반영 | 이름이 바뀌거나 단종된 아이콘을 Retired로 이동 |
| 카테고리마다 다른 색 | **반영 안 함** | NHN Cloud 아이콘은 전 카테고리가 브랜드 블루 #125DE6 단일색. 색 변경은 브랜드 결정 사항이라 팔레트 구분으로 대신함 |
| 벡터 스텐실(스타일로 색 변경) | **반영 안 함** | draw.io 본체 기여가 필요. SVG 이미지 임베드 방식 유지, 블랙 버전은 별도 라이브러리 |

## 라이브러리 구성

팔레트 1개 = draw.io 라이브러리 XML 1개입니다. draw.io는 `clibs` 링크에 적힌 순서대로 패널에 쌓으므로, 아래 순서가 곧 화면 순서입니다. 공통 팔레트는 AWS처럼 맨 위에 두고, 서비스 카테고리는 [NHN Cloud 공식 홈페이지 서비스 메뉴](https://www.nhncloud.com/kr/service)의 노출 순서를 따릅니다. 고객이 홈페이지·콘솔에서 보는 순서와 같아야 찾기 쉽기 때문입니다.

| 순서 | 팔레트 (패널 표시명) | 파일 | 내용 |
| --- | --- | --- | --- |
| 01 | NHN Cloud / Arrows | `NHNCloud-00-Arrows.xml` | 주·보조 경로, 성공·실패 상태 연결선 |
| 02 | NHN Cloud / General Resources | `NHNCloud-01-General.xml` | 사용자, 단말, 범용 인프라, 데이터·문서 |
| 03 | NHN Cloud / Industry & Concepts | `NHNCloud-02-Industry.xml` | 금융, 제조, 의료, IoT 등 산업·개념 일러스트 |
| 04 | NHN Cloud / Identity | `NHNCloud-03-Identity.xml` | NHN Cloud 계정·IAM 계정과 역할(Owner/Admin/Member/Viewer) |
| 05 | NHN Cloud / Groups | `NHNCloud-04-Groups.xml` | PPT 15쪽의 그룹 박스 15종 (아래 그룹 정의). 서비스 박스는 싣지 않는다 |
| 06\~27 | NHN Cloud / Compute \~ Governance & Audit | `NHNCloud-<category>.xml` | 서비스 카테고리 22개 (아래 분류표) |
| 28 | NHN Cloud / Retired | `NHNCloud-Retired.xml` | 홈페이지에서 빠지거나 개명된 아이콘. 기존 다이어그램 호환용 |

**서비스 카테고리 22개 (홈페이지 메뉴 순)**: Compute, Container, Network, Storage, Database, Monitoring, Hybrid & Private Cloud, Game, Security, Content Delivery, Notification, AI Service, Machine Learning, Application Service, Search, Data & Analytics, Dev Tools, Management, Bill, Collaboration, Contact Center, Governance & Audit

V2.2 PPT에 있던 Mobile Service(IAP)는 홈페이지에 없으므로 카테고리에서 빼고 Retired로 옮깁니다.

카테고리 구성은 V2.2의 Service Category Icons(20쪽) 23개와 정확히 일치합니다. V2.1에 있던 Dooray! 하위 서비스 아이콘과 IDC(NCC) 아이콘은 Retired 팔레트로 옮깁니다.

## 아이콘 유형과 크기 규칙

유형은 PPT 가이드의 3분류(서비스·리소스·일반)에 카테고리 아이콘과 그룹 아이콘을 더한 5종입니다. 원본 SVG 캔버스는 모두 60×60이므로, draw.io에 넣을 때 아래 크기로 정규화합니다. 서비스와 리소스의 크기 비율(64:48 = 0.75)은 AWS(78:48 ≈ 0.62)보다 조금 크게 잡아, 리소스 아이콘의 픽토그램이 작아져도 읽히도록 했습니다.

| 유형 | 정의 | draw.io 크기 | 팔레트 안 위치 | 레이블 |
| --- | --- | --- | --- | --- |
| 카테고리 아이콘 | 카테고리 자체를 나타내는 아이콘 (예: Compute) | 64×64 | 각 카테고리 팔레트 맨 앞 1개 | 아래 |
| 서비스 아이콘 | 콘솔에서 하나의 서비스로 제공되는 상품 (예: Instance, RDS for MySQL) | 64×64 | 카테고리 아이콘 다음, 알파벳 순 | 아래 |
| 리소스 아이콘 | 서비스에 종속된 하위 리소스 (예: Block Storage의 Volume, Snapshot) | 48×48 | 서비스 아이콘 다음, 상위 서비스별로 묶어 알파벳 순 | 아래 |
| 일반 아이콘 | 서비스와 무관하게 단독으로 쓰는 아이콘 (사용자, 단말, 문서 등) | 48×48 | General Resources, Industry & Concepts 팔레트 | 아래 |
| 그룹 아이콘 | 그룹 박스 왼쪽 위에 붙는 32×32 모서리 아이콘 | 박스 기본 320×200, 모서리 아이콘 24×24 | Groups 팔레트 | 박스 안 왼쪽 위 |

공통 스타일은 AWS와 같이 `aspect=fixed`(비율 고정), 레이블 아래 정렬, 글꼴 12px, 연결점 16개로 통일합니다. 이렇게 하면 크기를 바꿔도 아이콘이 찌그러지지 않고, 화살표가 아이콘 둘레의 같은 위치에 붙습니다.

**DB 엔진 Instance 아이콘의 위치**: MySQL Instance, Tibero Instance 같은 아이콘은 RDS의 하위 리소스가 아니라 홈페이지에 별도 서비스로 등록된 상품이므로 서비스 아이콘(64px)으로 둡니다. Kafka Instance, Deep Learning Instance도 같은 원칙을 따릅니다. 반대로 RDS Instance, Cache node는 리소스 아이콘(48px)입니다.

## 그룹 정의

그룹은 이미지가 아니라 **draw.io 컨테이너 도형**(선 스타일 + 왼쪽 위 모서리 아이콘 + 레이블)으로 만듭니다. AWS Groups 팔레트와 같은 방식이고, 안에 넣은 아이콘이 함께 움직이며 크기를 자유롭게 바꿀 수 있습니다. 선 색과 선 종류는 PPT 15쪽의 실제 도형 값(선 두께 1pt)을 그대로 옮겼습니다.

NHN Cloud의 그룹은 AWS처럼 그룹마다 다른 색을 쓰지 않고, **회색 농도로 계층을 표현**합니다. 바깥 계층일수록 진하고(#111111 → #555555 → #999999 → #BBBBBB), 리전과 가용 영역처럼 논리적 경계는 점선, VPC·서브넷처럼 실제 자원은 실선입니다. 색을 쓰는 그룹은 보안(분홍)과 컴퓨트 단위(브랜드 블루)뿐입니다.

| 중첩 순서 | 그룹 | 선 색 | 선 종류 | 모서리 아이콘 | 원본 파일 (`box_type/`) |
| --- | --- | --- | --- | --- | --- |
| 1 | NHN Cloud | #111111 | 실선 | NHN Cloud 로고 (검정 배경) | `General_Resources_Groups_NHN_Cloud` |
| 1 | On-Premise / IDC / Co-lo Zone | #555555 | 실선 | 건물 | `General_Resources_Groups_On_Premise` |
| 2 | Organization | #555555 | 실선 | 조직 | `General_Resources_Groups_Organization` |
| 3 | Project | #555555 | 실선 | 프로젝트 | `General_Resources_Groups_Project` |
| 4 | Region | #999999 | 점선 | 깃발 | `General_Resources_Groups_Region` |
| 5 | VPC | #999999 | 실선 | 구름 | `General_Resources_Groups_VPC` |
| 6 | Availability Zone | #B28FD1 | 점선 | 없음 | 없음 (PPT 도형) |
| 7 | Subnet (Public / Private) | #BBBBBB | 실선 | 자물쇠 | `General_Resources_Groups_Private subnet` |
| 8 | Security Groups | #EE97AA | 실선 | 없음 | 없음 (PPT 도형) |
| 9 | Auto Scaling Group | #125CE7 | 점선 | Auto Scale (상단 가운데) | `General_Resources_Groups_Auto_Scaling_Group` |
| 10 | Instance Contents | #125CE7 | 실선 | 인스턴스 | `IaaS-Compute-Instance` |
| 10 | Server Contents | #BBBBBB | 실선 | 서버 | `General_Resources_Server_content` |
| – | NHN Cloud Member | #BBBBBB | 실선 | 사용자 | `General_Resources_Groups_NHNCloud_Member` |
| – | Generic Group (점선) | #DDDDDD | 점선 | 없음 | 없음 (PPT 도형) |
| – | Generic Group (실선) | #DDDDDD | 실선 | 없음 | 없음 (PPT 도형) |

중첩 순서는 PPT 예시 구성도(10\~13쪽)에서 실제로 겹쳐 쓴 순서입니다. 같은 번호는 같은 계층의 형제 그룹입니다.

**모서리 아이콘과 레이블 배치** (PPT 15쪽·Figma `4597:219944` 양쪽에서 같음)

| 배치 | 대상 | draw.io 스타일 |
| --- | --- | --- |
| 아이콘 좌상단, 레이블 오른쪽 | 아이콘이 있는 10종 | `align=left;spacingLeft=40`(아이콘 32 + 간격 8), 아이콘 `x=0` |
| 아이콘 상단 가운데, 레이블 그 아래 가운데 | **Auto Scaling Group 만** | `align=center;spacingTop=36`(아이콘 32 + 간격 4), 아이콘 `x=(520-32)/2=244` |
| 아이콘 없음, 레이블 좌상단 | 아이콘이 없는 4종 | `align=left;spacingLeft=10` — 아이콘 자리만큼 들여쓰지 않는다 |


**(2026-11-12 철회)** 아래 서비스 박스 선정은 유지하되, **Groups 팔레트에는 싣지 않습니다.** Groups 팔레트는 PPT 15쪽의 그룹 박스 15종만 담습니다. SVG 는 `icons/05-groups/service-boxes/` 에 그대로 두었고, `taxonomy.yaml` 의 `service_boxes` 만 비웠습니다. 아래는 그때의 선정 근거입니다.

~~서비스 박스 아이콘은 149개에서 9개로 줄여 위 Groups 팔레트에 함께 넣습니다.~~ 별도 Service Groups 팔레트를 만들지 않는 이유는, 서비스 박스도 결국 안에 자원을 담는 컨테이너라 그룹 컨테이너 16종과 쓰임이 같기 때문입니다. 팔레트를 둘로 나누면 "박스를 찾을 때 어디를 봐야 하는지"가 모호해집니다. 패널에서는 그룹 컨테이너 16종 다음에 서비스 박스 9종을 둡니다.

남기는 기준은 **"NHN Cloud 공식 레퍼런스 아키텍처 36건에서 실제로 다른 자원을 담는 박스로 그려진 서비스"** 하나뿐입니다. 추정으로 넣은 항목은 없습니다. 중첩 순서는 모두 10(Instance Contents와 같은 최하위 계층)이며, 보통 서브넷 안에 놓입니다.

| 카테고리 | 서비스 박스 | 박스 안에 담는 것 | 근거 레퍼런스 아키텍처 | 건수 | 원본 파일 (`box_type/`) |
| --- | --- | --- | --- | --- | --- |
| Container | NHN Kubernetes Service (NKS) | node group → node → namespace → Container | e-Commerce, CI/CD | 2 | `ic-container-nks-box` |
| Container | NHN Container Service (NCS) | workload: prod / dev → Container | CI/CD | 1 | `ic-container-ncs-box` |
| Storage | Backup | Backup Store | 백업 전략 | 1 | `ic-storage-backup-box` |
| Database | RDS for MySQL | Master, Candidate Master, Read Replica | RDS for MySQL 고가용성, e-Commerce, 고가용성 구성, RPG 게임(2곳) | 5 | `ic-database-rds_for_mysql-box` |
| Database | EasyCache | Master, Replica | e-Commerce, RPG 게임 | 2 | `ic-database-easycache-box` |
| Hybrid & Private Cloud | NHN Cloud Private Station § | 내부 서비스 아이콘 6개 | NHN Cloud Private Station | 1 | 없음 (신규 제작) |
| Security | Network Firewall | Firewall + IPSec VPN, AZ(A) Active / AZ(B) Standby | Network Firewall 기본 구성, 고가용성 구성 | 2 | `ic-secutiry-network_firewall-box` |
| Machine Learning | AI EasyMaker | Notebook, Training, Model, Inference, Pipeline | MLOps | 1 | `ic-machine_learning-ai_easymaker-box` |
| Dev Tools | Pipeline | Source → Build → Deploy, Pipeline management(prod/stg/dev) | CI/CD | 1 | `ic-dev_tools-pipeline-box` |

그룹 컨테이너와 똑같이 **draw.io 컨테이너 도형**으로 만듭니다. 정적 이미지 박스를 그대로 쓰지 않고, 선 스타일 + 왼쪽 위 모서리 아이콘(24×24) + 레이블 조합으로 바꿔 크기 조절과 자식 이동이 되게 합니다. 모서리 아이콘은 해당 서비스의 서비스 아이콘을 그대로 씁니다.

**§** NHN Cloud Private Station 이름의 박스 SVG는 저장소에 없습니다. 저장소에는 구명칭으로 보이는 `ic-hybrid_n_private_cloud-nhn_private_cloud-box`가 있는데, 이것이 Private Station인지 Private Region인지 확인되지 않았습니다(아래 원본 정리 표 참고). 매핑을 확인해 개명하거나, 없으면 새로 만듭니다. 나머지 8개는 `box_type/color`에 원본이 있습니다.

어떤 서비스를 박스로 그려야 하는지 정의한 공식 매니페스트는 존재하지 않습니다. `box_type.md`는 그룹 컨테이너와 박스 테두리를 두른 서비스 아이콘을 구분하지 않는 평면 목록이고, 공식적으로 컨테이너로 정의된 것은 `General_Resources_Groups_*` 접두사를 가진 9개(NHN Cloud, Organization, Project, Region, VPC, Private subnet, On-Premise, NHN Cloud 계정, Auto Scaling Group)뿐입니다. 이는 그룹 컨테이너에 해당하며 서비스 박스는 포함하지 않습니다. 따라서 위 선정은 레퍼런스 아키텍처 실측이 현재 확보 가능한 최선의 근거입니다.

**1차안 20개에서 뺀 항목과 이유**

| 뺀 항목 | 이유 |
| --- | --- |
| GPU Instance, Virtual Desktop, Transit Hub, Object Storage, NAS, NHN Bastion, Kafka Instance | 36건 전부에서 단일 아이콘으로만 등장. 박스로 쓰인 사례 없음 |
| Load Balancer, WEB Firewall | 공공 보안 랜딩존 1건뿐이고, 그마저 서비스 박스가 아니라 서브넷 스타일(회색 자물쇠) 박스. 3-Tier·가용성 영역에서는 LB 아이콘이 멤버 인스턴스 **바깥**에 놓임 |
| RDS for PostgreSQL, RDS for MariaDB, RDS for MS-SQL | 박스로 그려진 사례는 RDS for MySQL뿐. 계열 일관성보다 관측 근거를 우선함 |
| Auto Scale | 레퍼런스 아키텍처가 Auto Scale을 파란 점선 "Auto Scaling group"으로 그리는데, 이는 Groups 팔레트 9번 `General_Resources_Groups_Auto_Scaling_Group`과 동일. Instance·VPC·Security Groups와 같은 중복 배제 규칙 적용 |

Instance, VPC, Security Groups 박스도 Groups 팔레트의 Instance Contents, VPC, Security Groups와 겹치므로 넣지 않습니다. 선정되지 않은 서비스 박스 127개는 **저장소에서 삭제했습니다**(커밋 `d1915f1` 이전 이력에 남아 있음). draw.io에서 박스가 필요하면 Generic Group에 서비스 아이콘을 얹어 씁니다.

**조사 방법**: 레퍼런스 아키텍처 목록(<https://www.nhncloud.com/kr/resource/reference-architecture>)은 페이지 스크립트로 그려져 일반 조회로는 "총 0개"만 나옵니다. 브라우저로 렌더링해 36건을 확보하고, 각 건의 본문은 콘텐츠 API(`/xcms-api/v1/contents/<id>`)로, 구성도는 `static.toastoven.net`의 원본 이미지(4124×2173 래스터)를 직접 보고 판별했습니다. 구성도가 전부 래스터라 자동 파싱은 불가능했고 눈으로 읽었습니다.

**주의**: 각 페이지의 "연관 서비스" 목록은 큐레이션 메타데이터라 구성도 내용과 다릅니다. 예를 들어 e-Commerce는 NHN Bastion, Auto Scale, VPN Gateway, Direct Connect를 연관 서비스로 걸어 두었지만 구성도에는 넷 다 없습니다. 판별 근거로 쓰지 않았습니다.

**같은 서비스도 구성도마다 표현이 다릅니다.** RDS for MySQL·EasyCache는 e-Commerce·RPG 게임에서는 박스지만 업무망/인터넷망 분리, 국가 보안관제에서는 단일 아이콘입니다. AI EasyMaker도 MLOps에서는 박스, 빅데이터 플랫폼에서는 아이콘입니다. 따라서 서비스 박스는 "항상 박스로 그리는 서비스"가 아니라 "박스가 필요할 때 쓸 수 있게 준비해 두는 서비스"입니다. N2SF 13건에는 서비스 박스가 하나도 없습니다.

**서브넷 표현 (확정)**: Public subnet과 Private subnet은 같은 스타일(#BBBBBB 실선, 자물쇠 아이콘)을 쓰고 레이블로만 구분합니다. AWS처럼 색을 나누지 않으므로 팔레트에는 "Public subnet", "Private subnet" 레이블이 미리 입력된 항목 2개를 둡니다.

**계정 그룹 표시명 (2026-11-12 변경)**: 팔레트 표시명을 PPT 15쪽 그대로 "NHN Cloud Member"로 되돌렸습니다. 앞서는 V2.2 확정 용어에 맞춰 "NHN Cloud 계정"으로 적기로 했으나, Groups 팔레트를 PPT 15쪽에서 그대로 옮기기로 하면서 출처 표기를 따릅니다. 본문·Identity 팔레트의 "NHN Cloud 계정" 표기는 그대로 둡니다.

## 공통 팔레트

**Arrows (2026-11-12 실측으로 교체)**: PPT 16쪽의 연결선 도형을 그대로 엣지 스타일로 등록합니다.
원본은 **6종이 아니라 18종**입니다. 슬라이드가 3열(Primary Path / Secondary Path / Success Status) x 6행이고,
3열만 녹색·빨강이 번갈아 들어가 Success 3종 + Failure 3종이 됩니다. 선 두께는 모두 1pt입니다.
값은 `icons/01-arrows/styles.yaml` 이 단일 원천이고, `tools/make_drawio_libs.py` 가 `dist/01.xml` 을 만듭니다.

| 항목 | 선 색 | 화살촉 조합 | 선 종류 | 종수 |
| --- | --- | --- | --- | --- |
| Primary Path | #555555 | 끝 / 양쪽 / 없음 | 각 실선·점선 | 6 |
| Secondary Path | #999999 | 끝 / 양쪽 / 없음 | 각 실선·점선 | 6 |
| Success Status | #09C72C | 끝 / 양쪽 / 없음 | 실선만 | 3 |
| Failure Status | #EF0F0F | 끝 / 양쪽 / 없음 | 실선만 | 3 |

- 화살촉은 PPT `triangle`(채운 삼각형)이고 draw.io 에서는 `endArrow=block;endFill=1` 이 같은 모양입니다.
- 점선은 OOXML 프리셋을 그대로 옮겼습니다. `dash` = `dashPattern=4 3`, `sysDash` = `dashPattern=3 1`.
- **원본 불일치 1건**: 1열 2행(Primary Path 점선, 끝 화살촉)만 `sysDash` 이고 나머지 점선은 모두 `dash` 입니다.
  PPT 작성상의 흔들림으로 보이지만 실물을 그대로 옮겨 두었습니다. 통일하려면 디자인팀 확인이 필요합니다.
- 이전 표에 있던 "Primary Path (연한 배경용)" 은 실물에 없는 항목이었습니다. #999999 열의 슬라이드 제목은
  Secondary Path 이고, 본문 설명은 실선=주 경로 / 점선=보조 경로로 따로 적고 있습니다.

**General Resources**: PPT 18\~19쪽의 일반 아이콘 중 사람, 단말, 범용 인프라, 데이터를 모읍니다. 팔레트 안에서는 AWS General Resources처럼 의미 묶음 순으로 둡니다.

| 묶음 | 아이콘 |
| --- | --- |
| 사람 | Administrator, Authenticated user, External User, Internal User, Users |
| 단말 | Client, Desktop, Desktop + Phone, Laptop, Mobile client, Mobile Devices, Phone |
| 범용 인프라 | Disk, Gateway, Internet, Globe, Interface, IP ACL, Peering, Private Network, Server, Servers, Storage, Subnet, Tape storage, Cold storage, Office building |
| 애플리케이션·개발 | Application Instance, Application Service, Generic application, Git repository, Programming language, Source code, SDK, Toolkit, Dev Tools, JSON script, NHN Cloud Console |
| 데이터·문서 | Data stream, Data table, Document, Documents, Folder, Folders, Logs, Metrics, Multimedia |
| 보안·알림 | Credentials, Login Security Settings, SAML token, SSL padlock, Alert, Chat |

**Industry & Concepts**: Finance, Manufacturing, Medical & Healthcare, IoT, Machine Learning 개념 아이콘입니다. AWS의 Illustrations에 해당하며, 구성도보다 제안서·개요 장표에서 쓰입니다. 5개 모두 확보했습니다(2026-11-12). 원본은 Figma `03 Architecture icon` 의 `[NHNCloud]_architecture_icon_Black` 변형에 한 줄로 모여 있고, Color 변형에는 없습니다. 이 5개는 브랜드 블루가 아니라 **`#222222` 단색**입니다. Finance 는 Dooray! ERP 재무(`ic-dooray_erp-finance`)와 같은 그림을 씁니다 — Figma 가 Finance 칸에 그 아이콘을 두고 있습니다.

**Identity**: PPT 17쪽의 계정과 역할 아이콘입니다. NHN Cloud 계정(Owner, Admin, Member, Viewer)과 IAM 계정(Admin, Member, Viewer) 2계열로 묶습니다. AWS는 IAM을 Security, Identity & Compliance 카테고리에 두지만, NHN Cloud에서 계정·역할은 Organization·Project 그룹과 함께 쓰이므로 Groups 바로 앞의 공통 팔레트로 둡니다. 표시명은 V2.2 확정 용어인 "NHN Cloud 계정", "IAM 계정"을 쓰고, 그룹 팔레트의 계정 그룹도 "NHN Cloud 계정"으로 맞춥니다.

현재 저장소의 General 라이브러리에는 30개만 있고, 그중 9개는 카테고리 아이콘(ic-ai\_service, ic-database 등)입니다. 카테고리 아이콘은 각 카테고리 팔레트 맨 앞으로 옮깁니다. **PPT에만 있는 일반 아이콘 약 40개는 PPT V2.2(18\~19쪽)에서 SVG로 추출해** General Resources와 Industry & Concepts 라이브러리에 추가합니다. 추출한 SVG는 다른 아이콘과 같은 60×60 캔버스, 브랜드 블루 #125DE6 기준으로 맞추고, 블랙 버전도 함께 만듭니다.

## 카테고리별 분류표

서비스 카테고리 22개에 홈페이지 서비스 119개(서비스 아이콘)와 리소스 아이콘 약 40개가 들어갑니다. 카테고리 순서와 카테고리 안의 서비스 순서는 모두 홈페이지 노출 순서입니다. **†** 는 홈페이지에 있지만 저장소에 서비스·리소스 SVG가 없는 아이콘(박스 버전만 있거나 PPT에만 있음)이고, **§** 는 아이콘이 아예 없어 새로 만들어야 하는 서비스입니다. 리소스 아이콘은 홈페이지에 목록이 없으므로 PPT V2.2를 따르고, `상위 서비스: 리소스` 형태로 적었습니다.

| 카테고리 | 서비스 아이콘 (64px) | 리소스 아이콘 (48px) |
| --- | --- | --- |
| Compute (8) | Instance, GPU Instance, Cloud Functions, Instance Template, Image, Image Builder, Auto Scale, Virtual Desktop | – |
| Container (3) | NHN Kubernetes Service (NKS), NHN Container Registry (NCR), NHN Container Service (NCS) | NKS: Container / NCR: Image, Registry / NCS: Workload |
| Network (20) | VPC, Network Interface, Flow Log†, Floating IP, Network ACL, Security Groups, Load Balancer, Load Balancer (DSR), NAT Instance, Transit Hub, Internet Gateway, Peering Gateway, Colocation Gateway, NAT Gateway, VPN Gateway (Site-to-Site VPN), Service Gateway, Traffic Mirroring, Private DNS, DNS Plus, Direct Connect | VPC: Router, Routing table, Peering connection / Transit Hub: Attachment / Colocation Gateway: NHN Cloud Zone / VPN Gateway: VPN connection / DNS Plus: DNS, GSLB |
| Storage (8) | Block Storage, NAS, NAS (offline), NAS for BigData, Object Storage, Backup, Data Transporter, Storage Gateway | Block Storage: Volume, Snapshot / NAS: File System / Object Storage: Container, Container Replication, Object / Backup: Backup Policy, Backup Store, Backup Replication, Backup Recovery / Data Transporter: Import-Export |
| Database (13) | RDS for MySQL, RDS for PostgreSQL, RDS for MariaDB, RDS for MS-SQL, EasyCache, MS-SQL Instance, MySQL Instance, PostgreSQL Instance, Tibero Instance, CUBRID Instance, MariaDB Instance, Valkey Instance, Database Migration Service§ | RDS for MySQL: RDS Instance / EasyCache: Cache node |
| Monitoring (2) | Service Monitoring, Cloud Monitoring | Cloud Monitoring: Dashboard, Notification |
| Hybrid & Private Cloud (4) | NHN Cloud Private Deck, NHN Cloud Private Station, NHN Cloud Private Region, NHN Hybrid Cloud | – |
| Game (5) | Gamebase, GameAnvil, GameStarter, Leaderboard, Launching | – |
| Security (16) | NHN AppGuard, App Security Check, Server Security Check, Basic Security, Webshell Threat Detector, Security Monitoring, WEB Firewall, Secure Key Manager, Vaccine, Security Compliance, DDoS Guard, SIEM, Security Advisor, Network Firewall, NHN Bastion, Cloud Access | Network Firewall: Firewall, IPSec VPN† |
| Content Delivery (2) | CDN, Image Manager | CDN: Edge Server |
| Notification (6) | Notification Hub, SMS, KakaoTalk Bizmessage, Push, RCS Bizmessage, Email | – |
| AI Service (4) | Face Recognition, OCR, Text to Speech, Speech to Text | – |
| Machine Learning (3) | Deep Learning Instance, AI EasyMaker, NHN Cloud Foundry§ | AI EasyMaker: Notebook†, Training†, Model†, Inference†, Pipeline† |
| Application Service (5) | ROLE, API Gateway, ShortURL, File-Crafter, Cloud Scheduler | – |
| Search (3) | Cloud Search, Autocomplete, Corporation Search | – |
| Data & Analytics (6) | Log & Crash Search, DataFlow, DataQuery, EasyQueue, Kafka Instance, Data Lake Storage | – |
| Dev Tools (3) | Pipeline, Deploy, Native Deck | – |
| Management (3) | Support Plan, Certificate Manager, Private CA | – |
| Bill (1) | eTax | – |
| Collaboration (1) | Dooray!† | – |
| Contact Center (1) | Contiple | – |
| Governance & Audit (2) | CloudTrail, Resource Watcher | – |

§표 2개(Database Migration Service, NHN Cloud Foundry)는 홈페이지에 신규 서비스로 올라와 있지만 PPT와 저장소 어디에도 아이콘이 없어 제작 요청이 필요합니다.

각 팔레트 안에서는 카테고리 아이콘 → 서비스 아이콘(홈페이지 순서) → 리소스 아이콘(상위 서비스 순서)으로 배치합니다. 홈페이지가 이미 RDS 계열과 EasyCache를 DB 엔진 Instance 계열보다 앞에 두므로 Database에도 별도 예외가 필요 없습니다.

**Retired 팔레트로 옮길 아이콘 (홈페이지에 없음)**: 다음 아이콘은 기존 다이어그램에 남아 있을 수 있어 삭제하지 않고 보존합니다.

| 카테고리 | 아이콘 |
| --- | --- |
| Compute | Bare Metal Instance, Ephemeral Storage Instance |
| Database | Redis Instance |
| Monitoring | Compute Monitoring |
| Game | Smart Downloader |
| Security | CAPTCHA, CSAP SaaS Guide |
| AI Service | AI Fashion, Face Liveness, Pose Estimation |
| Application Service | Maps, RTCS, JEUS Instance, WebtoB Instance |
| Search | Word Suggestion |
| Management | Managed |
| Contact Center | Mobile Contact |
| Mobile Service (카테고리 삭제) | IAP |
| IDC (카테고리 삭제) | NCC |
| Collaboration | V2.1의 Dooray! 하위 서비스 11개 (Calendar, Contacts, Drive, Mail, Messenger, Project, Wiki, ERP Finance, Human Resources, Communication Board, Workflow) |
| Hybrid & Private Cloud | 개명 전 NHN Private Cloud |

Retired 아이콘은 Retired 라이브러리로만 배포하고 기본 배포 링크에는 넣지 않습니다.

## 명명 규칙과 검색 태그

표시명은 콘솔의 공식 서비스명, 내부 이름은 소문자 snake\_case로 통일합니다. AWS가 표시명 "Lambda Function"과 내부 이름 `lambda_function`을 따로 두는 방식과 같습니다.

| 항목 | 규칙 | 예시 |
| --- | --- | --- |
| 표시명 (draw.io title) | 콘솔 공식 서비스명 그대로. 리소스는 리소스명만 쓰고 상위 서비스는 태그로 | `RDS for MySQL`, `Volume` |
| SVG 파일명 | `ic-<category>-<service>[-<resource>].svg`, 소문자 snake\_case, 영문만 | `ic-storage-block_storage-volume.svg` |
| 카테고리 키 | 저장소 폴더명과 동일 | `data_analytics`, `hybrid_private_cloud` |
| 박스 아이콘 | 서비스 파일명 + `-box` | `ic-network-vpc-box.svg` |
| 라이브러리 파일 | `NHNCloud-<Category>.xml`, 공통 팔레트는 번호 접두사 | `NHNCloud-Network.xml`, `NHNCloud-04-Groups.xml` |

파일명에서 `&`는 `n`으로 쓰는 기존 관례(`data_n_analytics`, `log_n_crash_search`)를 유지합니다. 다만 카테고리 키는 폴더명(`data_analytics`)과 파일명(`data_n_analytics`)이 달라서, 둘 중 하나로 맞춰야 합니다. 폴더명 쪽이 짧고 이미 라이브러리 생성 스크립트가 읽는 값이므로 폴더명 기준을 권장합니다.

검색 태그는 draw.io 검색창에서 쓰이며, AWS처럼 모든 항목에 공통 태그와 동의어를 넣습니다. 태그는 공백으로 구분한 소문자 문자열입니다.

```
공통:     nhn cloud nhncloud 엔에이치엔
카테고리: <카테고리 영문> <카테고리 한글>      예) storage 스토리지
이름:     <표시명 영문> <표시명 한글>          예) block storage 블록 스토리지
상위:     리소스 아이콘은 상위 서비스명        예) volume 볼륨 + block storage
동의어:   약어·풀네임·흔한 별칭                예) nks kubernetes 쿠버네티스 k8s
```

한글 표시명은 NHN Cloud 한국어 콘솔 메뉴명을 기준으로 하고, 약어 서비스(NKS, NCR, NCS, SIEM, ROLE, CDN)는 풀네임과 한글 설명을 함께 넣습니다.

## 원본 정리 필요 항목

분류 체계를 라이브러리로 만들기 전에 저장소 원본에서 아래 22건을 정리해야 합니다. 저장소 파일명과 폴더는 아직 V2.1 기준이고, PPT V2.2도 홈페이지와 다른 부분이 있어 두 곳 모두 홈페이지 기준으로 맞춰야 합니다. 새로 그려야 하는 아이콘은 §표 2개뿐이고, 나머지는 파일 정리와 추출 작업입니다.

| 구분 | 현재 상태 | 조치 |
| --- | --- | --- |
| 오탈자 | `secutiry` (Security 아이콘 16개), `lauching` (Game), `machinelearnign` (카테고리 아이콘) | `security`, `launching`, `machine_learning`으로 변경 |
| 중복 | `network-load_balancer(dsr)`과 `network-load_balancer_dsr` 두 파일 | `_dsr` 하나만 남김 |
| 위치 오류 | Database 리소스 2개(RDS Instance, Cache node)가 `services/database`에도 있음 | `resources/database`에만 둠 |
| 홈페이지 기준 단종 | 분류표 아래 Retired 목록의 아이콘 약 30개가 서비스·박스 폴더에 그대로 있음 (Redis Instance, Maps, JEUS Instance, Compute Monitoring 등) | `retired/` 폴더로 이동하고 Retired 라이브러리로만 배포 |
| 카테고리 삭제 | Mobile Service, IDC 폴더와 카테고리 아이콘(`mobileservice.png`, `ic-idc.png`)이 남아 있음 | Retired로 이동 |
| 카테고리 개편 | `collaboration` 폴더에 `dooray-project-box` 하나뿐이고, Dooray! 하위 박스 11개와 ERP Finance(일반 아이콘 폴더)가 흩어져 있음 | 홈페이지의 Dooray! 아이콘 1개를 서비스 아이콘으로 추가, 하위 11개는 Retired로 |
| 파일명 규칙 | 리소스 아이콘이 `IaaS-Storage-Backup-Backup_Policy`, `PaaS-…`, `Security_Sub_Firewall` 등 제각각 | `ic-<category>-<service>-<resource>`로 통일 |
| 파일명 규칙 | 리소스 파일명에 한글(`…Cloud_Monitoring-알림`) | `notification`으로 변경 |
| 파일명 규칙 | 박스 아이콘 일부에 `@2x`, `header@2x` 등 내보내기 접미사 | 접미사 제거, 불필요 파일 삭제 |
| 파일명 규칙 | 카테고리 아이콘이 `content delivery.png`(공백), `aiservice.png`(구분자 없음), `ic-collaboration.png` 혼재, PNG만 있음 | `ic-<category>.svg`로 통일, SVG 추가 |
| 명칭 불일치 | Contact Center: 홈페이지는 Contiple, 저장소는 `online_contact` | `online_contact`가 Contiple인지 확인 후 `contiple`로 변경 |
| 명칭 불일치 | Hybrid & Private Cloud: 홈페이지는 Private Deck / Private Station / Private Region, 저장소는 `cloud_station`, `nhn_private_cloud-box`(박스만) | 파일명을 `nhn_cloud_private_station`, `nhn_cloud_private_region`으로 변경, Private Region 서비스 아이콘 추가 |
| 명칭 불일치 | Dev Tools: 홈페이지는 "Native Deck", 저장소·PPT는 "NHN Native Deck" | 표시명을 Native Deck으로 |
| 명칭 불일치 | Security: 홈페이지 "Security Compliance", 파일 `compliance`. 일반 아이콘 "Settings"는 PPT에 2번 등장 | 파일명 `security_compliance`로 변경, 일반 아이콘 표시명 확정 |
| 홈페이지 기준 단종 | Bare Metal Instance는 저장소에만 있고 홈페이지·PPT에 없음 | Retired로 이동 |
| 누락 SVG | †표 서비스 아이콘 2개(Flow Log, Dooray!)는 박스 버전만 있음 | 박스 아이콘에서 서비스 아이콘 추출 |
| 누락 SVG | AI EasyMaker 리소스 5개, IPSec VPN, PPT 일반 아이콘 약 40개는 SVG 없음 | PPT V2.2에서 SVG 추출 |
| 신규 제작 | §표 2개(Database Migration Service, NHN Cloud Foundry)는 아이콘 자체가 없음 | 디자인팀에 신규 아이콘 제작 요청 |
| PNG 제거 | PNG 596개가 SVG 546개보다 많아 드리프트 중 (`services/network/color`는 PNG 21 / SVG 20) | PNG를 전부 삭제하고 SVG만 관리. PNG는 draw.io 내보내기·Copy as Image로 대체 |
| 크기 | 서비스·리소스 원본 캔버스 60×60, 현재 리소스 라이브러리 56×56 | 64 / 48로 정규화 (원본 SVG는 그대로, 라이브러리 생성 시 지정) |
| 문서 | PPT V2.2의 서비스 목록이 홈페이지와 다름 (Face Liveness 중복 표기, 단종 아이콘 포함, 신규 2개 누락) | PPT 다음 개정을 홈페이지 기준으로 요청 |
| 문서 | 저장소 README와 `service_icons.md`가 V2.1 구성 | 홈페이지 기준으로 갱신 |

파일명을 바꾸면 기존 다이어그램은 영향을 받지 않습니다. draw.io 라이브러리는 SVG를 XML 안에 base64로 넣기 때문에, 이미 그린 다이어그램은 원본 파일 경로를 참조하지 않습니다.

## 저장소 구조

디렉터리 번호를 팔레트 번호와 같게 둡니다. 저장소를 열면 draw.io 패널 순서가 그대로 보이고, 생성 스크립트도 디렉터리만 훑으면 됩니다.

```
Icons/
├─ taxonomy.yaml          단일 원천 (분류·표시명·한글명·유형·순서·태그)
├─ icons/                 원본 SVG (팔레트 28개와 1:1)
├─ dist/                  생성물, 커밋 대상 (팔레트 1개 = XML 1개, 25개)
├─ tools/                 make_drawio_libs.py, validate.py
├─ docs/                  scheme.md, taxonomy.yaml에서 생성한 카탈로그
└─ assets/pptx/
```

`dist/`를 커밋해야 하는 이유는 draw.io `clibs` 링크가 GitHub raw URL을 직접 읽기 때문입니다. 생성물이라도 저장소에 있어야 배포가 됩니다.

### icons/ 배치

```
icons/
├─ 01-arrows/                    styles.yaml (엣지 스타일 정의, SVG 없음)
├─ 02-general/
├─ 03-industry/
├─ 04-identity/
├─ 05-groups/
│   ├─ containers/               grp-vpc.svg …                            16종
│   └─ service-boxes/            box-container-nks.svg …                  9종
├─ 06-compute/
│   ├─ category/                 ic-compute.svg
│   ├─ services/                 ic-compute-instance.svg …
│   └─ resources/                (리소스가 있는 8개 카테고리만)
├─ 07-container/ … 27-governance-audit/
└─ 28-retired/                   + RETIRED.md (사유·시점·대체 아이콘)
```

카테고리 06\~27은 홈페이지 메뉴 순서입니다: compute, container, network, storage, database, monitoring, hybrid-private-cloud, game, security, content-delivery, notification, ai-service, machine-learning, application-service, search, data-analytics, dev-tools, management, bill, collaboration, contact-center, governance-audit.

### 파일명 규칙

| 유형 | 규칙 | 예 |
| --- | --- | --- |
| 카테고리 | `ic-<category>` | `ic-database` |
| 서비스 | `ic-<category>-<service>` | `ic-database-rds-for-mysql` |
| 리소스 | `ic-<category>-<service>-<resource>` | `ic-database-rds-for-mysql-rds-instance` |
| 그룹 컨테이너 | `grp-<name>` | `grp-private-subnet` |
| 서비스 박스 | `box-<category>-<service>` | `box-container-nks` |

전부 소문자 kebab-case입니다. **파일명은 슬러그일 뿐이고 표시명은 `taxonomy.yaml`에만 둡니다.** 지금은 `secutiry`·`lauching` 오탈자와 한글 파일명, `@2x` 접미사가 그대로 라이브러리 표시명으로 새어 나오는데, 이 규칙으로 끊깁니다.

### 파일 형식: 컬러 SVG 하나

원본은 **컬러 SVG 한 가지만** 관리합니다. PNG 와 블랙 버전은 저장소에 두지 않습니다.

재편 전에는 PNG 596개가 SVG 546개와 어긋나 드리프트 중이었고(`services/network/color` 는
PNG 21 / SVG 20), 블랙은 199개가 컬러와 짝이 맞지 않았습니다. 관리 대상을 하나로 줄여
짝 맞추기 문제 자체를 없앴습니다.

PNG 는 draw.io 에서 필요할 때 얻습니다.

| 방법 | 경로 | 비고 |
| --- | --- | --- |
| 내보내기 | File > Export as > PNG | 확대율, DPI, 여백, 투명 배경, 선택 영역만 지정 가능 |
| 클립보드 복사 | 선택 후 우클릭 > Copy as Image (`Ctrl+Alt+X`, v21.7.3+) | PPT·Word 에 바로 붙여넣기 |

주의: Copy as Image 로 붙여넣으면 배경이 검게 나오는 사례가 보고돼 있습니다.
문서 배경을 흰색으로 지정하거나 내보내기에서 투명 배경을 끄면 해결됩니다.

흑백 인쇄가 필요하면 draw.io 내보내기에서 처리하거나, 블랙 자산이 다시 필요해지면
`d1915f1` 이전 이력에서 복구할 수 있습니다.

### draw.io 로 제어할 수 없는 것 (실측)

배포 방식을 정하면서 실제로 시험해 확인한 한계다. 다시 조사하지 않도록 남긴다.

| 항목 | 결과 |
| --- | --- |
| 검색 범위 | **제한 불가.** `libs=none` 은 표시 팔레트만 끄고 검색은 draw.io 내장 스텐실 전체를 뒤진다. `search=0`, Configuration `search:false`, `enabledLibraries:[]` 모두 효과 없음. "load balancer" 를 치면 Alibaba·AWS 아이콘이 나온다 |
| 팔레트 순서 | **보장 불가.** 같은 링크를 열어도 방문마다 정순/역순이 바뀐다. 링크에서 순서를 뒤집어 보정해도 한쪽만 맞는다. 라이브러리를 비동기로 받아 도착 순서대로 쌓기 때문으로 보이나 확인하지는 못했다 |
| 팔레트 접힘 고정 | **리다이렉트 방식에서는 불가.** 펼친 상태가 `collapsedLibraries` 로 사용자 브라우저에 저장되고 URL 로 못 덮는다. `expandLibraries:false` 는 Configuration 전용이고 Configuration 은 임베드에서만 전달된다 |
| 탭 제목 | `title=` 파라미터는 무시된다. 열린 **파일 이름**을 쓰므로 이름만 있는 시작 파일을 `#U` 로 연다. 한글 파일명은 퍼센트 인코딩된 채 노출되고, 조각에 한글을 그대로 넣으면 로드가 실패한다 |
| iframe 임베드 | `app.diagrams.net` 은 `X-Frame-Options` 로 거부한다. `embed.diagrams.net` 을 써야 하는데, 그 경우 저장을 호스트 페이지가 떠안아 기기 저장·Drive·OneDrive·공유가 사라진다 |

그래서 **리다이렉트 방식**을 택했다. 접힘 고정과 순서 일관성은 포기하고, 클라우드 저장과
공유 기능을 지켰다. 임베드 시험판은 `embed/` 에 남겨 두었다(배포용 아님).

#### 갱신: 설정 링크(`#_CONFIG_`) 방식으로 해결된 항목

위 표 중 일부는 **app.diagrams.net 의 설정 링크**로 해결된다. Configuration 은 임베드뿐 아니라
`https://app.diagrams.net/#_CONFIG_<압축 JSON>` 링크로도 전달된다(Extras → Configuration → Link 가
만드는 형식). 사용자가 확인 2번을 누르면 그 브라우저에 저장되고, 이후 파라미터 없이 열어도 유지된다.
`tools/make_config_link.py` 가 이 링크와 배포 페이지를 만든다. draw.io 최신 소스로 로컬 실측했다.

| 항목 | 설정 링크 방식 결과 |
| --- | --- |
| 검색 범위 | 내장 스텐실 제외는 여전히 **불가**. 다만 Configuration `libraries` 로 등록한 팔레트는 **검색 색인에 들어간다.** `Gamebase`, `Auto Scale` 은 NHN Cloud 아이콘이 첫 결과. `Instance` 같은 흔한 단어는 내장 도형이 먼저 나온다. 순위 가중치(`librarySearchWeights`)는 설정으로 못 바꾼다. 대신 라이브러리에 `tags="nhn nhncloud"` 를 넣어 **`nhn load balancer` 처럼 치면 NHN Cloud 아이콘만** 남게 했다(검색은 단어 AND) |
| 팔레트 순서 | **고정.** `libraries` 의 `libs` 배열 순서대로 팔레트가 만들어진다 |
| 팔레트 접힘 고정 | **가능.** `expandLibraries:false` 면 저장된 펼침 상태와 관계없이 항상 접힌 채로 시작 |
| 탭 제목 | **고정 가능.** 위 표의 "`title=` 는 무시된다"는 실측이 틀렸다. `?title=NHN%20Cloud%20Icons` 가 파일 이름을 덮어써 제목이 그대로 쓰인다(확장자도 안 붙는다). 설정 해시와 같이 쓰려면 시작 파일을 `#U` 가 아니라 질의 문자열 `?url=` 로 준다. `?url=<시작 파일>&title=<제목>#_CONFIG_<설정>` 이면 설정 적용 후 새로고침에도 질의 문자열이 남아 첫 방문부터 제목이 고정된다 |
| 팔레트 이름 표시 | **가능.** `sidebarTitles:true` 면 팔레트를 펼쳤을 때 도형 아래에 이름이 보인다(`sidebarTitleSize` 로 크기 조절, 기본 8pt). 그룹 박스는 테두리만 다르고 생김새가 같아 이름 없이는 구분이 안 된다. 설정이라 모든 팔레트에 함께 적용된다 |
| '그 외 도형' | `libraries` 로 'NHN Cloud' 항목이 추가되어 AWS 처럼 체크 하나로 켜고 끈다 |

남는 비용: 브라우저마다 첫 방문 때 확인 2번, 설정 구조나 `dist/` 가 바뀌면 다음 방문 때 확인 2번.

### 기존 경로 호환

전면 개편이므로 구 경로는 유지하지 않습니다. 저장소 SVG를 raw URL로 직접 링크해 쓰던 곳은 깨지며, README에 안내만 둡니다. 이미 그린 draw.io 다이어그램은 SVG가 base64로 내장돼 있어 영향받지 않습니다.

## 배포 구성과 다음 단계

배포는 현재 저장소의 `drawio/` 폴더와 `clibs` 링크 방식을 그대로 쓰고, 파일을 4개에서 29개(컬러) + 29개(블랙)로 나눕니다. 사용자는 링크 3종 중 하나를 북마크하면 됩니다.

| 링크 | 포함 팔레트 | 용도 |
| --- | --- | --- |
| 전체 | 공통 5 + 카테고리 22 | 일반 구성도 작성 (기본 안내 링크) |
| 인프라 | 공통 5 + Compute, Container, Database, Network, Security, Storage | 인프라 구성도만 그리는 경우 |
| 블랙 | 위 "전체"의 블랙 버전 | 흑백 인쇄, 사내 문서 |

Retired는 링크에 넣지 않고 README에서 따로 안내합니다. 자체 호스팅 draw.io나 Confluence에서는 `defaultCustomLibraries`에 "전체" 목록을 넣어 기본 로드합니다.

라이브러리 XML은 손으로 만들지 않고, 분류표를 데이터 파일 하나(`taxonomy.yaml`: 아이콘별 카테고리, 유형, 상위 서비스, 표시명, 한글명, 태그)로 관리한 뒤 기존 `make_drawio_libs.py`가 이 파일을 읽어 생성하도록 바꿉니다. Exoscale 저장소처럼 생성 스크립트에 `--dry-run`을 두면 누락·중복을 배포 전에 잡을 수 있습니다.

- [ ] 남은 확인 사항 결정: 카테고리 키 기준(폴더명), Contiple 파일 매핑
- [x] 서비스 박스 후보를 레퍼런스 아키텍처 36건과 대조해 9개로 확정하고 Groups 팔레트에 통합 (2026-11-11)
- [ ] `nhn_private_cloud-box`가 Private Station인지 Private Region인지 확인 후 개명, 아니면 Private Station 박스 신규 제작
- [ ] 저장소 `files/pptx/` 사본을 포털 최신판(2026.4.8, 58쪽)으로 교체
- [ ] 저장소를 `icons/` 28개 디렉터리 구조로 재배치 (팔레트 번호 = 디렉터리 번호)
- [x] 모든 PNG와 블랙 자산 삭제, 컴러 SVG 단일 관리로 전환 (2026-11-11)
- [ ] `validate.py` 작성 (블랙 누락, 슬러그 규칙 위반, taxonomy 미등록 검출)
- [ ] 원본 정리 22건 반영 (파일명 변경, 중복 제거, Retired 이동)
- [ ] †표 아이콘과 PPT 일반 아이콘 약 40개 SVG 추출, §표 2개 신규 제작 요청
- [ ] `taxonomy.yaml` 작성과 생성 스크립트 수정 (카테고리·서비스 순서는 홈페이지 기준)
- [ ] 그룹 16종(Public/Private subnet 레이블 프리셋 포함)·화살표 6종 컨테이너 스타일 구현
- [ ] 컬러·블랙 라이브러리 생성, 샘플 구성도(PPT 10\~13쪽 예시)로 검증
- [ ] README, `service_icons.md`, PPT 다음 개정을 홈페이지 기준으로 갱신
- [ ] 홈페이지 서비스 목록이 바뀔 때 분류표를 다시 맞추는 주기(예: 분기 1회) 정하기
