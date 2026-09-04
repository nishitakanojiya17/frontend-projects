/* ============================================================
   MYNTRA CLONE – JAVASCRIPT
   ============================================================ */

/* ============================================================
   1. PRODUCT DATA
   ============================================================ */
const allProducts = [
  // MEN
  { id:1,  brand:'H&M',        name:'Slim Fit Casual Shirt',          category:'men',       price:799,   mrp:1599,  off:50, rating:4.2, reviews:1842, icon:'fa-shirt',
    img:'https://images.unsplash.com/photo-1602810316693-3667c854239a?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL','XXL'] },
  { id:2,  brand:"Levi's",     name:'511 Slim Fit Jeans',             category:'men',       price:2249,  mrp:3999,  off:44, rating:4.5, reviews:3201, icon:'fa-person',
    img:'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=533&fit=crop',
    sizes:['28','30','32','34','36'] },
  { id:3,  brand:'Nike',       name:'Dri-FIT Training T-Shirt',       category:'sports',    price:1499,  mrp:2499,  off:40, rating:4.6, reviews:5672, icon:'fa-shirt',
    img:'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL'] },
  { id:4,  brand:'Adidas',     name:'Trefoil Hoodie',                 category:'men',       price:2999,  mrp:4999,  off:40, rating:4.3, reviews:2134, icon:'fa-shirt',
    img:'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL','XXL'] },
  { id:5,  brand:'Puma',       name:'Essentials Logo Sweatshirt',     category:'men',       price:1799,  mrp:2999,  off:40, rating:4.1, reviews:987,  icon:'fa-shirt',
    img:'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL'] },
  { id:6,  brand:'Wrangler',   name:'Regular Fit Cargo Pants',        category:'men',       price:1299,  mrp:2499,  off:48, rating:4.0, reviews:756,  icon:'fa-person',
    img:'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&h=533&fit=crop',
    sizes:['30','32','34','36','38'] },
  // WOMEN
  { id:7,  brand:'Zara',       name:'Floral Wrap Midi Dress',         category:'women',     price:2499,  mrp:4999,  off:50, rating:4.7, reviews:4321, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L','XL'] },
  { id:8,  brand:'H&M',        name:'Ribbed-knit Crop Top',           category:'women',     price:599,   mrp:999,   off:40, rating:4.3, reviews:2876, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1594938298603-c8148c4b4357?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L'] },
  { id:9,  brand:'FabIndia',   name:'Embroidered Kurti',              category:'ethnic',    price:1199,  mrp:2199,  off:45, rating:4.6, reviews:6543, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L','XL','XXL'] },
  { id:10, brand:'Libas',      name:'Anarkali Ethnic Dress',          category:'ethnic',    price:999,   mrp:1999,  off:50, rating:4.4, reviews:3210, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL','XXL'] },
  { id:11, brand:'W',          name:'Printed Straight Kurta',         category:'ethnic',    price:849,   mrp:1699,  off:50, rating:4.2, reviews:1987, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1631233859262-0d4a3e77c7b5?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L','XL'] },
  { id:12, brand:'Vero Moda',  name:'High-Rise Skinny Jeans',         category:'women',     price:1799,  mrp:3499,  off:49, rating:4.5, reviews:4102, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&h=533&fit=crop',
    sizes:['26','28','30','32','34'] },
  // KIDS
  { id:13, brand:'H&M',        name:'Printed Cotton T-Shirt',         category:'kids',      price:399,   mrp:799,   off:50, rating:4.4, reviews:1230, icon:'fa-child',
    img:'https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=400&h=533&fit=crop',
    sizes:['2Y','4Y','6Y','8Y','10Y'] },
  { id:14, brand:'Nike',       name:'Kids Printed Hoodie',            category:'kids',      price:1499,  mrp:2499,  off:40, rating:4.5, reviews:876,  icon:'fa-child',
    img:'https://images.unsplash.com/photo-1560506840-ec148e82a604?w=400&h=533&fit=crop',
    sizes:['4Y','6Y','8Y','10Y','12Y'] },
  { id:15, brand:'UCB Kids',   name:'Denim Dungaree',                 category:'kids',      price:899,   mrp:1799,  off:50, rating:4.3, reviews:654,  icon:'fa-child',
    img:'https://images.unsplash.com/photo-1471286174890-9c112ffca5b4?w=400&h=533&fit=crop',
    sizes:['2Y','4Y','6Y','8Y'] },
  // FOOTWEAR
  { id:16, brand:'Nike',       name:'Air Max 270 Sneakers',           category:'footwear',  price:7999,  mrp:12999, off:38, rating:4.8, reviews:8921, icon:'fa-shoe-prints',
    img:'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=533&fit=crop',
    sizes:['6','7','8','9','10','11'] },
  { id:17, brand:'Adidas',     name:'Ultraboost 22 Running Shoes',    category:'footwear',  price:9999,  mrp:15999, off:38, rating:4.7, reviews:7654, icon:'fa-shoe-prints',
    img:'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=533&fit=crop',
    sizes:['6','7','8','9','10'] },
  { id:18, brand:'Puma',       name:'Softride Sandal',                category:'footwear',  price:1299,  mrp:2499,  off:48, rating:4.2, reviews:2134, icon:'fa-shoe-prints',
    img:'https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400&h=533&fit=crop',
    sizes:['6','7','8','9','10','11'] },
  { id:19, brand:'Metro',      name:'Block Heel Pumps',               category:'footwear',  price:1499,  mrp:2999,  off:50, rating:4.3, reviews:1876, icon:'fa-shoe-prints',
    img:'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400&h=533&fit=crop',
    sizes:['3','4','5','6','7','8'] },
  { id:20, brand:'Crocs',      name:'Classic Clog',                   category:'footwear',  price:2999,  mrp:4499,  off:33, rating:4.6, reviews:5432, icon:'fa-shoe-prints',
    img:'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=400&h=533&fit=crop',
    sizes:['4','5','6','7','8','9','10'] },
  // SPORTS
  { id:21, brand:'Nike',       name:'Pro Training Tights',            category:'sports',    price:1999,  mrp:3499,  off:43, rating:4.5, reviews:3102, icon:'fa-running',
    img:'https://images.unsplash.com/photo-1547592180-85f173990554?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L','XL'] },
  { id:22, brand:'Adidas',     name:'Tiro 23 Track Pants',            category:'sports',    price:2499,  mrp:3999,  off:38, rating:4.4, reviews:2765, icon:'fa-running',
    img:'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL','XXL'] },
  { id:23, brand:'Puma',       name:'Evostripe Joggers',              category:'sports',    price:1599,  mrp:2799,  off:43, rating:4.2, reviews:1543, icon:'fa-running',
    img:'https://images.unsplash.com/photo-1483721310020-03333e577078?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL'] },
  // ACCESSORIES
  { id:24, brand:'Fossil',     name:'Minimalist Leather Watch',       category:'accessories',price:5999, mrp:9999,  off:40, rating:4.7, reviews:4321, icon:'fa-clock',
    img:'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=533&fit=crop',
    sizes:['Free Size'] },
  { id:25, brand:'Lavie',      name:'Large Tote Handbag',             category:'accessories',price:1299, mrp:2999,  off:57, rating:4.4, reviews:3210, icon:'fa-bag-shopping',
    img:'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=533&fit=crop',
    sizes:['Free Size'] },
  { id:26, brand:'Fastrack',   name:'Aviator Sunglasses',             category:'accessories',price:899,  mrp:1799,  off:50, rating:4.3, reviews:2109, icon:'fa-glasses',
    img:'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=533&fit=crop',
    sizes:['Free Size'] },
  // ETHNIC
  { id:27, brand:'Manyavar',   name:'Sherwani Set',                   category:'ethnic',    price:7999,  mrp:14999, off:47, rating:4.8, reviews:5678, icon:'fa-star',
    img:'https://images.unsplash.com/photo-1585842378054-ee2e52f94ba2?w=400&h=533&fit=crop',
    sizes:['S','M','L','XL','XXL'] },
  { id:28, brand:'Biba',       name:'Printed Salwar Suit Set',        category:'ethnic',    price:1699,  mrp:3499,  off:51, rating:4.5, reviews:4321, icon:'fa-person-dress',
    img:'https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=400&h=533&fit=crop',
    sizes:['XS','S','M','L','XL'] },
];

/* ============================================================
   2. STATE
   ============================================================ */
let cart      = JSON.parse(localStorage.getItem('myntra_cart'))      || [];
let wishlist  = JSON.parse(localStorage.getItem('myntra_wishlist'))  || [];
let currentFilter   = 'all';
let currentSort     = 'popular';
let visibleCount    = 8;
const PAGE_SIZE     = 8;

/* ============================================================
   3. HERO SLIDER
   ============================================================ */
const slides     = document.querySelectorAll('.hero-slide');
const dots       = document.querySelectorAll('.dot');
let   slideIndex = 0;
let   slideTimer;

function goToSlide(idx) {
  slides[slideIndex].classList.remove('active');
  dots[slideIndex].classList.remove('active');
  slideIndex = (idx + slides.length) % slides.length;
  slides[slideIndex].classList.add('active');
  dots[slideIndex].classList.add('active');
}

function startSlider() {
  slideTimer = setInterval(() => goToSlide(slideIndex + 1), 4000);
}
function resetSlider() {
  clearInterval(slideTimer);
  startSlider();
}

document.getElementById('slideNext').addEventListener('click', () => { goToSlide(slideIndex + 1); resetSlider(); });
document.getElementById('slidePrev').addEventListener('click', () => { goToSlide(slideIndex - 1); resetSlider(); });
dots.forEach(d => d.addEventListener('click', () => { goToSlide(+d.dataset.idx); resetSlider(); }));
startSlider();

/* ============================================================
   4. RENDER PRODUCTS
   ============================================================ */
function getFilteredSorted() {
  let list = currentFilter === 'all'
    ? [...allProducts]
    : allProducts.filter(p => p.category === currentFilter);

  switch (currentSort) {
    case 'low':      list.sort((a,b) => a.price - b.price);    break;
    case 'high':     list.sort((a,b) => b.price - a.price);    break;
    case 'discount': list.sort((a,b) => b.off - a.off);        break;
    case 'newest':   list.sort((a,b) => b.id - a.id);          break;
    default:         list.sort((a,b) => b.rating - a.rating);  break;
  }
  return list;
}

function renderProducts() {
  const grid = document.getElementById('productsGrid');
  const list = getFilteredSorted();
  const visible = list.slice(0, visibleCount);

  if (visible.length === 0) {
    grid.innerHTML = `
      <div class="no-products">
        <i class="fas fa-search"></i>
        <p>No products found</p>
      </div>`;
    document.getElementById('loadMoreBtn').style.display = 'none';
    return;
  }

  grid.innerHTML = visible.map(p => productCardHTML(p)).join('');
  attachCardEvents();

  const loadBtn = document.getElementById('loadMoreBtn');
  loadBtn.style.display = visibleCount >= list.length ? 'none' : 'block';
}

function productCardHTML(p) {
  const inWish = wishlist.some(w => w.id === p.id);
  const stars  = starHTML(p.rating);
  const imgHTML = p.img
    ? `<img src="${p.img}" alt="${p.brand} ${p.name}"
            loading="lazy"
            onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" />
       <div class="product-img-placeholder" style="display:none;">
         <i class="fas ${p.icon}"></i><span>${p.brand}</span>
       </div>`
    : `<div class="product-img-placeholder">
         <i class="fas ${p.icon}"></i><span>${p.brand}</span>
       </div>`;

  return `
    <div class="product-card" data-id="${p.id}">
      <div class="product-img-wrap">
        ${imgHTML}
        <span class="product-discount-badge">${p.off}% OFF</span>
        <button class="product-wishlist-btn ${inWish ? 'active' : ''}"
                data-id="${p.id}" onclick="toggleWishlist(event,${p.id})">
          <i class="${inWish ? 'fas' : 'far'} fa-heart"></i>
        </button>
        <button class="product-quick-add" onclick="addToCart(event,${p.id})">
          <i class="fas fa-shopping-bag"></i> QUICK ADD
        </button>
      </div>
      <div class="product-info">
        <p class="product-brand">${p.brand}</p>
        <p class="product-name">${p.name}</p>
        <div class="product-pricing">
          <span class="product-price">₹${p.price.toLocaleString('en-IN')}</span>
          <span class="product-mrp">₹${p.mrp.toLocaleString('en-IN')}</span>
          <span class="product-off">(${p.off}% OFF)</span>
        </div>
        <div class="product-rating">
          <span class="rating-stars">${stars}</span>
          <span class="rating-count">(${p.reviews.toLocaleString('en-IN')})</span>
        </div>
      </div>
    </div>`;
}

function starHTML(rating) {
  let s = '';
  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rating))        s += '<i class="fas fa-star"></i>';
    else if (i - rating < 1)            s += '<i class="fas fa-star-half-alt"></i>';
    else                                s += '<i class="far fa-star"></i>';
  }
  return s;
}

function attachCardEvents() {
  document.querySelectorAll('.product-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('.product-wishlist-btn') ||
          e.target.closest('.product-quick-add')) return;
      openModal(+card.dataset.id);
    });
  });
}

/* ============================================================
   5. FILTER & SORT
   ============================================================ */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    visibleCount  = PAGE_SIZE;
    renderProducts();
    document.getElementById('products').scrollIntoView({ behavior:'smooth', block:'start' });
  });
});

document.getElementById('sortSelect').addEventListener('change', (e) => {
  currentSort  = e.target.value;
  visibleCount = PAGE_SIZE;
  renderProducts();
});

// Category section cards
function filterByCategory(cat) {
  currentFilter = cat;
  visibleCount  = PAGE_SIZE;
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.filter === cat);
  });
  renderProducts();
  document.getElementById('products').scrollIntoView({ behavior:'smooth', block:'start' });
}

// Load more
document.getElementById('loadMoreBtn').addEventListener('click', () => {
  visibleCount += PAGE_SIZE;
  renderProducts();
});

/* ============================================================
   6. CART
   ============================================================ */
function addToCart(e, id) {
  if (e) e.stopPropagation();
  const product = allProducts.find(p => p.id === id);
  if (!product) return;

  const existing = cart.find(c => c.id === id);
  if (existing) {
    existing.qty++;
  } else {
    cart.push({ ...product, qty: 1, selectedSize: product.sizes[1] || product.sizes[0] });
  }
  saveCart();
  updateCartBadge();
  renderCartItems();
  showToast(`${product.brand} added to bag!`);
}

function removeFromCart(id) {
  cart = cart.filter(c => c.id !== id);
  saveCart();
  updateCartBadge();
  renderCartItems();
}

function changeQty(id, delta) {
  const item = cart.find(c => c.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) { removeFromCart(id); return; }
  saveCart();
  renderCartItems();
}

function saveCart() { localStorage.setItem('myntra_cart', JSON.stringify(cart)); }

function updateCartBadge() {
  const total = cart.reduce((s, c) => s + c.qty, 0);
  const badge = document.getElementById('cartCount');
  badge.textContent = total;
  badge.style.display = total > 0 ? 'flex' : 'none';
  document.getElementById('cartItemCount').textContent = `(${total} item${total !== 1 ? 's' : ''})`;
}

function renderCartItems() {
  const container  = document.getElementById('cartItems');
  const emptyEl    = document.getElementById('cartEmpty');
  const footerEl   = document.getElementById('cartFooter');

  if (cart.length === 0) {
    emptyEl.style.display   = 'flex';
    container.innerHTML     = '';
    footerEl.style.display  = 'none';
    return;
  }

  emptyEl.style.display  = 'none';
  footerEl.style.display = 'block';

  container.innerHTML = cart.map(item => `
    <div class="cart-item">
      <div class="cart-item-img">
        ${item.img
          ? `<img src="${item.img}" alt="${item.brand}"
                  style="width:100%;height:100%;object-fit:cover;border-radius:4px;"
                  onerror="this.style.display='none';this.nextElementSibling.style.display='block';" />
             <i class="fas ${item.icon}" style="display:none;font-size:1.8rem;color:#ccc;"></i>`
          : `<i class="fas ${item.icon}"></i>`}
      </div>
      <div class="cart-item-info">
        <p class="cart-item-brand">${item.brand}</p>
        <p class="cart-item-name">${item.name}</p>
        <p style="font-size:0.75rem;color:var(--grey);margin-bottom:4px;">
          Size: ${item.selectedSize}
        </p>
        <div class="product-pricing">
          <span class="cart-item-price">₹${item.price.toLocaleString('en-IN')}</span>
          <span class="cart-item-mrp">₹${item.mrp.toLocaleString('en-IN')}</span>
          <span class="cart-item-off">(${item.off}% OFF)</span>
        </div>
        <div class="cart-item-qty">
          <button class="qty-btn" onclick="changeQty(${item.id},-1)">−</button>
          <span class="qty-val">${item.qty}</span>
          <button class="qty-btn" onclick="changeQty(${item.id},1)">+</button>
        </div>
      </div>
      <button class="cart-item-remove" onclick="removeFromCart(${item.id})">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  `).join('');

  // Totals
  const totalMRP      = cart.reduce((s,c) => s + c.mrp   * c.qty, 0);
  const totalPrice    = cart.reduce((s,c) => s + c.price  * c.qty, 0);
  const totalDiscount = totalMRP - totalPrice;

  document.getElementById('totalMRP').textContent      = `₹${totalMRP.toLocaleString('en-IN')}`;
  document.getElementById('totalDiscount').textContent = `-₹${totalDiscount.toLocaleString('en-IN')}`;
  document.getElementById('grandTotal').textContent    = `₹${totalPrice.toLocaleString('en-IN')}`;
}

// Open/close cart sidebar
document.getElementById('cartBtn').addEventListener('click', () => {
  document.getElementById('cartSidebar').classList.add('open');
  document.getElementById('cartOverlay').classList.add('open');
});
document.getElementById('cartClose').addEventListener('click', closeCart);
document.getElementById('cartOverlay').addEventListener('click', closeCart);
function closeCart() {
  document.getElementById('cartSidebar').classList.remove('open');
  document.getElementById('cartOverlay').classList.remove('open');
}

/* ============================================================
   7. WISHLIST
   ============================================================ */
function toggleWishlist(e, id) {
  if (e) e.stopPropagation();
  const product = allProducts.find(p => p.id === id);
  if (!product) return;

  const idx = wishlist.findIndex(w => w.id === id);
  if (idx === -1) {
    wishlist.push({ ...product });
    showToast(`${product.brand} added to wishlist!`);
  } else {
    wishlist.splice(idx, 1);
    showToast(`Removed from wishlist`);
  }
  saveWishlist();
  updateWishlistBadge();
  renderWishlistItems();
  // Update heart icon on product card if visible
  const btn = document.querySelector(`.product-wishlist-btn[data-id="${id}"]`);
  if (btn) {
    const inWish = wishlist.some(w => w.id === id);
    btn.classList.toggle('active', inWish);
    btn.innerHTML = `<i class="${inWish ? 'fas' : 'far'} fa-heart"></i>`;
  }
}

function saveWishlist() { localStorage.setItem('myntra_wishlist', JSON.stringify(wishlist)); }

function updateWishlistBadge() {
  const badge = document.getElementById('wishlistCount');
  badge.textContent = wishlist.length;
  badge.style.display = wishlist.length > 0 ? 'flex' : 'none';
  document.getElementById('wishlistItemCount').textContent =
    `(${wishlist.length} item${wishlist.length !== 1 ? 's' : ''})`;
}

function renderWishlistItems() {
  const container = document.getElementById('wishlistItems');
  const emptyEl   = document.getElementById('wishlistEmpty');

  if (wishlist.length === 0) {
    emptyEl.style.display = 'flex';
    container.innerHTML   = '';
    return;
  }
  emptyEl.style.display = 'none';
  container.innerHTML = wishlist.map(item => `
    <div class="cart-item">
      <div class="cart-item-img">
        ${item.img
          ? `<img src="${item.img}" alt="${item.brand}"
                  style="width:100%;height:100%;object-fit:cover;border-radius:4px;"
                  onerror="this.style.display='none';this.nextElementSibling.style.display='block';" />
             <i class="fas ${item.icon}" style="display:none;font-size:1.8rem;color:#ccc;"></i>`
          : `<i class="fas ${item.icon}"></i>`}
      </div>
      <div class="cart-item-info">
        <p class="cart-item-brand">${item.brand}</p>
        <p class="cart-item-name">${item.name}</p>
        <div class="product-pricing">
          <span class="cart-item-price">₹${item.price.toLocaleString('en-IN')}</span>
          <span class="cart-item-mrp">₹${item.mrp.toLocaleString('en-IN')}</span>
          <span class="cart-item-off">(${item.off}% OFF)</span>
        </div>
        <button style="margin-top:8px;background:var(--pink);color:#fff;border:none;
                       padding:7px 16px;border-radius:3px;font-size:0.78rem;font-weight:700;
                       cursor:pointer;letter-spacing:0.5px;"
                onclick="moveToCart(${item.id})">
          MOVE TO BAG
        </button>
      </div>
      <button class="cart-item-remove" onclick="removeFromWishlist(${item.id})">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  `).join('');
}

function removeFromWishlist(id) {
  wishlist = wishlist.filter(w => w.id !== id);
  saveWishlist();
  updateWishlistBadge();
  renderWishlistItems();
  // Update card icon
  const btn = document.querySelector(`.product-wishlist-btn[data-id="${id}"]`);
  if (btn) { btn.classList.remove('active'); btn.innerHTML = '<i class="far fa-heart"></i>'; }
}

function moveToCart(id) {
  addToCart(null, id);
  removeFromWishlist(id);
  closeWishlist();
  document.getElementById('cartSidebar').classList.add('open');
  document.getElementById('cartOverlay').classList.add('open');
}

// Open/close wishlist
document.getElementById('wishlistBtn').addEventListener('click', () => {
  document.getElementById('wishlistSidebar').classList.add('open');
  document.getElementById('wishlistOverlay').classList.add('open');
});
document.getElementById('wishlistClose').addEventListener('click', closeWishlist);
document.getElementById('wishlistOverlay').addEventListener('click', closeWishlist);
function closeWishlist() {
  document.getElementById('wishlistSidebar').classList.remove('open');
  document.getElementById('wishlistOverlay').classList.remove('open');
}

/* ============================================================
   8. PRODUCT MODAL
   ============================================================ */
function openModal(id) {
  const p       = allProducts.find(x => x.id === id);
  if (!p) return;
  const inWish  = wishlist.some(w => w.id === id);
  const stars   = starHTML(p.rating);

  const modalImgHTML = p.img
    ? `<img src="${p.img}" alt="${p.brand} ${p.name}"
            style="width:100%;height:100%;object-fit:cover;"
            onerror="this.style.display='none';this.nextElementSibling.style.display='block';" />
       <i class="fas ${p.icon}" style="display:none;font-size:5rem;color:#ccc;"></i>`
    : `<i class="fas ${p.icon}"></i>`;

  document.getElementById('modalBody').innerHTML = `
    <div class="modal-img-side">
      ${modalImgHTML}
    </div>
    <div class="modal-info-side">
      <p class="modal-brand">${p.brand}</p>
      <p class="modal-name">${p.name}</p>
      <div class="modal-rating">
        <span class="modal-rating-box">${p.rating} <i class="fas fa-star"></i></span>
        <span class="modal-rating-count">${p.reviews.toLocaleString('en-IN')} Ratings</span>
      </div>
      <div class="modal-pricing">
        <span class="modal-price">₹${p.price.toLocaleString('en-IN')}</span>
        <span class="modal-mrp">₹${p.mrp.toLocaleString('en-IN')}</span>
        <span class="modal-off">${p.off}% OFF</span>
      </div>
      <div class="modal-sizes">
        <h4>SELECT SIZE</h4>
        <div class="size-options">
          ${p.sizes.map((s,i) =>
            `<button class="size-btn ${i===0?'active':''}"
                     onclick="selectSize(this)">${s}</button>`
          ).join('')}
        </div>
      </div>
      <div class="modal-actions">
        <button class="modal-bag-btn" onclick="addToCart(null,${p.id}); closeModal();">
          <i class="fas fa-shopping-bag"></i> ADD TO BAG
        </button>
        <button class="modal-wish-btn ${inWish?'active':''}"
                id="modalWishBtn"
                onclick="toggleWishlist(null,${p.id}); toggleModalHeart(${p.id});">
          <i class="${inWish?'fas':'far'} fa-heart"></i>
        </button>
      </div>
      <div style="margin-top:20px;border-top:1px solid var(--grey-border);padding-top:16px;">
        <div style="display:flex;gap:20px;flex-wrap:wrap;">
          <span style="font-size:0.78rem;color:var(--grey);display:flex;align-items:center;gap:5px;">
            <i class="fas fa-truck" style="color:var(--success)"></i> Free Delivery
          </span>
          <span style="font-size:0.78rem;color:var(--grey);display:flex;align-items:center;gap:5px;">
            <i class="fas fa-undo" style="color:var(--success)"></i> 30-Day Returns
          </span>
          <span style="font-size:0.78rem;color:var(--grey);display:flex;align-items:center;gap:5px;">
            <i class="fas fa-shield-alt" style="color:var(--success)"></i> 100% Authentic
          </span>
        </div>
      </div>
    </div>`;

  document.getElementById('productModal').classList.add('open');
  document.getElementById('modalOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  document.getElementById('productModal').classList.remove('open');
  document.getElementById('modalOverlay').classList.remove('open');
  document.body.style.overflow = '';
}

function selectSize(btn) {
  btn.closest('.size-options').querySelectorAll('.size-btn')
     .forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function toggleModalHeart(id) {
  const btn    = document.getElementById('modalWishBtn');
  const inWish = wishlist.some(w => w.id === id);
  if (btn) {
    btn.classList.toggle('active', inWish);
    btn.innerHTML = `<i class="${inWish?'fas':'far'} fa-heart"></i>`;
  }
}

document.getElementById('modalClose').addEventListener('click', closeModal);
document.getElementById('modalOverlay').addEventListener('click', closeModal);

/* ============================================================
   9. SEARCH
   ============================================================ */
const searchInput    = document.getElementById('searchInput');
const searchDropdown = document.getElementById('searchDropdown');
const searchClear    = document.getElementById('searchClear');

searchInput.addEventListener('focus', () => searchDropdown.classList.add('open'));
searchInput.addEventListener('input', () => {
  const val = searchInput.value.trim();
  searchClear.classList.toggle('visible', val.length > 0);
  if (val.length > 0) { liveSearch(val); }
  else                 { showPopularSearches(); }
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.nav-search')) searchDropdown.classList.remove('open');
});

searchClear.addEventListener('click', () => {
  searchInput.value = '';
  searchClear.classList.remove('visible');
  showPopularSearches();
  searchInput.focus();
});

searchInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    const val = searchInput.value.trim().toLowerCase();
    if (val) { doSearch(val); searchDropdown.classList.remove('open'); }
  }
});

function setSearch(term) {
  searchInput.value = term;
  searchClear.classList.add('visible');
  doSearch(term.toLowerCase());
  searchDropdown.classList.remove('open');
}

function doSearch(term) {
  currentFilter = 'all';
  visibleCount  = PAGE_SIZE;
  document.querySelectorAll('.filter-btn').forEach(b =>
    b.classList.toggle('active', b.dataset.filter === 'all'));

  // Temporarily override allProducts filter for search
  const results = allProducts.filter(p =>
    p.name.toLowerCase().includes(term) ||
    p.brand.toLowerCase().includes(term) ||
    p.category.toLowerCase().includes(term)
  );

  const grid = document.getElementById('productsGrid');
  if (results.length === 0) {
    grid.innerHTML = `
      <div class="no-products">
        <i class="fas fa-search"></i>
        <p>No results for "${searchInput.value}"</p>
      </div>`;
    document.getElementById('loadMoreBtn').style.display = 'none';
  } else {
    grid.innerHTML = results.slice(0, PAGE_SIZE).map(p => productCardHTML(p)).join('');
    attachCardEvents();
    document.getElementById('loadMoreBtn').style.display =
      results.length > PAGE_SIZE ? 'block' : 'none';
  }
  document.getElementById('products').scrollIntoView({ behavior:'smooth', block:'start' });
}

function liveSearch(term) {
  const results = allProducts.filter(p =>
    p.name.toLowerCase().includes(term.toLowerCase()) ||
    p.brand.toLowerCase().includes(term.toLowerCase())
  ).slice(0, 6);

  if (results.length === 0) {
    searchDropdown.innerHTML = `<p class="search-label">No suggestions found</p>`;
    return;
  }
  searchDropdown.innerHTML = `
    <p class="search-label">Suggestions</p>
    <div style="display:flex;flex-direction:column;gap:4px;">
      ${results.map(p => `
        <div onclick="setSearch('${p.brand}')"
             style="display:flex;align-items:center;gap:10px;padding:8px;border-radius:4px;
                    cursor:pointer;transition:background 0.2s;"
             onmouseover="this.style.background='var(--grey-light)'"
             onmouseout="this.style.background='transparent'">
          <i class="fas fa-search" style="color:var(--grey);font-size:0.75rem;"></i>
          <span style="font-size:0.85rem;color:var(--dark-2);">
            <strong>${p.brand}</strong> – ${p.name}
          </span>
        </div>`).join('')}
    </div>`;
}

function showPopularSearches() {
  searchDropdown.innerHTML = `
    <div class="search-popular">
      <p class="search-label">Popular Searches</p>
      <div class="search-tags">
        <span onclick="setSearch('Kurta')">Kurta</span>
        <span onclick="setSearch('Saree')">Saree</span>
        <span onclick="setSearch('Sneakers')">Sneakers</span>
        <span onclick="setSearch('Jeans')">Jeans</span>
        <span onclick="setSearch('Dress')">Dress</span>
        <span onclick="setSearch('Handbag')">Handbag</span>
        <span onclick="setSearch('Watch')">Watch</span>
        <span onclick="setSearch('Jacket')">Jacket</span>
      </div>
    </div>`;
}

/* ============================================================
   10. NAVBAR — scroll behaviour + active nav cat
   ============================================================ */
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  navbar.style.boxShadow = window.scrollY > 10
    ? '0 2px 12px rgba(0,0,0,0.1)'
    : '0 1px 4px rgba(0,0,0,0.06)';
}, { passive: true });

document.querySelectorAll('.nav-cat[data-cat]').forEach(cat => {
  cat.addEventListener('click', (e) => {
    e.preventDefault();
    document.querySelectorAll('.nav-cat').forEach(c => c.classList.remove('active'));
    cat.classList.add('active');
    filterByCategory(cat.dataset.cat);
  });
});

/* ============================================================
   11. TOAST
   ============================================================ */
let toastTimer;
function showToast(msg) {
  const toast  = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  toastMsg.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}

/* ============================================================
   12. KEYBOARD SHORTCUTS
   ============================================================ */
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
    closeCart();
    closeWishlist();
  }
  // Ctrl/Cmd + K → focus search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    searchInput.focus();
  }
});

/* ============================================================
   13. CHECKOUT BUTTON
   ============================================================ */
document.querySelector('.checkout-btn').addEventListener('click', () => {
  if (cart.length === 0) return;
  showToast('🎉 Order placed successfully!');
  cart = [];
  saveCart();
  updateCartBadge();
  renderCartItems();
  closeCart();
});

/* ============================================================
   14. INIT
   ============================================================ */
function init() {
  renderProducts();
  updateCartBadge();
  updateWishlistBadge();
  renderCartItems();
  renderWishlistItems();
}

init();
