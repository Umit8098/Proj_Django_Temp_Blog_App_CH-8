
- Bir projeyi tasarlarken en uzun zaman alan kısım database'i modelleme kısmıdır. 
  - Modellerde hangi bilgilerin kaydedileceği, 
  - Modellerin birbirleriyle olan ilişkisinin belirlenmesi, 
  - Frontend'de kullanıcıya hangi bilgilerin gösterileceğinin belirlenmesi..
 



 #### statics - root directory; 

- Normalde default olarak django her application içerisinde static klasörü arar. 
- Ancak biz ekstradan static files diye ana projemizin src sinin içerisine (root directory) bir static klasörü koymak istersek, bu yolu djangoya söylememiz gerekir şöyle;

settings.py
```py
STATIC_URL = .......
MEDIA_URL = ......
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_RO.......
```

- django static klasörünü mutlaka istiyor, 
- burada biz app içinde oluşturduk.
- bu static klasörünü app içerisinde değil de root directory'de de ekleyebilirdik.
- Tıpkı templates klasörü oluştururken yaptığımız gibi;
  - djago templates klasörünü de app'in içerisinde istiyor. Ancak biz root directory'de de bir templates klasörü oluşturmak ve bunu djangoda bildirmek için; settings.py'da TEMPLATES  değişkeninde -> 'DIRS':[BASE_DIR, 'templates'] yazarak, base directory'ye templates ekle (biz bu templates klasörünün içerisine base.html ve navbar.html koyacağız) demiştik.
  - Aynı şekilde app'in içerisinde istediği static klasörünü root directory'de oluştrumak istediğimizde, static folder'ımızı settings.py'da şu şekilde tanımlayarak, root directory'de oluşturduğumuz static klasörünü djangoya kabul ettirebiliriz.

- Base directory nin içerisinde bir tane static diye bir klasör oluşturuyoruz, 
- bu şekilde yaparsak eğer, ana projemizin içerisinde bir tane static klasörü oluşturup main.css imizi bunun içerisine de koyabiliriz. 
- Django bundan ne anlıyor? -> senin static file ların static diye bir klasörün altında ben o static'in içerisine gidip oradaki static file (css veya js)'larını alacağım, sonra nerede load ettiysen base.html de mi? buradaki template'e load edicem ama load etmem için bana url ini vermen gerekiyor, 
- link'in href'inde de satatic'e özgü url ini {% static 'blog/main.css' %} veriyoruz.
- bir de static'ler için link verdiğimiz template'te {% load static %} tag'ini eklememiz gerekiyor.





/// Ekstra Başladı ///

- EKSTRA    
- Eğer kullanıcı post'u;
  - Like etmişse, buttonun ismi 'Unlike'
  - Like etmemişse 'Like'

views.py
```py
def post_detail(request, slug):
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug) # slug=learn-drf-3c78be2186
    
    has_liked = False  # Varsayılan olarak False
    # Kullanıcının bu gönderiyi beğenip beğenmediğini kontrol et
    if request.user.is_authenticated:  # Kullanıcı giriş yapmışsa
        has_liked = Like.objects.filter(user=request.user, post=obj).exists()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = obj
            comment.save()
            return redirect('blog:detail', slug=slug) # best practice.
            # return redirect(request.path) # bu şeklide de yapılabilir.
    context = {
        'object':obj,
        'form': form,
        'has_liked': has_liked,  # Beğeni durumunu template'e gönder
    }
    return render(request, 'blog/post_detail.html', context) 
```

post_detail.html
```html
<form action="{% url 'blog:like' object.slug %}" method="POST">
    {% csrf_token %}
    <input type="hidden" name="post">
    <input type="hidden" name="user">
    <button type="submit">
        {% if has_liked %}
            Unlike
        {% else %}
            Like
        {% endif %}
    </button> {{ object.like_count }}
</form>

```
/// Ekstra Bitti ///






- ARAŞTIR !
- Bizim yazdığımız like çok düzgün değil, like yaptığımız zaman sayfa komple render oluyor, bulunduğu kısım yani sadece like yenilenmiyor, 
- bunlar genelde AJAX (Asyncron Javascript Xml) ile yazılıyor. 
- AJAX backende sayfayı refresh etmeden veri göndermek için kullanılıyor. 
- Html sayfasında AJAX kodu yazıyoruz Javascript ile,  
- bu sefer Http response gönderiyoruz databse e Javascript koduyla , GET POST methodu yapabiliyoruz. O zaman like yapınca tüm sayfanın yenilenmesinden kurtuluyoruz.

- Flusk daha basit ama djangonun built-in sağladığı security özellikleri yok, ORM yapısı yok, flusk node js ile muadil bir framework





/*****  - form içindeki bir field'ın custom validation örneği: *****/

- custom validation örneği:
- first_name ekledik ve bir validation yazdık;
- clean_fielad_name -> clean_first_name
    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if "a" in name:
            raise forms.ValidationError('Your name include "a"')
        return name 

- eğer "first_name" field'ı içeriğinde "a" varsa kabul etme! hata döndür!

users/forms.py
```py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True) # doldurulması zorunlu olsun istiyorsak

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that one already taken')
        return email

    def clean_first_name(self):
        name = self.cleaned_data['first_name']
        if "a" in name:
            raise forms.ValidationError('Your name include "a"')
        return name 
```

/*******************/






