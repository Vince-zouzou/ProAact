import streamlit as st
import pandas as pd
import io
class Start:
    def __init__(self,Central,Common):
        self.Common = Common
        self.Central = Central
        self.Start_pages = [st.Page(self.Welcome_page,title="Welcome",icon = '👐'), 
                    st.Page(self.Login_page,title = "Login",icon = '🎫'),
                    st.Page(self.Common.ProACT_Pro_page,title="ProACT PRO",icon = '👑'), 
                    st.Page(self.Common.Contact_us_page,title="Contact Us",icon = "📧")]
        ng = st.navigation(self.Start_pages,expanded=True)
        self.sidebar_intro()
        ng.run()
    def Login_page(self):
        gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    text-align: center;
    font-size: 5em;

}
</style>
<div class="gradient-text">ProAct - Act like a Pro</div>
"""
        st.markdown(gradient_text_html, unsafe_allow_html=True)   
        st.header("Login to your account")
        role = False
        col0,col1,col22 = st.columns([14,21,14])
        with col1:
            with st.container():
                account = st.text_input("Account:",)
                password = st.text_input("Password",type='password')
                col1,col2,col3 = st.columns([7,2,2])
                with col3:
                    login = st.button('Login')
                    if login:
                        account,role = self.Central.account_verification(account,password)
                        if account and role:
                            #print('1',st.session_state)
                            st.session_state['account'] = account
                            st.session_state['login'] = True 
                            st.session_state['role'] = role
                            st.session_state['pro'] = self.Central.check_pro(account)
                            st.rerun()
                    else:
                        st.session_state['account'] = None
                        st.session_state['login'] = False 
                        st.session_state['role'] = None
                        
                if role == False and account == True and login :st.error("Wrong Account or Password.")
                elif account == False and login:st.error("Account does not exist.")
                    
            with col2:
                if st.button('Sign up'): self.signup()
            with col1:
                if st.button('Forgot Password?'): self.forget_password()
        with col22:
            with col22.container(border=True):

                df = pd.read_excel(st.secrets['database']['sample'])
                st.write("### For you to see the pages, We provide trail ProAct PRO account for you:")
                st.write("#### -Account:  Pro")
                st.write("#### -Password:  Pro")
                st.write("#### Also, If you want to try to make your account, you can try signup, and upload this file as your signup sample file for a subaccount:")
                st.download_button(
                        label="Download data as excel",
                        data = self.create_excel(df),
                        file_name="sample_data_file.excel",)
    
    def create_excel(self,df):
        # 使用 ExcelWriter 将 DataFrame 写入 Excel 文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return output
    def Welcome_page(self):
        gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    text-align: center;
    font-size: 9em;
        line-height: 5em;
}
</style>
<div class="gradient-text">ProAct - Act like a Pro</div>
"""

        st.markdown(gradient_text_html, unsafe_allow_html=True)   
    def login(self,account,password):
        if account in self.data.keys():
            if self.Central.user_data[account]['password'] == password:
                return True,False 
            else: 
                return False,False
        else:
            return False,True
        

    @st.dialog("Join Us Now", width="large")
    def signup(self):
    # 在这里定义对话框内容
        account = st.text_input("Account:",key="owner_signup_account")
        password = st.text_input("Password:",type='password',key="owner_signup_password")
        comfirm_password = st.text_input("Confirm Password:",type='password',key="owner_signup_confirm_password")
        email = st.text_input("Email:",key="owner_signup_email",placeholder="Input whatever you want")
        verification_code = st.text_input("Verification Code:",key="owner_signup_verification_code",placeholder="Don't leave blank")
        Pro_API = st.text_input("ProAct API Key:",key="owner_signup_API",placeholder="Leave Blank if you don't have one")
        passed = True
        col0,col1 = st.columns([10,2])
        if col1.button("Join us Now!"):
            
            account_,role = self.Central.account_verification(account,'')
            if account_:
                st.error("Account already exists.")
                passed = False
            elif password != comfirm_password:
                st.error("Passwords do not match.")
                passed = False
            elif not verification_code:
                st.error("Verification code is incorrect.")
                passed = False
            elif Pro_API == "" :
                pro = False
            elif Pro_API != "":
                exist,connect = self.Central.api_verification(Pro_API,account)
                if not exist:
                    st.error("ProAct API Key does not exist.")
                    passed = False
                elif exist and not connect:
                    st.error("ProAct API Key has been used.")
                    passed = False
                else:
                    pro = Pro_API
            if passed:
                self.Central.signup({"account":account,'password':password,'email':email,'role':'Owner',"Pro":pro})
                st.rerun()  # 提交后关闭对话框并刷新页面

    @st.dialog("Forget Password", width="large")
    def forget_password(self):
    # 在这里定义对话框内容
        st.title("Find your password")
        account = st.text_input("Account:",key = "forget_password_account")
        col0,col1 = st.columns([10,2])
        with col1:
            clicked = st.button("Send Email")
        with col0:
            if clicked:
                if not self.Central.account_verification(account,'')[0]:
                    st.error("Account already don't exist.")
                else: st.success("Check your email Please.")
        verfied = st.text_input("Verification Code:",key = "forget_password_code")
        new_pass = st.text_input("New Password:",key = "forget_password_pass")
        confirm_pass = st.text_input("Confirm Password:",key = "forget_password_confirm")
        col0,col1 = st.columns([10,2])
        if col1.button("Submit",) and self.Central.account_verification(account,'')[0]:
            passed = True
            if verfied == "":
                st.error('Verification code is wrong.')
                passed = False
            elif new_pass != confirm_pass:
                st.e('Passwords do not match.')
                passed = False
            if passed:
                self.Central.change_password(account,new_pass)
            st.rerun()  # 提交后关闭对话框并刷新页面       


    def sidebar_intro(self):
        with st.sidebar:
            gra = """
<style>{
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    text-align: center;
    font-size: 5em;

}
</style>
<div class="text">ProAct - Act like a Pro</div>
"""
            st.markdown(gra, unsafe_allow_html=True)   
            st.markdown("# ProAct ")   
            st.write("## We are a system with mainly the following 2 functions:")
            st.write("### 1. Sale record management system with AI forecast on future number of sales.")
            st.write("####  - DataDash for you to management and view your organized sales.")
            st.write("####  - Forecast for you to predict the future number of sales.")
            st.write("####  - ProAct Pro: AI-driven Chatbot for you to ask any questions about your data.")
            st.write("### 2. Provide Account system with different roles for different accounts.")
            st.write("####   - Owner account can own Manager accounts as Subaccounts .")
            st.write("####  - Internal Chatbox for you to direct send message and data to your colleagues")

