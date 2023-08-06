import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv("train.csv")
data = data.drop('Loan_ID',axis=1)

data.Gender = data.Gender.fillna('Male')
data.Married = data.Married.fillna('Yes')
data.Dependents = data.Dependents.fillna('0')
data.Self_Employed = data.Self_Employed.fillna('No')
data.LoanAmount = data.LoanAmount.fillna(data.LoanAmount.mean())
data.Loan_Amount_Term = data.Loan_Amount_Term.fillna(360.0)
data.Credit_History = data.Credit_History.fillna(1.0)
data.Dependents=data.Dependents.replace(to_replace="3+",value="4")

data['Gender']=data['Gender'].map({"Male":1,"Female":0}).astype("int")
data['Married']=data['Married'].map({"Yes":1,"No":0}).astype("int")
data['Education']=data['Education'].map({"Graduate":1,"Not Graduate":0}).astype("int")
data['Self_Employed']=data['Self_Employed'].map({"Yes":1,"No":0}).astype("int")
data['Property_Area']=data['Property_Area'].map({"Urban":1,"Rural":0,"Semiurban":2}).astype("int")
data['Loan_Status']=data['Loan_Status'].map({"Y":1,"N":0}).astype("int")

X = data.drop("Loan_Status",axis=1)
y = data['Loan_Status']

cols = ["ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term"]

st = StandardScaler()
X[cols] = st.fit_transform(X[cols])

lr_model = LogisticRegression()
lr_model.fit(X,y)
joblib.dump(lr_model,"model")