import numpy as np

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def _transform(previous_task, **kwargs):
    df = kwargs['ti'].xcom_pull(task_ids=previous_task)
    df.drop('issue_d', axis=1, inplace=True)
    feature = df.columns[:-1]

    cat_feature = [
        "initial_list_status",
        "application_type",
        "home_ownership",
        "verification_status",
        "purpose",
    ]

    cat_range = [
            np.arange(int(df[f].min()), int(df[f].max()) + 1)
            for f in cat_feature
    ]

    num_feature = list(set(feature) - set(cat_feature))

    transformer = ColumnTransformer(
        transformers = [("num", StandardScaler(), num_feature),
                        ("cat",
                        OneHotEncoder(
                            sparse=False,
                            handle_unknown="ignore",
                            drop="if_binary",
                            categories=cat_range,
                        ),
                        cat_feature,
                    )
                    ],
        sparse_threshold=0,
        remainder="passthrough",
        n_jobs=-1,
    )

    transformer.fit(df[feature])

    return transformer