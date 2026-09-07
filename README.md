<div dir="rtl">

<h2>سامانه مدیریت دستیاران آموزشی</h2>


<h2>پیش نیاز ها:</h2>

<ol>
<br>
<li>Python 3.10.0</li>
<br>
<li>ابتدا از <a href="https://jasmine.github.io/">اینجا</a> به وب سایت رسمی رفته و یکی از ورژن های آن را انتخاب کنید تا به صفحه آن منتقل شوید.</li>
<br>
<li>PostgreSQL</li>
<br>
<li>flask_sqlalchemy</li>
<br>
<img dir="ltr" src="./images/2023-01-14_22-40-49.png" style="display: block;padding:5px; auto;padding-top:10px; width: 30%; margin-left: auto;margin-right: auto;">
<br>
</ol>


<h2>اماده سازی:</h2>
<br>
برای اتصال دیتابیس postgre، نام کاربری و رمز عبور و نام دیتابیسی که ایجاد کرده اید را در سطر ۸ ام فایل app.py به صورت زیر وارد کنید: 
<br>
``` 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME(default: postgres):PASSWORD@localhost/DATABASE_NAME'
```
<br>
<br>
<br>



داخل فولدر spec ، یک فایل جاوااسکریپت برای نوشتن تست کیس ها بسازید.
<br>
در انتها آدرس هر دو فایل تست و کد جاوااسکریپت را به صورت زیر به SpecRunner.html اضافه کنید:
<br>
برای مشاهده نتیجه اجرای تست ها ، کافی است فایل SpecRunner.html را اجرا کنید. در این صورت با چنین صفحه ای مواجه خواهید شد:
<br>
<br>
<br>


<h2>اجرا</h2>
<br>

برای اجرای پروژه فایل app.py را اجرا کنید یا دستور زیر را در مسیر برنامه وارد کنید:

<div dir="ltr">

```

python app.py

```




``` js
describe("Adding single number ",function () { 
   it("should add numbers",function() { 
      expect(add(5,5)).toEqual(5); 
      expect(add(5,5)).toEqual(10); 
   });     
}

```
</div>
که در مثال بالا انتظار داریم مقدار تابع (5,5(add در فایل جاوااسکریپت مورد نظر میباشد، برابر با 10
شود؛ پس تست اول فیل و تست دوم پاس میشود. 
