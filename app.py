from flask import Flask, jsonify, request

app = Flask(__name__)

# A server restart wipes the order book, TODO add a db to persist
buys = [ { "qty":10, "prc":9.5 }, { "qty":10, "prc":7 } ]
sells = [ { "qty":10, "prc":13 },  { "qty":10, "prc":15 } ]

@app.route('/book', methods=['GET'])
def get_book():
    return jsonify({'buys': buys, 'sells': sells})

# refactored to be useful for both buy and sell side
#  order: e.g. {"qty":10, "prc":12}
#  match_book: orders against; attempt to match against these
#  add_book: orders on same side; add leftover liquidity here
#  comp: (prc) -> bool; takes price of potential match and returns true if given order matches
def process_order(order, match_book, add_book, comp):
    add_book.append(order)
    return jsonify({'result': 'success'})

@app.route('/buy', methods=['POST'])
def buy():
    return process_order(request.json, sells, buys, lambda prc: prc <= request.json.prc)

@app.route('/sell', methods=['POST'])
def sell():
    return process_order(request.json, buys, sells, lambda prc: prc >= request.json.prc)

if __name__ == '__main__':
    app.run(debug=True)
