(function(){
'use strict';
var WA='905523508446', MAIL='info@sofilxloto.com', KEY='sofilx_teklif';
var U=function(p){if(location.protocol!=='file:'||!p||p.charAt(0)!=='/')return p;var r=window.__ROOT__||'';return r+(p==='/'?'index':p.replace(/^\//,'').split('?')[0])+'.html'+(p.indexOf('?')>-1?p.slice(p.indexOf('?')):'')};
var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};

/* menü */
var burger=$('.burger'), nav=$('.nav');
if(burger&&nav){burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o);document.body.style.overflow=o?'hidden':''})}
$$('.dd>button').forEach(function(b){
  b.addEventListener('click',function(e){e.stopPropagation();var d=b.parentNode,o=!d.classList.contains('open');$$('.dd.open').forEach(function(x){x.classList.remove('open')});d.classList.toggle('open',o);b.setAttribute('aria-expanded',o)});
});
document.addEventListener('click',function(e){if(!e.target.closest('.dd'))$$('.dd.open').forEach(function(x){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')})});
document.addEventListener('keydown',function(e){if(e.key==='Escape')$$('.dd.open').forEach(function(x){x.classList.remove('open')})});

/* galeri */
var main=$('.gal .main img');
$$('.thumbs button').forEach(function(t){t.addEventListener('click',function(){
  main.src=t.dataset.full;main.alt=t.dataset.alt||main.alt;$$('.thumbs button').forEach(function(x){x.setAttribute('aria-current','false')});t.setAttribute('aria-current','true')})});

/* teklif sepeti */
function load(){try{return JSON.parse(localStorage.getItem(KEY))||[]}catch(e){return []}}
function save(c){try{localStorage.setItem(KEY,JSON.stringify(c))}catch(e){}badge(c)}
function badge(c){var n=(c||load()).reduce(function(a,i){return a+(+i.q||1)},0);$$('.cart-n').forEach(function(b){b.textContent=n;b.dataset.n=n})}
function toast(html){var t=$('.toast');if(!t){t=document.createElement('div');t.className='toast';t.setAttribute('role','status');document.body.appendChild(t)}t.innerHTML=html;t.classList.add('show');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('show')},3200)}
function add(d,q){var c=load(),f=c.find(function(i){return i.code===d.code});if(f)f.q=(+f.q||1)+q;else c.push({code:d.code,name:d.name,img:d.img,url:d.url,q:q});save(c);toast('<span><b>'+d.code+'</b> teklif sepetine eklendi</span><a href="'+U('/teklif')+'">Sepete git</a>')}
$$('[data-add]').forEach(function(b){b.addEventListener('click',function(){
  var qi=$('#qty'),q=qi?Math.max(1,parseInt(qi.value,10)||1):1;add(b.dataset,q);b.classList.add('added');var t=b.innerHTML;b.innerHTML='Eklendi ✓';setTimeout(function(){b.classList.remove('added');b.innerHTML=t},1600)})});
$$('.qty').forEach(function(w){var i=$('input',w);$$('button',w).forEach(function(b){b.addEventListener('click',function(){i.value=Math.max(1,(parseInt(i.value,10)||1)+(+b.dataset.d));i.dispatchEvent(new Event('change'))})})});
badge();

/* sepet sayfası */
var list=$('#cart-list');
function renderCart(){
  var c=load();list.innerHTML='';$('#cart-empty').style.display=c.length?'none':'block';$('#cart-form').style.display=c.length?'':'none';
  c.forEach(function(it,ix){
    var el=document.createElement('div');el.className='ci';
    el.innerHTML='<a href="'+U(it.url)+'"><img src="'+(location.protocol==='file:'&&it.img?(window.__ASSETS__||'')+it.img.replace(/^\/assets\//,''):it.img)+'" alt="" loading="lazy" width="72" height="72"></a><div><span class="code">'+it.code+'</span><div style="font-weight:600;margin-top:4px"><a href="'+U(it.url)+'">'+it.name+'</a></div></div><div class="qty"><button type="button" data-d="-1" aria-label="Azalt">−</button><input type="number" min="1" value="'+(it.q||1)+'" aria-label="Adet"><button type="button" data-d="1" aria-label="Arttır">+</button></div><button class="rm" type="button" aria-label="Kaldır"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>';
    var inp=$('input',el);
    $$('.qty button',el).forEach(function(b){b.addEventListener('click',function(){inp.value=Math.max(1,(parseInt(inp.value,10)||1)+(+b.dataset.d));inp.dispatchEvent(new Event('change'))})});
    inp.addEventListener('change',function(){var c2=load();c2[ix].q=Math.max(1,parseInt(inp.value,10)||1);save(c2)});
    $('.rm',el).addEventListener('click',function(){var c2=load();c2.splice(ix,1);save(c2);renderCart()});
    list.appendChild(el)});
}
function message(){
  var f=$('#cart-form'),c=load(),L=['Merhaba, aşağıdaki ürünler için fiyat teklifi rica ediyorum:',''];
  c.forEach(function(i){L.push('• '+i.code+' – '+i.name+' × '+(i.q||1))});
  L.push('');['ad','firma','tel','eposta','not'].forEach(function(k){var v=f.elements[k]&&f.elements[k].value.trim();if(v)L.push({ad:'Ad Soyad',firma:'Firma',tel:'Telefon',eposta:'E-posta',not:'Not'}[k]+': '+v)});
  return L.join('\n');
}
if(list){
  renderCart();
  $('#send-wa').addEventListener('click',function(){window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(message()),'_blank','noopener')});
  $('#send-mail').addEventListener('click',function(){location.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Teklif talebi – '+load().length+' ürün')+'&body='+encodeURIComponent(message())});
  $('#cart-clear').addEventListener('click',function(){save([]);renderCart()});
}

/* iletişim formu -> e-posta / whatsapp */
var cf=$('#contact-form');
if(cf){cf.addEventListener('submit',function(e){e.preventDefault();var v=function(k){return (cf.elements[k].value||'').trim()};
  var body='Ad Soyad: '+v('ad')+'\nFirma: '+v('firma')+'\nTelefon: '+v('tel')+'\nE-posta: '+v('eposta')+'\n\n'+v('mesaj');
  if(e.submitter&&e.submitter.value==='wa')window.open('https://wa.me/'+WA+'?text='+encodeURIComponent(body),'_blank','noopener');
  else location.href='mailto:'+MAIL+'?subject='+encodeURIComponent('Web sitesi mesajı – '+v('ad'))+'&body='+encodeURIComponent(body)})}

/* liste filtreleme */
var grid=$('[data-filter-grid]');
if(grid){
  var cards=$$('.pc',grid),chips=$$('.chip[data-cat]'),q=$('#q'),empty=$('.empty'),cat=(new URLSearchParams(location.search)).get('k')||'all';
  var norm=function(s){return (s||'').toLocaleLowerCase('tr').replace(/[ıi̇]/g,'i').replace(/ş/g,'s').replace(/ğ/g,'g').replace(/ü/g,'u').replace(/ö/g,'o').replace(/ç/g,'c').replace(/[^a-z0-9]/g,'')};
  function apply(){var t=norm(q&&q.value),n=0;cards.forEach(function(c){var ok=(cat==='all'||c.dataset.cat===cat)&&(!t||norm(c.dataset.s).indexOf(t)>-1);c.hidden=!ok;if(ok)n++});
    chips.forEach(function(ch){ch.setAttribute('aria-pressed',ch.dataset.cat===cat)});if(empty)empty.style.display=n?'none':'block';var cnt=$('#count');if(cnt)cnt.textContent=n}
  chips.forEach(function(ch){ch.addEventListener('click',function(){cat=ch.dataset.cat;var u=new URL(location);if(cat==='all')u.searchParams.delete('k');else u.searchParams.set('k',cat);history.replaceState(null,'',u);apply()})});
  if(q){var iq=(new URLSearchParams(location.search)).get('q');if(iq)q.value=iq;q.addEventListener('input',apply)}
  apply();
}

/* görünürlük animasyonu */
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -40px 0px'});$$('.reveal').forEach(function(el){io.observe(el)})}
else $$('.reveal').forEach(function(el){el.classList.add('in')});
})();
