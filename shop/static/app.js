const $ = (selector) => document.querySelector(selector);
let token = localStorage.getItem('qa-token');
let me = null, products = [], favorites = [], cartTotal = 0, coupon = '';
let catalogPage = 1, pendingCancel = null;
const money = (cents) => (cents / 100).toLocaleString('ru-RU') + ' ₽';
function productImage(product) {
  const name = product.name.toLocaleLowerCase('ru-RU');
  const imageByName = [
    ['клавиатур', 'keyboard'],
    ['мыш', 'mouse'],
    ['монитор', 'monitor'],
    ['ноутбук', 'laptop'],
    ['кабел', 'cable'],
    ['науш', 'headphones'],
    ['рюкзак', 'backpack'],
    ['смартфон', 'smartphone'],
    ['планшет', 'tablet'],
    ['час', 'smartwatch'],
    ['веб-камер', 'webcam'],
    ['колонк', 'speaker'],
    ['микрофон', 'microphone'],
    ['флешк', 'flash'],
    ['роутер', 'router'],
    ['геймпад', 'gamepad'],
  ];
  const image = imageByName.find(([word]) => name.includes(word));
  const imageByCategory = {
    accessories: 'backpack',
    screens: 'monitor',
    computers: 'laptop',
    audio: 'headphones',
  };
  return image ? image[1] : imageByCategory[product.category] || 'backpack';
}
// getRandomValues доступен и на учебном http://web:8000 внутри Docker;
// randomUUID требует secure context и ломает такой запуск.
const newKey = () => Array.from(crypto.getRandomValues(new Uint8Array(16)), value => value.toString(16).padStart(2,'0')).join('');
const status = (text) => { $('#status').textContent = text; };
function node(tag, text, attrs = {}) { const el = document.createElement(tag); el.textContent = text; for (const [k,v] of Object.entries(attrs)) el.setAttribute(k,v); return el; }
async function api(path, method = 'GET', body, extra = {}) {
  const response = await fetch('/api' + path, {method, headers: {'Content-Type':'application/json', ...(token ? {Authorization:'Bearer ' + token} : {}), ...extra}, ...(body === undefined ? {} : {body:JSON.stringify(body)})});
  const data = response.status === 204 ? null : await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Проверьте заполнение полей');
  return data;
}
function action(fn) { return async () => { try { await fn(); } catch (e) { status(e.message); } }; }
async function identity() {
  $('#auth').hidden = Boolean(me);
  $('#identity').replaceChildren();
  if (me) { $('#identity').append(node('span', me.email, {'data-testid':'identity-email'})); const b = node('button','Выйти'); b.onclick = action(async()=>{await api('/logout','POST');localStorage.removeItem('qa-token');location.reload();});$('#identity').append(b); }
}
async function auth(register = false) {
  const form = $('#auth-form');
  const body = {email:form.elements.email.value,password:form.elements.password.value};
  if (register) { await api('/users','POST',body); status('Пользователь создан. Теперь войдите.'); return; }
  const data = await api('/login','POST',body); token=data.token;me=data.user;localStorage.setItem('qa-token',token);await identity();await loadProducts();status('Вы вошли');
}
$('#auth-form').onsubmit = (event) => {event.preventDefault();action(()=>auth())();};
$('#register').onclick = action(()=>auth(true));
async function loadProducts(resetPage = true) {
  if (resetPage) catalogPage = 1;
  const params = new URLSearchParams({q:$('#search').value,category:$('#category').value,sort:$('#sort').value,limit:'100'});
  products = await api('/products?' + params);
  favorites = me ? await api('/favorites') : [];
  const min = $('#min-price').value, max = $('#max-price').value;
  const invalid = (min !== '' && (!Number.isFinite(Number(min)) || Number(min) < 0)) || (max !== '' && (!Number.isFinite(Number(max)) || Number(max) < 0)) || (min !== '' && max !== '' && Number(min) > Number(max));
  $('#filter-error').hidden = !invalid;
  $('#min-price').setAttribute('aria-invalid', String(Boolean(invalid)));
  $('#max-price').setAttribute('aria-invalid', String(Boolean(invalid)));
  if (invalid) { $('#filter-error').textContent = 'Укажите неотрицательные цены: цена от не должна превышать цену до'; return; }
  if ($('#only-favorites').checked && !me) status('Войдите, чтобы посмотреть избранное');
  const visible = products.filter(p => (!$('#only-favorites').checked || favorites.includes(p.id)) && (!$('#in-stock').checked || p.stock > 0) && (min === '' || p.price >= Math.round(Number(min)*100)) && (max === '' || p.price <= Math.round(Number(max)*100)));
  const size = Number($('#page-size').value);
  const pages = Math.max(1, Math.ceil(visible.length / size));
  catalogPage = Math.min(catalogPage, pages);
  $('#result-count').textContent = 'Найдено товаров: ' + visible.length;
  $('#result-count').dataset.count = visible.length;
  $('#page-info').textContent = 'Страница ' + catalogPage + ' из ' + pages;
  $('#previous-page').disabled = catalogPage === 1;
  $('#next-page').disabled = catalogPage === pages;
  $('#products').replaceChildren();
  if (!visible.length) $('#products').append(node('p','Товары не найдены',{'data-testid':'empty-catalog'}));
  for (const p of visible.slice((catalogPage-1)*size, catalogPage*size)) {
    const card = node('article','',{'data-testid':'product-card','data-id':p.id,'data-category':p.category,'data-price':p.price});
    const image = node('img','', {
      class: 'product-image',
      src: '/static/products/' + productImage(p) + '.jpg',
      alt: p.name,
      loading: 'lazy',
    });
    card.append(image,node('h2',p.name),node('p',money(p.price)),node('p',p.stock ? 'В наличии: ' + p.stock : 'Нет в наличии', {'data-testid':'product-stock'}));
    const details=node('button','Подробнее');details.onclick=()=>{$('#details-image').src='/static/products/'+productImage(p)+'.jpg';$('#details-image').alt=p.name;$('#details-name').textContent=p.name;$('#details-description').textContent=p.description;$('#details-price').textContent=money(p.price);$('#details').showModal();};
    const add=node('button','В корзину');add.disabled=p.stock===0;add.onclick=action(async()=>{const c=await api('/cart');const old=c.items.find(i=>i.product_id===p.id);await api('/cart','PUT',{product_id:p.id,quantity:(old?.quantity||0)+1});status('Товар добавлен');});
    const favorite=node('button',favorites.includes(p.id)?'Убрать из избранного':'В избранное');favorite.onclick=action(async()=>{await api('/favorites/'+p.id,favorites.includes(p.id)?'DELETE':'PUT');await loadProducts();status('Избранное обновлено');});
    card.append(details,add,favorite);$('#products').append(card);
  }
}
$('#find').onclick=action(()=>loadProducts());
$('#in-stock').onchange=action(()=>loadProducts());
$('#page-size').onchange=action(()=>loadProducts());
$('#previous-page').onclick=action(async()=>{catalogPage--;await loadProducts(false);});
$('#next-page').onclick=action(async()=>{catalogPage++;await loadProducts(false);});
$('#show-password').onchange=()=>{$('[name="password"]').type=$('#show-password').checked?'text':'password';};
$('#search').onkeydown=(event)=>{if(event.key==='Enter') action(loadProducts)();};
$('#sort').onchange=action(loadProducts);$('#category').onchange=action(loadProducts);$('#only-favorites').onchange=action(loadProducts);
$('#reset-filters').onclick=action(async()=>{$('#search').value='';$('#category').value='';$('#sort').value='id';$('#only-favorites').checked=false;$('#in-stock').checked=false;$('#min-price').value='';$('#max-price').value='';$('#page-size').value='100';await loadProducts();});
$('#close-details').onclick=()=>$('#details').close();
function discount() { const total=coupon==='SAVE10'?Math.floor(cartTotal*90/100):cartTotal;$('#discount-total').textContent='К оплате: '+money(total);$('#discount-total').dataset.cents=total; }
async function loadCart() {
  const data=await api('/cart');cartTotal=data.total;$('#cart-items').replaceChildren();
  if(!data.items.length) $('#cart-items').append(node('p','Корзина пуста',{'data-testid':'empty-cart'}));
  for(const item of data.items){
    const row=node('article','',{'data-testid':'cart-row','data-id':item.product_id});row.append(node('strong',item.name));
    const label=node('label','Количество');const qty=node('input','',{type:'number',min:'1',max:'99',value:item.quantity,'aria-label':'Количество '+item.name});
    qty.onchange=action(async()=>{try { await api('/cart','PUT',{product_id:item.product_id,quantity:Number(qty.value)});await loadCart();status('Количество обновлено'); } catch(error) { await loadCart(); throw error; }});label.append(qty);row.append(label,node('span',money(item.price*item.quantity)));
    const remove=node('button','Удалить');remove.onclick=action(async()=>{await api('/cart/'+item.product_id,'DELETE');await loadCart();status('Товар удалён');});row.append(remove);$('#cart-items').append(row);
  }
  $('[data-testid="cart-total"]').textContent=money(data.total);$('[data-testid="cart-total"]').dataset.cents=data.total;discount();
}
$('#apply-coupon').onclick=()=>{const value=$('#coupon').value.trim();if(value!==''&&value!=='SAVE10'){coupon='';discount();status('Промокод недействителен');return;}coupon=value;discount();status(value?'Скидка 10% применена':'Промокод удалён');};
$('#checkout').onclick=action(async()=>{const invalid=$('#address').value.trim().length<5 || $('#address').value.length>300;$('#address-error').hidden=!invalid;$('#address').setAttribute('aria-invalid',String(invalid));if(invalid){$('#address-error').textContent='Укажите адрес: от 5 до 300 символов';return;}const result=await api('/orders','POST',{address:$('#address').value,coupon},{'Idempotency-Key':newKey()});await view('orders');status('Заказ №'+result.id+' создан');});
async function loadOrders(){
  const data=await api('/orders');$('#order-list').replaceChildren();
  if(!data.length)$('#order-list').append(node('p','Заказов пока нет',{'data-testid':'empty-orders'}));
  const orders = data.filter(order=>!$('#order-filter').value || order.status===$('#order-filter').value);
  if(data.length && !orders.length)$('#order-list').append(node('p','Заказы с таким статусом не найдены',{'data-testid':'empty-filtered-orders'}));
  for(const order of orders){const row=node('article','',{'data-testid':'order-card','data-id':order.id,'data-status':order.status});
    row.append(node('h2','Заказ №'+order.id),node('p',order.status,{'data-testid':'order-status'}),node('p',money(order.total),{'data-testid':'order-total','data-cents':order.total}),node('p',order.address));
    if(order.status==='new'){const cancel=node('button','Отменить заказ');cancel.onclick=()=>{pendingCancel=order.id;$('#cancel-dialog').showModal();};const pay=node('button','Оплатить');pay.onclick=action(async()=>{await api('/orders/'+order.id+'/pay','POST');await loadOrders();status('Оплата передана в обработку');});row.append(cancel,pay);}
    $('#order-list').append(row);
  }
}
$('#refresh-orders').onclick=action(loadOrders);
$('#order-filter').onchange=action(loadOrders);
$('#keep-order').onclick=()=>{pendingCancel=null;$('#cancel-dialog').close();};
$('#cancel-dialog').onclose=()=>{pendingCancel=null;};
$('#confirm-cancel').onclick=action(async()=>{if(pendingCancel===null)return;const id=pendingCancel;await api('/orders/'+id+'/cancel','POST');$('#cancel-dialog').close();await loadOrders();status('Заказ отменён');});
async function view(name){if(name!=='catalog'&&!me){status('Требуется вход');return;}if(name==='cart')await loadCart();if(name==='orders')await loadOrders();if(name==='profile'){me=await api('/me');$('[data-testid="profile-email"]').textContent=me.email;$('#profile-name').value=me.name;}for(const section of document.querySelectorAll('.view'))section.hidden=section.id!==name;}
for(const button of document.querySelectorAll('[data-view]'))button.onclick=action(()=>view(button.dataset.view));
$('#save-profile').onclick=action(async()=>{const name=$('#profile-name').value;const invalid=!name.trim() || name.length>100;$('#profile-error').hidden=!invalid;$('#profile-name').setAttribute('aria-invalid',String(invalid));if(invalid){$('#profile-error').textContent='Введите имя: от 1 до 100 символов, не только пробелы';return;}me=await api('/me','PATCH',{name:$('#profile-name').value});status('Профиль сохранён');});
action(async()=>{if(token){try{me=await api('/me');}catch{localStorage.removeItem('qa-token');token=null;}}await identity();await loadProducts();document.body.dataset.ready='true';})();
