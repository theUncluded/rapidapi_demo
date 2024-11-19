import streamlit as st
from operations.functions import get_data , get_wt_score , get_stats, get_specifics

st.header("Streamlit UX For Config of Rent Estimates By Area")

st.write("Select variables, then press the GO button when ready")

params = ["county" , "timeZone" , "state" , "city" , "propertyTaxRate" , "zpid" , "rentZestimate"]

#address = centerpoint address of search
#diameter = diameter (in miles) of rental properties (Min=0.05 , Max=0.5)
#p_type = property type (Options: SingleFamily , Condo , MultiFamily , Townhouse , Apartment)
#toggle = bool var to handle if includeComps is passed (no doc on comps im assuming it's if gas or water is included)
address = st.text_input("Address - The Center Point of Your Search")
diameter = st.slider("Diameter of Search In Miles - Min 0.05 , Max 0.5",0.05,0.5)
p_type = st.radio("Choose The Property Type:",["SingleFamily","Condo","MultiFamily","Townhouse","Apartment"])
u_choice = st.radio("Choose Specific Parameters You Wish To View:" , params)

if st.button("GO"):  
    data = get_data(address)
    
    st.dataframe(data)
    st.write(get_specifics(data , u_choice))

    stats = get_stats(address,diameter,p_type)
    n_amount = stats["TotalCompared"]
    median_rent = stats["MedianRent"]
    high_rent = stats["HighestRent"]
    low_rent = stats["LowestRent"]

    st.write(f"{address} was compared with {n_amount} properties.")
    st.write(f"The median rent for {p_type}s within {diameter} miles of {address} is ${median_rent}")
    st.write(f"From the compared properties, the highest rent of the area is ${high_rent}, whilst the lowest is ${low_rent}")