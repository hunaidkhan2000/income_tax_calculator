### RUN USING streamlit run streamlit_incometax_calculator.py it will start on localhost:8501 ###
## for 0 prediction weekday, tem- 20 ,25,27,490,0.003
## Author- Hunaidkhan Pathan 
# Updated date - 08-07-2025
##streamlit run streamlit_incometax_calculator.py


import streamlit as st
import SessionState
import pandas as pd
import math

session_state = SessionState.get(old_regime_tax=0, new_regime_tax=0,
                                 basic_salary=0, da=0, hra=0, lta=0, special_allowance=0,
                                 counter=0, unique_count=0)

def calc_surcharge(income, tax):
    rate = 0
    if income > 5e6:
        rate = 0.37
    elif income > 2e6:
        rate = 0.25
    elif income > 1e6:
        rate = 0.15
    elif income > 0.5e6:
        rate = 0.10
    return tax * rate

@st.cache()
def tax_old(income):
    tax = 0
    if income > 250000:
        tax += min(income, 500000) - 250000 * 0.05
    if income > 500000:
        tax += (min(income, 1000000) - 500000) * 0.20
    if income > 1000000:
        tax += (income - 1000000) * 0.30
    tax += calc_surcharge(income, tax)
    tax *= 1.04
    return tax

@st.cache()
def tax_new(income):
    taxable = max(0, income - 75000)
    slabs = [(400000,0), (800000,0.05), (1200000,0.10),
             (1600000,0.15), (2000000,0.20), (2400000,0.25),
             (float('inf'),0.30)]
    tax = 0; prev = 0
    for limit, rate in slabs:
        if taxable > prev:
            tax += (min(taxable, limit) - prev) * rate
            prev = limit
        else:
            break
    tax += calc_surcharge(income, tax)
    tax *= 1.04
    return tax

def run():
    st.title("🇮🇳 India Income Tax Calculator (FY 2025‑26)")
    menu = st.sidebar.selectbox("Choose regime:", ["Old Regime", "New Regime", "Compare Regimes", "About"])
    final_old = final_new = 0

    if menu in ["Old Regime", "New Regime"]:
        st.subheader(menu)
        basic = st.number_input("Yearly basic salary", value=session_state.basic_salary, min_value=0)
        da = st.number_input("Yearly DA", value=session_state.da, min_value=0)
        hra = st.number_input("Yearly HRA", value=session_state.hra, min_value=0)
        lta = st.number_input("Yearly LTA", value=session_state.lta, min_value=0)
        special = st.number_input("Yearly Special allowance", value=session_state.special_allowance, min_value=0)

        session_state.basic_salary, session_state.da = basic, da
        session_state.hra, session_state.lta = hra, lta
        session_state.special_allowance = special

        if menu == "Old Regime":
            pf = st.number_input("PF deduction", min_value=0, max_value=150000, value=80000)
            sodexo = st.number_input("Sodexo deduction", min_value=0, max_value=36000, value=2000)
            deduction_80c = st.number_input("80C deduction (joining PF)", min_value=0, max_value=150000-pf, value=0)
            pt = st.number_input("Professional tax", min_value=0, max_value=3000, value=200)
            ded_80d = st.number_input("80D medical", min_value=0, max_value=75000, value=0)
            ded_nps = st.number_input("80CCD NPS", min_value=0, max_value=150000, value=0)
            ded_80g = st.number_input("80G donation", min_value=0, value=0)
            ded_home = st.number_input("Home loan interest (Sec 24)", min_value=0, max_value=350000, value=0)
            location = st.selectbox("Metro or Non-Metro", ["Metro","Non-Metro"])
            std_ded = 50000
            da_hra = basic + da
            actual_hra = min(hra, da_hra * (0.5 if location=="Metro" else 0.4),
                             hra - 0.1 * da_hra)
            hra_exempt = max(0, math.ceil(actual_hra))
            taxable = basic + da + hra + lta + special - (pf + sodexo + pt + ded_80c +
                        ded_80d + ded_nps + ded_80g + ded_home + std_ded + hra_exempt)

            if st.button("Calculate Old Regime Tax"):
                final_old = math.ceil(tax_old(taxable))
                session_state.old_regime_tax = final_old

            if final_old:
                st.success(f"Total yearly tax (Old): ₹{final_old}")
                st.info(f"Monthly = ₹{math.ceil(final_old/12)}")

        else:  # New Regime
            std_ded = 75000
            taxable = basic + da + hra + lta + special - std_ded

            if st.button("Calculate New Regime Tax"):
                final_new = math.ceil(tax_new(taxable))
                session_state.new_regime_tax = final_new

            if final_new:
                st.success(f"Total yearly tax (New): ₹{final_new}")
                st.info(f"Monthly = ₹{math.ceil(final_new/12)}")

    elif menu == "Compare Regimes":
        old, new = session_state.old_regime_tax, session_state.new_regime_tax
        if old==0 and new==0:
            st.warning("Please calculate both regimes first!")
        else:
            diff = new - old
            better = "Old" if old < new else "New"
            st.success(f"{better} Regime is better by ₹{abs(diff)}")

    else:  # About
        st.write("Built with Streamlit by Hunaidkhan Pathan")
        st.write("Last updated: FY 2025–26 (Assessment Year 2026–27) tax rules")

    st.sidebar.write(f"Visits: {session_state.unique_count}")
    st.sidebar.button("Clear & Refresh")

if __name__ == "__main__":
    run()


