import sys
import os

sys.path.insert(0, '.')

import sqlite3
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM users LIMIT 1;")
try:
    result = cursor.fetchall()
    print('用户数据:', result)
except Exception as e:
    print('查询用户表失败:', e)

cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print('数据库中的表:', tables)

cursor.execute("PRAGMA table_info(users);")
columns = cursor.fetchall()
print('users表结构:', columns)

conn.close()