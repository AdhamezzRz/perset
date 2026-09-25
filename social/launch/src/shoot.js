const {chromium} = require('playwright');
const path=require('path');
(async()=>{
  const files = process.argv.slice(2);
  const browser = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  for (const f of files){
    const [w,h] = f.includes('reel') ? [1080,1920] : [1080,1350];
    const page = await browser.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
    await page.goto('file://'+path.resolve(f));
    await page.evaluate(()=>document.fonts.ready);
    await page.waitForTimeout(800);
    const out = f.replace('.html','.png');
    await page.screenshot({path:out, clip:{x:0,y:0,width:w,height:h}});
    console.log('wrote',out); await page.close();
  }
  await browser.close();
})();
