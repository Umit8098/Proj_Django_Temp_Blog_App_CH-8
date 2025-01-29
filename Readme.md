<!-- Please update value in the {}  -->

<h1 align="center">Project_Django_Template_Blog_App</h1>

<p align="center"><strong>📝 Django Template Blog App is a full-stack application that allows users to easily create and edit blog posts and interact with other users. Users can have full control over their blog posts and enjoy the advanced features of the app.
 📝</strong></p>

---

<p align="center">📝 Django Template Blog App, kullanıcıların blog gönderilerini kolayca oluşturmasını, düzenlemesini ve diğer kullanıcılarla etkileşimde bulunmasını sağlayan bir full-stack uygulamadır. Kullanıcılar, blog gönderileri üzerinde tam kontrol sahibi olabilir ve uygulamanın gelişmiş özelliklerinden yararlanabilirler. 📝</p>


<div align="center">
  <h3>
    <a href="https://umit8112.pythonanywhere.com/">
      Live Demo
    </a>
  </h3>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Blog Posts](#blog-posts)
  - [User Profile](#user-profile)
  - [Admin Panel](#admin-panel)
  - [User Password Change](#user-password-change)
  - [User Password Reset](#user-password-reset)
- [Built With](#built-with)
- [How To Use](#how-to-use)
  - [Test User Information](#test-user-information)
- [About This Project](#about-this-project)
- [Key Features](#key-features)
- [Contact](#contact)

<!-- OVERVIEW -->
## Overview

- Django Template Blog App is a blog application with both frontend and backend created using Django. 
- This app offers the following features:

- Users can view posts anonymously.
- Registered users:
  - Can create, update and delete posts.
  - Can comment and add likes to posts.
  - Can edit his own profile information.
- In case the password is forgotten, a password reset link will be sent to the registered e-mail address.
- Each post:
  - Number of likes
  - Number of views
  - The number of comments is displayed.
- Users are informed about the actions taken via on-screen messages.

---

- Django Template Blog App, hem frontend hem de backend kısmı Django kullanılarak oluşturulmuş bir blog uygulamasıdır. 
- Bu uygulama aşağıdaki özellikleri sunar:

- Kullanıcılar anonim olarak gönderileri görüntüleyebilir.
- Kayıtlı kullanıcılar:
  - Gönderi oluşturabilir, güncelleyebilir ve silebilir.
  - Gönderilere yorum yapabilir ve beğeni ekleyebilir.
  - Kendi profil bilgilerini düzenleyebilir.
- Şifre unutulması durumunda, kayıtlı e-posta adresine şifre sıfırlama bağlantısı gönderilir.
- Her gönderinin:
  - Beğeni sayısı
  - Görüntülenme sayısı
  - Yorum sayısı görüntülenir.
- Kullanıcılar yapılan işlemler hakkında ekran mesajlarıyla bilgilendirilir.

### User Registration
<!-- ![screenshot](project_screenshot/register.png) -->
<img src="project_screenshot/register.png" alt="Kullanıcı Kayıt Olma" width="400"/>
➡ User registration page for the application.

---

### User Login
<!-- ![screenshot](project_screenshot/login.png) -->
<img src="project_screenshot/login.png" alt="Kullanıcı Login" width="400"/>
➡ Screen where users can log in and access blog posts.

---

### Blog Posts
<!-- ![screenshot](project_screenshot/Blog_App.gif) -->
<img src="project_screenshot/Blog_App.gif" alt="Blog Gönderileri" width="400"/>
➡ Overview of blog posts.

---

### User Profile
<!-- ![screenshot](project_screenshot/profile.png) -->
<img src="project_screenshot/profile.png" alt="Kullanıcı Profili" width="400"/>
➡ Profile editing page of registered users.

---

### Admin Panel
<!-- ![screenshot](project_screenshot/admin_panel.png) -->
<img src="project_screenshot/admin_panel.png" alt="Yönetici Paneli" width="400"/>
➡ A view from the admin panel of the blog application.

---

### User Password Change
<!-- ![screenshot](project_screenshot/change_password.png) -->
<img src="project_screenshot/change_password.png" alt="Kullanıcı Password Change" width="400"/>
➡ Verification screen used for password change.

---

### User Password Reset
<!-- ![screenshot](project_screenshot/reset_password.png) -->
<img src="project_screenshot/reset_password.png" alt="Kullanıcı Password Reset" width="400"/>
➡ Email verification screen for password reset.


## Built With

<!-- This section should list any major frameworks that you built your project using. Here are a few examples.-->
This project was developed using the following tools and libraries:

- [Django Templates](https://docs.djangoproject.com/en/5.1/topics/templates/): For creating dynamic web pages.
- [Bootstrap4](https://getbootstrap.com/docs/4.6/getting-started/introduction/): To provide a responsive and modern user interface.
- [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/): To easily style forms.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/): User authentication and authorization module.


## How To Use

<!-- This is an example, please update according to your application -->

To clone and run this application, you'll need [Git](https://github.com/Umit8098/Proj_Django_Temp_Blog_App_CH-8)

When installing the required packages in the requirements.txt file, review the package differences for windows/macOS/Linux environments. 

Complete the installation by uncommenting the appropriate package.

---

requirements.txt dosyasındaki gerekli paketlerin kurulumu esnasında windows/macOS/Linux ortamları için paket farklılıklarını inceleyin. 

Uygun olan paketi yorumdan kurtararak kurulumu gerçekleştirin.

```bash
# Clone this repository
$ git clone https://github.com/Umit8098/Proj_Django_Temp_Blog_App_CH-8.git

# Install dependencies
    $ python -m venv env
    $ python3 -m venv env (for macOs/linux OS)
    $ env/Scripts/activate (for win OS)
    $ source env/bin/activate (for macOs/linux OS)
    $ pip install -r requirements.txt
    $ python manage.py migrate (for win OS)
    $ python3 manage.py migrate (for macOs/linux OS)

# Create and Edit .env
# Add Your SECRET_KEY in .env file

"""
# example .env;

SECRET_KEY =123456789abcdefg...

# Sending email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = {YOUR EMAIL ADDRESS}
EMAIL_HOST_PASSWORD = {YOUR HOST PASSWORD}
EMAIL_USE_TLS = True

"""


# Run the app
    $ python manage.py runserver
```

### Test User Information

For the live demo, you can use the following test user information:
- **Username**: testuser
- **Password**: testpassword123


## About This Project
- This project was developed to enable users to easily create, edit blog posts and interact with other users. The application aims to solve the following problems:
- Manage blog posts with a user-friendly interface.
- Advanced features that meet user needs such as password reset and change.
- Both frontend and backend support for CRUD operations.
- Users can view posts anonymously.
- If they want to create a post, comment on the post, or like the post, they must register and log in to the application. After registering, they can update the profile information created for them.
- Users can perform CRUD (Create-Read-Update_Delete) operations.
- The user is notified of the actions taken by a message that appears and disappears on the screen.
- If they have forgotten their login password, an e-mail will be sent to their registered e-mail address so that they can create a login password.
- They can also change their login passwords if they wish.
- Like, view and comment statistics of all posts are displayed.

---

- Bu proje, kullanıcıların blog gönderilerini kolayca oluşturmasını, düzenlemesini ve diğer kullanıcılarla etkileşimde bulunmasını sağlamak için geliştirilmiştir. Uygulama, aşağıdaki sorunları çözmeyi hedefler:
- Kullanıcı dostu bir arayüz ile blog gönderilerini yönetme.
- Şifre sıfırlama ve değiştirme gibi kullanıcı ihtiyaçlarını karşılayan gelişmiş özellikler.
- CRUD işlemleri için hem frontend hem de backend desteği.
- Kullanıcılar anonim olarak gönderileri görüntüleyebilirler.
- Gönderi oluşturmak, gönderiye yorum yazmak, gönderiyi beğenmek isterlerse uygulamaya kayıt olup giriş yapmaları gerekir. Kayıt olduktan sonra kendileri için oluşturulan profil bildilerini güncelleyebiliriler.
- Kullanıcılar CRUD (Create-Read-Update_Delete) işlemleri yapabilir.
- Yaptığı işlemler ekranda belirip kaybolan bir mesajla kullanıcıya bildirilir.
- Eğer giriş şifrelerini unutmuşlarsa, kayıtlı e posta adreslerine giriş şifresi oluşturabilmeleri için posta gönderilir.
- Ayrıca isterlerse giriş şifrelerini değiştirebilirler.
- Tüm gönderilerin beğeni, görüntülenme, yorum istatiktikleri görüntülenmektedir.


## Key Features

- **Post Management**: Viewing, creating, editing and deleting blog posts.
- **User Management**: Registration, login, profile editing, password reset and change.
- **Interactions**: Commenting and adding likes to posts.
- **Statistics**: Tracking the number of likes, views and comments for each post.
- **User Notifications**: Notification with on-screen messages about the actions taken.

---

- **Gönderi Yönetimi**: Blog gönderilerini görüntüleme, oluşturma, düzenleme ve silme işlemleri.
- **Kullanıcı Yönetimi**: Kayıt, giriş, profil düzenleme, şifre sıfırlama ve değiştirme.
- **Etkileşimler**: Gönderilere yorum yapma ve beğeni ekleme.
- **İstatistikler**: Her gönderi için beğeni, görüntülenme ve yorum sayılarının izlenmesi.
- **Kullanıcı Bildirimleri**: Yapılan işlemler hakkında ekran mesajlarıyla bilgilendirme.


## Contact

<!-- - Website [your-website.com](https://{your-web-site-link}) -->
- **GitHub** [@Umit8098](https://github.com/Umit8098)

- **LinkedIn** [@umit-arat](https://linkedin.com/in/umit-arat/)
<!-- - Twitter [@your-twitter](https://{twitter.com/your-username}) -->


