import pandas as pd

RAW_PATH = "data/raw/rawPay.csv"
WAGES_OUTPUT_PATH = "data/cleaned/wages.csv"
COMPANIES_OUTPUT_PATH = "data/cleaned/companies.csv"

def clean_number(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
        .astype(int)
    )

wages = pd.read_csv(RAW_PATH)

wages = wages.drop(
    columns=[
        "Index",
        "CEO: Lower quarter employee ratio",
        "CEO: Median employee ratio",
        "CEO: Upper quartile employee ratio",
    ]
)

wages = wages.rename(
    columns={
        "CEO pay (£000)": "ceo_pay_k",
        "Lower quartile employee's pay (£)": "lq_pay",
        "Median employee's pay (£)": "m_pay",
        "Upper quartile employee's pay (£)": "uq_pay",
        "Year End": "Year",
        "Number of UK employees": "employees",
    }
)

wages = wages.dropna()
wages["Year"] = wages["Year"].str.split(".").str[-1].astype(int)

for column in ["ceo_pay_k", "employees", "lq_pay", "m_pay", "uq_pay"]:
    wages[column] = clean_number(wages[column])

company_rows = wages.sort_values("employees", ascending=False).drop_duplicates("Company")

companies = company_rows[["Company", "Industry", "Sector", "employees"]].copy()
companies = companies.sort_values("employees", ascending=False).head(20)

wages = wages.drop(columns=["Industry", "Sector"])

wages.to_csv(WAGES_OUTPUT_PATH, index=False)
companies.to_csv(COMPANIES_OUTPUT_PATH, index=False)
