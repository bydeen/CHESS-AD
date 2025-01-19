# CHESS-AD: Resolving Ambiguous Questions with Example Table Generation in Text-to-SQL

This repository is a fork of the code and data for the paper **"CHESS: Contextual Harnessing for Efficient SQL Synthesis."**

## AMBROSIA Dataset

CHESS-AD supports the **AMBROSIA** dataset. The dataset is available at https://ambrosia-benchmark.github.io/.

## Setting up the Environment

1. **Clone the repository**:

   ```bash
   git clone https://github.com/bydeen/CHESS-AD.git
   cd CHESS-AD
   ```

2. **Create a `.env` file** in the root directory using `env.example` as a template.

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Preprocessing

To retrieve database catalogs, preprocess the databases with a targeted ambiguity type:

1. **Run the preprocessing script**:

   ```bash
   bash run/run_preprocess_ambrosia.sh {scope, attachment, vague}
   ```

   Replace `{scope, attachment, vague}` with one of the ambiguity types (e.g., `scope`). This script will create the minhash and LSH for each of the databases in the specified directory.

## Running the Code

After preprocessing the databases, generate SQL queries for the AMBROSIA dataset with a targeted ambiguity type:

1. **Run the main script**:

   ```bash
   bash run/run_main_ad_ir_cg.sh {scope, attachment, vague}
   ```

   Replace `{scope, attachment, vague}` with one of the ambiguity types. Ensure the same ambiguity type is used as in preprocessing.
