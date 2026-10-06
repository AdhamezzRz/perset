// usage: node render.js page.html outDir fps duration png|jpeg transparent(0|1)
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{
  const [html,out,fps,dur,fmt,tr]=process.argv.slice(2);
  fs.rmSync(out,{recursive:true,force:true}); fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve(html)); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(800);
  const n=Math.round(parseFloat(dur)*parseInt(fps));
  for(let i=0;i<n;i++){
    await p.evaluate(t=>window.setT(t), i/parseInt(fps));
    const ext=fmt==='jpeg'?'jpg':'png';
    const opts={path:`${out}/f${String(i).padStart(4,'0')}.${ext}`, type:fmt};
    if(fmt==='jpeg') opts.quality=93; if(tr==='1') opts.omitBackground=true;
    await p.screenshot(opts);
  }
  await b.close(); console.log('rendered',n,'frames to',out);
})();
