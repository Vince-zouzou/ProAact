import streamlit as st
import time as t
from UIs.Start import Start
from UIs.Manager import Manager
from UIs.Owner import Owner
from UIs.Common import Common
from dfdatabase_interaction import Central
from Model import Model
class UI:
    def __init__(self):

        uri = st.secrets['database']['uri'] # Neo4j 默认本地地址
        user = st.secrets['database']['user']            # 默认用户名
        password = st.secrets['database']['password']    # 替换为你设置的密码

        
        self.Central = Central()
        self.Common = Common(self.Central)
        self.Model = Model()
        st.set_page_config(layout='wide',initial_sidebar_state='expanded')
        if 'login' not in st.session_state:
            st.session_state = {
                "login":False,
                "account":None,
                "role":None,
                "pro":False,
                "verified":False,
                'subaccount_target':None,
                "dialog":True,
                "trained":False,
                'clicked':False,
                "talkto":False,
                'previous_talkto':False,
                "Common":self.Common,
                "Central":self.Central,
                "Model":self.Model,
                "User Data":None
                }
        print("UI init")
        if st.session_state['login'] == True:
            if st.session_state['role'] == 'Owner':
                Owner(self.Central,self.Common)
            if st.session_state['role'] == 'Manager':
                Manager(self.Central,self.Common)
        else:
            Start(self.Central,self.Common)
    def render(self):
        pass



if __name__ == "__main__":

    UI().render()
