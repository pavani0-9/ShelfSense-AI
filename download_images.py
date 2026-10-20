elif screen == "My cart & locations":
    st.markdown('<div class="section-title">Your cart & shelf locations</div><div class="muted">Use the highlighted aisle and shelf code to collect each item.</div>', unsafe_allow_html=True)
    st.write("")
    if not st.session_state.cart:
        st.info("Your cart is empty. Go to “Find a product” and add items.")
        if st.button("Browse products", type="primary"):
            st.session_state.screen = "Find a product"
            rerun()
    else:
        lookup = products_df.set_index("id")
        st.markdown(f'<div class="step-pill">{cart_count()} ITEMS TO COLLECT</div>', unsafe_allow_html=True)
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
                  <div style="margin-top:8px;color:#60796f;font-size:13px">Quantity: <b>{qty}</b> &nbsp; · &nbsp; Unit price: <b>{money(row['price'])}</b></div>
                  <div class="location-chip">📍 AISLE {int(row['aisle'])}</div><div class="location-chip">SHELF {escape(str(row['shelf']))}</div>
                </div>
                """, unsafe_allow_html=True)
            with right:
                st.write("")
                st.write("")
                st.markdown(f"<div class='price'>{money(float(row['price']) * qty)}</div>", unsafe_allow_html=True)
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
            st.markdown(f'<div class="metric-box"><div class="metric-label">CART TOTAL</div><div class="metric-value">{money(cart_total())}</div></div>', unsafe_allow_html=True)
        with action_col:
            st.write("")
            if st.button("Continue to final bill →", type="primary", use_container_width=True):
                st.session_state.screen = "Final bill"
                rerun()

# ---------- Screen 3: Bill ----------
else:
    st.markdown('<div class="section-title">Final bill</div><div class="muted">Review your items before checkout.</div>', unsafe_allow_html=True)
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
          <div style="font-size:30px;font-weight:900;color:#197a58;margin-top:12px">{money(receipt['total'])}</div>
        </div>
        """, unsafe_allow_html=True)
        receipt_df = pd.DataFrame(receipt["items"])
        st.dataframe(receipt_df, use_container_width=True, hide_index=True)
        st.download_button("⬇ Download receipt (.csv)", receipt_df.to_csv(index=False).encode("utf-8"), file_name=f"shelfsense_receipt_{receipt['number']}.csv", mime="text/csv")
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
            st.dataframe(bill_df[["Product", "Qty", "Unit price", "Amount"]], use_container_width=True, hide_index=True)
            subtotal = float(bill_df["Amount"].sum())
            st.markdown("---")
            a, b = st.columns(2)
            with a:
                st.markdown('<div class="metric-box"><div class="metric-label">ITEMS</div><div class="metric-value">' + str(cart_count()) + '</div></div>', unsafe_allow_html=True)
            with b:
                st.markdown(f'<div class="metric-box"><div class="metric-label">AMOUNT DUE</div><div class="metric-value">{money(subtotal)}</div></div>', unsafe_allow_html=True)
            st.caption("Demo bill: taxes and payment processing are not included.")
            if st.button("✓ Confirm checkout & generate bill", type="primary", use_container_width=True):
                st.session_state.receipt = {
                    "number": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                    "total": subtotal,
                    "items": bill_rows,
                }
                st.balloons()
                rerun()
            st.markdown('</div>', unsafe_allow_html=True)

