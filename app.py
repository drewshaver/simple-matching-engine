from flask import Flask, jsonify, request

app = Flask(__name__)

# A server restart wipes the order book, TODO add a db to persist
# Both arrays are maintained in sorted order with most attractive offers first
buys = []
sells = []

@app.route('/book', methods=['GET'])
def get_book():
    return jsonify({'buys': buys, 'sells': sells})

# refactored to be easily usable for both buy and sell side
#  order: e.g. {"qty":10, "prc":12} NOTE this object gets modified in process
#  match_book: orders against; attempt to match against these
#  add_book: orders on same side; add leftover liquidity here
#  matches: (order) -> bool; takes potential match and returns true if orders cross
#  better: (order) -> bool; takes competing order and returns true if new order is better
#    ** matches could be used twice, instead of having a second function better, but then it is awkward to preserve ordering
#    ** this way, whoever submits order first has book priority if two prices are the same
# RETURNS: a JSON string of fills
def process_order(order, match_book, add_book, matches, better):
    fills = []

    # match from the front of the book onwards, until price no longer crosses
    # always examining the first element of match_book, fills are deleted from front as we iterate
    while order['qty'] > 0 and len(match_book) > 0:
        match = match_book[0]
        if not matches(match):
            break # match_book[1:] cannot match if match_book[0] doesn't, b/c [0] is the best offer

        if match['qty'] <= order['qty']: # top of book is full match
            fills.append(match)
            order['qty'] -= match['qty']
            del match_book[0]
        else: # top of book has remaining liquidity
            fills.append({ 'qty': order['qty'], 'prc': match['prc'] })
            match['qty'] -= order['qty']
            order['qty'] = 0

    # if there is liquidity remaining, find the right spot to insert to the book
    if order['qty'] > 0:
        # there should be a more pythonic way to do this search
        idx = 0
        while idx < len(add_book):
            if better(add_book[idx]):
                break
            idx += 1
        add_book.insert(idx, order)

    return jsonify({ 'fills': fills })


# TODO input values are not validated at all!

@app.route('/buy', methods=['POST'])
def buy():
    prc = request.json['prc']
    return process_order(request.json, sells, buys, lambda order: prc >= order['prc'], lambda order: prc > order['prc'])

@app.route('/sell', methods=['POST'])
def sell():
    prc = request.json['prc']
    return process_order(request.json, buys, sells, lambda order: prc <= order['prc'], lambda order: prc < order['prc'])

if __name__ == '__main__':
    app.run(debug=True, port=3000)
