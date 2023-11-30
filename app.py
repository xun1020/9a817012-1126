from lib import read_credentials, authenticate, create_database, read_data_and_insert, display_menu, display_records

# 讀取帳密檔
credentials = read_credentials('pass.json')

# 使用者身份驗證
while True:
    input_username = input("請輸入帳號： ")
    input_password = input("請輸入密碼： ")

    if authenticate(input_username, input_password, credentials):
        break
    else:
        print("=>帳密錯誤，程式結束")
        exit()

conn, cursor = create_database()


try:
    while True:
        display_menu()
        choice = input("請輸入您的選擇 [0-7]: ")

        if choice == '1':
            if conn and cursor:
                print("=>資料庫已建立")
            else:
                print("=>建立資料庫失敗")

        elif choice == '2':
            if cursor:
                read_data_and_insert('members.txt', cursor)
            else:
                print("=>請先建立資料庫")

        elif choice == '3':
            cursor.execute('SELECT COUNT(*) FROM members')
            record_count = cursor.fetchone()[0]

            if record_count == 0:
                print("=>查無資料")
            else:
                display_records(cursor)

        elif choice == '4':
            name = input("請輸入姓名: ")
            sex = input("請輸入性別: ")
            phone = input("請輸入手機號碼: ")

            cursor.execute('''
                INSERT INTO members (mname, msex, mphone) VALUES (?, ?, ?)
            ''', (name, sex, phone))

            conn.commit()
            print("=>異動 1 筆記錄")

        elif choice == '5':
            name_to_update = input("請輸入想修改記錄的姓名: ")
            if not name_to_update:
                print("=>必須指定姓名才可修改記錄")
                continue

            new_sex = input("請輸入要改變的性別: ")
            new_phone = input("請輸入要改變的手機號碼: ")

            # 取得原資料
            cursor.execute('SELECT * FROM members WHERE mname=?', (name_to_update,))
            original_record = cursor.fetchone()

            if original_record:
                print("\n原資料：")
                print(f"姓名：{original_record[1]}，性別：{original_record[2]}，手機：{original_record[3]}")

                # 更新資料
                cursor.execute('''
                    UPDATE members SET msex=?, mphone=? WHERE mname=?
                ''', (new_sex, new_phone, name_to_update))

                conn.commit()
                print("=>異動 1 筆記錄")

                # 顯示修改後的資料
                cursor.execute('SELECT * FROM members WHERE mname=?', (name_to_update,))
                updated_record = cursor.fetchone()

                if updated_record:
                    print("\n修改後資料：")
                    print(f"姓名：{updated_record[1]}，性別：{updated_record[2]}，手機：{updated_record[3]}")
                else:
                    print("=>查無修改後的資料")
            else:
                print("=>查無原始資料")

        elif choice == '6':
            phone_to_query = input("請輸入想查詢記錄的手機: ")
            cursor.execute('SELECT * FROM members WHERE mphone=?', (phone_to_query,))
            records = cursor.fetchall()

            if not records:
                print("=>查無資料")
            else:
                print("\n姓名         性別      手機")
                print("----------------------------")
                for record in records:
                    print(f"{record[1]:<12} {record[2]:<8} {record[3]}")

        elif choice == '7':
            cursor.execute('DELETE FROM members')
            conn.commit()
            print(f"=>異動 {cursor.rowcount} 筆記錄")

        elif choice == '0':
            break

        else:
            print("=>無效的選擇")

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()
