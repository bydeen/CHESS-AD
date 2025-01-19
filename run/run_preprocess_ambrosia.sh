#!/bin/bash
source .env

ambiguity_type=$1
ambrosia_path=$DB_ROOT_PATH
data_mode=$DATA_MODE
verbose=true
signature_size=100
n_gram=3
threshold=0.01

if [ -z "$ambiguity_type" ]; then
  echo "Error: Ambiguity type is required. Choose from [scope, attachment, vague]."
  exit 1
fi

db_root_path="${ambrosia_path}/${ambiguity_type}"
if [ ! -d "$db_root_path" ]; then
  echo "Error: Directory ${db_root_path} does not exist."
  exit 1
fi

for db_root_directory in "$db_root_path"/*; do
    if [ -d "$db_root_directory" ]; then
        for db_path in "$db_root_directory"/*; do
            if [ -d "$db_path" ]; then
                db_id=$(basename "$db_path")
                echo "Preprocessing $db_id"

                python3 -u ./src/preprocess.py --data_mode "${data_mode}" \
                                              --db_root_directory "${db_root_directory}" \
                                              --signature_size "${signature_size}" \
                                              --n_gram "${n_gram}" \
                                              --threshold "${threshold}" \
                                              --db_id "${db_id}" \
                                              --verbose "${verbose}"
            fi
        done
    fi
done