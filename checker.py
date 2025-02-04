import streamlit as st
import pandas as pd
import re


def validate_zip_codes(df):
    for col in df.columns:
        if 'zip' in col.lower():
            try:
                invalid_zips = df[col].astype(str).str.len() != 5
                count_invalid = invalid_zips.sum()
                if count_invalid > 0:
                    st.error(f"❌ Column '{col}': {count_invalid} invalid ZIP codes found")
                else:
                    st.success(f"✅ Column '{col}': OK")
            except Exception as e:
                st.warning(f"❌ Error processing ZIP codes in '{col}': {e}")


def validate_names(df):
    for col in df.columns:
        if 'name' in col.lower():
            try:
                invalid_names = df[col].astype(str).str.contains(r'\d', regex=True)
                count_invalid = invalid_names.sum()
                if count_invalid > 0:
                    st.error(f"❌ Column '{col}': {count_invalid} names contain numbers")
                else:
                    st.success(f"✅ Column '{col}': OK")
            except Exception as e:
                st.warning(f"❌ Error processing names in '{col}': {e}")


def validate_emails(df):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    for col in df.columns:
        if 'email' in col.lower():
            try:
                invalid_emails = ~df[col].astype(str).str.match(email_regex, na=False)
                count_invalid = invalid_emails.sum()
                if count_invalid > 0:
                    st.error(f"❌ Column '{col}': {count_invalid} invalid email addresses found")
                else:
                    st.success(f"✅ Column '{col}': OK")
            except Exception as e:
                st.warning(f"❌ Error processing emails in '{col}': {e}")


def validate_phone_numbers(df, area_codes):
    for col in df.columns:
        if 'number' in col.lower():
            try:
                invalid_phones = ~df[col].astype(str).str[:3].isin(area_codes)
                count_invalid = invalid_phones.sum()
                if count_invalid > 0:
                    st.error(f"❌ Column '{col}': {count_invalid} invalid phone numbers found")
                else:
                    st.success(f"✅ Column '{col}': OK")
            except Exception as e:
                st.warning(f"❌ Error processing phone numbers in '{col}': {e}")


def validate_age(df):
    for col in df.columns:
        if col.lower() == 'age':
            try:
                invalid_ages = ~df[col].astype(str).str.match(r'^[0-9]+$', na=False)
                count_invalid = invalid_ages.sum()
                if count_invalid > 0:
                    st.error(f"❌ Column '{col}': {count_invalid} invalid age values found")
                else:
                    st.success(f"✅ Column '{col}': OK")
            except Exception as e:
                st.warning(f"❌ Error processing age in '{col}': {e}")


st.title("Avcon Upload File Pre-Testing")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])


def validate_state(df):
    for col in df.columns:
        try:
            if "state" in col.lower():
                invalid_values = df[~df[col].isin(states)][col]
                if invalid_values.empty:
                    st.success(f"✅ Column '{col}' is valid.")
                else:
                    st.error(f"❌ Column '{col}' contains {len(invalid_values)} invalid state values.")

        except Exception as e:
            st.warning(f"❌ Error processing state in '{col}': {e}")


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("### Columns in File:", df.columns.tolist())
        st.write("### Sample Data:")
        st.dataframe(df.head())

        states = [
            "Select State", "AL", "DC", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
            "FL", "GA", "HI", "ID", "IL",
            "IN", "IA",
            "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
            "NV", "NH", "NJ", "NM", "NY", "NC",
            "ND",
            "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA",
            "WA", "WV", "WI", "WY"
        ]

        area_codes = [
            "205", "251", "256", "334", "907", "480", "520", "602", "623", "928",
            "479", "501", "870", "209", "213", "310", "323", "408", "415", "510", "530",
            "559", "562", "619", "626", "650", "661", "707", "714", "760", "805", "818",
            "831", "858", "909", "916", "925", "949", "951", "303", "719", "720", "970",
            "203", "475", "860", "959", "302", "239", "305", "321", "352", "386", "407",
            "561", "727", "754", "772", "786", "813", "850", "863", "904", "941", "954",
            "229", "404", "470", "478", "678", "706", "762", "770", "912", "808", "208",
            "217", "224", "309", "312", "331", "618", "630", "708", "773", "779", "815",
            "847", "872", "219", "260", "317", "463", "574", "765", "812", "930", "319",
            "515", "563", "641", "712", "316", "620", "785", "913", "270", "364", "502",
            "606", "859", "225", "318", "337", "504", "985", "207", "240", "301", "410",
            "443", "667", "339", "351", "413", "508", "617", "774", "781", "857", "978",
            "231", "248", "269", "313", "517", "586", "616", "734", "810", "906", "947",
            "989", "218", "320", "507", "612", "651", "763", "952", "228", "601", "662",
            "769", "314", "417", "573", "636", "660", "816", "406", "308", "402", "531",
            "702", "725", "775", "603", "201", "551", "609", "732", "848", "856", "862",
            "908", "973", "505", "575", "212", "315", "332", "347", "516", "518", "585",
            "607", "631", "646", "680", "716", "718", "845", "914", "917", "929", "934",
            "252", "336", "704", "743", "828", "910", "919", "980", "984", "701", "216",
            "220", "234", "330", "380", "419", "440", "513", "567", "614", "740", "937",
            "405", "539", "580", "918", "458", "503", "541", "971", "215", "223", "267",
            "272", "412", "445", "484", "570", "610", "717", "724", "814", "878", "401",
            "803", "843", "854", "864", "605", "423", "615", "629", "731", "865", "901",
            "931", "210", "214", "254", "281", "325", "346", "361", "409", "430", "432",
            "469", "512", "682", "713", "737", "806", "817", "830", "832", "903", "915",
            "936", "940", "956", "972", "979", "385", "435", "801", "802", "276", "434",
            "540", "571", "703", "757", "804", "206", "253", "360", "425", "509", "564",
            "304", "681", "262", "414", "534", "608", "715", "920", "307"
        ]

        validate_zip_codes(df)
        validate_names(df)
        validate_emails(df)
        validate_phone_numbers(df, area_codes)
        validate_age(df)
        validate_state(df)
    except Exception as e:
        st.error(f"Error reading the file: {e}")

