# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()

Order_name = st.text_input("Name on Smoothie")
st.write("Name on Smoothie will be", Order_name)


my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data = my_dataframe, use_container_width=True)
pd_df = my_dataframe.to_pandas()
ingredients_list = st.multiselect('Choose up to 5 ingrients: ', 
                                  my_dataframe, 
                                  max_selections=5)



if ingredients_list:
    ingredients_string =  ' '

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(each_fruit + ' Nutrition Inforamtion')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
