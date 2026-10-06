// usage: node shoot.js W H file1.html file2.html ...   -> file.png
const {chromium}=require('playwright');const path=require('path');
(async()=>{
  const [W,H,...files]=process.argv.slice(2);
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  for(const f of files){
    const p=await b.newPage({viewport:{width:+W,height:+H},deviceScaleFactor:1});
    await p.goto('file://'+path.resolve(f)); await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(700);
    if(await p.evaluate(()=>typeof window.setT==='function')) await p.evaluate(()=>window.setT(99));
    await p.screenshot({path:f.replace('.html','.png')}); console.log('wrote',f.replace('.html','.png')); await p.close();
  }
  await b.close();
})();
