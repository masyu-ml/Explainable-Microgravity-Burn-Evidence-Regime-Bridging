/* EMBER V30 — NASA evidence synthesis, grounded in existing experiment records. */
(()=>{
'use strict';
if(document.getElementById('emberSynthesisV30'))return;
const panel=document.getElementById('nasaExplorer');if(!panel)return;
const el=(t,c,v)=>{const n=document.createElement(t);if(c)n.className=c;if(v!==undefined)n.textContent=String(v);return n};
const css=el('style');
css.textContent='#emberSynthesisV30{margin:13px 0 16px;display:flex;flex-direction:column;gap:12px;color:#d8eaf1;font:12px/1.6 Inter,system-ui,sans-serif}#emberSynthesisV30 *{box-sizing:border-box}#emberSynthesisV30 .es-hero{background:linear-gradient(130deg,#112d3d,#0c1f2b);border:1px solid #446b7c;border-left:4px solid #78cbd9;border-radius:11px;padding:15px}#emberSynthesisV30 .es-row{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap}#emberSynthesisV30 .es-kicker{font-size:10px;font-weight:700;color:#98d9e9;letter-spacing:.1em;text-transform:uppercase}#emberSynthesisV30 .es-status{font-size:9px;padding:2px 9px;border:1px solid #517c8a;border-radius:30px;color:#cedfe7}#emberSynthesisV30 h3{font-size:18px;line-height:1.3;color:#f2fbff;font-weight:650;margin:10px 0}#emberSynthesisV30 .es-main{margin:0;font-size:12px;line-height:1.75;color:#d8e9f0}#emberSynthesisV30 .es-context{font-size:10px;color:#abc5d2;margin:10px 0 0}#emberSynthesisV30 a{color:#96ddec;text-underline-offset:3px}#emberSynthesisV30 h4{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:#e5f4fa;margin:0 0 8px}#emberSynthesisV30 .es-findings{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px}#emberSynthesisV30 .es-finding{border:1px solid #395a67;background:#102734;border-radius:9px;padding:11px;min-width:0}#emberSynthesisV30 .es-finding strong{display:block;font-size:11px;color:#cae9f4;margin:0 0 4px}#emberSynthesisV30 .es-finding p{font-size:11px;line-height:1.65;color:#c6dbe4;overflow-wrap:anywhere;margin:0}#emberSynthesisDetailsV30{border:1px solid #355868;border-radius:9px;background:#10232e;min-width:0}#emberSynthesisDetailsV30>summary{cursor:pointer;list-style:none;padding:13px;min-height:44px;color:#e7f6fb;font-size:12px;font-weight:650}#emberSynthesisDetailsV30>summary::-webkit-details-marker{display:none}#emberSynthesisDetailsV30>summary:after{content:" +";float:right;color:#a1d9e7;font-size:16px}#emberSynthesisDetailsV30[open]>summary:after{content:" −"}#emberSynthesisDetailsV30>summary:focus-visible{outline:2px solid #9adff4}#emberSynthesisDetailsV30>.es-detail-body{padding:9px;border-top:1px solid #355060;min-width:0}@media(max-width:820px){#emberSynthesisV30 .es-findings{grid-template-columns:1fr}}';
document.head.append(css);
const section=el('section');section.id='emberSynthesisV30';section.setAttribute('aria-label','NASA evidence brief and findings');
const hero=el('div','es-hero'),header=el('div','es-row'),kicker=el('span','es-kicker','01 · Evidence Summary'),status=el('span','es-status','AWAITING ANALYSIS');
header.append(kicker,status);const title=el('h3','','What the retrieved NASA evidence shows');
const summary=el('p','es-main','Run a scenario to summarize documented experimental records, measurements and data gaps. EMBER will not infer a burn outcome from similarity columns.');
summary.setAttribute('aria-live','polite');
const context=el('p','es-context','Only source-grounded conclusions are shown. ISS microgravity is distinct from lunar and Martian gravity.');
const citation=el('p','es-context','Primary source: ');
const sourceLink=el('a','','NASA BASS-II Summary Report');sourceLink.href='https://ntrs.nasa.gov/citations/20210011385';sourceLink.target='_blank';sourceLink.rel='noopener noreferrer';citation.append(sourceLink);
hero.append(header,title,summary,context,citation);
const findings=el('section');findings.append(el('h4','','02 · Key Findings'));
const cards=el('div','es-findings'),cardBodies=[];
[['Observed evidence','Experiment measurements and outcome annotations will be counted separately.'],['Scenario comparison','The selected conditions will be compared against the evidence scope.'],['Missing information','Unreported test outcomes and missing parameters will be highlighted.'],['Scientific limits','Metadata similarity is not evidence of equivalent flame behavior.']].forEach(([h,p])=>{const c=el('div','es-finding');c.append(el('strong','',h));const body=el('p','',p);c.append(body);cards.append(c);cardBodies.push(body)});
findings.append(cards);section.append(hero,findings);
const detail=el('details');detail.id='emberSynthesisDetailsV30';
detail.append(el('summary','','03 · Detailed Evidence — Records, Columns, Comparisons & Gower Scores'));
const inside=el('div','es-detail-body');detail.append(inside);
const heading=[...panel.children].find(x=>x.classList?.contains('panel-head'));
[...panel.children].forEach(x=>{if(x!==heading)inside.append(x)});
if(heading)heading.insertAdjacentElement('afterend',section);else panel.prepend(section);
section.insertAdjacentElement('afterend',detail);
let seq=0;
const fmt=(v,d=1)=>v!==null&&v!==undefined&&Number.isFinite(+v)?(+v).toFixed(d):'not reported';
const gravity=g=>Math.abs(+g-1)<.02?'Earth gravity':Math.abs(+g-.38)<.03?'Martian gravity':Math.abs(+g-.166)<.03?'lunar gravity':+g<.01?'near-microgravity':fmt(g,3)+' g';
const finding=(i,s)=>cardBodies[i].textContent=s;
const coverage=report=>Array.isArray(report?.evidence?.results)?report.evidence.results:[];
function render(report,s,records,error){
 const matches=coverage(report),count=records.length,annotated=records.filter(r=>r.outcome_class&&r.outcome_class!=='NOT_REPORTED'&&r.outcome_class!=='UNKNOWN').length;
 const rates=records.reduce((n,r)=>n+(r.measurements||[]).filter(m=>m.spread_rate_mm_s!==null&&Number.isFinite(+m.spread_rate_mm_s)).length,0);

 const observedRates=records.flatMap(r=>(r.measurements||[]).map(m=>m.spread_rate_mm_s).filter(v=>v!==null&&v!==undefined&&Number.isFinite(+v)).map(Number));
 const classTotals={};
 for(const r of records){
   const k=r.outcome_class;
   if(k&&k!=='NOT_REPORTED'&&k!=='UNKNOWN')classTotals[k]=(classTotals[k]||0)+1;
 }
 const labels={QUENCHED:'quenched',NO_IGNITION:'no ignition',BLOWOFF:'blowoff',NO_BLOWOFF:'no blowoff',IGNITION_OBSERVED:'ignition observed',ONE_SIDED_FLAME:'one-sided flame'};
 const grouped=Object.entries(classTotals).sort((a,b)=>b[1]-a[1]);
 const examples=grouped.slice(0,4).map(([k,n])=>n+' '+(labels[k]||k.toLowerCase().replaceAll('_',' '))).join(', ');
 const additional=grouped.slice(4).reduce((n,x)=>n+x[1],0);
 const outcomes=annotated?'NASA report-derived outcome annotations include '+examples+(additional?' and '+additional+' in other categories':'')+'.':'No overall outcome categories are classified for these tests in EMBER’s present catalog.';
 const spreadRange=observedRates.length?' Reported spread-rate measurements range from '+fmt(Math.min(...observedRates),3)+' to '+fmt(Math.max(...observedRates),3)+' mm/s across different documented test conditions.':'';

 const alerts=records.filter(r=>r.oxygen_warning).length,notClassified=count-annotated;
 const material=s.material||'selected material',g=gravity(s.gravity_g);
 const o2=fmt(+s.oxygen_fraction*100,1),flow=fmt(+s.forced_flow_m_s*100,1),press=fmt(s.pressure_kpa,1);
 const indexed=material==='PMMA'||material==='SIBAL';
 const top=matches.length&&Number.isFinite(+matches[0].score)&&matches[0].score!==null?' Highest metadata retrieval score: '+fmt(+matches[0].score*100,1)+'% (not physical equivalence).':'';
 status.textContent=error?'SOURCE INCOMPLETE':'EVIDENCE-GROUNDED';
 title.textContent='NASA evidence for '+material;
 context.textContent='User-defined target: '+material+' · '+g+' · '+press+' kPa · '+o2+'% oxygen · '+flow+' cm/s airflow. Original BASS-II experiments were performed in ISS microgravity.';
 if(error){
   summary.textContent='The NASA experiment-level service is unavailable or returned an incomplete record page. EMBER retrieved '+matches.length+' curated research-condition match(es), but cannot verify experimental outcomes from them. No burn conclusion is supported.';
   finding(0,'Experiment-level observations cannot be counted while the source endpoint is unavailable.');
   finding(1,'This scenario has not been shown equivalent to a reported NASA test.');
   finding(2,'Missing outcomes cannot be accurately enumerated until the experiment data is available.');
   finding(3,'A metadata ranking is not a flame prediction or safety assessment.');
   return;
 }
 if(!indexed){
   const threshold=report?.threshold_lookup?.status==='NASA_OBSERVED_THRESHOLD';
   summary.textContent='EMBER’s experiment-level BASS-II subset contains PMMA and SIBAL records, not direct '+material+' tests. '+matches.length+' related literature-condition match(es) were retrieved.'+(threshold?' A separate NASA historical oxygen-threshold reference is available; it is not a threshold prediction for this input.':' These matches do not establish an observed combustion outcome for the chosen scenario.')+top;
   finding(0,threshold?'A historical NASA oxygen-threshold reference is available; its published test conditions must be retained.':'No material-specific experiment outcome is indexed in this particular BASS-II subset.');
   finding(1,'The input '+g+' environment is not validated as equivalent to reported experiment conditions.');
   finding(2,'A missing record in this subset does not mean NASA has never studied the material.');
   finding(3,'No unsupported inference about ignition, flame spread or extinguishment is made.');
   return;
 }
 summary.textContent='For '+material+', NASA BASS-II indexed '+count+' ISS microgravity test record(s) and '+rates+' reported video-tracked spread-rate measurement(s).'+spreadRange+' '+outcomes+' '+notClassified+' record(s) have no classified overall outcome in this subset. EMBER separately retrieved '+matches.length+' literature-condition match(es). None of these findings establishes flame behavior for your selected '+g+' chamber.'+top;
 finding(0,count+' NASA experiment(s) and '+rates+' measured spread-rate value(s). '+outcomes+' These observations describe their original test conditions, not a simulation.');
 finding(1,'NASA BASS-II reports ISS microgravity rather than the selected '+g+'. Your pressure '+press+' kPa, oxygen '+o2+'%, and flow '+flow+' cm/s must not be assumed experimentally matched.');
 finding(2,notClassified+' record(s) lack classified outcomes. Per-test measured pressure and gravity are unavailable here.'+(alerts?' '+alerts+' oxygen-data warning(s) require careful source review.':''));
 finding(3,'The original specimen geometry and test protocol matter. Gower proximity cannot validate combustion chemistry, flame equivalence or spacecraft fire safety.');
}
async function update(report,s){
 if(!report||!s)return;
 const token=++seq;status.textContent='CHECKING SOURCES';title.textContent='Preparing scientific evidence brief';
 summary.textContent='Checking the returned literature records against NASA BASS-II experiment-level entries.';
 let records=[],err=false;
 if(s.material==='PMMA'||s.material==='SIBAL'){
   try{
     const q=new URLSearchParams({material:s.material,page:'1',per_page:'50'});
     const res=await fetch('/api/v3/experiments?'+q,{cache:'no-store'});
     if(!res.ok)throw Error('NASA experiment service error');
     const data=await res.json();
     if(!Array.isArray(data.results)||Number(data.total)>data.results.length)throw Error('Incomplete results');
     records=data.results.map(x=>x.record).filter(Boolean);
   }catch(e){err=true}
 }
 if(token===seq)render(report,s,records,err);
}
const prior=window.renderNASAExplorer;
if(typeof prior==='function')window.renderNASAExplorer=function(report,scenario){const r=prior.apply(this,arguments);update(report,scenario);return r};
document.getElementById('scenarioForm')?.addEventListener('submit',()=>{status.textContent='ANALYSIS REQUESTED'},true);
})();