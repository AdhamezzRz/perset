const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve('table.html')); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(600);
  fs.rmSync('fr',{recursive:true,force:true}); fs.mkdirSync('fr');
  let n=0; const shot=async(k,bounce,foot)=>{await p.evaluate(([k,b,f])=>window.setState(k,b,f),[k,bounce,foot]); await p.screenshot({path:`fr/f${String(n++).padStart(4,'0')}.png`});};
  for(let i=0;i<10;i++) await shot(0,1,0);
  // 12fps: each piece: drop-in 1.18 -> 0.97 -> 1.0 then hold 2 = 5 frames
  for(let k=1;k<=24;k++){ for(const s of [1.18,0.97,1.0,1.0,1.0]) await shot(k,s,0); }
  for(let i=0;i<40;i++) await shot(24,1,Math.min(1,i/8));
  await b.close(); console.log('frames',n);
})();
