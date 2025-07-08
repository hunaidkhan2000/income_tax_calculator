### RUN USING streamlit run streamlit_incometax_calculator.py it will start on localhost:8501 ###
## for 0 prediction weekday, tem- 20 ,25,27,490,0.003
## Author- Hunaidkhan Pathan 
# Updated date - 10-04-2023  
##streamlit run streamlit_incometax_calculator.py

import streamlit as st
import SessionState
import pandas as pd
import math



new_regime_tax = []
old_regime_tax = []
session_state = SessionState.get(old_regime_tax=0, new_regime_tax=0,basic_salary = 0,hra = 0,lta = 0,special_allowance=0,counter = 0,unique_count = 0,da = 0)

def run():

    from PIL import Image
    image = Image.open('dsp3.jpeg')
    image = image.resize((300,100))
    #new_img.save("car_resized.jpg", "JPEG", optimize=True)
    image_hk = Image.open('HK _Tricks.jpg')
    image_hk = image_hk.resize((300,200))

    #st.image(image,use_column_width=True)
    st.sidebar.image(image)
    add_selectbox = st.sidebar.selectbox(
    "Which income tax Regime do you want to calculate tax for ?",
    ("Old regime", "New Regime","Regime Difference","About"))

    st.sidebar.info('Using this app, Indians can calculate their income tax')
    #st.sidebar.success('https://www.pycaret.org')
    
    st.sidebar.image(image_hk)
    #st.sidebar.image(image_meeting_room)
    final_tax = 0
    final_tax_new = 0

    st.title("India Income Tax calculator")
    
    @st.cache()
    def tax_calc(income):
        if income <= 500000:
            tax = 0
        elif income <= 1000000: 
            tax = (income - 500000) * 0.2 + 12500              # 10% on income above 10K
        elif income <= 5000000:
            tax = (income-1000000) * 0.3 + 112500  # 20% on income above 20K, plus tax on 10K of income below 20K
        elif income <= 10000000: 
            tax = ((income-1000000) * 0.3 + 112500 ) * 1.10            # 10% Surcharge on income above 50 lakhs
        elif income <= 20000000:                # 15% Surcharge on income above 1cr upto 2 cr 
            tax = ((income-1000000) * 0.3 + 112500 ) * 1.15 
        elif income <= 50000000:   # 25% Surcharge on income above 2cr upto 5cr 
            tax = ((income-1000000) * 0.3 + 112500 ) * 1.25     
        else:
            tax = ((income-1000000) * 0.3 + 112500 ) * 1.37    # 37% Surcharge on income above 5cr 
      
        return tax
    @st.cache()
    def tax_calc_new_regime(income):
        
        if income <= 300000:
            tax = 0
        elif income <= 600000:  
            tax = (income - 300000)*0.05           # 5% tax above 3LPA upto 6 LPA
        elif income <= 900000: 
            tax = (income - 600000)*0.1 + 15000     # 10% on income above 6 LPA upto 9 LPA
        elif income <= 1200000: 
            tax = (income - 900000)*0.15 + 45000   # 15% on income from 9 LPA upto 12 LPA
        elif income <= 1500000: 
            tax = (income - 1200000)*0.2 + 90000   # 20% on income from 12 LPA upto 15 LPA
        else: 
            tax = (income - 1500000)*0.3 + 150000  # 30% on income above 15 LPA
        
        if income <= 700000:
            tax = 0
        
        # Add surcharge based on income range
        if income <= 5000000:
            surcharge_rate = 0
        elif income <= 10000000:
            surcharge_rate = 0.1 # 10% Surcharge on income above 50 lakhs
        elif income <= 20000000:
            surcharge_rate = 0.15  # 15% Surcharge on income above 1cr upto 2 cr 
        else:
            surcharge_rate = 0.25 # 25% Surcharge on income above 2cr
        
        surcharge = tax * surcharge_rate
        total_tax = tax + surcharge
        
        return total_tax

    
    if add_selectbox == 'Old regime':
        location = st.selectbox('Enter your location Metro or non metro',("Metro","Non-Metro"))
        basic_salary = st.number_input('Enter your yearly Basic salary', min_value=0, value=550000)
        da =  st.number_input('Enter your yearly Dearness allowance', min_value=0, value=0)
        hra = st.number_input('Enter your yearly HRA', min_value=0,max_value = int(0.5*basic_salary), value=50000)
        hra_actual = st.number_input('Enter your yearly Actual HRA paid(yearly house rent paid)', min_value=0,max_value = int(0.5*basic_salary), value=0)
        lta = st.number_input('Enter your yearly Leave Travel allowance', min_value=0, value=80000)
        special_allowance = st.number_input('Enter your yearly Special Allowance', min_value=0, value=150000)
        pf_deduction = st.number_input('Enter your yearly PF deduction', min_value=0,max_value=150000, value=80000)
        sodexo_deduction = st.number_input('Enter your yearly Sodexo meal coupon deduction', min_value=0,max_value=36000, value=2000)
        deduction_80c= st.number_input('Enter your yearly 80C deduction', min_value=0,max_value=150000-pf_deduction,value = 0)
        pt_deduction = st.number_input('Enter your yearly Professional tax deduction', min_value=0,max_value=3000, value=200)
        deduction_80d = st.number_input('Enter your yearly family Medicalaim(80D) deduction', min_value=0,max_value=75000,value = 0)
        deduction_NPS= st.number_input('Enter your yearly NPS(80CCD) deduction', min_value=0,max_value=150000,value = 0)
        deduction_80G= st.number_input('Enter your yearly Government recognised donations deduction', min_value=0,value = 0)
        deduction_interest_on_loan= st.number_input('Enter your yearly interest on home loan(Sec 24(B) deduction', min_value=0,max_value=350000,value = 0)
        standard_deduction = 50000
        if location == "Metro":
            hra_final = max(0,math.ceil(min(0.5 * (basic_salary+da), hra ,(hra_actual - 0.1*(basic_salary+da)))))
        else:
            hra_final = max(0,math.ceil(min(0.4*( basic_salary+da), hra , (hra_actual - 0.1*(basic_salary+da)))))
        #print("total actual HRA is ",hra_final, "from total of " ,hra)
        
        taxable_income = basic_salary + hra +da + lta + special_allowance -pf_deduction - sodexo_deduction - pt_deduction-deduction_80d -  deduction_NPS - deduction_80G - deduction_interest_on_loan - standard_deduction- hra_final - deduction_80c
        
        session_state.basic_salary = basic_salary
        session_state.hra = hra
        session_state.lta = lta
        session_state.special_allowance = special_allowance
        session_state.da = da
        session_state.counter += 1
        session_state.unique_count += 1

        
        
        
        if st.button("Calculate"):
            final_tax = math.ceil(tax_calc(taxable_income) * 1.04)
            
            old_regime_tax.append(final_tax)
            session_state.old_regime_tax = final_tax
            print("old Regime total tax ",final_tax)
            
                   
       
        
        st.success(f'Your Total tax for the financial year(Old regime) is Rs.{final_tax}')
        st.success(f'Your Total Monthly tax is (Old regime) is Rs.{math.ceil(final_tax/12)}')
    
    
    if add_selectbox == 'New Regime':
        basic_salary1 = st.number_input('Enter your yearly Basic salary', min_value=0, value=session_state.basic_salary)
        da1 = st.number_input('Enter your yearly Dearness Allowance', min_value=0, value=session_state.da)
        hra1 = st.number_input('Enter your yearly HRA', min_value=0,max_value = int(0.5*basic_salary1), value=session_state.hra)
        lta1 = st.number_input('Enter your yearly Leave travel allowance', min_value=0, value=session_state.lta)
        special_allowance1 = st.number_input('Enter your yearly Special Allowance', min_value=0, value=session_state.special_allowance)
        standard_deduction1 = 50000
        
        taxable_income_new = basic_salary1 + hra1 +da1 + lta1 + special_allowance1 - standard_deduction1
        ## for website counts ###
        session_state.counter += 1
        session_state.unique_count += 1
        print("unique website views are",session_state.unique_count)
        
        
        
        
        if st.button("Calculate"):
            final_tax_new = math.ceil(tax_calc_new_regime(taxable_income_new)*1.04)
            print("new regime final tax is",final_tax_new)
            session_state.new_regime_tax = final_tax_new
            
            ##website count ##
            session_state.counter += 1
            
            #new_regime_tax.append(final_tax_new)
            
                   
       
        
        st.success(f'Yout Total tax for the financial year(New regime) is Rs.{final_tax_new}')
        st.success(f'Your Total Monthly tax is (New regime) is Rs.{math.ceil(final_tax_new/12)}')
    
    


    
    if add_selectbox == 'Regime Difference':
        
        if session_state.old_regime_tax  < session_state.new_regime_tax:
            #print(session_state.old_regime_tax,"SESSION difference is ", session_state.new_regime_tax)
            st.success(f'Old regime is more beneficial for you, the yearly difference in tax is Rs. {int(session_state.new_regime_tax - session_state.old_regime_tax)}')
        else: 
            st.success(f'New regime is more beneficial for you, the yearly difference in tax is Rs.{int( session_state.old_regime_tax - session_state.new_regime_tax)}')
        
        session_state.counter += 1    
      
        
        
    if add_selectbox == 'About':
                
                    st.subheader("Built with Streamlit")
                    st.subheader("Hunaidkhan Pathan")
                    st.subheader("https://www.linkedin.com/in/hunaidkhan/")
                    clck = st.button("Appreciate the author")
                    if clck:
                        st.balloons()
                    st.write("Last updated date 10th April 2023")
    
    
    st.button("Re-run")
    print("website tab count is ",session_state.counter )
if __name__ == '__main__':
    run()
