### RUN USING streamlit run streamlit_incometax_calculator.py it will start on localhost:8501 ###
## for 0 prediction weekday, temp- 20, 25, 27, 490, 0.003
## Author- Hunaidkhan Pathan
# Updated date - 08-07-2025
##streamlit run streamlit_incometax_calculator.py

import streamlit as st
import math

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

@st.cache_data
def tax_old(income):
    tax = 0
    if income > 250_000:
        tax += (min(income, 500_000) - 250_000) * 0.05
    if income > 500_000:
        tax += (min(income, 1_000_000) - 500_000) * 0.20
    if income > 1_000_000:
        tax += (income - 1_000_000) * 0.30

    # Apply 87A rebate for old regime
    rebate = min(tax, 12_500) if income <= 500_000 else 0  # ₹12,500 rebate up to ₹5 L :contentReference[oaicite:1]{index=1}
    tax = max(0, tax - rebate)

    tax += calc_surcharge(income, tax)
    tax *= 1.04
    return tax

@st.cache_data
def tax_new(income):
    taxable = max(0, income - 75_000)
    slabs = [(400_000, 0), (800_000, 0.05), (1_200_000, 0.10),
             (1_600_000, 0.15), (2_000_000, 0.20), (2_400_000, 0.25),
             (float('inf'), 0.30)]
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
    # Sidebar with images
    st.sidebar.text("Built with Streamlit")
    ##Use Markdown with custom CSS to style the text
    st.sidebar.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap" rel="stylesheet">

        <style>
        .fancy-title {
            font-size: 24px !important;
            color: white;
            font-family: 'Montserrat', sans-serif;
            font-weight: bold;
            text-shadow: 1px 1px 2px #000000;
        }
        </style>

        <div class="fancy-title">
            Hunaidkhan Pathan
        </div>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
       st.markdown("[Hunaidkhan's Linkedin profile](https://www.linkedin.com/in/hunaidkhan/)")
    #st.page_link("https://www.linkedin.com/in/hunaidkhan/", label="Hunaidkhan Linkedin profile")
    st.sidebar.image("HK _Tricks.jpg", use_container_width=True)
    st.sidebar.text("") 
    
    st.sidebar.image("dsp3.jpeg", width=200)
    st.sidebar.text("")
    # Use Markdown with custom CSS to style the text
    # Use Markdown with custom CSS to style the text

#


    st.title("🇮🇳 India Income Tax Calculator (FY 2025‑26)")
    basic = st.number_input("Yearly Basic Salary", min_value=0,value=1500000)
    da = st.number_input("Yearly DA", min_value=0)
    hra = st.number_input("Yearly HRA", min_value=0)
    lta = st.number_input("Yearly LTA", min_value=0)
    special = st.number_input("Yearly Special Allowance", min_value=0)
    pf = st.number_input("PF deduction (Old Regime)", min_value=0, max_value=150_000, value=80000)
    sodexo = st.number_input("Sodexo deduction", min_value=0, max_value=36_000, value=2000)
    ded_80c = st.number_input("80C deduction beyond PF", min_value=0, max_value=150000-pf, value=0)
    pt = st.number_input("Professional Tax", min_value=0, max_value=3000, value=200)
    ded_80d = st.number_input("80D Medical", min_value=0, max_value=75000, value=0)
    ded_nps = st.number_input("80CCD (NPS)", min_value=0, max_value=150000, value=0)
    ded_80g = st.number_input("80G Donation", min_value=0, value=0)
    ded_home = st.number_input("Home-loan interest", min_value=0, max_value=350000, value=0)
    location = st.selectbox("Metro or Non‑Metro (Old Regime HRA)", ["Metro", "Non‑Metro"])

    if st.button("Analyze Taxes ▶"):
        # Old Regime taxable income
        da_hra = basic + da
        actual_hra = min(hra,
                         da_hra * (0.5 if location == "Metro" else 0.4),
                         hra - 0.1 * da_hra)
        hra_exempt = max(0, math.ceil(actual_hra))
        taxable_old = basic + da + hra + lta + special - (
            pf + sodexo + ded_80c + pt + ded_80d + ded_nps +
            ded_80g + ded_home + 50_000 + hra_exempt
        )
        taxable_old = max(0, taxable_old)

        # New Regime taxable income
        taxable_new = max(0, basic + da + hra + lta + special - 75_000)

        old_tax = math.ceil(tax_old(taxable_old))
        new_tax = math.ceil(tax_new(taxable_new))
        diff = abs(new_tax - old_tax)
        better = "Old Regime" if old_tax < new_tax else "New Regime"

        st.markdown("### 📊 Tax Comparison")
        df = {
            "": ["Taxable Income", "Total Tax (Yearly)", "Monthly Tax"],
            "Old Regime": [f"₹{taxable_old:,}", f"₹{old_tax:,}", f"₹{math.ceil(old_tax/12):,}"],
            "New Regime": [f"₹{taxable_new:,}", f"₹{new_tax:,}", f"₹{math.ceil(new_tax/12):,}"]
        }
        st.table(df)
        st.markdown(f"**💡 Better Regime:** {better}  \n**Tax Saved:** ₹{diff:,}")

if __name__ == "__main__":
    run()
