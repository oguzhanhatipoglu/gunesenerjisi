import streamlit as st

st.title("Güneş Enerjisi Projesi NPV Hesaplama Aracı")

# 1. Parametre Girdileri
st.header("Parametreleri Girin:")
initial_cost = st.number_input("İlk yatırım maliyeti (USD)", min_value=0.0, value=0.0)
license_cost = st.number_input("Lisans maliyeti (USD)", min_value=0.0, value=0.0)
license_sale = st.number_input("Lisans satış bedeli – proje sonu geliri (USD)", min_value=0.0, value=0.0)
operating_years = st.number_input("İşletme süresi (yıl)", min_value=1, value=20, step=1)
discount_rate = st.number_input("Faiz Oranı (%)", min_value=0.0, value=10.0, step=0.1)
annual_production = st.number_input("Yıllık toplam üretim (kWh)", min_value=0.0, value=1500000.0, step=1000.0)
price_per_kwh = st.number_input("Elektrik birim fiyatı (USD/kWh)", min_value=0.0, value=0.10, step=0.01)

# Bakım masrafı için seçim ve girdi
maint_option = st.radio("Yıllık bakım/işletme masrafı türü:", options=["Sabit Tutar (USD)", "Gelirin Yüzdesi (%)"])
if maint_option == "Sabit Tutar (USD)":
    annual_maint_cost = st.number_input("Yıllık bakım masrafı (USD)", min_value=0.0, value=0.0)
    maint_percent = None
else:
    maint_percent = st.number_input("Bakım masrafı (% cinsinden, gelirin yüzdesi)", min_value=0.0, value=0.0, step=0.1)
    annual_maint_cost = None

# Panel yenileme için opsiyonel girdi
panel_interval = st.number_input("Panel yenileme aralığı (yıl) - opsiyonel", min_value=0, value=0, step=1)
panel_replace_cost = st.number_input("Panel yenileme maliyeti (USD) - opsiyonel", min_value=0.0, value=0.0)

# 2. Hesaplama ve 3. Sonuç Gösterimi
if st.button("Hesapla"):
    # Yıllık nakit akışlarını hesapla
    cash_flows = []  
    # Yıl 0: başlangıç giderleri (negatif)
    cash_flows.append(-(initial_cost + license_cost))
    # Yıl 1'den işletme süresi sonuna kadar:
    for year in range(1, int(operating_years) + 1):
        # Gelir ve bakım gideri hesapla
        revenue = annual_production * price_per_kwh
        if maint_option == "Sabit Tutar (USD)":
            cost = annual_maint_cost or 0.0
        else:
            cost = (maint_percent or 0.0) / 100.0 * revenue
        net_cash = revenue - cost
        # Eğer bu yıl panel yenileme periyoduna denk geliyorsa, yenileme maliyetini düş
        if panel_interval and panel_replace_cost and year % panel_interval == 0:
            net_cash -= panel_replace_cost
        # Son yılda lisans satışı geliri ekle
        if year == operating_years and license_sale:
            net_cash += license_sale
        cash_flows.append(net_cash)
    # NPV hesapla
    r = discount_rate / 100.0
    NPV = 0.0
    for t, cash in enumerate(cash_flows):
        NPV += cash / ((1 + r) ** t)
    # Sonucu göster
    st.subheader("Net Bugünkü Değer (NPV) Sonucu:")
    st.write(f"Net Bugünkü Değer (NPV): **{NPV:,.2f} USD**")
    sp_annual_return = 0.11
    sp_future_value = 1800000 * (1 + sp_annual_return) ** operating_years
    st.write("Eğer projeyi satıp elde edilen para S&P 500'e yatırılsaydı, 45 yıl sonra elde edilecek değer:")
    st.write(f"**{sp_future_value:,.2f} USD**")
