import pandas as pd

RAW_PATH = "data/raw/rawPay.csv"
WAGES_OUTPUT_PATH = "data/cleaned/wages.csv"
COMPANIES_OUTPUT_PATH = "data/cleaned/companies.csv"

ENERGY_INDUSTRIES = {"Oil and Gas", "Energy", "Utilities"}
ENERGY_SECTORS = {
    "Oil and Gas Producers",
    "Oil Equipment and Services",
    "Oil, Gas and Coal",
    "Oil, Gas & Coal",
    "Gas, Water and Multi-Utilities",
    "Electricity",
}

def clean_number(series, allow_missing=False):
    cleaned = (
        series.astype("string")
        .str.replace(",", "", regex=False)
        .str.replace(" ", "", regex=False)
    )
    numeric = pd.to_numeric(cleaned, errors="coerce")
    if allow_missing:
        return numeric.astype("Int64")
    return numeric.astype(int)

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

wages = wages.dropna(subset=["ceo_pay_k", "lq_pay", "m_pay", "uq_pay", "Year"])
wages["Year"] = wages["Year"].str.split(".").str[-1].astype(int)

for column in ["ceo_pay_k", "lq_pay", "m_pay", "uq_pay"]:
    wages[column] = clean_number(wages[column])
wages["employees"] = clean_number(wages["employees"], allow_missing=True)

energy_mask = wages["Industry"].isin(ENERGY_INDUSTRIES) | wages["Sector"].isin(ENERGY_SECTORS)
wages = wages[energy_mask].copy()

company_year_counts = wages.groupby("Company")["Year"].nunique()
companies_with_enough_history = company_year_counts[company_year_counts > 4].index
wages = wages[wages["Company"].isin(companies_with_enough_history)].copy()

company_rows = wages.sort_values("employees", ascending=False).drop_duplicates("Company")

companies = company_rows[["Company", "Industry", "Sector", "employees"]].copy()
companies = companies.sort_values("employees", ascending=False).head(20)

wages = wages.drop(columns=["Industry", "Sector"])

wages.to_csv(WAGES_OUTPUT_PATH, index=False)
companies.to_csv(COMPANIES_OUTPUT_PATH, index=False)
