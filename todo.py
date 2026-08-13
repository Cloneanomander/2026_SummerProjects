# ToDoリストのタスクを保存するための空のリスト
# これから、このリストにタスクを追加していきます
tasks = []

print("===== ToDoリストアプリ =====")

# ユーザーが「4」を入力するまで、このループがずっと続きます
try:
    with open('tasks.txt', 'r', encoding='utf-8') as f:
        for line in f:
            tasks.append(line.strip())
except FileNotFoundError:
    print("タスクファイルが見つかりませんでした。新しいファイルを作成します。")
while True:
    # ユーザーに何をしたいか尋ねるメニュー
    print("\n何をしますか？")
    print("1: タスクを追加する")
    print("2: タスクを一覧表示する")
    print("3: タスクを削除する")
    print("4: タスクを更新する")
    print("5: アプリを終了する")

    # ユーザーからのキーボード入力を受け取る
    choice = input("番号（1-5）を入力してください: ")

    # ---- 入力された番号に応じて、処理を分ける ----

    if choice == '1':
        # ユーザーに追加したいタスクを入力してもらう
        new_task = input("追加するタスクを入力してください: ")
        #入力されたタスクをtaskリストに追加する
        tasks.append(new_task)
        print(f"タスク「{new_task}」を追加しました。")

    elif choice == '2':
        # 追加されたタスクを一覧表示する
        if len(tasks) == 0:
            print("現在、タスクはありません。")
        else:
            print("現在のタスク一覧です。")
            for task in tasks:
                print(task)



        

    elif choice == '3':
        
        if tasks:
            for index, task in enumerate(tasks):
                #人間には1から始まる方が分かりやすいので、index + 1
                print(f"{index + 1}: {task}")
            try:
                delete_number = int(input("削除する番号を入力してください："))
                if 1 <= delete_number <= len(tasks):
                    deleted_task = tasks.pop(delete_number - 1)
                    print(f"{deleted_task} を削除しました。")
                else:
                    print("エラー：その番号のタスクはありません。")
            except ValueError:
                print("エラー：半角数字で入力してください。")
        else:
            print("削除するタスクがありません。")
    elif choice == '4':
        if tasks:
            for index, task in enumerate(tasks):
                print(f"{index + 1}: {task}")
            try:
                edit_number = int(input("編集するタスクの番号を入力してください。"))
                if 1 <= edit_number <= len(tasks):
                    new_task = input("新しいタスクを入力してください")
                else:
                    print("エラー：その番号のタスクはありません。")
                tasks[edit_number - 1] = new_task
                print(f"番号{edit_number}のタスクを更新しました。")
            except ValueError:
                print("エラー：半角数字で入力してください。")    
    elif choice == '5':
        with open('tasks.txt', 'w', encoding='utf-8') as f:
            for task in tasks:
                f.write(task + '\n')
        print("ファイルを保存しました。アプリを終了します。")
        break  # この `break` で while ループを強制的に終了させます

    else:
        # 1, 2, 3, 4 以外が入力された場合
        print("エラー：1から4の正しい番号を入力してください。")