import sqlite3
import streamlit as st

# Konfigurasi Database Sederhana
conn = sqlite3.connect("fotocopy.db", check_same_thread=False)
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
"""
)
conn.commit()

st.title("🖨️ Sistem Manajemen Toko Fotocopy")

# Menu Sidebar
menu = st.sidebar.selectbox(
    "Pilih Menu", ["Kasir (POS)", "Kelola Stok", "Laporan Keuangan"]
)

if menu == "Kasir (POS)":
  st.header("Halaman Kasir & Transaksi")

  # Ambil data produk/jasa dari database
  cursor.execute("SELECT id, name, price, stock FROM products")
  products = cursor.fetchall()

  if not products:
    st.warning(
        "Belum ada produk/jasa. Silakan tambahkan di menu Kelola Stok terlebih"
        " dahulu."
    )
  else:
    product_dict = {f"{p[1]} (Rp {p[2]})": p for p in products}
    selected_prod_name = st.selectbox(
        "Pilih Layanan atau Barang ATK", list(product_dict.keys())
    )

    selected_prod = product_dict[selected_prod_name]

    # Jika produk adalah jasa cetak/fotocopy, beri opsi input lembar
    qty = 1
    if "Fotocopy" in selected_prod[1] or "Print" in selected_prod[1]:
      qty = st.number_input(
          "Jumlah Lembar / Halaman", min_value=1, value=1, step=1
      )
    else:
      qty = st.number_input("Jumlah Beli", min_value=1, value=1, step=1)

    subtotal = selected_prod[2] * qty
    st.info(f"Subtotal: **Rp {subtotal:,.0f}**")

    if st.button("Tambah ke Transaksi"):
      st.success(f"Berhasil menambahkan {qty}x {selected_prod[1]} ke kasir.")

elif menu == "Kelola Stok":
  st.header("Manajemen Stok & Harga")
  with st.form("add_product"):
    name = st.text_input("Nama Produk / Layanan (Contoh: Fotocopy A4, Pulpen)")
    category = st.selectbox("Kategori", ["Jasa", "ATK", "Bahan Baku"])
    price = st.number_input("Harga Satuan (Rp)", min_value=0.0, step=500.0)
    stock = st.number_input("Stok Awal", min_value=0, step=1)
    submit = st.form_submit_button("Simpan Produk")

    if submit:
      cursor.execute(
          "INSERT INTO products (name, category, price, stock) VALUES (?, ?,"
          " ?, ?)",
          (name, category, price, stock),
      )
      conn.commit()
      st.success(f"Produk {name} berhasil disimpan!")

elif menu == "Laporan Keuangan":
  st.header("Rekapitulasi Omzet & Keuangan")
  st.metric(label="Total Omzet Hari Ini", value="Rp 0")
  st.write("Grafik dan rekapitulasi transaksi harian akan muncul di sini.")
