/* EMBER V29: restore original console header; keep optional demo presets unobtrusive. */
(()=>{
'use strict';
const title='Cross-Gravity Combustion Analysis Console';
const hero=document.querySelector('.page-head .head-copy');
const heading=hero?.querySelector('h1');
const subtitle=hero?.querySelector('p');
if(heading)heading.textContent=title;
if(subtitle)subtitle.textContent='Model-scoped combustion analysis Â· traceable NASA evidence Â· explicit scientific limits';
document.title='EMBER â Cross-Gravity Combustion Analysis Console';
const ribbon=document.getElementById('emberDemoRouteV27');
const presets=document.getElementById('emberDemoPresetsV28');
const form=document.getElementById('scenarioForm');
if(presets&&form){
 const parent=document.createElement('details');
 parent.id='emberDemoOptionsV29';
 parent.className='ember-demo-options';
 parent.setAttribute('aria-label','Optional demo scenarios');
 const summary=document.createElement('summary');
 summary.textContent='Demo presets (optional)';
 summary.title='Reveal the two tested demonstration scenarios';
 parent.appendChild(summary);
 presets.parentElement?.removeChild(presets);
 parent.appendChild(presets);
 form.insertAdjacentElement('afterend',parent);
}
if(ribbon)ribbon.remove();
})();

