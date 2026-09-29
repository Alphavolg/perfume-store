#!/usr/bin/env python3
"""Generates the static homepage (public/) and the WordPress block theme
(wp-content/themes/bagh-atr/) from a single source, so both stay identical."""
import json, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
THEME = ROOT / "wp-content/themes/bagh-atr"
PUBLIC = ROOT / "public"

FONTS = ("https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700"
         "&family=Vazirmatn:wght@400;500;700&display=swap")

# ---------- data ----------
PRODUCTS = [
    ("گل محمدی کاشان", "گل محمدی، مشک سفید، صندل", "۵۰ میلی‌لیتر", "۳٬۲۰۰٬۰۰۰", "#C2416B", "#E2A62A", "پرفروش"),
    ("زعفران قائنات", "زعفران، عود، وانیل", "۵۰ میلی‌لیتر", "۴٬۸۰۰٬۰۰۰", "#D98E1F", "#8E1F45", ""),
    ("باغ نارنج", "بهارنارنج، ترنج، چای سبز", "۵۰ میلی‌لیتر", "۲٬۹۰۰٬۰۰۰", "#8FAE2E", "#17706F", "تازه"),
    ("مشک شیراز", "مشک، عنبر، گل سرخ", "۳۰ میلی‌لیتر", "۳٬۹۵۰٬۰۰۰", "#5B2F86", "#E2A62A", ""),
    ("سرو دماوند", "سرو، ترنج، خزه", "۵۰ میلی‌لیتر", "۳٬۴۰۰٬۰۰۰", "#1F6B5A", "#F7ECE9", ""),
    ("شب یلدا", "انار، رز، دارچین", "۳۰ میلی‌لیتر", "۲٬۷۰۰٬۰۰۰", "#8E1F45", "#E2A62A", "پرفروش"),
    ("عود سلطانی", "عود، چرم، اسطوخودوس", "۳۰ میلی‌لیتر", "۸٬۵۰۰٬۰۰۰", "#3A2418", "#E2A62A", ""),
    ("یاس شبانه", "یاس، هلو، مسک", "۵۰ میلی‌لیتر", "۲٬۸۰۰٬۰۰۰", "#D98BA8", "#22366B", ""),
]

FAMILIES = [
    ("گلی", "گل محمدی، یاس، نرگس", "#EBC3CC", "#C2416B"),
    ("شرقی و عودی", "عود، مشک، عنبر", "#D9C3A0", "#3A2418"),
    ("چوبی و خاکی", "سرو، صندل، خزه", "#B9D3C7", "#1F6B5A"),
    ("زعفرانی و ادویه‌ای", "زعفران، هل، دارچین", "#F1D9A0", "#D98E1F"),
    ("مرکباتی و تازه", "بهارنارنج، ترنج، لیمو", "#D6E2A8", "#8FAE2E"),
]

NOTES = [
    ("گل محمدی", "#C2416B"), ("زعفران", "#E2A62A"), ("بهارنارنج", "#8FAE2E"),
    ("عود", "#3A2418"), ("مشک", "#5B2F86"), ("سرو", "#1F6B5A"),
    ("انار", "#8E1F45"), ("هل", "#17706F"),
]

POSTS = [
    ("تفاوت عطر، ادکلن و ادوپرفیوم چیست؟", "۵ دقیقه مطالعه", "#F1D9A0", "#8E1F45"),
    ("چطور عطر را روی پوست ماندگارتر کنیم؟", "۴ دقیقه مطالعه", "#B9D3C7", "#17706F"),
    ("راهنمای انتخاب عطر برای هدیه", "۶ دقیقه مطالعه", "#EBC3CC", "#22366B"),
]

REVIEWS = [
    ("بوی گل محمدی دقیقاً همان بوی باغ مادربزرگم است. ماندگاری‌اش هم تا آخر شب می‌ماند.", "سارا م.", "تهران"),
    ("نمونه ۲ میلی‌لیتری کمک کرد بدون نگرانی انتخاب کنم. بسته‌بندی هم برای هدیه عالی بود.", "علی ر.", "اصفهان"),
    ("زعفران قائنات گرم و غلیظ است و اصلاً شبیه عطرهای تکراری بازار نیست.", "نیلوفر ک.", "شیراز"),
]

# ---------- html pieces ----------
DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <symbol id="bottle" viewBox="0 0 120 200">
      <rect x="44" y="6" width="32" height="32" rx="5" fill="var(--cap,#E2A62A)"/>
      <rect x="51" y="38" width="18" height="14" fill="#E9DCD8"/>
      <rect x="20" y="50" width="80" height="140" rx="16" fill="#FFFBFA" fill-opacity=".9" stroke="#2A1420" stroke-opacity=".25" stroke-width="2"/>
      <rect x="27" y="82" width="66" height="102" rx="10" fill="var(--liquid,#C2416B)"/>
      <rect x="39" y="108" width="42" height="48" rx="3" fill="#FFFBFA" fill-opacity=".92"/>
      <g transform="translate(60 132)" fill="none" stroke="var(--liquid,#C2416B)" stroke-width="2">
        <rect x="-8" y="-8" width="16" height="16"/><rect x="-8" y="-8" width="16" height="16" transform="rotate(45)"/>
      </g>
      <path d="M31 60v112" stroke="#fff" stroke-opacity=".55" stroke-width="3" stroke-linecap="round"/>
    </symbol>
    <symbol id="star" viewBox="-12 -12 24 24">
      <g fill="none" stroke="currentColor" stroke-width="1.8"><rect x="-8" y="-8" width="16" height="16"/><rect x="-8" y="-8" width="16" height="16" transform="rotate(45)"/></g>
    </symbol>
    <pattern id="girih" width="44" height="44" patternUnits="userSpaceOnUse">
      <g fill="none" stroke="#E2A62A" stroke-opacity=".3" stroke-width="1">
        <rect x="10" y="10" width="24" height="24"/><rect x="10" y="10" width="24" height="24" transform="rotate(45 22 22)"/>
      </g>
    </pattern>
  </defs>
</svg>"""

def icon(paths):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'

I_SEARCH = icon('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>')
I_USER = icon('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>')
I_BAG = icon('<path d="M5 8h14l-1 12H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>')
I_TRUCK = icon('<path d="M2 6h11v10H2zM13 10h4l4 3v3h-8"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>')
I_SHIELD = icon('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>')
I_VIAL = icon('<path d="M10 3h4M11 3v5l-4 9a3 3 0 0 0 2.7 4h4.6A3 3 0 0 0 17 17l-4-9V3"/>')
I_LOCK = icon('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>')

def bottle(liquid=None, cap=None, cls="bottle", extra=""):
    style = ""
    if liquid: style += f"--liquid:{liquid};"
    if cap: style += f"--cap:{cap};"
    return f'<svg class="{cls}" viewBox="0 0 120 200" style="{style}" aria-hidden="true"{extra}><use href="#bottle"/></svg>'

HEADER = f"""{DEFS}
<div class="topbar"><div class="wrap">
  <span>ارسال رایگان برای سفارش‌های بالای ۳٬۰۰۰٬۰۰۰ تومان</span>
  <span>با هر سفارش، دو نمونه ۲ میلی‌لیتری هدیه بگیرید</span>
</div></div>
<header class="site-header"><div class="wrap bar">
  <a class="brand" href="/" aria-label="باغ‌عطر، صفحه اصلی"><svg class="brand-mark" aria-hidden="true"><use href="#star"/></svg><span>باغ‌عطر</span></a>
  <nav class="primary" aria-label="منوی اصلی"><ul>
    <li><a href="#bestsellers">همه عطرها</a></li>
    <li><a href="#families">خانواده‌های بویایی</a></li>
    <li><a href="#notes">بر اساس نُت</a></li>
    <li><a href="#gifts">ست هدیه</a></li>
    <li><a href="#story">داستان ما</a></li>
    <li><a href="#journal">مجله</a></li>
  </ul></nav>
  <div class="tools">
    <form class="search" role="search" action="#bestsellers">
      {I_SEARCH}<label class="sr" for="q">جستجو</label>
      <input id="q" type="search" placeholder="جستجوی عطر یا نُت">
    </form>
    <a class="icon-btn" href="#" aria-label="حساب کاربری">{I_USER}</a>
    <a class="icon-btn" href="#" aria-label="سبد خرید">{I_BAG}<span class="cart-count">۰</span></a>
  </div>
</div></header>"""

HERO = f"""<section class="hero" aria-labelledby="hero-title"><div class="wrap hero-grid">
  <div class="hero-copy">
    <h1 id="hero-title">بوی باغ‌های ایران، در یک شیشه</h1>
    <p class="lead">گل محمدی کاشان، زعفران قائنات، بهارنارنج و عود؛ عطرهایی که با نُت‌های ایرانی ساخته می‌شوند و با تضمین اصالت به دستتان می‌رسند.</p>
    <div class="cta-row">
      <a class="btn btn-primary" href="#bestsellers">مشاهده پرفروش‌ها</a>
      <a class="btn btn-ghost" href="#notes">عطر مناسب من کدام است؟</a>
    </div>
  </div>
  <div class="hero-art">
    <svg viewBox="0 0 440 560" role="img" aria-label="شیشه عطر در یک طاق ایرانی">
      <path d="M10 560V220a210 210 0 0 1 420 0V560z" fill="#8E1F45"/>
      <path d="M32 560V220a188 188 0 0 1 376 0V560z" fill="url(#girih)"/>
      <path d="M32 560V220a188 188 0 0 1 376 0V560" fill="none" stroke="#E2A62A" stroke-width="2"/>
      <ellipse cx="220" cy="528" rx="92" ry="10" fill="#000" fill-opacity=".28"/>
      <use href="#bottle" x="130" y="228" width="180" height="300" style="--liquid:#E2A62A;--cap:#F7ECE9"/>
    </svg>
    <span class="note-tag note-1">گل محمدی<small>نُت سر</small></span>
    <span class="note-tag note-2">زعفران<small>نُت میانی</small></span>
    <span class="note-tag note-3">عود و مشک<small>نُت پایه</small></span>
  </div>
</div></section>"""

TRUST = f"""<section class="trust" aria-label="تضمین‌های خرید"><div class="wrap"><ul>
  <li>{I_SHIELD}<div><strong>اصالت کالا تضمین‌شده</strong><span>بازگشت وجه در صورت تقلبی بودن</span></div></li>
  <li>{I_TRUCK}<div><strong>ارسال به سراسر ایران</strong><span>تهران، ۲۴ ساعته</span></div></li>
  <li>{I_VIAL}<div><strong>نمونه ۲ میلی‌لیتری</strong><span>قبل از خرید امتحان کنید</span></div></li>
  <li>{I_LOCK}<div><strong>پرداخت امن</strong><span>درگاه بانکی معتبر</span></div></li>
</ul></div></section>"""

def families_html():
    items = "".join(
        f'<a class="family" href="#" style="--bg:{bg}"><div class="family-arch">{bottle(liq, "#F7ECE9")}</div>'
        f'<h3>{name}</h3><p>{sub}</p></a>'
        for name, sub, bg, liq in FAMILIES)
    return f"""<section class="section" id="families" aria-labelledby="fam-title"><div class="wrap">
  <div class="section-head"><h2 id="fam-title">خانواده‌های بویایی</h2>
  <p>اگر نُت‌ها را نمی‌شناسید، از خانواده‌ای شروع کنید که بوی آن را دوست دارید.</p></div>
  <div class="families">{items}</div>
</div></section>"""

def products_html():
    cards = []
    for name, notes, size, price, liq, cap, tag in PRODUCTS:
        badge = f'<span class="badge">{tag}</span>' if tag else ""
        cards.append(
            f'<article class="product"><a class="product-media" href="#" style="--liquid:{liq}" aria-label="{name}">'
            f'{bottle(liq, cap)}{badge}</a>'
            f'<div class="product-body"><h3><a href="#">{name}</a></h3><p class="notes">{notes}</p>'
            f'<div class="buy"><div class="price"><small>{size}</small><strong>{price}<span>تومان</span></strong></div>'
            f'<button class="btn btn-small" type="button">افزودن به سبد</button></div></div></article>')
    return f"""<section class="section products-section" id="bestsellers" aria-labelledby="prod-title"><div class="wrap">
  <div class="section-head"><h2 id="prod-title">پرفروش‌های باغ‌عطر</h2>
  <div class="chips" role="group" aria-label="فیلتر عطرها">
    <button class="chip" type="button" aria-pressed="true">همه</button>
    <button class="chip" type="button" aria-pressed="false">زنانه</button>
    <button class="chip" type="button" aria-pressed="false">مردانه</button>
    <button class="chip" type="button" aria-pressed="false">یونیسکس</button>
  </div><a class="link-more" href="#">مشاهده همه عطرها</a></div>
  <div class="product-grid">{''.join(cards)}</div>
</div></section>"""

def notes_html():
    chips = "".join(f'<a href="#" style="--dot:{c}">{n}</a>' for n, c in NOTES)
    return f"""<section class="section notes-band" id="notes" aria-labelledby="notes-title"><div class="wrap notes-wrap">
  <div><h2 id="notes-title">بوی مورد علاقه‌تان را پیدا کنید</h2>
  <p>یک نُت را انتخاب کنید تا همه عطرهایی که آن را دارند ببینید.</p></div>
  <div class="note-chips">{chips}</div>
</div></section>"""

STORY = f"""<section class="section story" id="story" aria-labelledby="story-title"><div class="wrap story-grid">
  <div>
    <h2 id="story-title">هر سال، از سپیده‌دم اردیبهشت شروع می‌شود</h2>
    <p class="lead">گل محمدی فقط چند هفته در سال می‌شکفد. ما همان روزها در کاشان گل می‌چینیم و به روش سنتی تقطیر می‌کنیم تا بوی باغ، بی‌واسطه به شیشه برسد.</p>
    <ol class="steps">
      <li><div><h3>چیدن پیش از طلوع آفتاب</h3><p>گل‌ها تا پیش از گرم شدن هوا چیده می‌شوند تا عطرشان از دست نرود.</p></div></li>
      <li><div><h3>تقطیر در دیگ مسی</h3><p>عرق و اسانس به‌آرامی و با روش سنتی گرفته می‌شود.</p></div></li>
      <li><div><h3>رسیدن در شیشه</h3><p>هر عطر پیش از عرضه چند هفته می‌ماند تا نُت‌هایش با هم یکی شوند.</p></div></li>
    </ol>
  </div>
  <div class="story-art">
    <svg viewBox="0 0 400 480" role="img" aria-label="طرح هندسی ایرانی">
      <rect width="400" height="480" rx="14" fill="#17706F"/>
      <rect width="400" height="480" rx="14" fill="url(#girih)"/>
      <path d="M40 480V210a160 160 0 0 1 320 0V480" fill="#2A1420" fill-opacity=".25" stroke="#E2A62A" stroke-width="2"/>
      <use href="#bottle" x="140" y="200" width="120" height="200" style="--liquid:#C2416B;--cap:#E2A62A"/>
    </svg>
  </div>
</div></section>"""

GIFTS = f"""<section class="section gifts" id="gifts" aria-labelledby="gift-title"><div class="wrap gifts-grid">
  <div>
    <h2 id="gift-title">ست هدیه برای نوروز، یلدا و هر روز خاص</h2>
    <p>ست‌های آماده در جعبه‌ی دست‌دوز، همراه با کارت تبریک دست‌نویس. تهران، همان روز ارسال می‌شود.</p>
    <a class="btn btn-light" href="#">مشاهده ست‌های هدیه</a>
  </div>
  <div class="gift-bottles" aria-hidden="true">
    {bottle("#E2A62A", "#8E1F45")}{bottle("#C2416B", "#F7ECE9")}{bottle("#3A2418", "#E2A62A")}
  </div>
</div></section>"""

def reviews_html():
    cards = "".join(
        f'<figure class="review"><div class="stars" role="img" aria-label="پنج ستاره">★★★★★</div>'
        f'<blockquote>{q}</blockquote><figcaption><footer><strong>{n}</strong>، {c}</footer></figcaption></figure>'
        for q, n, c in REVIEWS)
    return f"""<section class="section" aria-labelledby="rev-title"><div class="wrap">
  <div class="section-head"><h2 id="rev-title">نظر مشتریان</h2></div>
  <div class="reviews-grid">{cards}</div>
</div></section>"""

def journal_html():
    posts = "".join(
        f'<a class="post" href="#"><div class="post-media" style="--tint:{t};--ink:{i}"><svg aria-hidden="true"><use href="#star"/></svg></div>'
        f'<h3>{title}</h3><p>{meta}</p></a>'
        for title, meta, t, i in POSTS)
    return f"""<section class="section journal" id="journal" aria-labelledby="jour-title"><div class="wrap">
  <div class="section-head"><h2 id="jour-title">مجله عطر</h2><a class="link-more" href="#">همه مقاله‌ها</a></div>
  <div class="journal-grid">{posts}</div>
</div></section>"""

NEWSLETTER = """<section class="section newsletter" aria-labelledby="news-title"><div class="wrap"><div class="box">
  <div><h2 id="news-title">از عطرهای تازه زودتر باخبر شوید</h2><p>ماهی یک ایمیل، همراه با کد تخفیف اولین خرید.</p></div>
  <form class="news-form" action="#"><label class="sr" for="email">ایمیل</label>
    <input id="email" type="email" placeholder="ایمیل شما" autocomplete="email">
    <button class="btn btn-primary" type="submit">عضویت</button></form>
</div></div></section>"""

FOOTER = """<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div><a class="brand" href="/"><svg class="brand-mark" aria-hidden="true"><use href="#star"/></svg><span>باغ‌عطر</span></a>
      <p>فروشگاه آنلاین عطرهای ایرانی، با ارسال به سراسر کشور.</p></div>
    <div><h3>خرید</h3><ul><li><a href="#bestsellers">همه عطرها</a></li><li><a href="#families">خانواده‌های بویایی</a></li><li><a href="#gifts">ست هدیه</a></li><li><a href="#">گلاب و عرقیات</a></li></ul></div>
    <div><h3>راهنما</h3><ul><li><a href="#">نحوه سفارش و ارسال</a></li><li><a href="#">بازگشت کالا</a></li><li><a href="#">سؤالات متداول</a></li><li><a href="#">پیگیری سفارش</a></li></ul></div>
    <div><h3>ارتباط با ما</h3><ul><li>تلفن: ۰۲۱-۰۰۰۰۰۰۰۰</li><li>ایمیل: info@example.ir</li><li>همه روزه ۹ تا ۲۱</li></ul></div>
  </div>
  <div class="footer-base">
    <span>© ۱۴۰۵ باغ‌عطر. همه حقوق محفوظ است.</span>
    <div class="trust-badges" aria-label="نمادهای اعتماد"><span>نماد اعتماد الکترونیکی</span><span>ساماندهی</span><span>اتحادیه کسب‌وکار مجازی</span></div>
  </div>
</div></footer>"""

MAIN_SECTIONS = [HERO, TRUST, families_html(), products_html(), notes_html(), STORY, GIFTS, reviews_html(), journal_html(), NEWSLETTER]

def wp(chunk):
    return f"<!-- wp:html -->\n{chunk}\n<!-- /wp:html -->"

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def main():
    css = (ROOT / "src/style.css").read_text(encoding="utf-8")

    # --- static export (Vercel) ---
    page = f"""<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>باغ‌عطر | فروشگاه آنلاین عطرهای ایرانی</title>
<meta name="description" content="خرید آنلاین عطرهای ایرانی با نُت‌های گل محمدی، زعفران، بهارنارنج و عود. اصالت کالا تضمین‌شده و ارسال به سراسر ایران.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
{HEADER}
<main>
{chr(10).join(MAIN_SECTIONS)}
</main>
{FOOTER}
</body>
</html>
"""
    write(PUBLIC / "index.html", page)
    write(PUBLIC / "assets/style.css", css)

    # --- WordPress block theme ---
    write(THEME / "assets/style.css", css)
    write(THEME / "style.css", """/*
Theme Name: Bagh-Atr (باغ‌عطر)
Description: Block theme for a Persian perfume store. RTL, Vazirmatn + Aref Ruqaa.
Version: 1.0.0
Requires at least: 6.6
Requires PHP: 7.4
Text Domain: bagh-atr
*/
""")
    write(THEME / "theme.json", json.dumps({
        "$schema": "https://schemas.wp.org/trunk/theme.json",
        "version": 3,
        "settings": {
            "layout": {"contentSize": "1240px", "wideSize": "1440px"},
            "color": {"palette": [
                {"slug": "blush", "name": "Blush", "color": "#F7ECE9"},
                {"slug": "plum", "name": "Plum", "color": "#2A1420"},
                {"slug": "pomegranate", "name": "Pomegranate", "color": "#8E1F45"},
                {"slug": "turquoise", "name": "Turquoise", "color": "#17706F"},
                {"slug": "saffron", "name": "Saffron", "color": "#E2A62A"},
            ]},
        },
        "styles": {
            "color": {"background": "#F7ECE9", "text": "#2A1420"},
            "spacing": {"blockGap": "0"},
        },
    }, ensure_ascii=False, indent=2))
    write(THEME / "functions.php", f"""<?php
add_action('wp_enqueue_scripts', function () {{
    wp_enqueue_style('bagh-atr-fonts', '{FONTS}', [], null);
    wp_enqueue_style('bagh-atr', get_theme_file_uri('assets/style.css'), [], wp_get_theme()->get('Version'));
}});
add_action('after_setup_theme', function () {{
    add_theme_support('wp-block-styles');
}});
""")
    write(THEME / "parts/header.html", wp(HEADER))
    write(THEME / "parts/footer.html", wp(FOOTER))
    parts_header = '<!-- wp:template-part {"slug":"header","tagName":"div"} /-->'
    parts_footer = '<!-- wp:template-part {"slug":"footer","tagName":"div"} /-->'
    main = "\n\n".join(wp(s) for s in MAIN_SECTIONS)
    write(THEME / "templates/front-page.html",
          f'{parts_header}\n\n<!-- wp:group {{"tagName":"main","layout":{{"type":"default"}}}} -->\n'
          f'<main class="wp-block-group">\n{main}\n</main>\n<!-- /wp:group -->\n\n{parts_footer}\n')
    generic = (f'{parts_header}\n\n<!-- wp:group {{"tagName":"main","layout":{{"type":"constrained"}}}} -->\n'
               f'<main class="wp-block-group section"><!-- wp:post-title /-->\n<!-- wp:post-content /--></main>\n'
               f'<!-- /wp:group -->\n\n{parts_footer}\n')
    write(THEME / "templates/index.html", generic)
    write(THEME / "templates/page.html", generic)
    print("built: public/ and wp-content/themes/bagh-atr/")

if __name__ == "__main__":
    main()
