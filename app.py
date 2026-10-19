
import streamlit as st
import pandas as pd
from datetime import datetime
from html import escape

st.set_page_config(
    page_title="ShelfSense AI | Smart Bazaar Finder",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Product catalogue: 20 categories x 10 products ----------
CATALOGUE = {
    "Biscuits & Cookies": ["Parle-G", "Good Day Butter", "Oreo Original", "Dark Fantasy", "Hide & Seek", "Marie Gold", "Bourbon", "Treat Chocolate", "50-50 Maska Chaska", "Monaco"],
    "Chips & Snacks": ["Lay's Classic Salted", "Lay's Magic Masala", "Kurkure Masala Munch", "Doritos Nacho Cheese", "Bingo Mad Angles", "Uncle Chipps", "Haldiram Aloo Bhujia", "Too Yumm! Chips", "Pringles Original", "Balaji Wafers"],
    "Instant Noodles": ["Maggi Masala", "Maggi Atta Noodles", "Yippee Magic Masala", "Top Ramen Curry", "Knorr Soupy Noodles", "Ching's Hakka Noodles", "Sunfeast Pasta", "Cup Noodles", "Korean Spicy Noodles", "Oats Noodles"],
    "Chocolates & Candy": ["Dairy Milk", "KitKat", "5 Star", "Perk", "Munch", "Milkybar", "Temptations", "Fuse", "Mentos", "Pulse Candy"],
    "Dairy & Milk": ["Full Cream Milk", "Toned Milk", "Skimmed Milk", "Curd", "Greek Yogurt", "Paneer", "Butter", "Cheese Slices", "Fresh Cream", "Buttermilk"],
    "Bread & Bakery": ["White Bread", "Brown Bread", "Multigrain Bread", "Burger Buns", "Pizza Base", "Pav", "Rusk", "Fruit Cake", "Croissant", "Garlic Bread"],
    "Breakfast & Cereals": ["Corn Flakes", "Chocos", "Muesli", "Oats", "Granola", "Poha", "Upma Mix", "Dosa Mix", "Pancake Mix", "Peanut Butter"],
    "Tea & Coffee": ["Tata Tea Gold", "Red Label Tea", "Taj Mahal Tea", "Green Tea", "Instant Coffee", "Filter Coffee", "Cold Coffee Mix", "Masala Chai Mix", "Lemon Tea", "Decaf Coffee"],
    "Soft Drinks & Juices": ["Coca-Cola", "Sprite", "Thums Up", "Fanta", "Maaza", "Real Orange Juice", "Apple Juice", "Lemon Soda", "Mango Drink", "Packaged Coconut Water"],
    "Rice & Grains": ["Basmati Rice", "Sona Masoori Rice", "Brown Rice", "Raw Rice", "Idli Rice", "Quinoa", "Wheat Dalia", "Jowar", "Bajra", "Ragi Flour"],
    "Atta & Flours": ["Whole Wheat Atta", "Multigrain Atta", "Maida", "Besan", "Rice Flour", "Corn Flour", "Ragi Flour Pack", "Jowar Flour", "Bajra Flour", "Idiyappam Flour"],
    "Pulses & Lentils": ["Toor Dal", "Moong Dal", "Masoor Dal", "Urad Dal", "Chana Dal", "Kabuli Chana", "Rajma", "Black Chana", "Green Moong", "Mixed Dal"],
    "Cooking Oils": ["Sunflower Oil", "Groundnut Oil", "Rice Bran Oil", "Mustard Oil", "Olive Oil", "Coconut Oil", "Soybean Oil", "Sesame Oil", "Canola Oil", "Ghee"],
    "Spices & Masalas": ["Turmeric Powder", "Red Chilli Powder", "Garam Masala", "Cumin Seeds", "Coriander Powder", "Black Pepper", "Mustard Seeds", "Kitchen King Masala", "Biryani Masala", "Sambar Powder"],
    "Sauces & Spreads": ["Tomato Ketchup", "Green Chilli Sauce", "Soy Sauce", "Mayonnaise", "Pasta Sauce", "Schezuan Sauce", "Vinegar", "Honey", "Jam", "Chocolate Spread"],
    "Personal Care": ["Bathing Soap", "Shampoo", "Conditioner", "Toothpaste", "Toothbrush", "Face Wash", "Body Lotion", "Deodorant", "Handwash", "Hair Oil"],
    "Home Cleaning": ["Dishwash Liquid", "Laundry Detergent", "Fabric Softener", "Floor Cleaner", "Toilet Cleaner", "Glass Cleaner", "Scrub Pad", "Cleaning Cloth", "Room Freshener", "Bleach Cleaner"],
    "Paper & Stationery": ["A4 Paper", "Notebook", "Ball Pen", "Pencil Pack", "Eraser", "Sticky Notes", "Marker Set", "Envelope Pack", "Tissue Box", "Paper Towels"],
    "Frozen Foods": ["Frozen Peas", "Sweet Corn", "French Fries", "Veg Nuggets", "Frozen Paratha", "Paneer Tikka", "Ice Cream Vanilla", "Ice Cream Chocolate", "Frozen Momos", "Mixed Vegetables"],
    "Pet Supplies": ["Dog Food Chicken", "Dog Biscuits", "Cat Food Tuna", "Cat Litter", "Pet Shampoo", "Chew Toy", "Pet Bowl", "Bird Seed Mix", "Fish Food", "Pet Wipes"],
}

BASE_PRICES = {
    "Biscuits & Cookies": 10, "Chips & Snacks": 10,
    "Instant Noodles": 14, "Chocolates & Candy": 5,
    "Dairy & Milk": 25, "Bread & Bakery": 20,
    "Breakfast & Cereals": 45, "Tea & Coffee": 60,
    "Soft Drinks & Juices": 20, "Rice & Grains": 55,
    "Atta & Flours": 35, "Pulses & Lentils": 50,
    "Cooking Oils": 90, "Spices & Masalas": 25,
    "Sauces & Spreads": 35, "Personal Care": 30,
    "Home Cleaning": 35, "Paper & Stationery": 10,
    "Frozen Foods": 60, "Pet Supplies": 40,
}

ICONS = [
    "🍪", "🥔", "🍜", "🍫", "🥛", "🍞", "🥣", "☕", "🥤", "🍚",
    "🌾", "🫘", "🫒", "🧂", "🥫", "🧴", "🧹", "📒", "🧊", "🐾"
]

rows = []
for aisle_no, (category, items) in enumerate(CATALOGUE.items(), start=1):
    for product_no, product in enumerate(items, start=1):
        shelf_letter = "A" if product_no <= 5 else "B"
        shelf_level = ((product_no - 1) % 5) + 1
        rows.append({
            "id": f"{aisle_no:02d}-{product_no:02d}",
            "product": product,
            "category": category,
            "price": float(BASE_PRICES[category] + (product_no - 1) * 5),
            "aisle": aisle_no,
            "shelf": f"{shelf_letter}{shelf_level}",
            "icon": ICONS[aisle_no - 1],
        })

products_df = pd.DataFrame(rows)

# ---------- Session state ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "receipt" not in st.session_state:
    st.session_state.receipt = None
if "screen" not in st.session_state:
    st.session_state.screen = "Find a product"

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f8f7; color: #20332f; }
[data-testid="stHeader"] { background: rgba(245,248,247,.92); }
.block-container { padding-top: 1.25rem; padding-bottom: 3rem; max-width: 1440px; }
[data-testid="stSidebar"] { background: #edf5f1; border-right: 1px solid #dce9e2; }
[data-testid="stSidebar"] * { color: #203b34; }
.brand { background: linear-gradient(115deg,#e1f4ea,#e7f0ff); border:1px solid #d8e9e0; padding:24px 28px; border-radius:22px; margin-bottom:20px; }
.brand h1 { font-family:Manrope,sans-serif; font-size:30px; letter-spacing:-1px; margin:0; color:#183c32; }
.brand p { color:#527268; margin:7px 0 0 0; font-size:14px; }
.eyebrow { color:#37836a; text-transform:uppercase; letter-spacing:2px; font-size:11px; font-weight:800; }
.section-title { font-family:Manrope,sans-serif; font-size:25px; font-weight:800; color:#203b34; margin:0 0 4px 0; }
.muted { color:#71847d; font-size:13px; }
.product-card { background:white; border:1px solid #e0eae5; border-radius:17px; padding:16px; min-height:154px; box-shadow:0 4px 14px rgba(32,59,52,.035); margin-bottom:10px; }
.product-name { font-size:16px; font-weight:800; color:#213c34; margin:6px 0 3px; }
.category-tag { display:inline-block; font-size:11px; color:#507469; background:#eef6f1; padding:4px 8px; border-radius:7px; }
.price { color:#197a58; font-weight:800; font-size:19px; margin-top:9px; }
.location-chip { display:inline-block; background:#fff2cf; border:1px solid #f0d88e; color:#7c5600; border-radius:9px; padding:7px 10px; font-weight:800; font-size:13px; margin:5px 4px 0 0; }
.location-hero { background:linear-gradient(110deg,#fff1c9,#fff8e8); border:2px solid #f0cc63; border-radius:17px; padding:15px 18px; margin:12px 0; }
.location-hero .big { font-size:23px; font-weight:900; color:#765000; }
.location-hero .small { color:#8b6a1c; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }
.metric-box { background:white; border:1px solid #dfebe5; padding:15px 18px; border-radius:15px; }
.metric-label { color:#6c8178; font-size:12px; font-weight:700; }
.metric-value { color:#1b6b4e; font-size:25px; font-weight:900; }
.step-pill { display:inline-block; border-radius:999px; padding:7px 12px; background:#e7f4ec; color:#236849; font-size:12px; font-weight:800; }
.bill-box { background:white; border:1px solid #dfe9e4; border-radius:18px; padding:20px; }
div.stButton > button { border-radius:10px; border:1px solid #cfe1d7; font-weight:700; min-height:40px; }
div.stButton > button[kind="primary"] { background:#247957; border-color:#247957; color:white; }
div.stButton > button[kind="primary"]:hover { background:#1b6246; border-color:#1b6246; }
div[data-testid="stTextInput"] input { border-radius:12px; }
hr { border-color:#e0eae5; }
</style>
""", unsafe_allow_html=True)


def money(value):
    return f"₹{value:,.2f}"


def location_markup(row):
    return f"""<div class="location-hero">
      <div class="small">📍 Find it in store</div>
      <div class="big">AISLE {int(row['aisle'])} &nbsp; · &nbsp; SHELF {escape(str(row['shelf']))}</div>
      <div style="color:#785c1e;font-size:13px;margin-top:5px;">{escape(str(row['category']))} section</div>
    </div>"""


def rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


def add_to_cart(product_id):
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1
    st.session_state.receipt = None


def cart_count():
    return sum(st.session_state.cart.values())


def cart_total():
    lookup = products_df.set_index("id")
    return sum(
        float(lookup.loc[pid, "price"]) * qty
        for pid, qty in st.session_state.cart.items()
        if pid in lookup.index
    )


# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown('<div class="eyebrow">SMART BAZAAR</div>', unsafe_allow_html=True)
    st.markdown("## ShelfSense AI")
    st.caption("Search it. Find it. Shop faster.")
    st.markdown("---")

    screens = ["Find a product", "My cart & locations", "Final bill"]
    screen = st.radio(
        "YOUR SHOPPING",
        screens,
        index=screens.index(st.session_state.screen),
        key="screen_navigation",
    )
    st.session_state.screen = screen

    st.markdown("---")
    st.markdown(
        f'<div class="metric-box"><div class="metric-label">ITEMS IN CART</div>'
        f'<div class="metric-value">{cart_count()}</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        f'<div class="metric-box"><div class="metric-label">CURRENT TOTAL</div>'
        f'<div class="metric-value">{money(cart_total())}</div></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.caption("Demo shelf map: aisle numbers and shelf codes are sample store locations.")

st.markdown("""
<div class="brand">
  <div class="eyebrow">SMART BAZAAR PRODUCT FINDER</div>
  <h1>Find your product. Skip the searching.</h1>
  <p>Search any item and see its aisle and shelf highlighted instantly.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Screen 1: Product search ----------
if screen == "Find a product":
    st.markdown(
        '<div class="section-title">Find a product</div>'
        '<div class="muted">200 products · 20 categories · clear shelf directions</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    search_col, cat_col = st.columns([2.2, 1])
    with search_col:
        query = st.text_input(
            "Search products",
            placeholder="Try Maggi, Oreo, shampoo, rice...",
            label_visibility="collapsed",
        )
    with cat_col:
        selected_category = st.selectbox(
            "Category",
            ["All categories"] + list(CATALOGUE.keys()),
            label_visibility="collapsed",
        )

    filter_col, sort_col = st.columns([1, 1])
    with filter_col:
        max_price = st.slider(
            "Maximum price", min_value=10, max_value=200,
            value=200, step=5,
        )
    with sort_col:
        sort_by = st.selectbox(
            "Sort products",
            ["Recommended", "Price: low to high", "Price: high to low", "Aisle number"],
        )

    shown = products_df.copy()
    if query.strip():
        mask = (
            shown["product"].str.contains(query.strip(), case=False, na=False)
            | shown["category"].str.contains(query.strip(), case=False, na=False)
        )
        shown = shown[mask]

    if selected_category != "All categories":
        shown = shown[shown["category"] == selected_category]

    shown = shown[shown["price"] <= max_price]

    if sort_by == "Price: low to high":
        shown = shown.sort_values("price")
    elif sort_by == "Price: high to low":
        shown = shown.sort_values("price", ascending=False)
    elif sort_by == "Aisle number":
        shown = shown.sort_values(["aisle", "shelf"])

    st.write("")
    st.markdown(
        f'<span class="step-pill">{len(shown)} MATCHING PRODUCTS</span>',
        unsafe_allow_html=True,
    )

    if query.strip() and not shown.empty:
        first = shown.iloc[0]
        st.markdown("### Best match — location highlighted")
        st.markdown(location_markup(first), unsafe_allow_html=True)

    if shown.empty:
        st.warning("No matching products. Try another product name or choose All categories.")
    else:
        for start in range(0, len(shown), 3):
            chunk = shown.iloc[start:start + 3]
            cols = st.columns(3)
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    st.markdown(f"""
                    <div class="product-card">
                      <div style="font-size:25px">{row['icon']}</div>
                      <div class="product-name">{escape(row['product'])}</div>
                      <span class="category-tag">{escape(row['category'])}</span>
                      <div class="price">{money(row['price'])}</div>
                      <div class="location-chip">📍 Aisle {int(row['aisle'])}</div>
                      <div class="location-chip">Shelf {escape(row['shelf'])}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button(
                        "＋ Add to cart",
                        key=f"add_{row['id']}",
                        type="primary",
                        use_container_width=True,
                    ):
                        add_to_cart(row["id"])
                        st.toast(f"{row['product']} added to cart")
                        rerun()

# ---------- Screen 2: Cart and locations ----------
elif screen == "My cart & locations":
    st.markdown(
        '<div class="section-title">Your cart & shelf locations</div>'
        '<div class="muted">Use the highlighted aisle and shelf code to collect each item.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if not st.session_state.cart:
        st.info('Your cart is empty. Go to "Find a product" and add items.')
        if st.button("Browse products", type="primary"):
            st.session_state.screen = "Find a product"
            rerun()
    else:
        lookup = products_df.set_index("id")
        st.markdown(
            f'<div class="step-pill">{cart_count()} ITEMS TO COLLECT</div>',
            unsafe_allow_html=True,
        )
        st.write("")

        for pid in list(st.session_state.cart.keys()):
            if pid not in lookup.index:
                continue

            row = lookup.loc[pid]
            qty = st.session_state.cart[pid]
            left, right = st.columns([3, 1])

            with left:
                st.markdown(f"""
                <div class="product-card" style="min-height:0">
                  <div class="product-name">{row['icon']} {escape(str(row['product']))}</div>
                  <span class="category-tag">{escape(str(row['category']))}</span>
                  <div style="margin-top:8px;color:#60796f;font-size:13px">
                    Quantity: <b>{qty}</b> &nbsp; · &nbsp;
                    Unit price: <b>{money(row['price'])}</b>
                  </div>
                  <div class="location-chip">📍 AISLE {int(row['aisle'])}</div>
                  <div class="location-chip">SHELF {escape(str(row['shelf']))}</div>
                </div>
                """, unsafe_allow_html=True)

            with right:
                st.write("")
                st.write("")
                st.markdown(
                    f"<div class='price'>{money(float(row['price']) * qty)}</div>",
                    unsafe_allow_html=True,
                )
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("＋", key=f"plus_{pid}", use_container_width=True):
                        add_to_cart(pid)
                        rerun()
                with c2:
                    if st.button("−", key=f"minus_{pid}", use_container_width=True):
                        if st.session_state.cart[pid] <= 1:
                            del st.session_state.cart[pid]
                        else:
                            st.session_state.cart[pid] -= 1
                        rerun()

        st.markdown("---")
        total_col, action_col = st.columns([2, 1])
        with total_col:
            st.markdown(
                f'<div class="metric-box"><div class="metric-label">CART TOTAL</div>'
                f'<div class="metric-value">{money(cart_total())}</div></div>',
                unsafe_allow_html=True,
            )
        with action_col:
            st.write("")
            if st.button(
                "Continue to final bill →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.screen = "Final bill"
                rerun()

# ---------- Screen 3: Final bill and checkout ----------
else:
    st.markdown(
        '<div class="section-title">Final bill</div>'
        '<div class="muted">Review your items before checkout.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if not st.session_state.cart and not st.session_state.receipt:
        st.info("There are no items to bill yet. Add products to your cart first.")
        if st.button("Find products", type="primary"):
            st.session_state.screen = "Find a product"
            rerun()

    elif st.session_state.receipt:
        receipt = st.session_state.receipt
        st.balloons()
        st.markdown(f"""
        <div class="brand" style="text-align:center">
          <div style="font-size:42px">🎉</div>
          <div class="eyebrow">CHECKOUT COMPLETE</div>
          <h1>Thank you for shopping!</h1>
          <p>Receipt {receipt['number']} · {receipt['time']}</p>
          <div style="font-size:30px;font-weight:900;color:#197a58;margin-top:12px">
            {money(receipt['total'])}
          </div>
        </div>
        """, unsafe_allow_html=True)

        receipt_df = pd.DataFrame(receipt["items"])
        st.dataframe(receipt_df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download receipt (.csv)",
            receipt_df.to_csv(index=False).encode("utf-8"),
            file_name=f"shelfsense_receipt_{receipt['number']}.csv",
            mime="text/csv",
        )

        if st.button("Start a new shopping session", type="primary"):
            st.session_state.cart = {}
            st.session_state.receipt = None
            st.session_state.screen = "Find a product"
            rerun()

    else:
        lookup = products_df.set_index("id")
        bill_rows = []

        for pid, qty in st.session_state.cart.items():
            if pid not in lookup.index:
                continue
            row = lookup.loc[pid]
            bill_rows.append({
                "Product": row["product"],
                "Category": row["category"],
                "Qty": qty,
                "Unit price": float(row["price"]),
                "Amount": float(row["price"]) * qty,
                "Aisle": int(row["aisle"]),
                "Shelf": row["shelf"],
            })

        bill_df = pd.DataFrame(bill_rows)

        if not bill_df.empty:
            st.markdown('<div class="bill-box">', unsafe_allow_html=True)
            st.dataframe(
                bill_df[["Product", "Qty", "Unit price", "Amount"]],
                use_container_width=True,
                hide_index=True,
            )

            subtotal = float(bill_df["Amount"].sum())
            st.markdown("---")
            a, b = st.columns(2)

            with a:
                st.markdown(
                    '<div class="metric-box"><div class="metric-label">ITEMS</div>'
                    f'<div class="metric-value">{cart_count()}</div></div>',
                    unsafe_allow_html=True,
                )
            with b:
                st.markdown(
                    '<div class="metric-box"><div class="metric-label">AMOUNT DUE</div>'
                    f'<div class="metric-value">{money(subtotal)}</div></div>',
                    unsafe_allow_html=True,
                )

            st.caption("Demo bill: taxes and payment processing are not included.")

            if st.button(
                "✓ Confirm checkout & generate bill",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.receipt = {
                    "number": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "total": subtotal,
                    "items": bill_rows,
                }
                st.balloons()
                rerun()

            st.markdown("</div>", unsafe_allow_html=True)
