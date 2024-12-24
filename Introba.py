import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Home")

st.title("Germany Apartment Rental Market Analysis")
sidebar = st.sidebar
df= {
"newlyConst": sidebar.slider("New Property?",0,1,value=1),  # 是否是新建物业，1表示是，0表示不是
"balcony": sidebar.slider("Have Balcony?",0,1,value=1),  # 是否有阳台，1表示有，0表示没有
"hasKitchen": sidebar.slider("Have Kitchen?",0,1,value=1),  # 是否有厨房，1表示有，0表示没有 
"lift": sidebar.slider("Have Lift?",0,1,value=1),# 是否有电梯，1表示有，0表示没有
"livingSpaceRange": sidebar.slider("Living Space Range",1,7,value=1),  # 物业面积范围（平方米）
"UploadSpeed_10": sidebar.slider("Internet Speed Greater than 10?",0,1,value=1),  # 是否提供10Mbps上传速度，1表示有，0表示没有
"UploadSpeed_40": sidebar.slider("Internet Speed Greater than 40?",0,1,value=1),  # 是否提供40Mbps上传速度，1表示有，0表示没有
"houseAge": sidebar.slider("House Age",1,100),  # 物业年龄（年）
"sinceRefurbish": sidebar.slider("Year after refurbish",1,100),  # 上次翻修距离的年数
"condition_refurbished": sidebar.slider("Refurbished before?",0,1,value=1),  # 是否已翻修，1表示是，0表示不是
"interiorQual_normal": sidebar.slider("Interior quality",0,1,value=1)  # 室内质量，0表示普通，1表示豪华
}
    
xs = pd.DataFrame([i for i in range(1,300)],columns=["Living space"])
    #print(xs)

xs['Rent'] = [np.exp(2.4433 + 0.1049 * df['newlyConst'] + 0.0901 * df['balcony'] + 
                        0.1925 * df['hasKitchen'] + 
                        0.9193 * np.log(x) + 
                        0.1706 * df['lift'] + 
                        0.0159 * df['livingSpaceRange'] + 
                        0.1105 * df['UploadSpeed_10'] + 
                        0.0952 * df['UploadSpeed_40'] - 
                        0.0556 * np.log(df['houseAge']) - 
                        0.0345 * np.log(df['sinceRefurbish']) - 
                        0.0583 * df['condition_refurbished'] - 
                        0.2097 * df['interiorQual_normal']) for x in xs['Living space']]
xs = xs.set_index('Living space')



col0,col1 = st.columns((5,5))
ls = col0.slider("Living Space",1,300,value=100)
rt = np.exp(2.4433 + 0.1049 * df['newlyConst'] + 0.0901 * df['balcony'] + 
                        0.1925 * df['hasKitchen'] + 
                        0.9193 * np.log(ls) + 
                        0.1706 * df['lift'] + 
                        0.0159 * df['livingSpaceRange'] + 
                        0.1105 * df['UploadSpeed_10'] + 
                        0.0952 * df['UploadSpeed_40'] - 
                        0.0556 * np.log(df['houseAge']) - 
                        0.0345 * np.log(df['sinceRefurbish']) - 
                        0.0583 * df['condition_refurbished'] - 
                        0.2097 * df['interiorQual_normal'])
col1.write("## Predicted rent is :      {}".format(round(rt)))

st.line_chart(xs,width=150,height = 400)