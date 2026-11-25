/* Jacksonville Mobile Mechanics — design preview by RGWebD */
(function(){
"use strict";
var RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var d=document,root=d.documentElement;
if(!RM) root.classList.add('js');

/* loader (home only, once per session) */
var L=d.querySelector('.loader');
if(L){
  var seen=false; try{seen=sessionStorage.getItem('jmm-l')==='1'}catch(e){}
  if(RM||seen){L.remove()}else{
    try{sessionStorage.setItem('jmm-l','1')}catch(e){}
    var tks=L.querySelectorAll('.tk'),cnt=L.querySelector('[data-hr]'),i=0;
    var iv=setInterval(function(){ if(i<tks.length){tks[i].classList.add('on');if(cnt)cnt.textContent=String(i+1).padStart(2,'0')+':00';i++} else {clearInterval(iv);setTimeout(function(){L.classList.add('done');setTimeout(function(){L.remove()},1100)},180)} },48);
  }
}

/* nav state + progress */
var nav=d.querySelector('.nav'),bar=d.querySelector('.progress');
function onScroll(){var y=window.scrollY,h=root.scrollHeight-innerHeight;if(nav)nav.classList.toggle('scrolled',y>30);if(bar)bar.style.transform='scaleX('+(h>0?y/h:0)+')';tl();para(y)}
addEventListener('scroll',onScroll,{passive:true});

/* mobile menu */
var mb=d.querySelector('.menu-btn'),mm=d.getElementById('mmenu');
function closeM(){d.body.classList.remove('menu-open');mb&&mb.setAttribute('aria-expanded','false');mm&&mm.setAttribute('aria-hidden','true')}
if(mb){mb.addEventListener('click',function(){var o=d.body.classList.toggle('menu-open');mb.setAttribute('aria-expanded',o);mm.setAttribute('aria-hidden',!o);if(o){var f=mm.querySelector('a');f&&f.focus()}});
 mm.querySelectorAll('a').forEach(function(a){a.addEventListener('click',closeM)});
 d.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.body.classList.contains('menu-open')){closeM();mb.focus()}});}

/* live clock — Jacksonville is America/New_York; listing says Open 24 hours */
var clocks=d.querySelectorAll('[data-clock]');
function tick(){var t;try{t=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'}).format(new Date())}catch(e){t=''}
 clocks.forEach(function(c){c.innerHTML=t?('<span class="sfx">It\u2019s </span>'+t+' in Jax<span class="sfx"> \u2014 we\u2019re open</span>'):''})}
if(clocks.length){tick();setInterval(tick,15000)}

/* reveals */
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08}):null;
d.querySelectorAll('.rv,.split').forEach(function(el){if(io&&!RM)io.observe(el);else el.classList.add('in')});

/* counters + gauges (land exactly on real values) */
function count(el){var to=parseFloat(el.dataset.to),dec=parseInt(el.dataset.dec||'0',10),dur=1800,s=null;
 if(RM){el.textContent=to.toFixed(dec);return}
 function f(ts){if(!s)s=ts;var p=Math.min((ts-s)/dur,1),e=1-Math.pow(1-p,4);el.textContent=(to*e).toFixed(dec);if(p<1)requestAnimationFrame(f);else el.textContent=to.toFixed(dec)}requestAnimationFrame(f)}
var gio=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;var g=e.target;
  g.querySelectorAll('[data-to]').forEach(count);
  var v=g.querySelector('.val');if(v){var c=parseFloat(v.getAttribute('stroke-dasharray'));v.style.strokeDashoffset=String(c*(1-parseFloat(v.dataset.frac)))}
  gio.unobserve(g)})},{threshold:.35}):null;
d.querySelectorAll('.gauge,.cnt').forEach(function(g){if(gio)gio.observe(g);else{g.querySelectorAll('[data-to]').forEach(count);var v=g.querySelector('.val');if(v)v.style.strokeDashoffset=String(parseFloat(v.getAttribute('stroke-dasharray'))*(1-parseFloat(v.dataset.frac)))}});

/* timeline draw */
var T=d.querySelector('.tl'),steps=T?T.querySelectorAll('.step'):[];
function tl(){if(!T)return;var r=T.getBoundingClientRect(),mid=innerHeight*.6,p=Math.max(0,Math.min(1,(mid-r.top)/r.height));T.style.setProperty('--p',RM?1:p);
 steps.forEach(function(s){var sr=s.getBoundingClientRect();s.classList.toggle('lit',RM||sr.top<mid)})}

/* hero parallax (big type + photo) */
var px=d.querySelectorAll('[data-px]');
function para(y){if(RM)return;px.forEach(function(el){el.style.transform='translate3d(0,'+(y*parseFloat(el.dataset.px))+'px,0)'})}

/* tilt cards + magnetic buttons (pointer: fine only) */
if(!RM&&matchMedia('(pointer:fine)').matches){
 d.querySelectorAll('[data-tilt]').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='rotateY('+(x*10)+'deg) rotateX('+(-y*10)+'deg)'});c.addEventListener('pointerleave',function(){c.style.transform=''})});
 d.querySelectorAll('.mag').forEach(function(b){b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect(),x=e.clientX-r.left-r.width/2,y=e.clientY-r.top-r.height/2;b.style.transform='translate('+x*.22+'px,'+y*.3+'px)'});b.addEventListener('pointerleave',function(){b.style.transform=''})});
}

/* hotspots (tap to toggle on touch) */
d.querySelectorAll('.hot').forEach(function(h){h.addEventListener('click',function(){var o=h.classList.toggle('open');h.setAttribute('aria-expanded',o);d.querySelectorAll('.hot').forEach(function(x){if(x!==h){x.classList.remove('open');x.setAttribute('aria-expanded','false')}})})});

/* day/night slider */
d.querySelectorAll('.dn').forEach(function(w){var k=w.querySelector('.knob'),drag=false;
 function set(p){p=Math.max(4,Math.min(96,p));w.style.setProperty('--x',p+'%');k.setAttribute('aria-valuenow',Math.round(p))}
 function mv(e){var r=w.getBoundingClientRect();set((e.clientX-r.left)/r.width*100)}
 w.addEventListener('pointerdown',function(e){drag=true;w.setPointerCapture(e.pointerId);mv(e)});
 w.addEventListener('pointermove',function(e){if(drag)mv(e)});
 w.addEventListener('pointerup',function(){drag=false});w.addEventListener('pointercancel',function(){drag=false});
 k.addEventListener('keydown',function(e){var v=parseFloat(k.getAttribute('aria-valuenow'));if(e.key==='ArrowLeft'){set(v-5);e.preventDefault()}if(e.key==='ArrowRight'){set(v+5);e.preventDefault()}});
 if(!RM&&io){var once=new IntersectionObserver(function(es){if(es[0].isIntersecting){once.disconnect();var t0=null;function an(ts){if(drag)return;if(!t0)t0=ts;var p=(ts-t0)/1600;if(p>1)return;set(50+Math.sin(p*Math.PI*2)*22);requestAnimationFrame(an)}requestAnimationFrame(an)}},{threshold:.5});once.observe(w)}
});

/* reviews carousel — pauses on hover/focus */
d.querySelectorAll('.car-root').forEach(function(rt){var sl=rt.querySelectorAll('.slide'),ds=rt.querySelectorAll('.dots button'),n=0,tm=null,paused=false;
 function go(i){n=(i+sl.length)%sl.length;sl.forEach(function(s,j){s.classList.toggle('on',j===n);s.setAttribute('aria-hidden',j!==n)});ds.forEach(function(b,j){b.setAttribute('aria-current',j===n)})}
 function play(){clearInterval(tm);if(!RM)tm=setInterval(function(){if(!paused)go(n+1)},6500)}
 rt.querySelector('.pv').addEventListener('click',function(){go(n-1);play()});
 rt.querySelector('.nx').addEventListener('click',function(){go(n+1);play()});
 ds.forEach(function(b,j){b.addEventListener('click',function(){go(j);play()})});
 rt.addEventListener('mouseenter',function(){paused=true});rt.addEventListener('mouseleave',function(){paused=false});
 rt.addEventListener('focusin',function(){paused=true});rt.addEventListener('focusout',function(){paused=false});
 go(0);play()});

/* gallery drag-scroll */
d.querySelectorAll('.rail-g').forEach(function(r){var down=false,sx=0,sl=0,moved=false;
 r.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse')return;down=true;moved=false;sx=e.clientX;sl=r.scrollLeft});
 addEventListener('pointermove',function(e){if(!down)return;var dx=e.clientX-sx;if(Math.abs(dx)>5){moved=true;r.classList.add('drag')}r.scrollLeft=sl-dx});
 addEventListener('pointerup',function(){if(down){down=false;setTimeout(function(){r.classList.remove('drag')},0)}});
 r.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true)});

/* filters */
d.querySelectorAll('.filters').forEach(function(f){var bs=f.querySelectorAll('button'),items=d.querySelectorAll('.masonry .gi');
 bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.setAttribute('aria-pressed',x===b)});var k=b.dataset.f;items.forEach(function(it){it.hidden=!(k==='all'||it.dataset.cat.indexOf(k)>-1)})})})});

/* lightbox: keyboard, swipe, focus trap */
var lb=d.querySelector('.lb');
if(lb){var im=lb.querySelector('img'),cap=lb.querySelector('figcaption'),ct=lb.querySelector('.ct'),list=[],idx=0,last=null;
 function vis(){return Array.prototype.filter.call(d.querySelectorAll('[data-lb]'),function(b){return !b.closest('[hidden]')})}
 function show(i){idx=(i+list.length)%list.length;var b=list[idx];im.src=b.dataset.lb;im.alt=b.querySelector('img').alt;cap.textContent=b.dataset.cap||'';ct.textContent=(idx+1)+' / '+list.length}
 function open(b){list=vis();last=b;show(list.indexOf(b));lb.classList.add('open');lb.setAttribute('aria-hidden','false');d.body.style.overflow='hidden';lb.querySelector('.x').focus()}
 function close(){lb.classList.remove('open');lb.setAttribute('aria-hidden','true');d.body.style.overflow='';last&&last.focus()}
 d.querySelectorAll('[data-lb]').forEach(function(b){b.addEventListener('click',function(){open(b)})});
 lb.querySelector('.x').addEventListener('click',close);lb.querySelector('.pv').addEventListener('click',function(){show(idx-1)});lb.querySelector('.nx').addEventListener('click',function(){show(idx+1)});
 lb.addEventListener('click',function(e){if(e.target===lb)close()});
 d.addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowRight')show(idx+1);if(e.key==='ArrowLeft')show(idx-1);
  if(e.key==='Tab'){var f=lb.querySelectorAll('button'),a=f[0],z=f[f.length-1];if(e.shiftKey&&d.activeElement===a){z.focus();e.preventDefault()}else if(!e.shiftKey&&d.activeElement===z){a.focus();e.preventDefault()}}});
 var tx=null;lb.addEventListener('touchstart',function(e){tx=e.touches[0].clientX},{passive:true});lb.addEventListener('touchend',function(e){if(tx===null)return;var dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>45)show(idx+(dx<0?1:-1));tx=null});
}

/* text-us form → pre-filled SMS (nothing is submitted anywhere) */
var fm=d.getElementById('txtform');
if(fm){fm.addEventListener('submit',function(e){e.preventDefault();var g=function(n){return (fm.elements[n].value||'').trim()};
 var body='Hi! '+(g('name')?'This is '+g('name')+'. ':'')+(g('vehicle')?'Vehicle: '+g('vehicle')+'. ':'')+(g('where')?'Location: '+g('where')+'. ':'')+(g('issue')?'Issue: '+g('issue'):'');
 var ios=/iPad|iPhone|iPod|Macintosh/.test(navigator.userAgent);location.href='sms:'+fm.dataset.tel+(ios?'&':'?')+'body='+encodeURIComponent(body)})}

/* demo pill */
var dp=d.querySelector('.demo');if(dp){try{if(sessionStorage.getItem('jmm-demo')==='x')dp.classList.add('gone')}catch(e){}
 dp.querySelector('button').addEventListener('click',function(){dp.classList.add('gone');try{sessionStorage.setItem('jmm-demo','x')}catch(e){}})}

d.querySelectorAll('[data-year]').forEach(function(y){y.textContent=new Date().getFullYear()});
onScroll();
})();
