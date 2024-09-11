# main.py
from flask import Flask, g
from trade import trade_blueprint
import mysql.connector

app = Flask(__name__)

# 配置数据库连接信息
app.config['DB_HOST'] = "localhost"
app.config['DB_USER'] = "root"
app.config['DB_PASSWORD'] = "tpc12351744"
app.config['DB_NAME'] = "Trade_System"
app.config['DB_PORT'] = 3306
app.config['DB_CHARSET'] = 'utf8mb4'
app.config['DB_COLLATION'] = 'utf8mb4_general_ci'

def get_db():
    if 'db' not in g:
        # 连接数据库
        g.db = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'],
            port=app.config['DB_PORT'],
            charset=app.config['DB_CHARSET'],  # 设置字符集
            collation=app.config['DB_COLLATION']  # 设置排序规则
        )
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 注册 trade 蓝图
app.register_blueprint(trade_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
