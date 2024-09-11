# trade.py
from flask import Blueprint, render_template, request, jsonify, current_app, g
import pymysql

trade_blueprint = Blueprint('trade', __name__)

# 声明当前成交价格（Last Traded Price）
LAST_TRADED_PRICE = 56746.00

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="tpc12351744",
    database="Trading_System"
)

@trade_blueprint.route('/')
def index():
    return render_template('trade.html')

@trade_blueprint.route('/api/buy-orders', methods=['GET'])
def get_buy_orders():
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT price, amount FROM buy_orders ORDER BY price DESC LIMIT 10")
    buy_orders = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "total": row[0]*row[1]} for row in buy_orders])


@trade_blueprint.route('/api/sell-orders', methods=['GET'])
def get_sell_orders():
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT price, amount FROM (SELECT price, amount FROM sell_orders ORDER BY price ASC LIMIT 10)AS subquery ORDER BY price DESC")
    sell_orders = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "total": row[0]*row[1]} for row in sell_orders])


@trade_blueprint.route('/api/odd', methods=['GET'])
def get_odd():
    data = [{"odd": LAST_TRADED_PRICE}]
    return jsonify(data)


@trade_blueprint.route('/api/trade-history', methods=['GET'])
def get_trade_history():
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT price, amount, DATE_FORMAT(created_at, '%H:%i:%s') as time, type FROM trade_history ORDER BY created_at DESC LIMIT 20")
    trade_history = cursor.fetchall()
    return jsonify([{"price": row[0], "amount": row[1], "time": row[2], "type": row[3]} for row in trade_history])


@trade_blueprint.route('/api/trade', methods=['POST'])
def submit_trade():
    # 获取数据库连接
    mycursor = mydb.cursor()

    # 从请求中获取输入框的数据
    data = request.json
    price = float(data.get('price'))
    amount = float(data.get('amount'))
    trade_type = data.get('type')

    if trade_type == "buy":
        if price < LAST_TRADED_PRICE:
            # 检查 buy_orders 表中是否有对应价格表项
            mycursor.execute("SELECT * FROM buy_orders WHERE price = %s", (price,))
            existing_order = mycursor.fetchone()
            if existing_order:
                # 更新 amount 值
                new_amount = existing_order[2] + amount  # existing_order[2] 假设是 amount 列
                mycursor.execute("UPDATE buy_orders SET amount = %s WHERE price = %s", (new_amount, price))
            else:
                # 插入新的订单到 buy_orders 表
                sql = "INSERT INTO buy_orders (price, amount) VALUES (%s, %s)"
                mycursor.execute(sql, (price, amount))
            mydb.commit()
            return jsonify({"status": "success", "message": "Buy order processed."})

        elif price >= LAST_TRADED_PRICE:
            # 以盘点值结算到市场交易数据 trade_history 中
            sql = "INSERT INTO trade_history (price, amount, type) VALUES (%s, %s, %s)"
            mycursor.execute(sql, (LAST_TRADED_PRICE, amount, 'buy'))
            mydb.commit()
            return jsonify({"status": "success", "message": "Trade executed at LAST_TRADED_PRICE.", "price": LAST_TRADED_PRICE, "amount": amount})

    elif trade_type == "sell":
        if price > LAST_TRADED_PRICE:
            # 检查 sell_orders 表中是否有对应价格表项
            mycursor.execute("SELECT * FROM sell_orders WHERE price = %s", (price,))
            existing_order = mycursor.fetchone()
            if existing_order:
                # 更新 amount 值
                new_amount = existing_order[2] + amount  # existing_order[2] 假设是 amount 列
                mycursor.execute("UPDATE sell_orders SET amount = %s WHERE price = %s", (new_amount, price))
            else:
                # 插入新的订单到 sell_orders 表
                sql = "INSERT INTO sell_orders (price, amount) VALUES (%s, %s)"
                mycursor.execute(sql, (price, amount))
            mydb.commit()
            return jsonify({"status": "success", "message": "Sell order processed."})

        elif price <= LAST_TRADED_PRICE:
            # 以盘点值结算到市场交易数据 trade_history 中
            sql = "INSERT INTO trade_history (price, amount, type) VALUES (%s, %s, %s)"
            mycursor.execute(sql, (LAST_TRADED_PRICE, amount, 'sell'))
            mydb.commit()
            return jsonify({"status": "success", "message": "Trade executed at LAST_TRADED_PRICE.", "price": LAST_TRADED_PRICE, "amount": amount})

    return jsonify({"status": "error", "message": "Invalid trade type or conditions."})
