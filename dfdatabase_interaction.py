import os
from Model import Model 
import pandas as pd
import joblib
import streamlit as st

class Central:
    def __init__(self): 
        self.folder = "CSV_DataBase"
        self.record = "Record"
        self.files = {"API":"API.csv","Manager":"Manager.csv","Owner":"Owner.csv","Store":"Store.csv","Sales":"Record.csv"}
        self.Model = Model()
    def exist(self,file):
        return os.path.exists(file)
    def signup(self, info):

        tar = os.path.join(self.folder,self.files["Owner"])

        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            df.loc[len(df)] = info
        else:
            df = pd.DataFrame([info])
        df.to_csv(tar,index=False)

    def signup_manager(self, owner,info):
        tar = os.path.join(self.folder,self.files["Manager"])
        info["owner"] = owner
        if info['data'] and info['data_type']:
            if info['data_type'] == 'File':
                data_for_enhanced = pd.read_excel(info['data'])
                print('{}'.format(info['account'])+'.csv')
                data_add = os.path.join(self.folder,self.record,'{}'.format(info['account'])+'.csv')
                print(data_add)
                data_stored = data_for_enhanced.to_csv(data_add,index=False)
                info['data_add'] = data_add
                cmodel = joblib.load(st.secrets['model']['model_path'])
                print("Data get already")
                model,path = self.Model.train_model_enhanced(data_for_enhanced,cmodel,info['account'])
                print("Model Trained Already")
                info['model'] = path
        
        if self.exist(tar):
                df = pd.read_csv(tar,dtype=str)
                df.loc[len(df)] = info
                print("")
        else:
                df = pd.DataFrame([info])
        
        df.to_csv(tar,index=False)
        return True



    def remove_subaccount(self,account,selected):

        owner = account
        manager = selected
        tar = os.path.join(self.folder,self.files["Manager"])
        print(tar)
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            if not df[(df["account"]==manager) & (df["owner"]==owner)].empty:
                df.loc[(df["account"] == manager) & (df["owner"] == owner), 'owner'] = None
                df.to_csv(tar,index=False)
        return False
    
    def add_subaccount(self,account,selected):
        owner = account
        manager = selected
        tar = os.path.join(self.folder,self.files["Manager"])
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            if not df[df["account"]==manager].empty:
                df.loc[df["account"]==manager,'owner'] = owner
                df.to_csv(tar,index=False)


    def change_password(self,account,password):
        tar = os.path.join(self.folder,self.files["Owner"])
        tar_m = os.path.join(self.folder,self.files["Manager"])
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            if not df[df["account"]==account].empty:
                df.loc[df["account"]==account,'password'] = password
                df.to_csv(tar,index=False)
        elif self.exist(tar_m):
            df = pd.read_csv(tar_m,dtype=str)
            if not df[df["account"]==account].empty:
                df.loc[df["account"]==account,'password'] = password
                df.to_csv(tar_m,index=False)

    def api_verification(self, api, account):
        tar = os.path.join(self.folder, self.files["API"])
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            print(df[df["key"] == api].empty)
            if not df[df["key"] == api].empty:
                if (df[df['key'] == api]['connection'] >= 1).any():
                    return True, False
                else:
                    return True,True
            else:
                return False,False
        else: pd.DataFrame([{"key":"MSBA",'connection':0}]).to_csv(tar,index=False)
        
    def account_verification(self, account, password):
        tar = os.path.join(self.folder, self.files["Owner"])
        tar_m = os.path.join(self.folder, self.files["Manager"])

        if self.exist(tar):
            acc_e = False
            df = pd.read_csv(tar,dtype=str)
            print(df)
            if not df[df['account']==account].empty:
                acc_e = True
                role = "Owner"
                if not df[df['account'] == account].empty and df[df['account'] == account]['password'].iloc[0] == password:
                    pass_e = True
                else:
                    pass_e = False
            else: pass_e = False
            if acc_e:
                if pass_e:
                    return account, role
                else:
                    return acc_e,pass_e
        elif self.exist(tar_m):
            df = pd.read_csv(tar_m,dtype=str)
            if not df[df['account']==account].empty:
                acc_e = True
                role = 'Manager'
                if not df[df['account'] == account].empty and df[df['account'] == account]['password'].iloc[0] == password:
                    pass_e = True
                else:
                    pass_e = False
            else: pass_e = False
            if acc_e:
                if pass_e:
                    return account, role
                else:
                    return acc_e,pass_e
        return False,False
    def find_subaccount(self,account):
        tar = os.path.join(self.folder, self.files["Manager"])
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            if not df[df['owner']==account].empty:
                print(df[df['owner']==account]['account'].values.tolist())
                return df[df['owner']==account]['account'].values.tolist()
            else: return []
        return []
    
    def get_restaurant_from_owner(self,owneraccount):
        subaccounts = self.find_subaccount(owneraccount)
        dfs = []
        if subaccounts:
            tar = os.path.join(self.folder, self.files["Manager"])
            df = pd.read_csv(tar,dtype=str)
            dfs = []
            for subaccount in subaccounts:
                dft = pd.read_csv(df[df['account'] == subaccount]["data_add"].iloc[0],dtype=str)
                dfs.append(dft)
        if dfs == []:
            print(dfs)
            return pd.DataFrame()
        print(dfs)
        return pd.concat(dfs,ignore_index=True)

    def check_pro(self,account):
        tar = os.path.join(self.folder, self.files["Owner"])
        tarm = os.path.join(self.folder, self.files["Manager"])
                
        if self.exist(tar):
            df = pd.read_csv(tar,dtype=str)
            if not df[df['account']==account].empty:
                filtered_df = df[df['account'] == account]
                if not filtered_df.empty and filtered_df['Pro'].iloc[0] != False:
                    return True

        elif self.exist(tarm):
            df = pd.read_csv(tarm,dtype=str)
            if not df[df['account']==account].empty:
                filtered_df = df[df['account'] == account]
                if not filtered_df.empty and filtered_df['Pro'].iloc[0] != False:
                    return True

        return False
    

    def put(self,text,font,tar = st,color='white',height = 2):
        tar.markdown(f"""
        <div style='taswqqsxext-align: left; color: {color}; font-size: {font}px; font-family: Arial; line-height: {height};'>
            {text}
        </div>
        """, unsafe_allow_html=True)

    def load_model(self,account):
        tar = os.path.join(self.folder, self.files["Manager"])
        if self.exist(tar):
            df = pd.read_csv(tar)
            if not df.empty:
                print(f"Model Path: {df[df['account'] == account]['model'].values[0]}")
                return df[df['account'] == account]['model'].values[0]


