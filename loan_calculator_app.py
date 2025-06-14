import streamlit as st
import pandas as pd

st.title("📊 Кредитен калкулатор")

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
    st.write(f"**Годишна лихва:** {R * 100:.2f} %")
    st.write(f"**Месечна лихва:** {r * 100:.2f} %")
    st.write(f"**Срок:** {n} месеца")
    st.write(f"**Месечна вноска:** {M:.2f} {currency}")
    st.write(f"**Обща сума за плащане (без такси):** {total_sum:.2f} {currency}")
    st.write(f"**Обща стойност на платените лихви:** {total_sum - P0:.2f} {currency}")
    st.markdown("---")

    # Table generation
    data = []
    total_interest = 0
    balance = P0

    for i in range(1, n + 1):
        interest = balance * r
        principal = M - interest

        end_balance = balance - principal

        total_interest += interest

        # Store/display values rounded to 2 digits
        data.append({
            "Месец": i,
            "Стартова Главница": round(balance, 2),
            "Платена лихва": round(interest, 2),
            "Вноска": round(M, 2),
            "Крайна Главница": round(end_balance, 2),
            "Натрупана Лихва": round(total_interest, 2)
        })

        balance = end_balance

    df = pd.DataFrame(data)
    st.subheader("📅 План за погасяване")
    st.dataframe(df.style.format({col: "{:.2f}" for col in df.columns if df[col].dtype != 'int'}), use_container_width=True)





