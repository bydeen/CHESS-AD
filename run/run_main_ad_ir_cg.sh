#!/bin/bash
source .env

ambiguity_type=$1
domain=$2
db_id=$3
data_mode=$DATA_MODE
if [ $data_mode != "ambrosia" ]; then
    data_path=$DATA_PATH
fi

config="./run/configs/CHESS_AD_IR_CG.yaml"

num_workers=1 # Number of workers to use for parallel processing, set to 1 for no parallel processing

if [ $data_mode == "ambrosia" ]; then
    if [ -z "$ambiguity_type" ]; then
        echo "Error: Ambiguity type is required. Choose from [scope, attachment, vague]."
        exit 1
    fi
    db_root_path="${DB_ROOT_PATH}/${ambiguity_type}"
    if [ ! -d "$db_root_path" ]; then
        echo "Error: Directory ${db_root_path} does not exist."
        exit 1
    fi

    # if domain and db_id are provided, process only that database
    if [ ! -z "$domain" ] && [ ! -z "$db_id" ]; then
        echo "Domain \"$domain\""
        export DB_ROOT_DIRECTORY="${db_root_path}/${domain}"
        
        db_path="${db_root_path}/${domain}/${db_id}"
        if [ ! -d "$db_path" ]; then
            echo "Error: Directory ${db_path} does not exist."
            exit 1
        fi
        echo "Processing \"$db_id\""
        data_path="${db_path}/examples.json"

        python3 -u ./src/main.py --data_mode ${data_mode} \
                                 --data_path "${data_path}" \
                                 --db_id "${db_id}" \
                                 --config "$config" \
                                 --num_workers ${num_workers} \
                                 --pick_final_sql true \
                                 --user_selection true
    # if only domain is provided, process all databases in that domain
    elif [ ! -z "$domain" ]; then
        echo "Domain \"$domain\""
        export DB_ROOT_DIRECTORY="${db_root_path}/${domain}"

        for db_path in "${db_root_path}/${domain}"/*; do
            if [ -d "$db_path" ]; then
                db_id=$(basename "$db_path")
                echo "Processing \"$db_id\""
                data_path="${db_path}/examples.json"

                python3 -u ./src/main.py --data_mode ${data_mode} \
                                         --data_path "${data_path}" \
                                         --db_id "${db_id}" \
                                         --config "$config" \
                                         --num_workers ${num_workers} \
                                         --pick_final_sql true \
                                         --user_selection true
            fi
        done
    else
        for db_root_directory in "$db_root_path"/*; do
            if [ -d "$db_root_directory" ]; then
                echo "Domain \"$db_root_directory\""
                export DB_ROOT_DIRECTORY="$db_root_directory"

            for db_path in "$db_root_directory"/*; do
                    if [ -d "$db_path" ]; then
                        db_id=$(basename "$db_path")
                        echo "Processing \"$db_id\""
                        data_path="${db_path}/examples.json"

                        python3 -u ./src/main.py --data_mode ${data_mode} \
                                                 --data_path "${data_path}" \
                                                 --db_id "${db_id}" \
                                                 --config "$config" \
                                                 --num_workers ${num_workers} \
                                                 --pick_final_sql true \
                                                #  --user_selection true
                    fi
                done
            fi
        done
    fi
else
    python3 -u ./src/main.py --data_mode ${data_mode} \
                                --data_path ${data_path} \
                                --config "$config" \
                                --num_workers ${num_workers} \
                                --pick_final_sql true
fi