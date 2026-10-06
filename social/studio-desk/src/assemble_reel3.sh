#!/bin/bash
cd "$(dirname "$0")"
NODE_PATH=$(npm root -g) node - <<'JS'
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
for(const f of ['o1','o2','o3']){const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+path.resolve(f+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);await p.screenshot({path:f+'.png',omitBackground:true});await p.close();}
await b.close();})();
JS
FF=$(cat ../../ffpath); G=../gen
clip(){ $FF -y -loglevel error -i $G/$1.mp4 -loop 1 -t 5.04 -i $2.png -filter_complex "[0:v]scale=1080:1920:flags=lanczos,fps=30,noise=alls=7:allf=t+u,format=yuv420p[v];[1:v]format=rgba,fade=t=in:st=0.5:d=0.7:alpha=1,fade=t=out:st=4.3:d=0.5:alpha=1[o];[v][o]overlay=0:0:shortest=1,format=yuv420p[out]" -map "[out]" -t 5.04 -c:v libx264 -preset medium -crf 21 -r 30 -pix_fmt yuv420p $3; }
clip k_honey o1 s1.mp4 && clip k_oil o2 s2.mp4 && clip k_sumac o3 s3.mp4 && $FF -y -loglevel error -i s1.mp4 -i s2.mp4 -i s3.mp4 -i s4.mp4 -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.25:offset=4.79[x1];[x1][2:v]xfade=transition=fade:duration=0.25:offset=9.58[x2];[x2][3:v]xfade=transition=fade:duration=0.4:offset=14.37[x3]" -map "[x3]" -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -r 30 -movflags +faststart reel-3-three-pours.mp4 && $FF -y -loglevel error -i reel-3-three-pours.mp4 -vf "select='eq(n\,60)+eq(n\,200)+eq(n\,340)',scale=360:-1,tile=3x1" -frames:v 1 -vsync vfr r3_check.jpg && echo R3DONE
