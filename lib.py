import sqlite3
import json


def read_credentials(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as pass_file:
            pass_data = json.load(pass_file)

        # 確保密碼被視為字串
        for user_data in pass_data:
            user_data['密碼'] = str(user_data['密碼'])

        return pass_data
    except Exception as e:
        print(f"Error reading credentials file: {e}")
        return None


def authenticate(username: str, password: str, credentials: dict) -> bool:
    if credentials:
        for user_data in credentials:
            stored_username = user_data['帳號']
            stored_password = user_data['密碼']

            # 去除空白字元
            username = username.strip()
            password = password.strip()

            # 直接比較帳號和密碼
            if stored_username == username and stored_password == password:
                return True

    return False


def create_database() -> tuple:
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                mname TEXT NOT NULL,
                msex TEXT NOT NULL,
                mphone TEXT NOT NULL
            )
        ''')
        conn.commit()

        return conn, cursor  # 直接返回 conn 和 cursor，而不是一個 tuple
    except Exception as e:
        print(f"Error creating database: {e}")
        return None, None


def close_database(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except Exception as e:
        print(f"Error closing database: {e}")


def read_data_and_insert(file_path: str, cursor: sqlite3.Cursor) -> None:
    try:
        with open(file_path, 'r', encoding='utf-8') as data_file:
            lines = data_file.readlines()
            for line in lines:
                data = line.strip().split(',')
                cursor.execute('''
                    INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)
                ''', (data[0], data[1], data[2]))
        print(f"=>異動 {len(lines)} 筆記錄")
    except Exception as e:
        print(f"Error reading data file or inserting into database: {e}")


def display_menu() -> None:
    print("\n---------- 選單 ----------")
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("--------------------------")


def display_records(cursor: sqlite3.Cursor) -> None:
    try:
        cursor.execute('SELECT * FROM members')
        records = cursor.fetchall()

        print("\n姓名         性別      手機")
        print("----------------------------")
        for record in records:
            print("{:<10}{:>2}{:>15}".format(record[1], record[2], record[3]))
    except Exception as e:
        print(f"Error displaying records: {e}")


def modify_record(conn, cursor, name, new_sex, new_phone):
    try:
        cursor.execute("SELECT * FROM members WHERE mname = ?", (name,))
        record_before = cursor.fetchone()

        if not record_before:
            print(f"=>找不到姓名為 {name} 的記錄")
            return

        print("\n原資料：")
        print(f"姓名：{record_before[1]}，性別：{record_before[2]}，手機：{record_before[3]}")

        cursor.execute("UPDATE members SET msex=?, mphone=? WHERE mname=?", (new_sex, new_phone, name))
        conn.commit()
        print("=>異動 1 筆記錄")

        cursor.execute("SELECT * FROM members WHERE mname = ?", (name,))
        record_after = cursor.fetchone()

        print("\n修改後資料：")
        print(f"姓名：{record_after[1]}，性別：{record_after[2]}，手機：{record_after[3]}")

    except Exception as e:
        print(f"Error modifying record: {e}")


def query_phone(cursor: sqlite3.Cursor, phone: str) -> None:
    try:
        phone = phone.strip()
        cursor.execute('SELECT * FROM members WHERE phone = ?', (phone,))
        records = cursor.fetchall()

        if records:
            print("\n姓名         性別      手機")
            print("----------------------------")
            for record in records:
                print(f"{record[1]:<12} {record[2]:<8} {record[3]}")
        else:
            print("查無資料")
    except Exception as e:
        print(f"Error querying records: {e}")
