# 🚀 کوتاه‌کننده لینک حرفه‌ای | URL Shortener Pro

<div align="center">

[![Django Version](https://img.shields.io/badge/Django-5.2-092e20?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20&color=44b78b)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776ab?style=for-the-badge&logo=python&logoColor=white&labelColor=3776ab&color=ffde57)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-A%2B-brightgreen?style=for-the-badge&logo=shield&logoColor=white&color=00d27e)](https://owasp.org/)
[![Rate Limit](https://img.shields.io/badge/Rate%20Limit-100%2Fmin-ff6b6b?style=for-the-badge&logo=speed&logoColor=white&color=ff6b6b)](https://en.wikipedia.org/wiki/Rate_limiting)

[![GitHub stars](https://img.shields.io/github/stars/mobinhasanghasemi/url-shortener?style=for-the-badge&logo=github&color=ff69b4)](https://github.com/mobinhasanghasemi/url-shortener/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/mobinhasanghasemi/url-shortener?style=for-the-badge&logo=github&color=blue)](https://github.com/mobinhasanghasemi/url-shortener/network)
[![License](https://img.shields.io/badge/License-MIT-f1c40f?style=for-the-badge&logo=license&logoColor=white&color=f1c40f)](LICENSE)

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png" width="100%">

</div>

## 🎯 درباره پروژه

یک سیستم کوتاه‌کننده لینک **حرفه‌ای، فوق‌امن و با کارایی بالا** ساخته شده با **Django 5.2** که می‌تواند هزاران درخواست را همزمان پردازش کند.

### ✨ ویژگی‌های کلیدی

| 🛡️ امنیت | ⚡ عملکرد | 📊 آمار | 🎨 UI |
|:---:|:---:|:---:|:---:|
| SQL Injection | 100+ درخواست همزمان | شمارش کلیک‌ها | واکنش‌گرا |
| XSS Protection | < 100ms پاسخ | زمان بازدید | داریک/لایت مود |
| CSRF Protection | کش چندلایه | IP کاربر | انیمیشن‌های زیبا |
| Rate Limiting | آپدیت غیرهمزمان | نمودار رشد | RTL پشتیبانی |

---

## 🛠️ نصب و راه‌اندازی

### 📋 پیش‌نیازها

- Python 3.14+
- pip
- git
- (اختیاری) Redis برای کش

### 🔧 مراحل نصب


# 1️⃣ کلون کردن پروژه
git clone https://github.com/mobinhasanghasemi/url-shortener.git
cd url-shortener

# 2️⃣ ایجاد محیط مجازی
python -m venv venv
# در لینوکس/مک:
source venv/bin/activate
# در ویندوز:
venv\Scripts\activate

# 3️⃣ نصب وابستگی‌ها
pip install -r requirements.txt

# 4️⃣ تنظیمات دیتابیس
python manage.py migrate

# 5️⃣ جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput

# 6️⃣ اجرای سرور
python manage.py runserver  


---

## 📞 ارتباط با من

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mobinhasanghasemi)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/mobin-hasanghasemi)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mobin.hasanghasemi.m@gmail.com)

</div>

---

## 💬 سوالات متداول

<details>
<summary><b>❓ چگونه می‌توانم لینک خود را کوتاه کنم؟</b></summary>

<br>

فقط کافیست لینک خود را در کادر مشخص شده وارد کنید و روی دکمه "کوتاه کن" کلیک کنید. لینک کوتاه شده شما در کمتر از یک ثانیه ساخته می‌شود!

</details>

<details>
<summary><b>❓ آیا لینک‌های من تاریخ انقضا دارند؟</b></summary>

<br>

در نسخه فعلی، لینک‌ها تاریخ انقضا ندارند و تا زمانی که شما حذفشان نکنید، فعال باقی می‌مانند.

</details>

<details>
<summary><b>❓ آیا می‌توانم آمار لینک خود را ببینم؟</b></summary>

<br>

بله! با اضافه کردن `/stats/` به انتهای لینک کوتاه خود می‌توانید آمار کامل کلیک‌ها را مشاهده کنید.

</details>

<details>
<summary><b>❓ حداکثر طول لینک کوتاه چقدر است؟</b></summary>

<br>

لینک‌های کوتاه شده شامل 6 تا 8 کاراکتر هستند. به عنوان مثال: `http://localhost:8000/3kM7xR`

</details>

---

## 🌟 حمایت از پروژه

اگر از این پروژه راضی هستید و به کار شما آمده، لطفاً:

- ⭐ یک **Star** به پروژه بدید
- 🔄 **Fork** کنید و با دوستان خود به اشتراک بگذارید
- 🐛 **Issues** خود را گزارش دهید
- 💰 **Sponsor** کنید (در صورت امکان)

---
<div align="center">

<br><br>
<img src="https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif" width="400">
<br><br>
<img src="https://media.giphy.com/media/26n6WywJyh39n1pBu/giphy.gif" width="400">
<br><br>
<img src="https://media.giphy.com/media/l0MYEqEzwMWFCg8rm/giphy.gif" width="400">
<br><br>
