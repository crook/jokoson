#!/bin/bash -xe

unset http_proxy
unset https_proxy

ENDPOINT='http://10.110.126.208:8888/'

function json_escape
{
  echo -n "$1" | python -c 'import json,sys; print json.dumps(sys.stdin.read())'
}

function get_id
{
    json_data=$1
    ID=`echo $json_data | python -c 'import json,sys;obj=json.load(sys.stdin);print(obj["id"])'`
    echo -n $ID
}

function curl_post_cmd
{
    obj=$1
    json_file=$2

    end_point="${ENDPOINT}${obj}/"
    cmd="curl --silent -X POST -u admin:zaq12WSX "
    cmd="$cmd -H Content-Type:application/json "
    cmd="$cmd -d @${json_file} ${end_point}"

    output=$($cmd)
    if [ $? != 0 ]; then
        echo "FAIL to post $obj with json file: $json_file"
        exit 1;
    fi
    ID=$(get_id $output)
    echo -n $ID
}

function curl_get_cmd
{
    obj_with_id=$1

    end_point="${ENDPOINT}${obj_with_id}/"
    cmd="curl -s ${end_point}"

    output=$($cmd)
    if [ $? != 0 ]; then
        echo "FAIL to get $obj_with_id"
        exit 1;
    fi
    ID=$(get_id $output)
    echo -n $ID
}

function curl_delete_cmd
{
    obj_with_id=$1

    end_point="${ENDPOINT}${obj_with_id}/"
    cmd="curl -s -X DELETE -u admin:zaq12WSX -H Content-Type:application/json ${end_point}"

    output=$($cmd)

    if [ $? != 0 ]; then
        echo "FAIL to delete $obj_with_id"
        exit 1;
    fi

    echo $output
}

function model_ops
{
    model=$1

    # Create one equip
    ID=$(curl_post_cmd $model "${model}_create.json")
    # List the equip
    ID2=$(curl_get_cmd "$model/$ID")
    # Update the equip

    # Delte the equip
    curl_delete_cmd "$model/$ID2"

}


#### Main #####
models=$1
if [ -z "$models" ]; then
    models="orders equips vendors categories gpssensors gpsdatas"
fi


for item in $models
    do
        model_ops $item
        if [ $? == 0 ]; then
            echo "PASS: test $item"
        fi
    done

echo "PASS: All is ok"
