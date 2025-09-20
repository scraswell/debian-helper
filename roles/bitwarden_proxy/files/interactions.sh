curl -kfsSL \
    -X POST 'http://localhost:8087/unlock' \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' \
    -d '{"password":"thisisapassword"}' | jq

curl -kfsSL \
    -X GET 'http://localhost:8087/list/object/items' \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' | jq

curl -kfsSL \
    -X GET 'http://localhost:8087/object/item/2f72ba71-c65e-4886-8c73-c9154416d60f' \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' | jq

curl -kfsSL \
    -X POST 'http://localhost:8087/lock' \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json' | jq