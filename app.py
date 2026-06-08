import streamlit as st
import pandas as pd


# =========================
# LOAD DATA
# =========================

all_sheets = pd.read_excel(
    "master_data.xlsx",
    sheet_name=None
)

df = pd.concat(
    all_sheets.values(),
    ignore_index=True
)

df = df.fillna("")


# =========================
# CLEAN COLUMN NAMES
# =========================

df.columns = (
    df.columns
    .str.lower()
    .str.strip()
)


# =========================
# CLEAN DATA
# =========================

columns_to_clean = [
    'sector',
    'beneficiary type',
    'women_focused',
    'central/state',
    'target region/state'
]

for col in columns_to_clean:

    if col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.strip()
        )


# =========================
# RECOMMENDATION FUNCTION
# =========================

def recommend_schemes_scored(
    sector=None,
    beneficiary=None,
    women_focused=None,
    state=None,
    central_state=None,
    top_n=20
):

    filtered_df = df.copy()

    filtered_df['score'] = 0


    # =========================
    # CLEAN USER INPUT
    # =========================

    sector = sector.lower().strip() if sector else ""
    beneficiary = beneficiary.lower().strip() if beneficiary else ""
    state = state.lower().strip() if state else ""
    women_focused = women_focused.lower().strip() if women_focused else ""
    central_state = central_state.lower().strip() if central_state else ""


    # =========================
    # SECTOR FILTER
    # =========================

    if sector:

        filtered_df = filtered_df[

            filtered_df['sector']
            .str.contains(
                sector,
                case=False,
                na=False
            )

        ]

        filtered_df.loc[:, 'score'] += 3


    # =========================
    # BENEFICIARY FILTER
    # =========================

    if beneficiary:

        filtered_df = filtered_df[

            filtered_df['beneficiary type']
            .str.contains(
                beneficiary,
                case=False,
                na=False
            )

        ]

        filtered_df.loc[:, 'score'] += 2


    # =========================
    # STATE FILTER
    # =========================

    if state:

        filtered_df = filtered_df[

            filtered_df['target region/state']
            .str.contains(
                state,
                case=False,
                na=False
            )

            |

            filtered_df['target region/state']
            .str.contains(
                'pan india',
                case=False,
                na=False
            )

            |

            filtered_df['target region/state']
            .str.contains(
                'all india',
                case=False,
                na=False
            )

        ]

        filtered_df.loc[

            filtered_df['target region/state']
            .str.contains(
                state,
                case=False,
                na=False
            ),

            'score'

        ] += 2


    # =========================
    # WOMEN FOCUSED FILTER
    # =========================

    if women_focused == "yes":

        filtered_df = filtered_df[

            filtered_df['women_focused']
            .isin([
                'yes',
                'preferential'
            ])

        ]

        filtered_df.loc[:, 'score'] += 2


    elif women_focused == "no":

        filtered_df = filtered_df[

            filtered_df['women_focused']
            .isin([
                'no',
                'not mentioned'
            ])

        ]

        filtered_df.loc[:, 'score'] += 1


    elif women_focused == "preferential":

        filtered_df = filtered_df[

            filtered_df['women_focused']
            == 'preferential'

        ]

        filtered_df.loc[:, 'score'] += 2


    elif women_focused == "not mentioned":

        filtered_df = filtered_df[

            filtered_df['women_focused']
            == 'not mentioned'

        ]

        filtered_df.loc[:, 'score'] += 1


    # =========================
    # CENTRAL / STATE FILTER
    # =========================

    if central_state:

        filtered_df = filtered_df[

            filtered_df['central/state']
            == central_state

        ]

        filtered_df.loc[:, 'score'] += 2


    # =========================
    # REMOVE ZERO SCORE
    # =========================

    if (
        sector
        or beneficiary
        or women_focused
        or state
        or central_state
    ):

        filtered_df = filtered_df[
            filtered_df['score'] > 0
        ]


    # =========================
    # SORT RESULTS
    # =========================

    filtered_df = filtered_df.sort_values(
        by='score',
        ascending=False
    )


    return filtered_df.head(top_n)



# =========================
# STREAMLIT UI
# =========================

st.title("Government Scheme Recommendation System")


sector = st.text_input(
    "Enter Sector"
)

beneficiary = st.text_input(
    "Enter Beneficiary"
)


women_focused = st.selectbox(
    "Women Focused",
    [
        "",
        "yes",
        "no",
        "preferential",
        "not mentioned"
    ]
)


state = st.text_input(
    "Enter State"
)


central_state = st.selectbox(
    "Central or State",
    [
        "",
        "central",
        "state"
    ]
)


# =========================
# BUTTON
# =========================

if st.button("Get Recommendations"):

    results = recommend_schemes_scored(
        sector=sector,
        beneficiary=beneficiary,
        women_focused=women_focused,
        state=state,
        central_state=central_state
    )

    st.write(
        f"Total Recommendations Found: {len(results)}"
    )

    st.dataframe(results)


    # =========================
    # DEBUGGING (OPTIONAL)
    # =========================

    with st.expander("Debug Unique Values"):

        st.write(
            "Women Focused Values:"
        )

        st.write(
            df['women_focused'].unique()
        )

        st.write(
            "Central/State Values:"
        )

        st.write(
            df['central/state'].unique()
        )

        st.write(
            "State Values:"
        )

        st.write(
            df['target region/state'].unique()
        )