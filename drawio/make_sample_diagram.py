"""리포지토리 아이콘을 임베드한 draw.io 예시 구성도(.drawio) 생성."""
import base64
import html
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()

cells = []
_id = [10]


def uri(rel: str) -> str:
    p = ROOT / rel
    b64 = base64.b64encode(p.read_text(encoding="utf-8").encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml,{b64}"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def nid() -> str:
    _id[0] += 1
    return f"n{_id[0]}"


def group(label, rel, x, y, w, h, stroke, fill, parent="1"):
    i = nid()
    style = (
        "rounded=0;html=1;whiteSpace=wrap;container=1;collapsible=0;recursiveResize=0;"
        f"pointerEvents=0;fillColor={fill};strokeColor={stroke};dashed=1;dashPattern=8 4;"
        "verticalAlign=top;align=left;spacingLeft=40;spacingTop=6;fontSize=13;"
        f"fontStyle=1;fontColor={stroke};"
    )
    cells.append(
        f'<mxCell id="{i}" value="{esc(label)}" style="{esc(style)}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
    )
    badge = (
        "shape=image;html=1;imageAspect=0;aspect=fixed;movable=0;resizable=0;"
        f"rotatable=0;deletable=0;editable=0;connectable=0;image={uri(rel)};"
    )
    cells.append(
        f'<mxCell id="{nid()}" value="" style="{esc(badge)}" vertex="1" parent="{i}">'
        f'<mxGeometry x="8" y="8" width="26" height="26" as="geometry"/></mxCell>'
    )
    return i


def icon(label, rel, x, y, parent="1", size=58):
    i = nid()
    style = (
        "shape=image;html=1;labelBackgroundColor=none;imageAspect=0;aspect=fixed;"
        "verticalLabelPosition=bottom;verticalAlign=top;fontSize=11;fontColor=#333333;"
        f"image={uri(rel)};"
    )
    cells.append(
        f'<mxCell id="{i}" value="{esc(label)}" style="{esc(style)}" vertex="1" parent="{parent}">'
        f'<mxGeometry x="{x}" y="{y}" width="{size}" height="{size}" as="geometry"/></mxCell>'
    )
    return i


def edge(src, dst, label="", dashed=0, color="#5B6B7C"):
    style = (
        "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jettySize=auto;orthogonalLoop=1;"
        f"strokeColor={color};strokeWidth=1.5;fontSize=10;fontColor={color};"
        f"endArrow=blockThin;endFill=1;dashed={dashed};"
    )
    cells.append(
        f'<mxCell id="{nid()}" value="{esc(label)}" style="{esc(style)}" edge="1" '
        f'parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>'
    )


# ---------------------------------------------------------------- 레이아웃

S = "files/services"
G = "files/general_icons/color"
B = "files/box_type/black"

user = icon("사용자", f"{G}/General_Resources_Icon_External_User_dk.svg", 60, 330)
cdn = icon("CDN", f"{S}/content_delivery/color/ic-content_delivery-cdn.svg", 60, 500)
obs = icon("Object Storage", f"{S}/storage/color/ic-storage-object_storage.svg", 60, 670)

region = group("NHN Cloud / 한국(평촌) 리전",
               f"{B}/General_Resources_Groups_Region.svg",
               260, 60, 900, 800, "#8C9BAB", "#F7F9FB")
vpc = group("VPC  10.0.0.0/16", f"{B}/General_Resources_Groups_VPC.svg",
            40, 60, 820, 700, "#125DE6", "none", parent=region)

pub = group("Public Subnet  10.0.1.0/24", f"{G}/Subnet_dk.svg",
            40, 60, 740, 140, "#2BA84A", "none", parent=vpc)
igw = icon("Internet Gateway", f"{S}/network/color/ic-network-internet_gateway.svg",
           50, 50, parent=pub)
lb = icon("Load Balancer", f"{S}/network/color/ic-network-load_balancer.svg",
          290, 50, parent=pub)
nat = icon("NAT Gateway", f"{S}/network/color/ic-network-nat_gateway.svg",
           550, 50, parent=pub)

app = group("Private Subnet (App)  10.0.11.0/24",
            f"{B}/General_Resources_Groups_Private subnet.svg",
            40, 230, 740, 270, "#7A4FD6", "none", parent=vpc)
web1 = icon("Web #1", f"{S}/compute/color/ic-compute-instance.svg", 90, 55, parent=app)
web2 = icon("Web #2", f"{S}/compute/color/ic-compute-instance.svg", 90, 175, parent=app)
was1 = icon("WAS #1", f"{S}/application_service/color/ic-application_service-jeus_instance.svg",
            430, 55, parent=app)
was2 = icon("WAS #2", f"{S}/application_service/color/ic-application_service-jeus_instance.svg",
            430, 175, parent=app)

dbs = group("Private Subnet (DB)  10.0.21.0/24",
            f"{B}/General_Resources_Groups_Private subnet.svg",
            40, 530, 740, 110, "#7A4FD6", "none", parent=vpc)
rds = icon("RDS for MySQL", f"{S}/database/color/ic-database-rds_for_mysql.svg",
           150, 32, parent=dbs)
cache = icon("EasyCache", f"{S}/database/color/ic-database-easycache.svg",
             470, 32, parent=dbs)

edge(user, igw, "HTTPS")
edge(igw, lb)
edge(lb, web1)
edge(lb, web2)
edge(web1, was1)
edge(web2, was2)
edge(was1, rds)
edge(was2, rds)
edge(was1, cache, "", 1)
edge(user, cdn, "정적 콘텐츠")
edge(cdn, obs, "origin", 1)

# ---------------------------------------------------------------- 출력

model = (
    '<mxfile host="app.diagrams.net" type="device">'
    '<diagram name="NHN Cloud 3-Tier">'
    '<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
    'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" '
    'pageHeight="1169" math="0" shadow="0"><root>'
    '<mxCell id="0"/><mxCell id="1" parent="0"/>'
    + "".join(cells)
    + "</root></mxGraphModel></diagram></mxfile>"
)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(model, encoding="utf-8")
print(f"{OUT}  ({OUT.stat().st_size/1024:.1f} KB, {len(cells)} cells)")
