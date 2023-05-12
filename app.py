from flask import Flask, request, jsonify,render_template, redirect, flash
from _Connection import start, disconnect
import _vars as v
import time
import requests
from IB_BuySell import TradeHandler
from db_manager import PackageDB

global orderCashSize
orderCashSize = v.CASH

"""
1. Start the app
2. Call ngrok tunnel
   ngrok http -hostname=datathread.ngrok.io 5000
"""
def start_check(app):
    if not app.isConnected():
        # START
        starting()
        # requests.get("http://127.0.0.1:5000/start")
        # POSITIONS
        # ORDERS
        # ACCOUNT
        app.reqAccountUpdates(True, app.account_number)

ticker, time_frame, atr_away,days_to_expire = "SPY",'1m', 0.5, 0

PackageDB(ticker,days_to_expire,ATRAWAY=atr_away).update_range()
# print(">"*50)
# ticker = input("default SPY >> Enter a ticker: ") or "SPY"
# time_frame = input("default 1m >> Enter a time frame: ") or '1m'
# atr_away = float(input("default 1 >> Expected xATR: ") or 1)
# days_to_expire = int(input("default 0 >> Enter days to expire: ") or 0)
# print(">"*50)
app = TradeHandler(ticker=ticker,time_frame=time_frame,ATRAWAY=atr_away,days_to_expire=days_to_expire,)

tradeApp = Flask(__name__)

@tradeApp.route("/", methods=['GET', 'POST'])
def index():
    if not app.isConnected():
        # requests.get("http://127.0.0.1:5000/start")
        starting()
    direction, side = None, None
    if request.method == 'POST':
        # BUY CALL
        if request.form.get('bc'):
            direction, side = request.form.get('bc').split(" ")
        # BUY PUT
        elif  request.form.get('bp'):
            direction, side = request.form.get('bp').split(" ")
        # SELL CALL
        elif  request.form.get('sc'):
            direction, side = request.form.get('sc').split(" ")
        # SELL PUT
        elif  request.form.get('sp'):
            direction, side = request.form.get('sp').split(" ")
        
        # Close OPEN ORDERS
        elif  request.form.get('openOrders'):
            if request.form.get('openOrders')=='Close Open Orders':
                # requests.get("http://localhost:5000/globalOrderCancel")
                global_cancel_order()
        elif request.form.get("openPositions"):
            flash("Close Open positions!")
            app.close_all()
            return redirect(request.url)
        elif request.form.get('restart'):
            if app.isConnected():
                app.unsubscribe()
                time.sleep(0.1)
                disconnect(app)
            time.sleep(1)
            start(app,v.HOST,v.PORT,clientId=10)
            time.sleep(0.2)
            # requests.get("http://localhost:5000/globalOrderCancel")
            global_cancel_order()
        else:
            print("!!!!!!!!!!Illegal Entry!!!!!!!!!!!")
        if direction and side:
            
            side = side[0]
            print("="*100)
            print(f'Direction: {direction} Side: {side}')
            print("="*100)
            placed_order = app.place_options_order(unit=orderCashSize, signal=direction.upper(), side=side.upper(), orderAdj=True)
            print(placed_order)
            flash(f"Response: {placed_order}")
            return redirect(request.url)
            
    elif request.method == 'GET':
        return render_template('index.html')
    
    # print(f"Direction {direction} Side {side[0]}")
    
    return redirect(request.url)

@tradeApp.route("/start", methods = ['GET'])
def starting():
    start(app,v.HOST,v.PORT,clientId=10)
    time.sleep(0.1)
    if app.isConnected():
        return jsonify("Starting App...")
    else:
        return jsonify("Error Starting the App")

@tradeApp.route("/globalOrderCancel",methods=['GET'])
def global_cancel_order():
    if not app.isConnected():
        starting()
    app.reqGlobalCancel()
    return jsonify(f"Message : <<Orders Cancelled>> request placed!")

@tradeApp.route("/stop", methods = ['GET'])
def stoping():
    disconnect(app)
    return jsonify("Stopping App...")

@tradeApp.route("/buycall", methods = ['GET'])
def buy_call_option():
    app.place_options_order("BUY","c",orderAdj=True)
    
    return jsonify("BUY CALL >> ORDER PLACED")

@tradeApp.route("/sellcall", methods = ['GET'])
def sell_call_option():
    app.place_options_order("SELL","c",orderAdj=True)
    return jsonify("SELL CALL >> ORDER PLACED")


@tradeApp.route("/buyput", methods = ['GET'])
def buy_put_option():
    app.place_options_order("BUY","p",orderAdj=True)
    
    return jsonify("BUY PUT >> ORDER PLACED")

@tradeApp.route("/sellput", methods = ['GET'])
def sell_put_option():
    app.place_options_order("SELL","p",orderAdj=True)
    return jsonify("SELL PUT >> ORDER PLACED")


if __name__ == "__main__":
    tradeApp.secret_key = 'super secret key'
    tradeApp.config['SESSION_TYPE'] = 'filesystem'
    tradeApp.run(host='0.0.0.0',port=5001, debug= 'on')
    