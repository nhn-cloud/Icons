# dist

`taxonomy.yaml`과 `icons/`에서 생성한 draw.io 라이브러리입니다. **손으로 고치지 마세요.**

```
python tools/make_drawio_libs.py        # 생성
python tools/make_drawio_libs.py --dry-run
```

생성물이지만 커밋합니다. draw.io `clibs` 링크가 GitHub raw URL을 직접 읽기 때문에
저장소에 파일이 있어야 배포가 됩니다.

팔레트 1개 = XML 1개입니다. `color/` 26개, `black/` 25개, 엔트리 421개.
서비스 아이콘 64px, 리소스 아이콘 48px, 그룹 컨테이너와 서비스 박스는
320×200 컨테이너 도형(`container=1`)으로 생성합니다.
