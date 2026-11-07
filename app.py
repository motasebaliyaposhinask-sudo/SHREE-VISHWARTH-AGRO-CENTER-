import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Shree Vishwarth Agro Center",
    page_icon="🌱",
    layout="wide"
)

# Database
conn = sqlite3.connect("agro_center.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mobile TEXT,
    address TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    stock REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date TEXT,
    entry_type TEXT,
    customer TEXT,
    product TEXT,
    quantity REAL,
    rate REAL,
    total REAL,
    payment REAL,
    note TEXT
)
""")

conn.commit()

# Header
st.title("🌱 શ્રી વિશ્વરથ એગ્રો સેન્ટર")
st.caption("Billing | Purchase | Sales | Customer Account")

st.divider()

# Sidebar
st.sidebar.title("મુખ્ય મેનુ")

menu = st.sidebar.radio(
    "વિભાગ પસંદ કરો",
    [
        "ડેશબોર્ડ",
        "ગ્રાહક ઉમેરો",
        "પ્રોડક્ટ ઉમેરો",
        "વેચાણ બિલ",
        "ખરીદી એન્ટ્રી",
        "હિસાબ અને લેણું",
        "ડેટા બેકઅપ"
    ]
)

# Dashboard
if menu == "ડેશબોર્ડ":

    st.header("ડેશબોર્ડ")

    customers = pd.read_sql_query(
        "SELECT * FROM customers", conn
    )

    transactions = pd.read_sql_query(
        "SELECT * FROM transactions", conn
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("કુલ ગ્રાહકો", len(customers))

    if not transactions.empty:
        sales = transactions[
            transactions["entry_type"] == "વેચાણ"
        ]["total"].sum()

        purchase = transactions[
            transactions["entry_type"] == "ખરીદી"
        ]["total"].sum()
    else:
        sales = 0
        purchase = 0

    col2.metric("કુલ વેચાણ", f"₹ {sales:,.2f}")
    col3.metric("કુલ ખરીદી", f"₹ {purchase:,.2f}")

    st.subheader("તાજેતરની એન્ટ્રી")

    st.dataframe(
        transactions.tail(10),
        use_container_width=True
    )

# Add Customer
elif menu == "ગ્રાહક ઉમેરો":

    st.header("નવો ગ્રાહક ઉમેરો")

    with st.form("customer_form"):

        name = st.text_input("ગ્રાહકનું નામ")
        mobile = st.text_input("મોબાઇલ નંબર")
        address = st.text_area("સરનામું")

        submit = st.form_submit_button("ગ્રાહક સેવ કરો")

        if submit:
            if name.strip():
                cur.execute(
                    "INSERT INTO customers (name,mobile,address) VALUES (?,?,?)",
                    (name, mobile, address)
                )
                conn.commit()
                st.success("ગ્રાહક સફળતાપૂર્વક સેવ થયો.")
            else:
                st.error("ગ્રાહકનું નામ લખો.")

    st.subheader("ગ્રાહકોની યાદી")

    st.dataframe(
        pd.read_sql_query("SELECT * FROM customers", conn),
        use_container_width=True
    )

# Add Product
elif menu == "પ્રોડક્ટ ઉમેરો":

    st.header("નવો પ્રોડક્ટ ઉમેરો")

    with st.form("product_form"):

        product = st.text_input("પ્રોડક્ટનું નામ")
        price = st.number_input("ભાવ", min_value=0.0)
        stock = st.number_input("જથ્થો", min_value=0.0)

        submit = st.form_submit_button("પ્રોડક્ટ સેવ કરો")

        if submit:
            if product.strip():
                cur.execute(
                    "INSERT INTO products (name,price,stock) VALUES (?,?,?)",
                    (product, price, stock)
                )
                conn.commit()
                st.success("પ્રોડક્ટ સેવ થયો.")
            else:
                st.error("પ્રોડક્ટનું નામ લખો.")

    st.dataframe(
        pd.read_sql_query("SELECT * FROM products", conn),
        use_container_width=True
    )

# Sales and Purchase
elif menu in ["વેચાણ બિલ", "ખરીદી એન્ટ્રી"]:

    is_sale = menu == "વેચાણ બિલ"
    entry_type = "વેચાણ" if is_sale else "ખરીદી"

    st.header(menu)

    customers = pd.read_sql_query(
        "SELECT name FROM customers", conn
    )

    products = pd.read_sql_query(
        "SELECT name,price FROM products", conn
    )

    with st.form("transaction_form"):

        entry_date = st.date_input("તારીખ", date.today())

        customer_list = (
            customers["name"].tolist()
            if not customers.empty else []
        )

        product_list = (
            products["name"].tolist()
            if not products.empty else []
        )

        customer = st.selectbox(
            "ગ્રાહક / સપ્લાયર",
            customer_list + ["નવો / અન્ય"]
        )

        product = st.selectbox(
            "પ્રોડક્ટ",
            product_list if product_list else ["પ્રોડક્ટ ઉમેરો"]
        )

        quantity = st.number_input(
            "જથ્થો", min_value=0.0, step=1.0
        )

        rate = st.number_input(
            "ભાવ", min_value=0.0
        )

        payment = st.number_input(
            "મળેલ / ચૂકવેલ રકમ",
            min_value=0.0
        )

        note = st.text_input("નોંધ")

        total = quantity * rate

        st.write(f"*કુલ રકમ: ₹ {total:,.2f}*")

        submit = st.form_submit_button("એન્ટ્રી સેવ કરો")

        if submit:
            if quantity > 0 and rate >= 0:
                cur.execute("""
                    INSERT INTO transactions
                    (entry_date,entry_type,customer,product,
                    quantity,rate,total,payment,note)
                    VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    str(entry_date), entry_type, customer,
                    product, quantity, rate, total,
                    payment, note
                ))

                conn.commit()
                st.success("એન્ટ્રી સફળતાપૂર્વક સેવ થઈ.")
            else:
                st.error("જથ્થો યોગ્ય રીતે દાખલ કરો.")

# Ledger
elif menu == "હિસાબ અને લેણું":

    st.header("ગ્રાહક હિસાબ અને લેણું")

    data = pd.read_sql_query(
        "SELECT * FROM transactions", conn
    )

    if not data.empty:

        st.dataframe(data, use_container_width=True)

        customer_names = data["customer"].unique().tolist()

        selected = st.selectbox(
            "ગ્રાહક પસંદ કરો", customer_names
        )

        customer_data = data[
            data["customer"] == selected
        ]

        sales = customer_data[
            customer_data["entry_type"] == "વેચાણ"
        ]["total"].sum()

        purchases = customer_data[
            customer_data["entry_type"] == "ખરીદી"
        ]["total"].sum()

        payments = customer_data["payment"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("વેચાણ", f"₹ {sales:,.2f}")
        col2.metric("ખરીદી", f"₹ {purchases:,.2f}")
        col3.metric("જમા / ચૂકવણી", f"₹ {payments:,.2f}")

        st.dataframe(
            customer_data,
            use_container_width=True
        )

    else:
        st.info("હજુ કોઈ હિસાબ ઉપલબ્ધ નથી.")

# Backup
elif menu == "ડેટા બેકઅપ":

    st.header("ડેટા બેકઅપ")

    for table in ["customers", "products", "transactions"]:

        df = pd.read_sql_query(
            f"SELECT * FROM {table}", conn
        )

        st.download_button(
            label=f"{table} CSV ડાઉનલોડ કરો",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"{table}_backup.csv",
            mime="text/csv"
        )

    st.success("તમારો ડેટા CSV સ્વરૂપે બેકઅપ લઈ શકો છો.")

st.divider()
st.caption("© Shree Vishwarth Agro Center")
