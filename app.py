from flask import Flask, render_template_string, request, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time

app = Flask(__name__)

HTML = """
<h2>Login Page</h2>
<form method="post">
    <input id="username" name="username" placeholder="Username"><br><br>
    <input id="password" name="password" type="password" placeholder="Password"><br><br>
    <button id="login_btn">Login</button>
</form>
{% if error %}
<p style="color:red;">{{ error }}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            return redirect(url_for("dashboard"))
        else:
            return render_template_string(HTML, error="Wrong credentials")
    return render_template_string(HTML)

@app.route("/dashboard")
def dashboard():
    return "<h1>Welcome to Dashboard</h1>"

def selenium_test():
    time.sleep(2)  # Flask server start bo‘lishini kutamiz
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.ID, "login_btn").click()

    time.sleep(2)
    assert "Dashboard" in driver.page_source
    print("TEST PASSED")

    input("Brauzerni yopish uchun Enter bosing...")
    driver.quit()

if __name__ == "__main__":
    threading.Thread(target=selenium_test).start()
    app.run()
