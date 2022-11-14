import numpy  as np
import pandas as pd

SEPARATOR = "---------"

def _read_csv(file_path, **kwargs):
    start_df = pd.read_csv(file_path, low_memory=False)

    loans = start_df.copy(deep=True)
    # ------------------- TARGET
    # target

    loans = loans.loc[loans["loan_status"].isin(["Fully Paid", "Charged Off"])]
    # ------------------- DATA AVAILABLE

    # Remove data with more than 30% missing

    missing_fractions = loans.isnull().mean().sort_values(ascending=False)
    drop_list = sorted(list(missing_fractions[missing_fractions > 0.3].index))
    print(drop_list)

    # Only keep features known by investors

    keep_list = [
        "addr_state",
        "annual_inc",
        "application_type",
        "dti",
        "earliest_cr_line",
        "emp_length",
        "emp_title",
        "fico_range_high",
        "fico_range_low",
        "grade",
        "home_ownership",
        "id",
        "initial_list_status",
        "installment",
        "int_rate",
        "issue_d",
        "loan_amnt",
        "loan_status",
        "mort_acc",
        "open_acc",
        "pub_rec",
        "pub_rec_bankruptcies",
        "purpose",
        "revol_bal",
        "revol_util",
        "sub_grade",
        "term",
        "title",
        "total_acc",
        "verification_status",
        "zip_code",
    ]
    drop_list = [col for col in loans.columns if col not in keep_list]
    print(drop_list)

    loans.drop(labels=drop_list, axis=1, inplace=True)
    return loans

def _feature_engineering(previous_task, save_path, **kwargs):
    loans = kwargs['ti'].xcom_pull(task_ids=previous_task)
    # ----- SIMPLE REMOVAL
    # Remove id, to specific

    loans.drop("id", axis=1, inplace=True)

    # Remove emp_title to many different values

    loans.drop(labels="emp_title", axis=1, inplace=True)
    loans.drop("title", axis=1, inplace=True)
    loans.drop(labels=["zip_code", "addr_state"], axis=1, inplace=True)

    # Remove grade, redundant
    loans.drop("grade", axis=1, inplace=True)

    # ----- CONVERSION

    # convert term to integer
    loans["term"] = loans["term"].apply(lambda s: np.int8(s.split()[0]))

    # Convert emp_length

    loans["emp_length"].replace(to_replace="10+ years", value="10 years", inplace=True)
    loans["emp_length"].replace("< 1 year", "0 years", inplace=True)

    def emp_length_to_int(s):
        if pd.isnull(s):
            return s
        else:
            return np.int8(s.split()[0])

    loans["emp_length"] = loans["emp_length"].apply(emp_length_to_int)

    # # Home home ownerish replace any/none to other
    # loans["home_ownership"].replace(["NONE", "ANY"], "OTHER", inplace=True)

    # Date

    # loans["earliest_cr_line"] = pd.to_datetime(
    #     loans["earliest_cr_line"].fillna("1900-01-01")
    # ).apply(lambda x: int(x.strftime("%Y%m")))
    # loans["earliest_cr_line"] = loans["earliest_cr_line"].replace({190001: np.nan})
    # loans["issue_d"] = pd.to_datetime(loans["issue_d"]).apply(
    #     lambda x: int(x.strftime("%Y%m"))
    # )
    loans["earliest_cr_line"] = pd.to_datetime(loans["earliest_cr_line"])
    loans["issue_d"] = pd.to_datetime(loans["issue_d"])

    #  fico_range_low fico_range_high are correlated, take average

    loans["fico_score"] = 0.5 * loans["fico_range_low"] + 0.5 * loans["fico_range_high"]
    loans.drop(["fico_range_high", "fico_range_low"], axis=1, inplace=True)

    # grade

    replacements = [
        ("A", "1"),
        ("B", "2"),
        ("C", "3"),
        ("D", "4"),
        ("E", "5"),
        ("F", "6"),
        ("G", "7"),
    ]
    for r in replacements:
        loans["sub_grade"] = loans["sub_grade"].str.replace(r[0], r[1])
    loans["sub_grade"] = loans["sub_grade"].astype(float)
    loans["sub_grade"] = loans["sub_grade"].replace(
        np.sort(loans["sub_grade"].unique()),
        np.arange(loans["sub_grade"].unique().shape[0]).astype(int),
    )

    # Feature creation

    def diff_date_month(a, b):
        return 12 * (a.dt.year - b.dt.year) + (a.dt.month - b.dt.month)

    def ratio_pub_rec_pub_rec_bankruptcies(pub_rec_bankruptcies, pub_rec):
        if pub_rec > 0:
            return pub_rec_bankruptcies / pub_rec
        else:
            return -1

    loans["month_of_year"] = loans["issue_d"].dt.month - 1
    loans["ratio_loan_amnt_annual_inc"] = loans["loan_amnt"] / loans["annual_inc"]
    loans["ratio_open_acc_total_acc"] = loans["open_acc"] / loans["total_acc"]

    loans["month_since_earliest_cr_line"] = diff_date_month(
        loans["issue_d"], loans["earliest_cr_line"]
    )
    loans = loans.drop("earliest_cr_line", axis=1)

    loans["ratio_pub_rec_month_since_earliest_cr_line"] = (
        loans["pub_rec"] / loans["month_since_earliest_cr_line"]
    )
    loans["ratio_pub_rec_bankruptcies_month_since_earliest_cr_line"] = (
        loans["pub_rec_bankruptcies"] / loans["month_since_earliest_cr_line"]
    )
    loans["ratio_pub_rec_bankruptcies_pub_rec"] = loans.apply(
        lambda x: ratio_pub_rec_pub_rec_bankruptcies(x.pub_rec_bankruptcies, x.pub_rec),
        axis=1,
    )

    # Categorical to numbers

    for e in [
        "initial_list_status",
        "application_type",
        "home_ownership",
        "verification_status",
        "purpose",
    ]:
        unique_values = loans[e].unique()
        loans[e] = loans[e].replace(unique_values, np.arange(len(unique_values)))

    # Convert to charge off

    loans["charged_off"] = (loans["loan_status"] == "Charged Off").apply(np.uint8)
    loans.drop("loan_status", axis=1, inplace=True)

    loans.dropna(inplace=True)

    # Type
    for e in [
        "open_acc",
        "total_acc",
        "emp_length",
        "mort_acc",
        "pub_rec_bankruptcies",
        "month_since_earliest_cr_line",
        "sub_grade",
    ]:
        loans[e] = loans[e].astype(int)

    # Sort by date
    loans = loans.sort_values(by="issue_d")

    print(SEPARATOR)
    print("Saving dataset", loans.shape)
    print(loans.columns)
    loans.to_csv(save_path, index=False)
    # pd.DataFrame(loans.dtypes).to_csv('venus_dtypes.csv', index=True)

    return loans
