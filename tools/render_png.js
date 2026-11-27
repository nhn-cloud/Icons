// icons/**/*.svg 를 같은 자리에 *.png 로 만든다.
//
//     npm install                          # 한 번만 (package.json 의 @resvg/resvg-js)
//     npm run png                          # icons/ 전체, 60px
//     node tools/render_png.js icons 480   # 폴더·크기를 다르게 줄 때
//
// 저장소에서 Node 를 쓰는 곳은 여기뿐이다. 나머지 도구는 전부 Python 이라
// 평소에는 npm install 이 필요 없고, 아이콘을 더하거나 고쳤을 때만 돌리면 된다.
// 생성물(*.png)은 커밋한다 — 카탈로그의 PNG 단추가 그 파일을 집어 간다.
//
// 왜 Figma 에서 직접 내보내지 않는가
// --------------------------------
// 원본 Figma 파일(`03 Architecture icon`)은 타일이 1,300 개가 넘어 노드마다
// 내보내기를 거는 것이 현실적이지 않다. icons/ 의 SVG 가 이미 그 파일에서 뽑아
// 둔 같은 벡터라, 그것을 래스터로 굽는 편이 빠르고 카탈로그에 보이는 그림과
// 정확히 같다. Business 팔레트처럼 다른 Figma 파일에서 온 아이콘도 함께 덮는다.
//
// 크기 60px 은 SVG 캔버스와 1:1 이다. PPT 에 붙이면 약 1.6cm 로 들어와
// 장표에 바로 쓰기 좋은 크기다. 더 크게 쓸 일이 있으면 인자로 올리면 된다
// (벡터에서 굽는 것이라 어느 크기든 깨지지 않는다).
const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
const path = require('path');

const ROOT = process.argv[2] || path.join(__dirname, '..', 'icons');
const SIZE = Number(process.argv[3] || 60);

const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);

let made = 0;
const failed = [];
for (const f of walk(ROOT).filter((f) => f.endsWith('.svg'))) {
  try {
    const r = new Resvg(fs.readFileSync(f, 'utf8'), {
      fitTo: { mode: 'width', value: SIZE },
      background: 'rgba(0,0,0,0)',   // PPT 에 얹으므로 바탕은 비워 둔다
    });
    fs.writeFileSync(f.replace(/\.svg$/, '.png'), r.render().asPng());
    made++;
  } catch (e) {
    failed.push(path.relative(ROOT, f) + ' :: ' + e.message);
  }
}

console.log('PNG ' + made + '개 생성 (' + SIZE + 'px)');
if (failed.length) {
  console.log('실패 ' + failed.length + '건:');
  failed.forEach((x) => console.log('    ' + x));
  process.exitCode = 1;
}
