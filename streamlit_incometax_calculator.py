### RUN USING streamlit run streamlit_incometax_calculator.py it will start on localhost:8501 ###
## for 0 prediction weekday, temp- 20, 25, 27, 490, 0.003
## Author- Hunaidkhan Pathan
# Updated date - 08-07-2025
##streamlit run streamlit_incometax_calculator.py
import streamlit as st
import math

# Surcharge Calculation
def calc_surcharge(income, tax):
    rate = 0
    if income > 50000000:
        rate = 0.37
    elif income > 20000000:
        rate = 0.25
    elif income > 10000000:
        rate = 0.15
    elif income > 5000000:
        rate = 0.10
    return tax * rate, rate

# Old Regime
def compute_old_regime(taxable_income):
    steps = []
    tax = 0
    if taxable_income > 250000:
        slab_amt = min(taxable_income, 500000) - 250000
        slab_tax = slab_amt * 0.05
        tax += slab_tax
        steps.append(f"5% on ₹{slab_amt:,} = ₹{slab_tax:,.0f}")
    if taxable_income > 500000:
        slab_amt = min(taxable_income, 1000000) - 500000
        slab_tax = slab_amt * 0.20
        tax += slab_tax
        steps.append(f"20% on ₹{slab_amt:,} = ₹{slab_tax:,.0f}")
    if taxable_income > 1000000:
        slab_amt = taxable_income - 1000000
        slab_tax = slab_amt * 0.30
        tax += slab_tax
        steps.append(f"30% on ₹{slab_amt:,} = ₹{slab_tax:,.0f}")

    rebate = min(12500, tax) if taxable_income <= 500000 else 0
    if rebate:
        tax -= rebate
        steps.append(f"87A rebate = ₹{rebate:,.0f}")

    surcharge, rate = calc_surcharge(taxable_income, tax)
    tax += surcharge
    steps.append(f"Surcharge @ {rate*100}% = ₹{surcharge:,.0f}")

    cess = tax * 0.04
    total_tax = tax + cess
    steps.append(f"Cess 4% on ₹{tax:,.0f} = ₹{cess:,.0f}")
    steps.append(f"Total (Old Regime) = ₹{total_tax:,.0f}")

    return round(total_tax), steps

# New Regime
def compute_new_regime(gross_income):
    steps = []
    std_deduction = 75000
    taxable = max(0, gross_income - std_deduction)

    steps.append(f"Gross Income = ₹{gross_income:,}")
    steps.append(f"Standard Deduction = ₹{std_deduction:,}")
    steps.append(f"Taxable Income = ₹{taxable:,}")

    slabs = [
        (300000, 0.00),
        (600000, 0.05),
        (900000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (float('inf'), 0.30)
    ]

    tax = 0
    prev_limit = 0
    for limit, rate in slabs:
        if taxable > prev_limit:
            slab_amount = min(limit - prev_limit, taxable - prev_limit)
            slab_tax = slab_amount * rate
            tax += slab_tax
            steps.append(f"{int(rate*100)}% on ₹{slab_amount:,} = ₹{slab_tax:,.0f}")
            prev_limit = limit
        else:
            break

    # 87A rebate
    rebate = 0
    if taxable <= 700000:
        rebate = min(tax, 25000)
        tax -= rebate
        steps.append(f"87A rebate = ₹{rebate:,.0f}")

    surcharge, rate = calc_surcharge(gross_income, tax)
    tax += surcharge
    steps.append(f"Surcharge @ {rate*100}% = ₹{surcharge:,.0f}")

    cess = tax * 0.04
    total_tax = tax + cess
    steps.append(f"Cess 4% on ₹{tax:,.0f} = ₹{cess:,.0f}")
    steps.append(f"Total (New Regime) = ₹{total_tax:,.0f}")

    return round(total_tax), taxable, steps


# Streamlit App
def run():
    st.title("🇮🇳 India Income Tax Calculator (FY 2025‑26)")

    income = st.number_input("Enter Gross Salary (₹)", value=1280000)

    old_tax, old_steps = compute_old_regime(income)
    new_tax, new_taxable, new_steps = compute_new_regime(income)

    st.header("🧾 Old Regime Breakdown")
    for s in old_steps:
        st.text(s)

    st.header("🧾 New Regime Breakdown")
    for s in new_steps:
        st.text(s)

    # ✅ Comparison Table
    old_monthly = old_tax // 12
    new_monthly = new_tax // 12
    better = "Old Regime" if old_tax < new_tax else "New Regime"
    diff = abs(old_tax - new_tax)

    st.markdown("### 📊 Tax Comparison")
    st.table({
        "": ["Taxable Income", "Total Tax", "Monthly Tax"],
        "Old Regime": [f"₹{income:,}", f"₹{old_tax:,}", f"₹{old_monthly:,}"],
        "New Regime": [f"₹{new_taxable:,}", f"₹{new_tax:,}", f"₹{new_monthly:,}"]
    })

    st.success(f"✅ Better Regime: **{better}**\n💰 Tax Saved: ₹{diff:,}")

if __name__ == "__main__":
    run()
