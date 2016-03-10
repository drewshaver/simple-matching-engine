# TODO programmatically test results

curl localhost:3000/sell --data '{"qty":8,"prc":20}' -H "Content-Type: application/json" && echo
curl localhost:3000/sell --data '{"qty":20,"prc":22}' -H "Content-Type: application/json" && echo
curl localhost:3000/buy  --data '{"qty":5,"prc":7}' -H "Content-Type: application/json" && echo
curl localhost:3000/buy  --data '{"qty":4,"prc":7.5}' -H "Content-Type: application/json" && echo
curl localhost:3000/sell --data '{"qty":1, "prc":7.5}' -H "Content-Type: application/json" && echo
echo 'Should have filled 1 at 7.5'
curl localhost:3000/sell  --data '{"qty":2, "prc":1}' -H "Content-Type: application/json" && echo
echo 'Should have filled 2 at 7.5'
curl localhost:3000/sell --data '{"qty":7, "prc":7.5}' -H "Content-Type: application/json" && echo
echo 'Should have filled 1 at 7.5'
curl localhost:3000/buy --data '{"qty":3, "prc":8}' -H "Content-Type: application/json" && echo
echo 'Should have filled 3 at 7.5'
curl localhost:3000/buy --data '{"qty":20, "prc":20, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled none'
curl localhost:3000/buy --data '{"qty":20, "prc":20, "alo":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled none'
curl localhost:3000/sell --data '{"qty":1, "prc":20, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled none'
curl localhost:3000/buy --data '{"qty":11, "prc":20, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled 3 at 7.5 and 8 at 20'
curl localhost:3000/buy --data '{"qty":21, "prc":22, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled none'
curl localhost:3000/buy --data '{"qty":20, "prc":22, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled 20 at 22'
curl localhost:3000/sell --data '{"qty":21, "prc":1, "alo":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled none'
curl localhost:3000/sell --data '{"qty":5, "prc":5, "fok":true}' -H "Content-Type: application/json" && echo
echo 'Should have filled 5 at 7'
curl localhost:3000/book && echo
echo 'Should have cleared book'

# test argument validation
curl localhost:3000/sell --data '{"qty":1.5, "prc":6}' -H "Content-Type: application/json" && echo
echo 'Should have returned error'
curl localhost:3000/buy --data '{"qty":"12", "prc":6}' -H "Content-Type: application/json" && echo
echo 'Should have returned error'
curl localhost:3000/buy --data '{"qty":"1", "prc":false}' -H "Content-Type: application/json" && echo
echo 'Should have returned error'
curl localhost:3000/buy --data '{"qty":1, "prc":7, "fok":5}' -H "Content-Type: application/json" && echo
echo 'Should have returned error'
curl localhost:3000/buy --data '{"qty":1, "prc":7, "alo":"dd"}' -H "Content-Type: application/json" && echo
echo 'Should have returned error'
