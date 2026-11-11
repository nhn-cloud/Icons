# dist

`taxonomy.yaml`과 `icons/`에서 생성한 draw.io 라이브러리입니다. **손으로 고치지 마세요.**

```
python tools/make_drawio_libs.py        # 생성
python tools/make_drawio_libs.py --dry-run
```

생성물이지만 커밋합니다. draw.io `clibs` 링크가 GitHub raw URL을 직접 읽기 때문에
저장소에 파일이 있어야 배포가 됩니다.

> [!Note]\
> 아직 비어 있습니다. `make_drawio_libs.py`가 구 디렉터리 구조를 읽도록 되어 있어,
> `taxonomy.yaml` 기반으로 고쳐야 생성할 수 있습니다. 재편 전 라이브러리는 `archive/drawio-v1/`에 있습니다.
