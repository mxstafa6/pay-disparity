import pandas as pd

wages = pd.read_csv('data/raw/rawPay.csv')
wages.drop(columns=["Index", "CEO pay (£000)", "Number of UK employees", "CEO: Lower quarter employee ratio", "CEO: Median employee ratio", "CEO: Upper quartile employee ratio"], inplace=True)
wages.rename(columns={"Lower quartile employee's pay (£)":"lq_pay", "Median employee's pay (£)":"m_pay", "Upper quartile employee's pay (£)":"uq_pay", "Year End": "year"},inplace=True)
wages.dropna(inplace=True)
wages["year"]=wages["year"].str.split(".").str[-1].astype(int)
for col in ['lq_pay', 'm_pay', 'uq_pay']:
    wages[col] = wages[col].str.replace(",", "").str.replace(" ", "").astype(int)
dx=wages.drop_duplicates("Company")
companies={}
for index, row in dx.iterrows():
    companies[row["Company"]]=[row["Industry"],row["Sector"]]
companies=pd.DataFrame.from_dict(companies, orient="index")
companies.rename(columns={0:"Industry", 1:"Sector"}, inplace=True)
wages.to_csv("data/cleaned/wages.csv", index=False)
companies.to_csv("data/cleaned/companies.csv", index_label="Company")