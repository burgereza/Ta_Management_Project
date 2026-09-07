<div dir="rtl">

<h2>سامانه مدیریت دستیاران آموزشی</h2>


<h2>پیش نیاز ها:</h2>

<ol dir="rtl">
<br>
<li>Python 3.10.0</li>
<br>

```

pip install flask flask-sqlalchemy psycopg2-binary

```


<br>

<li> از <a href="https://www.postgresql.org/download/">اینجا</a> دیتابیس PostgreSQL را نصب کنید.</li>

<br>
<li>flask_sqlalchemy</li>
<br>

```

pip install flask flask-sqlalchemy psycopg2-binary

```

<br>
<br>
</ol>


<h2>آماده سازی:</h2>
<br>
<br>
برای اتصال دیتابیس postgre، نام کاربری و رمز عبور و نام دیتابیسی که ایجاد کرده اید را در سطر ۸ ام فایل app.py به صورت زیر وارد کنید: 
<br>
<br>

```

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME(default: postgres):PASSWORD@localhost/DATABASE_NAME'

```

<br>
<br>


<h2>نحوه اجرا:</h2>
<br>

برای اجرای پروژه فایل app.py را اجرا کنید یا دستور زیر را در مسیر برنامه وارد کنید:

<br>

<div dir="ltr">

```

python app.py

```
<br>

حال در مرورگر به آدرس http://127.0.0.1:5000 بروید.



<!-- ``` js
describe("Adding single number ",function () { 
   it("should add numbers",function() { 
      expect(add(5,5)).toEqual(5); 
      expect(add(5,5)).toEqual(10); 
   });     
}

``` -->

