// Headless local UI regression checks. Never executes PLC evaluation/model APIs.
const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
(async()=>{
  const output=path.resolve(process.env.PLC_UI_CHECK_OUTPUT||'results/raw/ui_localization_20261111');fs.mkdirSync(output,{recursive:true});
  const browser=await chromium.launch({channel:'msedge',headless:true});
  try{
    const page=await browser.newPage({viewport:{width:1440,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.route('**/api/evaluate',route=>route.abort());
    await page.route('**/api/check-reference-model',route=>route.abort());
    await page.goto((process.env.PLC_UI_CHECK_URL||'http://127.0.0.1:8765')+'/?task=PUB001&scope=all');
    await page.waitForFunction(()=>gCurrentTask?.task.id==='PUB001');
    assert.equal(await page.locator('#language-select').inputValue(),'zh');
    assert.equal(await page.locator('.pilot-card').count(),32);
    assert.match(await page.locator('#review-details').innerText(),/中文|题意/);
    await page.screenshot({path:path.join(output,'zh-overview.png'),animations:'disabled'});
    const listing=await page.evaluate(async()=>await (await fetch('/api/tasks')).json());
    let formulaCount=0;
    for(const task of listing.tasks){
      await page.selectOption('#task-select',task.id);
      await page.waitForFunction(id=>gCurrentTask?.task.id===id,task.id);
      assert.equal(await page.locator('#ltl-container tbody tr').count(),task.properties_count);
      assert.equal(await page.locator('#review-details-card').isVisible(),true);
      assert.doesNotMatch(await page.locator('#ltl-container').innerText(),/译文缺失|公式已变化|尚无中文说明/);
      const check=await page.evaluate(()=>{
        let count=0;
        for(const prop of gCurrentTask.task.ltl){
          const el=document.createElement('div');el.innerHTML=formatSpec(prop.formula);
          if(el.textContent.replace(/\s/g,'')!==prop.formula.replace(/\s/g,''))throw new Error('Formula changed');
          const pairs=[...el.querySelectorAll('[data-pair]')].map(n=>n.dataset.pair);
          for(const pair of new Set(pairs))if(pairs.filter(p=>p===pair).length!==2)throw new Error('Unmatched bracket pair');
          count++;
        }
        return count;
      });formulaCount+=check;
    }
    assert.equal(formulaCount,244);
    await page.selectOption('#task-select','PUB003');
    await page.waitForFunction(()=>gCurrentTask?.task.id==='PUB003');
    await page.locator('#ltl-container').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(output,'zh-specifications.png'),animations:'disabled'});
    const source='(* retained editor content *)\nFUNCTION_BLOCK FB_Task\nEND_FUNCTION_BLOCK';
    await page.locator('[data-tab="sandbox"]').click();
    await page.locator('#st-source-code').fill(source);
    await page.selectOption('#language-select','en');
    assert.equal(await page.locator('#st-source-code').inputValue(),source);
    assert.equal(await page.locator('#task-select').inputValue(),'PUB003');
    assert.match(await page.locator('#task-overview').innerText(),/Alarm Handling/);
    assert.match(await page.locator('#review-details').innerText(),/Teacher-provided public task/);
    assert.match(await page.locator('#ltl-container').innerText(),/How to review a specification/);
    for(const tab of ['benchmark','trace','sandbox','explorer']){
      await page.locator(`[data-tab="${tab}"]`).click();
      assert.equal(await page.locator(`[data-tab="${tab}"]`).getAttribute('class'),'nav-tab active');
      assert.equal(await page.locator('#tab-'+tab).isVisible(),true);
      assert.doesNotMatch(await page.locator('#tab-'+tab).innerText(),/[\u4e00-\u9fff]/);
      const clipped=await page.locator(`[data-tab="${tab}"]`).evaluate(el=>el.scrollWidth>el.clientWidth+1);
      assert.equal(clipped,false);
    }
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.screenshot({path:path.join(output,'en-overview.png'),animations:'disabled'});
    await page.reload();
    await page.waitForFunction(()=>gCurrentTask?.task.id==='PUB003');
    assert.equal(await page.locator('#language-select').inputValue(),'en');
    assert.equal(await page.locator('#pilot-only').count(),0);
    await page.selectOption('#kind-filter','self');
    assert.equal(await page.locator('.pilot-card').count(),12);
    await page.locator('#task-search').fill('重试');
    assert.equal(await page.locator('.pilot-card').count(),1);
    await page.waitForFunction(()=>gCurrentTask?.task.id==='SELF012');
    await page.selectOption('#language-select','zh');
    assert.match(await page.locator('#review-details').innerText(),/组内自建题/);
    assert.doesNotMatch(await page.locator('#review-details').innerText(),/老师原题|老师公开题/);
    await page.setViewportSize({width:390,height:844});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1),true);
    await page.screenshot({path:path.join(output,'zh-mobile.png'),animations:'disabled'});
    assert.equal(await page.evaluate(()=>formatSpec('<img src=x onerror=alert(1)>').includes('<img')),false);
    assert.deepEqual(errors,[]);
    const result={status:'PASS',task_count:32,property_count:formulaCount,bilingual:true,editor_preserved_on_language_switch:true,filters:true,language_persists:true,mobile_no_page_overflow:true,raw_formula_text_preserved:true,browser_errors:errors,scope:'HEADLESS_UI_ONLY_NO_PLC_OR_MODEL_EXECUTION'};
    fs.writeFileSync(path.join(output,'browser_validation.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
