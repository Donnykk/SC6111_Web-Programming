from flask import Flask, g, render_template, request, jsonify, g
from decimal import Decimal
import pymysql

app = Flask(__name__)

LAST_TRADED_PRICE = 57193.01

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="tpc12351744",
    database="Trading_System"
)
cursor = mydb.cursor()


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/buy-orders', methods=['GET'])
def get_buy_orders():
    cursor.execute(
        "SELECT price, amount FROM buy_orders ORDER BY price DESC LIMIT 10")
    buy_orders = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "total": row[0]*row[1]} for row in buy_orders])


@app.route('/api/sell-orders', methods=['GET'])
def get_sell_orders():
    cursor.execute(
        "SELECT price, amount FROM (SELECT price, amount FROM sell_orders ORDER BY price ASC LIMIT 10)AS subquery ORDER BY price DESC")
    sell_orders = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "total": row[0]*row[1]} for row in sell_orders])


@app.route('/api/odd', methods=['GET'])
def get_odd():
    data = [{"odd": LAST_TRADED_PRICE}]
    return jsonify(data)


@app.route('/api/trade-history', methods=['GET'])
def get_trade_history():
    cursor.execute(
        "SELECT price, amount, DATE_FORMAT(created_at, '%H:%i:%s') as time, type FROM trade_history ORDER BY created_at DESC LIMIT 10")
    trade_history = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "time": row[2], "type": row[3]} for row in trade_history])


@app.route('/api/trade', methods=['POST'])
def submit_trade():
    # 从请求中获取输入框的数据
    data = request.json
    price = float(data.get('price'))
    amount = Decimal(data.get('amount'))
    trade_type = data.get('type')

    if trade_type == "buy":
        if price < LAST_TRADED_PRICE:
            # 检查 buy_orders 表中是否有对应价格表项
            cursor.execute(
                "SELECT * FROM buy_orders WHERE price = %s", (price,))
            existing_order = cursor.fetchone()
            if existing_order:
                # 更新 amount 值
                # existing_order[2] 假设是 amount 列
                new_amount = existing_order[2] + amount
                cursor.execute(
                    "UPDATE buy_orders SET amount = %s WHERE price = %s", (new_amount, price))
            else:
                # 插入新的订单到 buy_orders 表
                sql = "INSERT INTO buy_orders (price, amount) VALUES (%s, %s)"
                cursor.execute(sql, (price, amount))
            mydb.commit()
            return jsonify({"status": "success", "message": "Buy order processed."})

        elif price >= LAST_TRADED_PRICE:
            # 以盘点值结算到市场交易数据 trade_history 中
            sql = "INSERT INTO trade_history (price, amount, type) VALUES (%s, %s, %s)"
            cursor.execute(sql, (LAST_TRADED_PRICE, amount, 'buy'))
            mydb.commit()
            return jsonify({"status": "success", "message": "Trade executed at LAST_TRADED_PRICE.", "price": LAST_TRADED_PRICE, "amount": amount})

    elif trade_type == "sell":
        if price > LAST_TRADED_PRICE:
            # 检查 sell_orders 表中是否有对应价格表项
            cursor.execute(
                "SELECT * FROM sell_orders WHERE price = %s", (price,))
            existing_order = cursor.fetchone()
            if existing_order:
                # 更新 amount 值
                # existing_order[2] 假设是 amount 列
                new_amount = existing_order[2] + amount
                cursor.execute(
                    "UPDATE sell_orders SET amount = %s WHERE price = %s", (new_amount, price))
            else:
                # 插入新的订单到 sell_orders 表
                sql = "INSERT INTO sell_orders (price, amount) VALUES (%s, %s)"
                cursor.execute(sql, (price, amount))
            mydb.commit()
            return jsonify({"status": "success", "message": "Sell order processed."})

        elif price <= LAST_TRADED_PRICE:
            # 以盘点值结算到市场交易数据 trade_history 中
            sql = "INSERT INTO trade_history (price, amount, type) VALUES (%s, %s, %s)"
            cursor.execute(sql, (LAST_TRADED_PRICE, amount, 'sell'))
            mydb.commit()
            return jsonify({"status": "success", "message": "Trade executed at LAST_TRADED_PRICE.", "price": LAST_TRADED_PRICE, "amount": amount})

    return jsonify({"status": "error", "message": "Invalid trade type or conditions."})


if __name__ == '__main__':
    app.run(debug=True)
