from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# A server restart wipes the order book, TODO add a db to persist
# Both arrays are maintained in sorted order with most attractive bid/offers first
buys = []
sells = []

@app.route('/book', methods=['GET'])
def get_book():
    return jsonify({'buys': buys, 'sells': sells})

@app.route('/buy', methods=['POST'])
def buy():
    return process_order(sells, buys, lambda prc1, prc2: prc1 > prc2)

@app.route('/sell', methods=['POST'])
def sell():
    return process_order(buys, sells, lambda prc1, prc2: prc1 < prc2)

# refactored to be easily usable for both buy and sell side
#  match_book: orders against; attempt to match against these
#  add_book: orders on same side; add leftover liquidity here
#  comp: (prc1, prc2) -> bool; returns true if prc1 is better than prc2
#          when buying, higher is better; when selling, lower is better
# RETURNS: a JSON string of fills
def process_order(match_book, add_book, comp):
    (qty, prc) = process_args()

    # (order) -> bool; returns true if new order is more attractively priced than given arg
    better = lambda offer: comp(prc, offer['prc'])
    # (order) -> bool; matching consideration is same as better except equality also matches
    matches = lambda offer: better(offer) or prc == offer['prc']

    fills = []

    # match from the front of the book onwards, until price no longer crosses
    # continually examining the first element of match_book, fills are deleted from front as we iterate
    while qty > 0 and len(match_book) > 0:
        match = match_book[0]
        if not matches(match):
            break # match_book[1:] cannot match if match_book[0] doesn't, b/c match_book is ordered, best-first

        if match['qty'] <= qty: # top of book is exhausted
            fills.append(match)
            qty -= match['qty']
            del match_book[0]
        else: # top of book has remaining liquidity, new order is exhausted
            fills.append({'qty': qty, 'prc': match['prc']})
            match['qty'] -= qty
            qty = 0

    # if there is liquidity remaining, find the right spot to insert to the book
    if qty > 0:
        # there should be a more pythonic way to do this search / insert
        idx = 0
        while idx < len(add_book):
            if better(add_book[idx]):
                break
            idx += 1
        add_book.insert(idx, {'qty': qty, 'prc': prc})

    return jsonify({ 'fills': fills })

# validate args from global request object, return (qty, price) tuple
# TODO return a JSON style error object?
def process_args():
    if 'qty' not in request.json or 'prc' not in request.json:
        abort(400)

    qty = request.json['qty']
    prc = request.json['prc']

    if type(qty) is not int:
        abort(400)
    if type(prc) is not int and type(prc) is not float:
        abort(400)
    if qty <= 0 or prc <= 0:
        abort(400)

    return (qty, prc)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
