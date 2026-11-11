# dist

`taxonomy.yaml` 과 `icons/` 에서 생성한 draw.io 라이브러리입니다. **손으로 고치지 마세요.**

```
python tools/make_drawio_libs.py             # 생성
python tools/make_drawio_libs.py --dry-run   # 쓰지 않고 점검만
```

생성물이지만 커밋합니다. draw.io `clibs` 링크가 GitHub raw URL 을 직접 읽기 때문에
저장소에 파일이 있어야 배포가 됩니다.

팔레트 1개 = XML 1개, 전부 25개입니다. 컬러 SVG 만 제공하므로 테마 구분이 없습니다.
서비스 아이콘 64px, 리소스 아이콘 48px, 그룹 컨테이너와 서비스 박스는
320×200 컨테이너 도형(`container=1`)으로 생성합니다.

`taxonomy.yaml` 에서 사라진 팔레트의 XML 은 생성 시 자동으로 지워집니다.
