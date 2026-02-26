def assess_data_quality(df, amount_col, date_col):

    issues = []

    if amount_col:
        missing_amount = df[amount_col].isnull().sum()
        if missing_amount > 0:
            issues.append(f"{missing_amount} records missing revenue")

    if date_col:
        missing_dates = df[date_col].isnull().sum()
        if missing_dates > 0:
            issues.append(f"{missing_dates} records missing dates")

    return issues