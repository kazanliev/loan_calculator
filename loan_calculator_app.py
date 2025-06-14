import streamlit as st
import pandas as pd

st.title("📊 Loan Calculator")

# User Inputs
currency = st.text_input("Валутата (напр. BGN, EUR)", "BGN")
P0 = st.number_input("Първоначална главница", min_value=0.0, step=100.0, format="%.2f")
R = st.number_input("Годишна лихва (%)", min_value=0.0, format="%.2f") / 100
N = st.number_input("Срок (в години)", min_value=1, step=1)

if P0 and R and N:
    # Calculations
    n = int(N * 12)
    r = R / 12
    M = P0 * (r * (1 + r)**n) / ((1 + r)**n - 1)
    total_sum  = n*M

    st.markdown("---")
    st.subheader("💰 Обобщение")
    st.write(f"**Първоначална главница:** {P0:,.2f} {currency}")
    st.write(f"**Лихва:** {R * 100:.2f} %")
    st.write(f"**Срок:** {n} месеца")
    st.write(f"**Месечна вноска:** {M:.2f} {currency}")
    st.write(f"**Обща сума за плащане:** {total_sum:.2f} {currency}")
    st.markdown("---")

    # Table generation
    data = []
    total_interest = 0
    balance = P0

    for i in range(1, n + 1):
        interest = round(balance * r, 2)
        principal = round(M - interest, 2)
        end_balance = round(balance - principal, 2)
        total_interest += interest

        data.append({
            "Месец": i,
            "Стартова Главница": balance,
            "Платена лихва": interest,
            "Вноска": M,
            "Крайна Главница": end_balance,
            "Натрупана Лихва": total_interest
        })

        balance = end_balance

    df = pd.DataFrame(data)
    st.subheader("📅 План за погасяване")
    st.dataframe(df.style.format({col: "{:.2f}" for col in df.columns if df[col].dtype != 'int'}), use_container_width=True)

    # File export
    st.markdown("---")
    if st.button("💾 Запиши в Excel файл"):
        excel_path = "loan_schedule.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        st.success(f"Файлът е запазен като `{excel_path}`")

