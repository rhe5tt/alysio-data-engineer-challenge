import sqlite3
import pandas as pd
import json
from datetime import datetime

# File paths
COMPANIES_FILE = "data/salesforce/companies.csv"
CONTACTS_FILE = "data/salesforce/contacts.json"
OPPORTUNITIES_FILE = "data/salesforce/opportunities.csv"
ACTIVITIES_FILE = "data/salesforce/activities.json"
DB_FILE = "crm_data.db"

# Create SQLite database and tables
def create_schema():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        domain TEXT,
        industry TEXT,
        size TEXT,
        country TEXT,
        created_date TEXT,
        is_customer BOOLEAN,
        annual_revenue REAL,
        last_modified_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT,
        last_name TEXT,
        title TEXT,
        company_id TEXT NOT NULL,
        phone TEXT,
        status TEXT,
        created_date TEXT,
        last_modified_date TEXT,
        FOREIGN KEY (company_id) REFERENCES companies (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id TEXT PRIMARY KEY,
        company_id TEXT NOT NULL,
        stage TEXT,
        value REAL,
        created_date TEXT,
        last_modified_date TEXT,
        FOREIGN KEY (company_id) REFERENCES companies (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id TEXT PRIMARY KEY,
        contact_id TEXT NOT NULL,
        opportunity_id TEXT,
        type TEXT,
        subject TEXT,
        timestamp TEXT,
        duration_minutes INTEGER,
        outcome TEXT,
        notes TEXT,
        FOREIGN KEY (contact_id) REFERENCES contacts (id),
        FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
    );
    """)

    conn.commit()
    conn.close()

# Load data into SQLite
def load_data():
    conn = sqlite3.connect(DB_FILE)

    # Load companies
    companies_df = pd.read_csv(COMPANIES_FILE)
    companies_df.to_sql('companies', conn, if_exists='replace', index=False)

    # Load contacts
    with open(CONTACTS_FILE, 'r') as file:
        contacts_data = json.load(file)
    contacts_df = pd.DataFrame(contacts_data)
    contacts_df.to_sql('contacts', conn, if_exists='replace', index=False)

    # Load opportunities
    opportunities_df = pd.read_csv(OPPORTUNITIES_FILE)
    opportunities_df.to_sql('opportunities', conn, if_exists='replace', index=False)

    # Load activities
    with open(ACTIVITIES_FILE, 'r') as file:
        activities_data = json.load(file)
    activities_df = pd.DataFrame(activities_data)
    activities_df.to_sql('activities', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

# Remove duplicate contacts
def remove_duplicate_contacts(conn):
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM contacts
    WHERE id NOT IN (
        SELECT MAX(id)
        FROM contacts
        GROUP BY email
    );
    """)
    conn.commit()

# Clean and normalize data
def clean_data():
    conn = sqlite3.connect(DB_FILE)

    # Remove duplicate contacts
    remove_duplicate_contacts(conn)

    # Fill missing industries with "Unknown"
    conn.execute("UPDATE companies SET industry = 'Unknown' WHERE industry IS NULL;")

    # Normalize company names
    conn.execute("UPDATE companies SET name = TRIM(UPPER(name));")

    # Remove contacts with missing critical fields
    conn.execute("DELETE FROM contacts WHERE email IS NULL;")

    # Validate and correct dates in companies
    companies_df = pd.read_sql_query("SELECT * FROM companies", conn)
    companies_df['created_date'] = pd.to_datetime(companies_df['created_date'], errors='coerce')
    companies_df['last_modified_date'] = pd.to_datetime(companies_df['last_modified_date'], errors='coerce')
    companies_df.dropna(subset=['created_date'], inplace=True)
    companies_df.to_sql('companies', conn, if_exists='replace', index=False)

    # Normalize phone numbers in contacts
    conn.execute("""
    UPDATE contacts
    SET phone = REPLACE(REPLACE(REPLACE(phone, '-', ''), '(', ''), ')', '')
    WHERE phone IS NOT NULL;
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_schema()
    load_data()
    clean_data()
    print(f"Database setup and data cleaning complete. Data loaded into {DB_FILE}")
