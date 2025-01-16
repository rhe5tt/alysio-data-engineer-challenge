# CRM Data Engineering Challenge

## Objective
Create a SQLite database from provided CRM data, implementing data cleaning and proper relational schema design.

## Data Description
- `companies.csv`: Company profiles with industry and revenue data
- `contacts.json`: Contact information with potential duplicates
- `opportunities.csv`: Sales pipeline data
- `activities.json`: Customer interaction logs

## Requirements

### 1. Database Schema
- Design normalized tables with proper relationships
- Implement appropriate constraints and indexes
- Document schema design decisions

### 2. Data Cleaning
- Standardize company names and industries
- Remove duplicate contacts while preserving relationship integrity
- Normalize phone numbers and email addresses
- Handle missing values appropriately
- Validate date formats and ranges

### 3. Data Loading
- Create ETL pipeline to load data into SQLite
- Implement error handling and logging
- Validate referential integrity
- Create process for incremental updates


## Deliverables
1. SQLite database with cleaned data
2. Python scripts for ETL process
3. SQL schema creation scripts
4. Documentation of cleaning rules and assumptions
5. Sample queries demonstrating data access

## Evaluation Criteria
- Schema design and normalization
- Data cleaning methodology
- Code quality and organization
- Error handling
- Query performance
- Documentation quality

## Setup
```bash
python -m venv venv
source venv/bin/activate  # or `env\Scripts\activate` on Windows
pip install -r requirements.txt
python src/data_generator.py
```

## Submission
1. Fork this repository
2. Complete the challenge
3. Submit pull request with all deliverables