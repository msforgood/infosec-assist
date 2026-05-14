SOURCE_CODE = {
    1: {
        "title": "Login Bypass - Basic",
        "desc": "SQL Injection을 이용하여 admin 계정으로 로그인하세요.",
        "hint": "입력값이 쿼리에 직접 삽입됩니다.",
        "code": """# 취약한 코드
username = request.form.get("username", "")
password = request.form.get("password", "")
conn = get_challenge_db(1)
cur = conn.cursor()
query_str = (
    f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
)
try:
    cur.execute(
        f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    )
    user = cur.fetchone()
    if user and user["username"] == "admin":
        flag = get_flag(1)
        result = {
            "success": True,
            "message": f"Correct! : {flag}",
        }
    elif user:
        result = {
            "success": False,
            "message": f"{user['username']}(으)로 로그인됨. admin으로 로그인하세요.",
        }
    else:
        result = {"success": False, "message": "로그인 실패"}""",
    },
    2: {
        "title": "Login Bypass - OR Filter",
        "desc": "or, OR 키워드가 필터링되어 있습니다. 우회하여 admin으로 로그인하세요.",
        "hint": "OR의 다른 표기법에 대해 알아보세요.",
        "code": """# 필터링 코드
username = request.form.get("username", "")
password = request.form.get("password", "")
# Filter: or, OR
if re.search(r"\bor\b", username, re.IGNORECASE) or re.search(
    r"\bor\b", password, re.IGNORECASE
):
    result = {"success": False, "message": "No Hack"}
    return render_template(
        "sqli_login.html",
        ch=SOURCE_CODE[2],
        num=2,
        result=result,
        query=None,
        challenge_id=2,
    )
conn = get_challenge_db(2)
cur = conn.cursor()
query_str = (
    f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
)
try:
    cur.execute(
        f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    )
    user = cur.fetchone()
    if user and user["username"] == "admin":
        flag = get_flag(2)
        result = {
            "success": True,
            "message": f"Correct! : {flag}",
        }
    elif user:
        result = {
            "success": False,
            "message": f"{user['username']}(으)로 로그인됨. admin으로 로그인하세요.",
        }
    else:
        result = {"success": False, "message": "로그인 실패"}""",
    },
    3: {
        "title": "Login Bypass - OR/|| Filter",
        "desc": "or, OR, ||가 모두 필터링되어 있습니다. 우회하여 admin으로 로그인하세요.",
        "hint": "주석을 활용한 로그인 우회도 가능합니다.",
        "code": """# 필터링 코드
username = request.form.get("username", "")
password = request.form.get("password", "")
if re.search(r"\bor\b", username, re.IGNORECASE) or "||" in username:
    result = {"success": False, "message": "No Hack"}
    return render_template(
        "sqli_login.html",
        ch=SOURCE_CODE[3],
        num=3,
        result=result,
        query=None,
        challenge_id=3,
    )
if re.search(r"\bor\b", password, re.IGNORECASE) or "||" in password:
    result = {"success": False, "message": "No Hack"}
    return render_template(
        "sqli_login.html",
        ch=SOURCE_CODE[3],
        num=3,
        result=result,
        query=None,
        challenge_id=3,
    )
conn = get_challenge_db(3)
cur = conn.cursor()
query_str = (
    f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
)
try:
    cur.execute(
        f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    )
    user = cur.fetchone()
    if user and user["username"] == "admin":
        flag = get_flag(3)
        result = {
            "success": True,
            "message": f"Correct! : {flag}",
        }
    elif user:
        result = {
            "success": False,
            "message": f"{user['username']}(으)로 로그인됨. admin으로 로그인하세요.",
        }
    else:
        result = {"success": False, "message": "로그인 실패"}
except Exception as e:
    result = {"success": False, "message": f"쿼리 에러: {e}"}
conn.close()""",
    },
    4: {
        "title": "Login Bypass - Space Filter",
        "desc": "공백(space)이 필터링되어 있습니다. 우회하여 admin으로 로그인하세요.",
        "hint": "MySQL에서 공백 대신 사용할 수 있는 것은?",
        "code": """# 필터링 코드
if request.method == "POST":
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    blocked = False
    for val in [username, password]:
        if " " in val or "#" in val or "--" in val:
            blocked = True

    if blocked:
        result = {"success": False, "message": "No Hack"}
        return render_template(
            "sqli_login.html",
            ch=SOURCE_CODE[4],
            num=4,
            result=result,
            query=None,
            challenge_id=4,
        )
    conn = get_challenge_db(4)
    cur = conn.cursor()
    query_str = (
        f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    )
    try:
        cur.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        )
        user = cur.fetchone()
        if user and user["username"] == "admin":
            flag = get_flag(4)
            result = {
                "success": True,
                "message": f"Correct! : {flag}",
            }
        elif user:
            result = {
                "success": False,
                "message": f"{user['username']}(으)로 로그인됨. admin으로 로그인하세요.",
            }
        else:
            result = {"success": False, "message": "로그인 실패"}""",
    },
    5: {
        "title": "Login Bypass - Comment Filter",
        "desc": "한줄 주석이 필터링되어 있습니다. 다른 방법으로 우회하세요.",
        "hint": "여러 줄 주석(/**/)도 사용 가능합니다.",
        "code": """# 필터링 코드
username = request.form.get("username", "")
password = request.form.get("password", "")

import re

blocked = False
for val in [username, password]:
    if re.search(r"\bor\b", val, re.IGNORECASE):
        blocked = True

    if "||" in val or "#" in val:
        blocked = True

if blocked:
    result = {"success": False, "message": "No Hack"}
    return render_template(
        "sqli_login.html",
        ch=SOURCE_CODE[5],
        num=5,
        result=result,
        query=None,
        challenge_id=5,
    )

conn = get_challenge_db(5)
cur = conn.cursor()
query_str = (
    f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
)
try:
    cur.execute(
        f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    )
    user = cur.fetchone()
    if user and user["username"] == "admin":
        flag = get_flag(4)
        result = {
            "success": True,
            "message": f"Correct! : {flag}",
        }
    elif user:
        result = {
            "success": False,
            "message": f"{user['username']}(으)로 로그인됨. admin으로 로그인하세요.",
        }
    else:
        result = {"success": False, "message": "로그인 실패"}
except Exception as e:
    result = {"success": False, "message": f"쿼리 에러: {e}"}
conn.close()""",
    },
    6: {
        "title": "Board - UNION Data Extraction",
        "desc": "게시판에서 UNION SELECT를 이용하여 secret 테이블의 flag를 추출하세요.",
        "hint": "UNION SELECT를 사용할 때는 컬럼 수를 맞춰야 합니다.",
        "code": """# 취약한 코드
results = []
query_str = None
keyword = ""
conn = get_challenge_db(6)
cur = conn.cursor()
if request.method == "POST":
    keyword = request.form.get("keyword", "")
    query_str = f"SELECT id, title, content, author FROM posts WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
    try:
        cur.execute(
            f"SELECT id, title, content, author FROM posts WHERE title LIKE '%{keyword}%' OR content LIKE '%{keyword}%'"
        )
        results = cur.fetchall()
    except Exception as e:
        results = [{"id": "-", "title": "Error", "content": str(e), "author": "-"}]
else:
    cur.execute("SELECT id, title, content, author FROM posts")
    results = cur.fetchall()
conn.close()""",
    },
    7: {
        "title": "Board - Boolean Blind SQLi",
        "desc": "Boolean-based Blind SQL Injection으로 secret 테이블의 flag를 한 글자씩 추출하세요.",
        "hint": "ASCII 코드를 활용하세요. 결과의 유무로 참/거짓을 판별합니다.",
        "code": """# 취약한 코드
post_id = request.form.get("post_id", "")
query_str = f"SELECT id, title, content, author FROM posts WHERE id={post_id}"
try:
    cur.execute(
        f"SELECT id, title, content, author FROM posts WHERE id={post_id}"
    )
    row = cur.fetchone()
    if row:
        result = {"exists": True, "post": row}
    else:
        result = {"exists": False}
except Exception as e:
    result = {"exists": False, "error": str(e)}""",
    },
    8: {
        "title": "Board - Error Based SQLi",
        "desc": "Error-based SQL Injection을 이용하여 secret 테이블의 flag를 추출하세요.",
        "hint": "extractvalue() 또는 updatexml() 함수를 활용하세요.",
        "code": """# 취약한 코드 (에러 메시지가 노출됨)
        result = None
        query_str = None
        post_id = ""
        conn = get_challenge_db(8)
        cur = conn.cursor()
        cur.execute("SELECT id, title, author FROM posts")
        posts = cur.fetchall()
        if request.method == "POST":
            post_id = request.form.get("post_id", "")
            query_str = f"SELECT id, title, content, author FROM posts WHERE id={post_id}"
            try:
                cur.execute(
                    f"SELECT id, title, content, author FROM posts WHERE id={post_id}"
                )
                row = cur.fetchone()
                if row:
                    result = {"success": True, "post": row}
                else:
                    result = {
                        "success": True,
                        "post": None,
                        "message": "게시글이 없습니다.",
                    }
            except Exception as e:
                result = {"success": False, "error": str(e)}
        conn.close()""",
    },
}
