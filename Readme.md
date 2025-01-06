
## Blog App CH-8

Blog application yapın, kullanıcılar crud işlemleri yapsın, ana sayfada bunlar sergilensin, comments, likes, views eklensin.

CRUD işlemlerinin yapıldığı bir alan, bir app ve bir de user ların olduğu bir app lazım
Önce django setup ı yapılması lazım, venv, decouple, db, .env ilk aşama bu ve %50 si
main projesinin içinde 
user app, CRUD app
CRUD dan başlanmalı
user işlemleri yapılmalı
decorator larla bağlanacak.
list
create
detail
update
delete
user da creation form ile register olacak, login olacak.
main in url inde bu iki app birleştirilecek.

Blog larımız olacak,
picture upload edebileceğiz,
blog başlığı olacak,
blog body sinin bir kısmını göstereceğiz,
kaç mesaj gelmiş göstereceğiz,
kaç uniq görüntüleme olmuş göstereceğiz,
kaç like almış göstereceğiz,
postun ne zaman yapıldığı (kaç saat önce yapıldığı) gösterilecek,
postları şekillendireceğiz.

detay
edit
delete


```bash
- py -m venv env
# - python3.10 -m venv env
- ./env/Scripts/activate
- pip install django 
# or 
# - py -m pip install django
- py -m pip install --upgrade pip
- pip install python-decouple
# or
# - py -m pip install python-decouple
- pip freeze > requirements.txt
- django-admin startproject main .
- py manage.py startapp blog
```

- create .gitignore  (projenin içine .gitignore oluşturalım.)

- create .env and .gitignore files, hidden to SECRET_KEY.
  
- Create .env file on root directory. We will collect our variables in this file.
```py
SECRET_KEY = o5o9...
```

- blog app'ini settings.py'daki INSTALLED_APPS' ekleyelim;

settings.py
```py
...
INSTALLED_APPS = [
    ...
    # my_apps
    'blog',
    # 'blog.apps.BlogConfig',
]
...
```


```bash
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

- blog application ımızı başlatmıştık, içerisinde işlemlerimize başlayacağız. İlk başta modellemeyi yapacağız, hangi tablolarımız olacak onu konuşacağız, modellerimizi yazdıktan sonra url lerimizi yazacağız. 

- Ama ondan önce projenin urls.py ında application ın urls.py ' ını include ediyoruz, hemen ardından blog application ın urls.py ' ını oluşturuyoruz.

main/urls.py
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

- blog application ın urls.py ' ını oluşturduktan sonra
blog app'in urls.py' ına gidip view imizin yolunu yazmamız gerekiyor ama biz daha view yazmadığımız için hata vermemesi adına şimdilik yoruma alıyoruz.

blog/urls.py
```py
from django.urls import path

urlpatterns = [
#     path('', )
]
```

### models

- Modellememizi yapacağız, modellerimizden bahsedelim, 
  - Category
  - Post
  - Comment
  - like
  - PostView

- Öncelikle Post modelimizle başlayalım. Hangi 
  fieldlarımız olacak?
  - title -> başlığımız,
  - content --> içerik,  
  - image -> fotoğraf,
  - category -> category, 
  - publish_date -> post oluşturulduğu zaman otomatik olarak tarih verecek, 
  - last_updated -> update edildiğinde zaman otomatik olarak tarih verecek,
  - author -> olmazsa olmaz bir tane yazarımız olacak, 
  - status -> bir tane status olacak ve ya draftı olacak isterse yazar bunu yayınlamayacak yada publish olacak ve ana sayfada gösterilecek. Ancak draft ta ise ana sayfada gösterilmeyecek kullanıcı isterse değişiklik yapıp publish'e çekip ana sayfada post unu yayınlanmasını sağlayacak, 
  - slug field -> genelde blog post ların.. şu şekilde url ler görünüyor -> "how-to-learn-django" böyle aralarında tire tire oluyor url de. 

- şimdi artık tek tek yazmaya başlıyoruz fieldlarımızı
  - title = models.CharField
    (max_length=100)  max length zorunlu
  - content = models.TextField() 
    max_length zorunlu değil vermiyoruz kullanıcının blog yazma kapasitesine bırakıyoruz
  - image = models.ImageField() image 
    ları media 
    file larını db ye kaydetmiyoruz, ayrı bir yerde tutuyoruz, kendi 
    projemiz içerisinde de değil genelede bunlar 3rd party depolama alanlarında tutuluyor, en popüleri de AWS3 storege service. Buraya geri döneceğiz.
  - category = models.ForeignKey
    (Category, 
    on_delete=models.PROTECT)  bir category tablosu oluşturacağuz, orayla 
    ForeingKey yapacağız, Category tablosuyla ForingKey i olacak ve on_delete=PROTECT olacak bu nedir yani bir postunuz varsa ve o posta ait bir category varsa category tablosundan bu postu silmesine izin vermiyor. CASCADE ise direkt siliyor yani category tablosundan category i silersek comple post u da siliyor, admin panelinde gösterilecek, burayı yoruma alıyoruz çünkü category tablosunu daha oluşturmadık.

    (OneToOne, ManyToMany, OneToMany relationship var. ForingKey OneToMany relationship dir, yani bunun anlamı bir post un sadece bir tane category si olacak ama bir category e ait birçok post olabilir. Category parent, post lar child. Bir child ın bir tane parent ı olur ama bir parent ın birden çok child ı olabilir.)

  - publish_date = models.DateTimeField
    (auto_now_add=True) post umuzu oluşturduğumuz zaman otomatik olarak tarih 
    saaat ekleniyor.
  - last_updated = models.DateTimeField
    (auto_now=True) her update edildiğinde otomatik olarak tarih saaat 
    ekleniyor.
  - author = models.ForeignKey Burada da user 
    model foringkey i göstereceğiz, bizim db de user tablomuz hazır 
    geliyordu yani user tablomuz var o tabloyu kullanacağız. User ilk başta migrate ettiğimizde bizim db imizde yani admin panelde de görünüyor hem bir grup tablomuz var hemde User tablomuz var işte o hazır verilen user tablomuzu kullanacağız. yine on_delete=models.CASCADE diyoruz yani user ı sildiğim zaman bu post da silinsin istiyorum. Çünkü bir anlamı yok yani user silinecekse postun kalmasının bir anlamı yok. author = models.ForeignKey(User, on_delete=models.CASCADE) Hata vermemesi için yoruma alıyoruz.
  - status = models.CharField() şimdi 
    bunu drop down menü gibi yapacağız, onun için bir yöntem var ondan 
    bahsedeceğiz; 
    field ların da üst tarafına, choices yada options diyebilirsiniz; bir tane tupple içerisinde biri db de kayıtlı olacağı şekliyle (d) diğeri kullanıcı dropdown menüsünde ise Draft diye gözükecek.
    OPTIONS = (
      ('d', 'Draft'),
      ('p', 'Published'),
    )
    Bu kısmı fieldların üst tarafına yazacağız, ardından yine charfield olduğu için max_length vermek zorundayız, bizim buraya gelebilecek en uzun kelimemiz Published 9 karakter olduğu için bir de bizden olsun diyoruz ve 10 yazıyoruz. status = models.CharField(max_length=10, choices=OPTIONS, default='d') 
    Bir de bu drop down un dinamik olarak nasıl kullanılıyor onu da gösterecek.

  - slug = models.SlugField(blank=True) 
    buna özel SlugField ı var, zorunlu olmadığını 
    blank=True ile belirtiyoruz, çünkü slug field ını zaten biz otomatik olarak generate edeceğiz, onu göstereceğiz nasıl generate edileceğini, dolayısıyla admin panelden doldurulmasına gerek kalmayacak. eğer doldurulması zorunlu olursa custom validationdan geçemeyecek hata verecek, bunun önüne geçmek için blank True diyoruz. Yine bunu uniq olmasını istiyoruz, çünkü bunu primary key yerine id yerine kullanacağız modelimizde o yüzden unique=True diyoruz. slug = models.SlugField(blank=True, unique=True)   id miz var ama genelde blog larda, e-ticaret sitelerinde de slug kullanılıyor, id kullanılmıyor genelde göstermiyorlar. 

    - SlugField -> arasında - olmayan birden çok string ifadeyi kabul etmiyor. SlugField olabilmesi için birden çok string ifade varsa arasında tire '-' olması gerekiyor. Bu field için signals kullanacağız ve orada slugify() methodu kullanarak, arasında boşluk bırakılmış string ifadelerin arasındaki boşluğu tire'-' ye çevirerek, SlugField'ın istediği yapıya çevirip db'ye kaydedeceğiz. 


blog/models.py
```py
from django.db import models

class Post(models.Model):
    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField()
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')
    slug = models.SlugField(blank=True, unique=True)
```

- şimdi yoruma aldığımız iki 
  field vardı bunları yorumdan kurtaracağız, hayata geçireceğiz, önce author da kullandığımız otomatik olarak djangonun auth application ının altındaki model file ında oluşturmuş olduğu ve bize sunduğu User modelini django.contrib.auth.models den User ı import ederek kullanıyoruz. importumuzu yaptıktan sonra author u yorumdan kurtarıyoruz.

blog/models.py
```py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    OPTIONS = (
        ('d', 'Draft'),
        ('p', 'Published')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField()
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    publish_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=OPTIONS, default='d')
    slug = models.SlugField(blank=True, unique=True)
```

- şimdi category field ımızda 
  kullandığımız Category modelimizi oluşturup yorumdan kurtaracağız. Category modelimizi Post modelimizin üstünde oluşturmamız lazım, çünkü Category modeli bizim parent modelimiz olacak, eğer altında tanımlarsak ForeignKey veremeyiz. Bunun sadece bir tane name field ı olacak ama bunu sonradan drop down olarak kullanacağız. Category ekleme işi de sadece admin panelinde olacak, sadece site yöneticisi Category ekleyebilecek, bunu form a koymayacağız ki her önüne gelen category eklemesin. Onun için bir tane default bir categoy ekleyeceğiz, eğer bir category bulamazsa "not categorized" diye default drop down seçenek koyacağız kullanıcı onu seçecek.
  name = models.CharField(max_length=100)


blog/models.py
```py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    
class Post(models.Model):
    ...
```

- Artık modelimizi admin panelde register edip kontrol edeceğiz,tabi önce migrations ve migrate etmemiz lazım.
- modelde ImageField kullandığımız için pillow paketinin de kurulması gerekiyor.

```bash
- pip install pillow
# or
# - py -m pip install pillow
- pip freeze > requirements.txt
- py manage.py makemigrations
- py manage.py migrate
```

- Şimdi artık modelimizi admin panelde register edip kontrol edeceğiz, app imizin (blog) içindeki <admin.py> a gidip;

blog/admin.py
```py
from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)
admin.site.register(Post)
```

- Admin panele gidiyoruz ve Category ve Post modelimiz görüyoruz.

```bash
- py manage.py runserver
```

Category nin sonuna gelen s takısı yani çoğul takısını class Meta ile düzelteceğiz. models.py'a gidip Category modelimizin içine class Meta yazarak düzelttik, admin panelden de düzeldiğine baktık ;

blog/models.py
```py
...
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
... 
```

- Admin panelde Protect ne işe yarıyordu onları gösterdi, 
- django isminde bir Category oluşturuyoruz, Object şeklinde görünen isimleri str metoduyla görüntüsünü düzeltik, Post class ında oluşturduğumuz instance ı nasıl gösterecek bana onu belirliyoruz, Category ve Post class larına str metoduyla bize nasıl görüneceğini yazıyoruz.(Category nin name i, Post un title ı)

blog/models.py
```py
...
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
class Post(models.Model):
    ...
    
    def __str__(self):
        return self.title
```

- Admin panelde django ve react  diye iki tane category ekledik, 


#### STATIC_URL, MEDIA_URL, ImageField

- image field ımız db ye kaydedilmiyor demiştik, onun için upload_to='' diye bir yol belirtmemiz gerekiyor. parantez içerisine hard coded birşey de oluşturabiliriz, blog/ yazarak blog 'un altına kaydet diye bu şekilde yazabiliriz ama daha dinamik bir yol gösterdi. 
- Projemizin settings.py'ına gittik, en altta STATIC_URL var, bu aslında djangonun static file larını bulmak için kullandığı prefix. staticten sonra kullandığımız staticler nelerse onların dosya yolunu yazıyoruz.
mesela STATIC_URL = 'static/css/main.css'  diye url de gözükecek. 
- Aynı bunu gibi bir tane de MEDIA_URL = ''  belirtmemiz gerekiyor, yoksa django sıkıntı çıkarıyor, ben bu media file ları nerede gösterceğim diye. Buna MEDIA_URL = '/media/' diyebilirsiniz, farklı birşey diyebilirsiniz ama best practice media deniyor.
   MEDIA_URL = '/media/' 

- Bundan sonrada MEDIA_ROOT='' diye bir yol tanıtmamızı istiyor django. Bunu yine BASE_DIR içerisindeki media_root diyoruz, MEDIA_ROOT = BASE_DIR/'media_root' 
     MEDIA_ROOT = BASE_DIR/'media_root' 

settings.py
```py
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 
```

- Bitti mi hayır bir ayar daha yapmamız gerekiyor, şimdi bu media root bizim media file larımızı koyacağımız directory olacak, yani ben ne dedim source un içerisinde ana base dır yolumun içerisinde bir tane media_root diye bir tane klasör açacak ve django kullanıcıların yüklediği media file larını bu klasörün altına yükleyecek.

- Ana projedeki urls.py' a gidiyoruz, burada şu importları yapıyoruz -> 
   from django.conf import settings
   from django.conf.urls.static import static 

- Alt kısma if settings.DEBUG:  (settings deki DEBUG True idi yani diyor ki sen geliştirme aşamasındaysan production a geçmemişsen DEBUG ın True iken benim o belirttiğim media root vardı ya sen media file larını devolopment dayken bu belirttiğim media root file ından kullan, mediaları oradan çek şuanda. 
- Ama ben daha sonra productiona geçtiğim zaman canlıya geçtiğim zaman ben bunları başka yere yükleyeceğim, sana settings.py da farklı configurasyon ayarları vereceğim ama şuanda geliştirme yaparken benim media file larımı benim gösterdiğim klasör içerisinden kullan diyoruz.)
urlpatterns'e += ile urlpatterns listesine ekliyoruz, settings.MEDIA_URL i al ondan sonra document_root da yani senin kullanacağın documentlerin root u da 
benim belirttiğim settings.MEDIA_ROOT olacak diyoruz.

- Aslında bu if bloğunun demek istediği geliştirme yaparken canlıya çıkmadan önce benim belirttiğim MEDIA_ROOT u ve  MEDIA_URL i kullan diyor, bukadar.

- Normalde media file larını ve static file larını (çok değişmeyen css, javascript,web sayfasında kullandığımız static, sabit resimler) en popüler depolama alanı olan AWS3 gibi 3rd party depolama araçlarında depolanıyor.

main/urls.py
```py
from django.contrib import admin
from django.urls import path, include
# for statics and medias
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('blog.urls')),
]

# for statics and medias
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- settings ve urls dosyalarında development aşamasında kullanacağımız static ve media dosyaları için gerekli ayarları yazpık.

- Şimdi root directory'de, application klasörümüz ile, manage.py dosyası ile aynı seviyede, settings.py da MEDIA_ROOT değişkeninde belirttiğimiz isimde 'media' folder ımızı oluşturuyoruz. 
- (Aslında biz bir 'media' isminde klasör oluşturmasak da, user bir image upload ettiğinde otomatik olarak oluşturulacak ve modelde upload kısmında belirtildiğ şekilde image kaydedilecek. Fakat biz ayrıca bir de default picture da oluşturmak istediğimizden bu default pictur'ı da bu 'media' klasörüne koymamız gerektiğinden manuel olarak bir 'media' klasörü oluşturuyoruz.)


##### ImageField

- Modelimize dönüyoruz (blog);

- image = models.ImageField() bu şekilde bırakırsak, user bir image eklediği zaman, settings.py'da belirttiğimiz 'media' ismi ile bir klasör oluşturur ve klasörünün içine user'ın eklediği image'ı kaydeder.

- image = models.ImageField(upload_to='image') bu şekilde upload_to diyerek, settings.py'da belirttiğimiz media klasörünün altında 'image' klasörü oluştur ve oraya bu dosyayı kaydet diyebiliriz.

- Ancak dinamik olarak bu işi yapabiliriz (bunu çok yerde göremeyebilirsiniz);
  - Bir fonksiyon yazıp, ve bu fonksiyonu da upload_to'da çağırarak image'ların ekleneceği yeri dinamik olarak gösterebiliriz; mesela app'imizin ismiyle bir klasör oluştur, altına image'ı ekleyen user'ın id'si ile bir klasör oluştur ve o klasörün içine de dosyanın ismini belirterek imege'ların konumunu dinamik olarak oluşturmuş oluruz.

    - def user_directory_path(instance, filename)  bu function içerisine instance (Post tan oluşturduğumuz bir obje) ve filename diye iki parametre alıyor, 
    - return 'blog/{0}/{1}'.format(instance.author.id, filename)
    
  - image field ımızın upload kısmına gidip fonksiyonumuzu kullan diyoruz, 
  - image yüklenmezse diye de default olarak bir image belirtiyoruz. Eğer default image belirtirsek önce manuel olarak, settings.py'da belirttiğimiz name'de ve konumda image'ların yükleneceği klasörü oluşturup içine belirlediğimiz default image' ı yerleştirmemiz gerekir.
        image = models.ImageField(upload=user_directory_path, default='django.jpg')
  
  - Artık user models de belirttiğimiz image field ına bir resim koyduğu zaman django otomatik olarak gidip media klasörünün altında blog diye bir klasör oluşturacak, onun altında id diye bir klasör oluşturacak, onun altına da resmi koyacak.

- Test ediyoruz; Admin panele gidip resim yüklüyoruz, draft seçiyoruz, 

blog/models.py
```py
...

def user_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.author.id, filename)


class Post(models.Model):
    ...
    image = models.ImageField(upload_to=user_directory_path, default='django.jpg')
    ...
```
    

#### signals,  slug_field, slug_field'a uuid kütüphanesi ile random sayı ekleme

- slug field a geldik,

- django signals;
  - şunu yaptığımda (klik ettiğimde, başlattığımda..) şunu yap. signals buna benziyor; burada ürettiğimiz Post objesini kaydetmeden önce (presave) şu işlemi yap diyebildiğimiz bir yapı. (postsave, presave, postdelete, predelete)
  
  - Nasıl kullanabiliriz?
  Signals ı kullanmak için bu modelin altında da belirtebiliriz, yapabiliriz ama best practice olarak app imizin (blog) içerisinde signals.py diye bir file oluşturuyoruz.
  
  - signals ı ayrı bir dosya içerisinde oluşturduğumuz için blog app klasörümüzün içerisindeki apps.py da bir değişiklik yapmamız gerekiyor.
  - AppConfig in içerisinde bize verilen def ready(self): hazır bir fonksiyonu override ediyoruz.
        def ready(self):
            import blog.signals

  - Yani diyoruz ki bu signals file ını import et ve bu signals file da işlem yap diyoruz.

  - Eğer signals ı modelin altında oluştursaydık apps.py da yapmamız gereken bu değişikliği yapmak zorunda kalmayacaktık.

  - Signals için ayrı bir file oluşturduğumuz için apps.py da bu değişiklik yapmamız gerekiyor. def ready(self) diye hazır bir function ı override ediyoruz. 
    
blog/apps.py
```py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        import blog.signals
```

  - Ama bu signals ı modelimizin içinde yazsaydık bu işleme gerek kalmayacaktı.Ekstradan signals.py oluşturduğumuz için apps.py da bu değişikliği yaptık.

  - Şimdi signals.py a gelelim; nedir, yararları nelerdir?
  - Birkaç tane import yapmamız gerekiyor signals ı kullanmak için;
   
    - oluşturduğumuz post u kaydetmeden önce bir slug oluştursun istiyoruz onun için pre_save metodunu kullanacağız o yüzden pre_save i import ediyoruz,
       from django.db.models.signals import pre_save

    - bir de receiver var, post u save et dediğimiz zaman bu receiver yazdığımız kodu gerçekleşmesini sağlıyor, dispatcher birleştirici, yani tıkladığımız an şu işlemi yap, kaydetme bekle, ben bu işlemi yapıcam ondan sonra kayıt işlemini tamamla! öyle düşünülebilir.
       from django.dispatch import receiver

    - slug field larının arasında tire var bu işlemi yapan slugify onu import edeceğiz. methodun içerisine koyduğumuz stringlerin arasında tire koyuyor.
       from django.template.defaultfilters import slugify
    
    - ve de modelimizi (Post) import ediyoruz.
       from .models import Post

    - receiver ımız bir decorator, içerisine parametre olarak  pre_save, sender= signal ı kim gönderecek? Post modelimiz gönderecek ya onu alıyor.
       @receiver(pre_save, sender=Post)

    - Daha sonra function ımızı yazıyoruz, istediğimiz ismi yazıyoruz, parametre olarak sender, instance (Post tan oluşturduğumuz obje düşünün), **kwargs (sayısını bilmediğimiz argumentler için (arguments ler için * koyuyoruz.)) koymak zorundayız.    
    - Eğer benim oluşturduğum instance ın slug ı yoksa
        def pre_save_create_slug(sender, instance, **kwargs): 
            if not instance.slug:
                instance.slug = slugify(instance.author.username + ' ' + instance.title)
    
    - user login olurken username kullandığımız için username field'ı unique olmak zorunda, burada unique bir değer girmek zorundayız onun için instance.auther.username kullanıyoruz (unique bir değer diye. Ancak bu unique işini bunu uuid ile de yapabiliriz), + ' ' + instance.title kullanıyoruz.

blog/signals.py
```py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Post

@receiver(pre_save, sender=Post)
def pre_save_create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + ' ' + instance.title)
```

blog/apps.py
```py
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        import blog.signals
```

- Test ediyoruz;
- Admin panele gidiyoruz, post oluşturuyoruz, slug ı boş bırakıyoruz otomatik oluştursun diye save ediyoruz, post a tıklıyoruz ve slug kısmına bakıyoruz evet aralarına tire koyarak slug oluşturmuş.

- Kullanıcımız silinebiliyor, kullanıcı silinince Post da siliniyor ama image lar db de kayıtlı olmadığı, file sisteminde kayıtlı olduğu için kullanıcını yüklediği  image lar silinmiyor. 
- File sisteminden folder ve içeriğinin silinmesi için signals.py da yapılanlar (ChatGPT);

blog/signals.py
```py
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
import os
import shutil


@receiver(post_delete, sender=User)
def delete_user_directory(sender, instance, **kwargs):
    """
    Kullanıcı silindiğinde, kullanıcıya ait media/blog/{user_id}/ klasörünü siler.
    """
    user_directory = os.path.join('media', 'blog', str(instance.id))
    if os.path.exists(user_directory):
        shutil.rmtree(user_directory)  # Klasör ve içindekileri siler.
```

- slug da username ve title kullandık, ancak bir user aynı title da yani başlıkta bir post daha oluşturunca hata alıyoruz, şöyle bir mantık kurmuştuk eğer username unique ise (ki evet unique olmak zorunda çünkü user ı biz djangonun default olarak bize verdiği User modelinden almıştık) bundan sonra title eklerse sıkıntı yaşamayız ama aynı user aynı title ile post oluşturunca hata almaya başladık.   
- biz aynı kullanıcı ile post lar eklediğimiz için eğer aynı post u tekrar oluşturursak bize hata verebiliyor, o yüzden slug'ımızı daha esnek yapmamız gerekiyor, bunu biraz değiştireceğiz,   
- python uuid kütüphanesinin uuid4() modülü ile random sayı ürettirip onu ekleyeceğiz.
 
- blog app imizin içerisine kendi script imizi yazacağımız bir file oluşturuyoruz, ismine de best practice "utils.py" diyoruz. 
    blog/utils.py

- uuid4 u kullanacağız, document e gidip inceliyoruz, 
    https://docs.python.org/3/library/uuid.html#uuid.uuid4

    uuid1(): Makine donanımına (MAC adresi) ve zaman bilgisine dayanır.
    uuid3(): MD5 hash tabanlıdır ve bir ad alanında benzersizdir.
    uuid4(): Rastgele oluşturulur.
    uuid5(): SHA-1 hash tabanlıdır ve bir ad alanında benzersizdir.

- generate a random UUID yani bize random (universal unique id) uuid üretmesini istiyoruz. 
- uuid kütüphanesinin uuid4() modülünü kullanarak harflerden ve rakamlardan oluşan string bir değer üreteceğiz. 
- uuid import ediyoruz, bir tane function yazıyoruz, 
    import uuid
    def get_random_code():
        code = uuid.uuid4() 

- bu bize integer olarak dönüyor ama bunu stringe çeviriyoruz, 
    code = str(uuid.uuid4())   

- bakalım bize ne dönüyor

blog/utils.py
```py
import uuid

def get_random_code():
    code = str(uuid.uuid4())
    return code

print(get_random_code())
```

- çalıştırdık ve terminalde uzun bir unique kod ('uuid.UUID' tipinde, sayı içeren bir obje) döndü.
  - biz bu kadar uzun istemiyoruz, 
  - 11 karakter istiyoruz, 
  - arada tire de olmasın istiyoruz, 

- burada algoritma düşünüyoruz, nasıl bir algoritma kurabiliriz? başlangıçtan itibaren 11 karakter al diyoruz, replace('-','') metodumuzla tireyi şununla (space değil) değiştir diyoruz.  
    code = str(uuid.uuid4())[:11].replace('-','')

- çalıştırdık ve tireyi aradan çıkararak 10 karakterlik bir unique değer (67d06a66b1) döndürdü.


blog/utils.py
```py
import uuid

def get_random_code():
    # code = uuid.uuid4() (string e çevirmemiz gerekiyor.)
    code = str(uuid.uuid4())[:11].replace('-','')
    return code
```


- Burası çalıştıktan sonra blog/signals.py a gidip username kısmını değiştireceğiz, 
- .utils den get_random_code fonksiyonunu import ediyoruz,
- slugify kısmına ise önce instance.title sonra boşluk ve ardından utils'de uuid ile unique değer oluşturan fonksiyonu ekliyoruz.
    slugify(instance.title + ' ' + get_random_code())

blog/signals.py
```py
...
from .utils import get_random_code

@receiver(pre_save, sender=Post)
def pre_save_create_slug(sender, instance, **kwargs):
    if not instance.slug:
        # instance.slug = slugify(instance.author.username + " " + instance.title)
        instance.slug = slugify(instance.title + " " + get_random_code())

...
```

- runserver yapıp çalıştırıyoruz, admin panelden yeni bir post oluşturuyoruz ve slug da istediğimiz unique değeri görüyoruz.


- Diğer modellerimize geçiyoruz;  

- Comment modeli;
- Comment modelimizi basit tuttuk, bu çok daha karmaşık yapılabilir.Twitter daki gibi içi içe de parent-child commentler de olabilir ama burada kısa tutuldu.Sadece mesaj atınca ekranda görünmesi için basit tutuldu.

- Bu comment e ait bir tane user field ımız olması lazım. User modeli ile ForignKey ilişkisi olacak, on_delete=models.CASCADE olacak yani user silindiğinde commentimiz silinsin istiyoruz,

- post field ımız olacak ve bunun Post ile bir ilişkisinin de olması lazım (aynı user field ında olduğu gibi), Post silindiği zaman altındaki yorumlarda silinmesi lazım, on_delete=models.CASCADE

- commentin oluşturulduğu zaman olacak (time_stamp field ımız) auto_now_add=True

- content field ımız olacak olacak models.TextField()

- Yine bu modelimize de str methodu belirliyoruz;
def __str__(self): return self.user.username

blog/models.py
```py
...
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return self.user.username 
```

- Like mmodeli;
- Like modelimizi yazıyoruz, günümüzde postlarda ne var? like, comment, görüntülenme var.
Like a ait bir tane user ımız olması lazım. User modeli ile ForignKey ilişkisi olacak, on_delete=models.CASCADE olacak yani user silindiğinde like da silinsin istiyoruz,

- post ile bir ilişkisinin de olması lazım, post silindiği zaman altındaki like ların da silinmesi lazım, on_delete=models.CASCADE

- str metodu belirliyoruz, def __str__(self): return self.user.username

blog/models.py
```py
...
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
```


- PostView modeli;
- (kim görüntülemiş, hangi postu görüntülemiş, saat kaçta görüntülemiş bu fieldları istiyoruz, tabi bunları çoğaltabiliriz de)

- PostView için de bir tane user ımız olması lazım. User modeli ile ForignKey ilişkisi olacak, on_delete=models.CASCADE olacak yani user silindiğinde PostView de silinsin istiyoruz,

- post ile bir ilişkisinin de olması lazım, post silindiği zaman altındaki View lerin de silinmesi lazım, on_delete=models.CASCADE

- time_stamp veriyoruz;

- str metodu belirliyoruz, def __str__(self): return self.user.username

blog/models.py
```py
...
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
```

- blog/admin.py a gidip oluşturduğumuz modelleri import ediyoruz ki admin panelde görebilelim;

blog/admin.py
```py
from django.contrib import admin
from .models import Category, Post, Comment, Like, PostView

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(PostView)
admin.site.register(Comment)
```

- modelde değişiklik yaptığımız için makemigrations ve migrate yapıyoruz;

```bash
- py manage.py makemigrations
- py manage.py migrate
- py manage.py runserver
```

- şimdiye kadar yaptığımız değişiklikleri sadece admin panelde görebiliyoruz, çünkü template lerimizi henüz oluşturmadık.

- Şu ana kadar db modellerini, tablolarını yazdık, 


### forms

- şimdi formları yazacağız, kullanıcıdan form a koyduğumuz field ları doldurmasını isteyeceğiz, 
- kullanıcı fieldları doldurunca biz onları frontend de template ler ile göstereceğiz. Şimdi formları yazacağız;
- blog app imizin içinde forms.py oluşturuyoruz, içinde PostForm ve CommentForm oluşturuyoruz, iki tane forma ihtiyacımız var, 
  - PostForm; hem postu oluşturmak için hem post create de kullanacağız hem de postu update ederken kullanacağız, 
  - CommentForm, comment için yani yorum için form oluşturacağız. 

- PostForm;
- Önce form oluşturmak için django dan forms import ediyoruz, sonra modelForm kullanacağımız için .models den Post ve Comment  modellerini import ediyoruz, PostForm mumuzu forms.ModelForm dan inherit ediyoruz,
   class PostForm(forms.ModelForm):

- class Meta nın altına modelimizi ve bu modelin fieldlarını belirtiyoruz. (Kullanacaklarımızı yazmak yerine exclude da yapabilirdik.)
  - title ı alıyoruz, title olmak zorunda,
  - content i alacağız,
  - image ı alacağız,
  - category olacak,
  - publish_date i django otomatik kaydediyor, last_updated i de almayacağız, author u da almayacağız, view'de otomatik olarak request.user ile otomatik ekleyeceğiz,
  - status ü alacağız,
```py
         class Meta:
            model = Post
            fields = (
                'title',
                'content',
                'image',
                'category',
                'status',
                # 'author', # view'de otomatik ekleyeceğiz.
            )
```
            

- status field'ını modelde drop down olarak kullanmıştık, bunu formda da kullanabiliriz, onu nasıl yapacağız? 
- class metanın hemen üstüne override edeceğimiz field ı yazıyoruz, burada status ü override ediyoruz, yani choices içerisine Post.OPTIONS u al diyoruz,
    status = formsce.ChoiceField(chois=Post.OPTIONS) 

- category field'ı için de djangonun şöyle güzel bir yöntemi var;  
- category db de kayıtlı, Options gibi static değil dinamik, yani biz admin panelden birşey eklediğimizde otomatik olarak drop down menüsüne onların da eklenmesini istiyoruz. 
- Bunun için ModelsChoiceField var bunun içerisine bir tane queryset yazıyoruz, Category tablomdaki objects lerin hepsini al diyoruz, tabi Category modelimizi import etmemiz lazım, şimdi bana dinamik olarak, ben category e admin panelden birşey eklediğim zaman form'da o eklediğim şey dinamik olarak gözükecek, ayrıca birşey seçilmediğinde emty_label='Select' yazarak Select görünmesini sağlıyoruz.     
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select')

- Başka bir tablodaki verileri form üzerinde dropdown menüsü olarak göstermek istiyorsanız bu ModelChoiceField çok kullanışlı.

blog/forms.py
```py
from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Post.OPTIONS)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Select')
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'image',
            'category',
            'status',
            # 'author', # view'de otomatik ekleyeceğiz.

        )
```

- CommentForm;
- forms.ModelForm dan inherit edilerek,
  - user otomatik, 
  - post otomatik, 
  - time_stamp otomatik olarak eklenecek. 
  - userdan sadece content verisini isteyeceğiz. tupple olarak kullandığımız için virgül kullanıyoruz, list olarak da yazabiliriz fark etmez.

    class CommentForm(forms.ModelForm):   
        class Meta:
        model = Comment
        fields = ('content',) 


blog/forms.py
```py
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
```


- Şuan; 
  - modellerimiz tamam, 
  - formlarımız tamam, 


### views

- artık view lerimizi oluşturmaya başlayacağız;
- blog view.py'a gidiyoruz, (frontend de template oluştururken bir home page yapmadık, home page imizi blogların listelendiği template olarak düşündük, extradan bir home page yapmadık.) 
    def post_list(request):  

- postlarımızı sayfada listeleyeceğiz. 
  - Ancak Post modeldeki status fieldına göre sadece Published-p olan postların herkes/tüm user'lar tarafından görülebilecek şekilde listelenmesini istiyoruz.
  - status field'ı Draft-d olan postların sadece onu create eden user tarafından görülebilmesini istiyoruz. (Bu daha sonra yapılacak.)

    <!-- qs = Post.objects.all()     -->
    qs = Post.objects.filter(status='d')    

- genelde
  - qs-queryset genelde bu şekilde kullanılıyor, 
  - obj-objects için de böyle kullanılıyor 

- Post'u .models den import ediyoruz, 
    context={
        'object_list':qs
    }

    return render(request, 'blog/post_list.html', context)

blog/views.py
```py
from django.shortcuts import render
from .models import Post

def post_list(request):
    # qs = Post.objects.all()
    qs = Post.objects.filter(status='p')
    context={
        'object_list':qs
    }
    return render(request, 'blog/post_list.html', context)
```


### templates

- template yapısını şu şekilde kuracağız;
  - root directory'de bir templates klasörümüz olacak ve tüm projede kullanılacak ortak template'ler (base.html, main.html, navbar.html) bu klasörün içinde olacak.
  - proje içindeki app'lerin de kendi içlerinde template klasörleri olacak ve app ile alakalı template'ler orada oluşturulacak.

- Önce settings.py'a gidip, TEMPLATES değişkeninde root directory'de bir templates klasörü oluşturulacağını belirtiyoruz. (default olarak django template'leri app'lerin içinde arar. Buradaki ayar ile root directory'de de bir templates klasörü var, sen oaraya da bak diyoruz.)

main/settings.py 
```py
TEMPLATES = [
    {
        ...,
        # 'DIRS': [],
        'DIRS': [BASE_DIR, "templates"],
        ... 
    },
]
```

- Bundan sonra root directory'de templates isimli new folder/yeni klasör açıp bunun içerisine de tüm projede ortak olarak kullanacağımız base.html template'ini oluşturuyoruz.
    templates/base.html

- Şimdi bir tane normal html template i koyuyoruz ama daha sonra bootstrap in starter template i var onu koyacağız, bootstrap le yapacağız ondan sonra.
title'ı değiştirip Umit Blog yazıyoruz. body nin içine block yapısı oluşturuyoruz.     
    {% block content %}   {% endblock content %}

base.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clarusway Blog</title>
</head>
<body>
    
    {% block content %}
        
    {% endblock content %}
        
</body>
</html>
```

#### list view-urls-template;

- base.html olarak tüm projede ortak kullanılan template'i oluşturduk, artık application'ımızda oluşturacağımız template ler için blog app imizin içine girip, templates isminde (templates ismi mecburi) bir klasör oluşturup, şu yapıda aynı zamanda home template'imizde olacak olana post_list.html template'imizi oluşturuyoruz;
    blog/templates/blog/post_list.html


- post_list.html template'imizde base.html temp'ini extend ediyoruz. 
    {% extends 'base.html' %} 

- sonra block larımızı koyuyoruz, (birçok block oluşturup içerisine farklı kodlar konulabilir.)
    {% block content %} {% endblock content %}

blog/templates/blog/post_list.html
```html
{% extends 'base.html' %} 

{% block content %}
    
{% endblock content %}
```

- özet: Buraya kadar ne yaptık? 
  - view de bir view oluşturduk, 
  - url'imizde daha view imizin yolunu yazmadık yazacağız, 
  - root directory'de templates klasörü yapısını kullanacağımız için settings.py'da TEMPLATES değişkeninde ayar yaptık,
  - root directory de bir tane templates klasörü ve içerisinde base.html template i oluşturduk, 
  - sonra application da kullanacağımız html template file'ları için bir tane templates klasörü ve içerisinde application ımızın ismi ile (blog) bir klasör ve onun da içerisinde post_list.html dosyasını oluşturduk,
  -  post_list.html'e de base.html dosyasını inherit ettik.


- Template yapımızı kurduk. Artık post_list view'deki kurduğumuz logic ile db'den çektiğimiz dataları template'imizde yakalayıp user'a sergileyeceğiz.

- views.py'da post_list view'ine bakıyoruz;
  - listelerken nasıl yapıyorduk, all yaptığımız için queryset dönecek, onun için bizim post_list.html içerisinde blockların arasında for ile döngü oluşturmamız gerekiyor. 
  - object_list bizim views.py'da oluşturduğumuz context içerisindeki key değerini aldık bunun içerisinde döngü oluşturuyoruz, 
  - bunun içerisindeki object in nelerini almak istiyoruz? 
       {{object.title}} ,  
  
  - resmi göstereceğiz, resmi gösterirken farklı birşey kullanıyoruz image tagı içerisinde src nin içerisinde gösteriyoruz,
       <img src="{{ object.image.url }}" alt="">   
       
  - post/object'in content'ini gösteriyoruz,
       {{object.content}}

blog/templates/blog/post_list.html
```html
{% extends 'base.html' %} 
{% block content %}

{% for object in object_list %}
{{object.title}}
<img src="{{ object.image.url }}" alt="">
{{object.content}}
{% endfor %}
    
{% endblock content %}
```

- blog app imizin blog urls.p'ında post_list view'imizi çalıştıracak/tetikleyecek endpoint/url path'imizi ekliyoruz.

blog/urls.py
```py
from django.urls import path
from .views import post_list

urlpatterns = [
    path('', post_list, name='list'),
]
```

- daha düzgün bir görünüş için;
  - {{object.title}} ı -> h1 ve 
  - {{object.content}} i -> p tagları arasına aldık,
  - object.content e | truncatechars:20 diye birşey yazdık,

blog/templates/blog/post_list.html
```html
{% extends 'base.html' %} 
{% block content %}
{% for object in object_list %}
    
    <h1>{{object.title}}</h1>
    <img src="{{ object.image.url }}" alt="">
    <p>{{object.content | truncatechars:20}}</p>

{% endfor %}
{% endblock content %}
```


##### truncatechars:20

- object.content | truncatechars:20 ne işe yarıyor? 

```html
blurb_text = 'You are pretty smart!'
{{ blurb_text|truncatechars:11 }}
You are pr…

blurb_text = 'You are pretty smart!'
{{ blurb_text|truncatewords:3 }}
You are pretty…

blurb = '<p>You are <em>pretty</em> smart!</p>'
{{ blurb|truncatewords_html:3 }}
<p>You are <em>pretty…</em></p>
```


#### create view-urls-template;

- create view i yapalım, arkasından update yapacağız.
- Create için user'a bir form vermemiz gerekiyor ki bu formda gönderdiği datalarla post create edilsin.
- view.py'a gidip view imizi yazmaya başlıyoruz,
    def post_create(request):

- formumuzu oluşturmuştuk (PostForm), onu kullanmak için import ediyoruz, 
    from .forms import PostForm
    form = PostForm() 

- önce PostForm umuzu boş bir şekilde ekrana getiriyoruz, bunun bir de kısa yöntemi var;
  - get ise boş bir form getir,
        form = PostForm()

  - ondan sonra eğer request method post ise
  - formu bu sefer PostForm un içerisini request.Post ile doldur diyoruz, 
  - ama biz media file da upload ettiğimiz için bir method daha eklememiz gerekiyor, 
        request.FILES

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)

```html
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
```

- Bu yöntemi bazen şöyle görebilirsiniz;
```html
def post_create(request):
    <!-- form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) -->
    form = PostForm(request.POST or None, request.FILES or None)
```
- form = PostForm(requset.POST or None, request.FILES or None) Bu ne anlama geliyor?  
  - Post varsa post u al, yoksa none olsun yani boş, 
  - files varsa files ı al yoksa none olsun yani boş. 
  - Yukarıdaki üç satır kod yerine tek satırda çözmüş. Hiç bir farkı yok ikisi de aynı kapıya çıkıyor.

-  Tamam devam ediyoruz bizim yöntemle, formumuz valid ise, 
    if form.is_valid():   

- Bu kısımda PostForm'da yoruma aldığımız Post modelimizin author field'ını otomatik ekleyeceğiz. Bu field'ı user'ın doldurmasını değil de, o anki oturum açmıç/authenticate olmuş user'ın id'si ile otomatik olarak burada biz ekleyeceğiz.
 
- eğer formumuz valid ise bir tane Post objesi oluşturup, post değişkenine tanımlıyoruz, ancak bunu commit=False diyerek henüz db'ye kaydetmiyoruz, çünkü daha Post objesinin author field'ı eksik. Bu eksik author field'ı User modeli ile ilişkili.   
    post = form.save(commit=False) 

- post değişkenindeki author field'ı eksik olan Post objesine, request.user ile o anki authenticate olmuş ve istek atan user'ı çekip post.auther olarak ekliyoruz.
    userpost.author = request.user 

- author field'ını da ekledikten sonra create işlemi tamamlanmış oluyor ve save() ediyoruz.
    post.save()

- Burası önemli bu çok kullanılan bir yapı.

- Postu oluşturduktan sonra redirect ediyoruz ama önce redirect i import ediyoruz,
    return redirect('list')


##### Name_Space
- Ha bu arada şöyle birşey daha var, mesela bizim birkaç tane daha app imiz var ve bu applerimizin de path name leri arasında da list olabilir, o zaman djangonun kafası karışıyor, bunu önlemek için   
- app (blog) urls.py da app_name = 'blog'  diye bir name space oluşturuyoruz ve blog diyoruz buna (çünkü app imizin ismi blog), nasıl kullanıyoruz bunu ;

    return redirect('blog:list') # blog application ın list ine gönder bunu!

blog/urls.py
```py
from django.urls import path
from .views import post_list, post_create

app_name='blog'
urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create, name='create'),
]
```


- Artık return redirect('blog:list')  blog app imizin list ine döndür diyerek view imizin context ini oluşturup template imize gönderiyoruz;
    context = {
        'form':form
    }
    return render(request, 'blog/post_create.html', context)

blog/views.py
```py
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

...

def post_create(request):
    
    #! kısa yol
    # form = PostForm(request.POST or None, request.FILES or None) 
    
    #! uzun yol
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # image için FİLES
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:list')
    context = {
        'form':form
    }
    return render(request, 'blog/post_create.html', context)
```

- Şimdi post_create views imizi çalıştıracak/tetikleyecek endpoint/url'i oluşturalım, 

blog/urls.py
```py
from django.urls import path
from .views import (
    post_list, 
    post_create,
)

app_name = 'blog'
urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create, name='create')
]
```

- create için template'imizi blog/templates klasörünün içerisine post_create.html ismiyle oluşturuyoruz; 
- base.html den extends edip, block larımızı yazıp arasına 
  - form tag'i ile oluşturuyoruz. 
  - form un action ı aynı sayfada olduğu için birşey yazmıyoruz, 
  - method='POST' olacak,
  - formda image gibi bir file kullandığımız için enctype="multipart/form-data" attribute'ünü de mutlaka ekliyoruz.
  - method post olduğu için csrf token tag ini {% csrf_token %} koyuyoruz, 
  - sonra bunun içerisine formumuzu paragraf tag i içerisinde {{ form.as_p}} gönderiyoruz,
  -  bir tane de button ekliyoruz type='submit' (POST diye) ,

blog/templates/blog/post_create.html
```html
{% extends 'base.html' %}

{% block content %}

<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">POST</button>
</form>

{% endblock content %} 
```

- runserver yapıp create/ sayfasına gidiyoruz,
  -  formu görüyoruz, 
  -  dolduryoruz, 
  -  post diyoruz, 
  -  yeni bir post oluşturduk.  

- post.author=......   kısmını yoruma alarak ve de form.save() yaparak çalıştırdık, create etmeye çalıştık, Post has no author hatası aldık. Ben bunu db ye kaydedeceğim ama Post un içinde author a ait bir bilgi yok, author da Post modelinde doldurulması zorunlu bir alan, onun için hata veriyor.


- status field ımızı da choices OPTIONS belirledik. Bunu atlamışız ama düzelteceğiz. d ve p db de kaydedilme şekli, Draft ve Published frontend de gösterilme şekli. 
- slug field ımız var, id gibidir. biz title olarak belirlemiştik. title a ne girersek kelimeler arasına tire koyarak slug hale getiriyor bu field. ve biz bunun unique olmasını istedik çünkü primary key yani id olarak kullanacağız modelimizde.

- Comment modeli gerekli olan fieldlar;
  - kimin comment yaptığı? bunu User modelinden forignkey olarak aldık.
  - hangi post a comment yapıldı? bunu da Post modelimize forignkey ile bağladık. 
  - time stamp ile hangi saatte yapıldı,
  - content field'ı. 

- Like modeli gerekli olan fieldlar; 
  - kim like etti? User modelinden foringkey ile bağladık.
  - hangi post u like etti? Post modelinden foringkey ile bağladık.

- PostView modeli gerekli olan fieldlar;
  - kim görüntüledi? User modelinden foringkey ile bağladık.
  - hangi post u görüntüledi? Post modelinden foringkey ile bağladık. 
  - saat kaçta görüntüledi? 



#### detail view-urls-template;

- view;
- detail page i oluşturacağız; 
- view.py a gidiyoruz ve post_detail view imizi yazıyoruz;
  - parametre olarak; 
    - request'i alıyor, 
    - burada biz specific yani özel bir obje ile işlem yapacağımız için o specific objeye ait unique bir değere ihtiyacımız var. Normalde buraya pk/id yazıyorduk. Ancak bu projede modelimizin bir slug field'ı var ve unique bir değer alıyor. Bu projede objenin unique olan slug field kullanıyoruz ve parametre olarak detail view'imize gönderiyoruz.
        def post_detail(request, slug):

- specific objemizi slug unique fieldı ile modelimizden yakalıyoruz, requestle beraber gelen ve slug'ı slug'a eşit olan Post taki objeyi alıp bunu frontend'e gönderiyoruz. (get_object_or_404 u da django.shortcuts dan import ediyoruz.)
    from django.shortcuts import get_object_or_404
    obj = get_object_or_404(Post, slug=slug)
    context = {
    'object': obj
    }
    return render (request, 'blog/post_detail.html', context) 

- bir de post_list'te yani ana sayfada postların listendiği yerde her post'un title'ına bir tane <a></a> anchor tag belirleyip ona tıkladığımızda bizi post_detail sayfasına yönlendirecek.
- burada hiçbir post işlemi yok. Sadece sayfa render ediyoruz.
- bunları daha geliştireceğiz yavaş yavaş ana çatımızı şekillendirelim, daha sonra post_detail'in içerisine CommentForm u göndereceğiz, daha işlevsel hale getireceğiz.

blog/views.py
```py
from django.shortcuts import get_object_or_404
...

def post_detail(request, slug):
    obj = get_object_or_404(Post, slug=slug) # slug=learn-drf-3c78be2186
    context = {
        'object': obj
    }
    return render(request, 'blog/post_detail.html', context)
```

- template;
- post_detail.html template'imizi yazalım,
- blog/templates/blog klasörü içerisine post_detail.html template imizi oluşturuyoruz, 
- base.html den extends'i yapıyoruz, 
- sonra context'in içinde gönderdiğimiz object in neyini görmek istiyorsak belirtiyoruz; 
  - object'in title'ı için;
        <h1>{{ object.title }}</h1>
  - object'in image'ı için img tag ındaki src=" " içerisine {{ object.image.url }} şeklinde yazmamız gerekiyor.
        <img src="{{ object.image.url }}" alt="">

  - post_list e benzer kodlar olacak şimdilik. p tagı içerisinde truncatchars ı silip content in tamamını göstersin istiyoruz.
        <p>{{ object.content }}</p>

- post_list.html'de post'un title'ına bir anchor tag ı belirleyeceğiz, title a tıkladığımızda bizi post_detail.html sayfasına yönlendirecek.

blog/post_detail.html
```html
{% extends 'base.html' %}
{% block content %}

<h1>{{ object.title }}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{ object.content }}</p>

{% endblock content %}
```

- urls;
- yazdığımız post_detail view'ini çalıştıracak endpoint/urls'i blog/urls.py'da tanımlayalım,
- daha önce "id" field'ını parametre olarak ekliyorduk path'imize ama burada "slug" field'ını ekleyeceğiz parametre olarak. Ayrıca değişik bir kullanım olarak; 
  - path'imizi "detail" olmadan sadece "slug" ile de yazabiliriz.
        <!-- path('detail/<str:slug>/', post_detail, name='detail') -->
        path('<str:slug>/', post_detail, name='detail')
    
- Mantığımız şu; 
  - url de postumuzun slug değeri geldiğinde bizi o posta ait slug ın post_detail sayfasına yönlendirsin. 
  - Mesela slug değeri şudur: test-1-5ff971487f/  
  - urls'de path imizin yolu da böyle görünüyor:  http://127.0.0.1:8000/test-1-5ff971487f/

blog/urls.py
```py
from .views import (
    ...,
    post_detail,
)

app_name='blog'
urlpatterns = [
    ...,
    # path('detail/<str:slug>/', post_detail, name='detail'),
    path('<str:slug>/', post_detail, name='detail'),
]
```

- post_list.html template'inde, listelediğimiz her post'un title'ını bir <a></a> (anchor) tag'ı içerisine alarak, list page'inden/sayfasından post_detail.html template'ine/sayfasına yönlendiriyoruz.
- <a></a> anchor tag'inin href'ine detail page'in url'ini ve slug'ı koyuyoruz, yani url'e blog:detail yaz, arkasından objenin slug'ını koy diyoruz. içerisine de h1 tag ının içerisinde bulunan object.title ı koyuyoruz.
    <a href="{% url 'blog:detail' object.slug %}">
        <h1>{{object.title}}</h1>
    </a>

blog/post_list.html
```html
{% extends 'base.html' %}
{% block content %}

{% for object in object_list %}
<a href="{% url 'blog:detail' object.slug %}">
    <h1>{{object.title}}</h1>
</a>
<img src="{{ object.image.url }}" alt="">
<p>{{object.content|truncatechars:20}}</p>
{% endfor %}

{% endblock content %}
```

- detail page imizi de oluşturduk, bunları süsleyeceğiz..


#### update view-urls-template;

- view;
- list, create ve detail yaptık şimdi update yapıcaz; 
- views.py'a gidip post_update view imizi yazıyoruz, 
- update fonksiyonumuzun içine request ile birlikte, specific yani özel bir obje ile işlem yapacağımız için o specific objeye ait unique bir değer olan slug field'ımızdaki değeri parametre olarak gönderiyoruz. 
    def post_update(request, slug):    

-  yine üzerinde işlem yapacağımız objemizi obj diye bir değişkene çekiyoruz,
    obj = get_object_or_404(Post, slug=slug)

- form umuzu çekiyoruz, ama bu sefer yukarıda post_create yaparken yoruma aldığımız şekliyle çekiyoruz. Ayrıca form bize gelirken dolu gelmesi için instance attribute ünü kullanıyoruz, instance obj (db den get ettiğimiz specific objenin tüm verileriyle dolu olarak gelmesi) ye eşit olsun diyoruz,
    form = PostForm(request.POST or None, request.FILES or None, instance=obj) 

- Böylelikle yukarıdaki kısmı yazmak zorunda kalmadan atlayabiliyoruz.
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)


- form valid ise form u save et, list e redirect et;
    if form.is_valid():
        form.save()    
        return redirect('blog:list')     

- eğer burada redirect yapmazsak kullanıcı refresh veya geri tuşuna bastığında form tekrar gönderilir. Onu engellemek için kullanıcıyı redirect ile post yapamayacağı bir sayfaya gönderilir.

- eğer method umuz get ise yani post yapılmamışsa template ne göndersin?..;
    context={
        'object':obj,
        'form': form
    }
    return render(request, 'blog/post_update.html', context)


blog/views.py
 ```py
...

def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('blog:list')
    context={
        'object':obj,
        'form':form
    }
    return render(request, 'blog/post_update.html', context)
```

- template;
- blog/templates/blog klasörü içerisine post_update.html template imizi oluşturuyoruz, 
- base.html den extends i yapıyoruz, 
- form gösteriyoruz, 
  - action ımız bu view da olduğu için birşey yazmıyoruz,
  - method='POST', 
  - img kullandığımız için ; enctype="multipart/form-data",
  - method='POST' kullandığımız için {% csrf_token %} {{ form.as_p }}
  - olmazsa olmaz submit button.

blog/templates/blog/post_update.html
```html
{% extends 'base.html' %}
{% block content %}

<h2>Update {{ object.title }}</h2>
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Update</button>
</form>

{% endblock content %}
```

- urls;
- urls.py'a gidip, update view'ini çalıştıracak url path ini/endpoint'ini yazıyoruz.
- Bu view'de post_update.html template'inin render edilmesini sağlıyor.
- daha önce path('<str:id>/', post_detail, name='detail') diye tanımlıyorduk, şimdi id değil de slug kullandığımız için path'i şöyle tanımlıyoruz;
    path('update/<str:slug>/', post_update, name='update')

blog/urls.py
```py
from .views import (
    ...
    post_update,
)

app_name='blog'
urlpatterns = [
    ...
    # path('update/<str:slug>/', post_update, name='update'),
    path('<str:slug>/update/', post_update, name='update'),
]
```


#### delete view-urls-template;

- view;
- views.py'a gidiyoruz, post delete view imizi yazıyoruz, 
- specific bir objeyi belirtmek için yine uniq bir değer olan slug ı request ile birlikte kullanıyoruz, ve diğer kodlar...
    def post_delete(request, slug):

blog/views.py
```py
...
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        obj.delete()
        return redirect('blog:list')
    context = {
        'object':obj
    }
    return render(request, 'blog/post_delete.html', context)
```

- urls;
- urls.py'a gidip post_delete view ini import ediyoruz,
- post_delete view'ini çalıştırarak, post_delete.html template'inin render edilmesini sağlayacak olan path'i/urls'i/endpoint'i/yolunu tanımlıyoruz. 
- daha önce; 
    path('<str:id>/', post_detail, name='detail') 

şeklinde tanımlıyorduk, şimdi id değil de slug kullandığımız için şu şekilde tanımlıyoruz;
    path('<str:slug>/delete/', post_delete, name='delete'), 

blog/urls.py
```py
from .views import (
    ...,
    post_delete,
)

app_name='blog'
urlpatterns = [
    ...,
    # path('delete/<str:slug>/', post_delete, name='delete'),
    path('<str:slug>/delete/', post_delete, name='delete'),
]
```

- template;
- delete için aslında bize bir template gerekmiyor. bunu bir button (type="submite") ile de yapabiliriz. Sadece buttonu Post meyhoduyla kullanabilmek için; methodu post olan, csrf token olan bir form içine almamız yeterli. Fakat best practice; bir template, post methodlu ve csrf token'lı bir form içinde submit eden bir button kullanılıyor.
- blog/templates/blog klasörü içerisine post_delete.html template imizi oluşturuyoruz, 
- base.html den extends i yapıyoruz, 
- form gösteriyoruz, 
  - action ımız bu view da olduğu için birşey yazmıyoruz,
  - method='POST', 
  - method='POST' kullandığımız için {% csrf_token %}
  - olmazsa olmaz submit button.
  - {{ object }} bize burada object ne dönüyor? title dönüyor. biraz önce object.title yazdık ama gerek yok, ama kafalar karışmasın diye yine de yazıyoruz, <p>Are you sure delete {{ object.title }}</p>
  - eğer delete etmekten vaz geçilirse diye de <a></a> (anchor tag ı ile list page e yönlendiriyoruz) bir button yerleştiriyoruz.


blog/templates/blog/post_delete.html
```html
{% extends 'base.html' %}
{% block content %}

<p>Are you sure delete {{ object.title }}</p>
<form action="" method="POST">
    {% csrf_token %}
    <button type="submit">Yes, Delete</button>
    <a href="{% url 'blog:list' %}">Cancel</a>
</form>

{% endblock content %}
```

- çalıştırıyoruz, bir post ta tıklayıp detail sayfasına geliyoruz ve url e http://127.0.0.1:8000/learn-drf-30c99a262e/delete   delete yazınca bizi delete html template ine gönderiyor, cancel dersek anchor tag i bizi list e , Yes dersek de bu sefer view logic i post u silip bizi list e redirect ediyor.


#### bootstrap4.5;

- Templete'leri frontend için güzelleştirelim. like kalp, göz ekleyeceğiz,

- base.html e gidiyoruz,

- bootstrap4.5 ten starter template i var onu koyacağız, daha farklı hazır templateleri de var , onları indirip kullanabilirsiniz ama bu şimdilik yeterli bizim için,
- bootstrap e gidiyoruz, 
    https://getbootstrap.com/docs/4.5/getting-started/introduction/  

- bootstrap4.5'i cdn aracılığı ile kullanıyorum.
- cdn kodlarını (link, poper, js) base.html template'ine yerleştiriyorum.
- Blocklarımızı class="container" div içerisine alıyoruz.

- v4.5 versiyonundaki starter templat ini kopyalayıp, temizlediğimiz base.html imize yapıştırıyoruz. (Yoruma alınmış kısımları silebiliriz)


base.html
```html
<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">

    <title>Umit Blog</title>
</head>
<body>
    <div class="container">
    {% block content %}
        
    {% endblock content %}
    </div>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>

</body>
</html>
```

- değişikliği gördük, şimdi bunu card componentine koyup yavaş yavaş ilerleyeceğiz.


- Navbar;
- Navbar ekleyeceğiz, navbar eklemenin farklı yollarını göreceğiz, 
- include tag i var exclude vardı ya inherit ediyorduk, bir de include edebiliyorsunuz yine onları,
- navbar kodlarımız için bir template oluşturacağız, 
- base.html'in bulunduğu klasörde navbar.html dosyası oluşturuyoruz. 
- Neden? -> base de fazla kodumuz olmasın, bizim navbar da değişiklik yaparsam eğer base.html'i fazla kurcalamayayım diye navbar için bir template oluşturuyoruz. 
- (Ayrıca https://getbootstrap.com/docs/4.5/components/navbar/ dan da istediğiniz bir navbarı alıp eklayebilisiniz, sağ tarafta olan linkler için ise birkaç kod yazmanız gerekiyor.) 
- Buradaki can alıcı nokta if bloklarının içindeki kullanıcı login ise şu linkleri göster, değilse bu linkleri göster kısmıdır. (template lerimiz daha hazır olmadığı için onların url kısımlarını körledik.)

navbar.html
```html
<header class="site-header">
    <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top ">
        <div class="container">
            <a class="navbar-brand mr-4" href="{% url 'blog:list' %}">Umit Blog</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar Toggle" 
            aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toogler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarToggle">
                <div class="navbar-nav mr-auto">
                    <a class="nav-item nav-link" href="{% url 'blog:list' %}">Home</a>
                    <a class="nav-item nav-link" href="#">About</a>
                </div>
                <!-- Navbar Right Side -->
                <div class="navbar-nav">
                    {% if user.is_authenticated %}
                        {% comment %} {% url 'logout' %} {% endcomment %}
                        <a class="nav-item nav-link" href="#">Logout</a>
                        {% comment %} {% url 'profile' %} {% endcomment %}
                        <a class="nav-item nav-link" href="#">Profile</a>
                        <a class="nav-item nav-link" href="{% url 'blog:create' %}">New Post</a>
                    {% else %}
                        {% comment %} {% url 'login' %} {% endcomment %}
                        <a class="nav-item nav-link" href="#">Login</a>
                        {% comment %} {% url 'register' %} {% endcomment %}
                        <a class="nav-item nav-link" href="#">Register</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>
</header>
```

- navbar.html template'imizi oluşturduktan sonra base.html e gidip, body'nin içine block'larımızın üstünde include ediyoruz.
    {% include 'navbar.html' %} 

base.html
```html
...
<body>

    {% include 'navbar.html' %}

    <div class="container">
        {% block content %}
            
        {% endblock content %}
    </div>
...
```

- çalıştırıyoruz, navbar'ın geldiğini gördük ama css eklememiz gerekiyor.

#### statics;

- static klasörünü oluşturup, tüm static dosyalarımızı (css, image, js) bu klasörümüzün içinde barındıracağız.
  
- django default olarak static klasörünü app'lerin altında bekler.(settings.py -> STATIC_URL = 'static/'
)

- blog app'imizin altında static klasörü, onun da altında app'imizin ismi ile (isim önemli) bir klasör daha oluşturup static dosyalarımızı buraya yerleştiriyoruz.
    blog/static/blog/

- css'ler için; static klasörünün içinde, blog klasörünün içinde main.css dosyası oluşturuyoruz.
    blog/static/blog/main.css

- Django da css, javascript, image kullanacağınız zaman yapıyı bu şekilde kuracaksınız. 
- app'in altında static diye bir klasör oluşturacaksınız, 
- içerisine blog oluşturmak size kalmış oluşturmayabilirsiniz ama application ları name spacing yapmak önemli, 
- içerisine de main.css dosyamızı oluşturup, css kodlarımızı yazıp,  
- base.html e gidip bootstrap css linkinin altına kendi css linkimizi ekleyeceğiz. 

blog/static/blog/main.css
```css
body {
    background: #fafafa;
    color: #333333;
    margin-top: 5rem;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #444444;
}

ul {
    margin: 0;
}

.bg-steel {
    background-color: #5f788a;
}

.site-header .navbar-nav .nav-link {
    color: #cbd5db;
}

.site-header .navbar-nav .nav-link:hover {
    color: #ffffff;
}

.site-header .navbar-nav .nav-link.active {
    font-weight: 500;
}

.content-section {
    background: #ffffff;
    padding: 10px 20px;
    border: 1px solid #dddddd;
    border-radius: 3px;
    margin-bottom: 20px;
}

.account-img {
    height: 110px;
    width: 110px;
    margin-right: 20px;
    margin-bottom: 16px;
}

.account-heading {
    font-size: 2.5rem;
}
```

- base.html e gidip css dosyamıza link ekleyeceğiz,
- Ancak djangoda static file ları kullanmak için base.html sayfamızın başına, en üst kısma {% load ststic %} yazmamız gerekiyor. 
    {% load ststic %}

- Link eklerken de href ine djangonun url belirtme yazım şekliyle url belirteceğiz, url de url yazıyorduk bunda ise static yazıyoruz; 
    <link rel="stylesheet" href="{% static 'blog/main.css' %}">

templates/base.html
```html
{% load static %}
...
    <link rel="stylesheet" href="{% static 'blog/main.css' %}">
...
```


#### statics - root directory; **************

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
************************************************

- Şimdi home page imize gidiyoruz, css lerimizin geldiğini ve çalıştıklarını görüyoruz, 
- login olmadığımızda navbar da gelen  menüleri görüyoruz, 
- kendi login sayfamızı/template imizi oluşturmadığımız için admin panelden login oluyoruz (djangoda session var, browserda bir sekmede login olunmuşsa diğer sekmelerde de login olarak tutuyor.) ve home page e döndüğümüzde if bloglarının çalıştığını ve login olmuş kullanıcı menülerini gösterdiğini görüyoruz. 
- Ayrıca New Post menüsüne tıkladığımızda post oluşturmak için bizim daha önce hazırladığımız create template imize gönderiyor,
- Umit Blog a tıkladığımızda list template imize gönderiyor,
- navbar ımız çalışıyor.


- base.html imizi oluşturduk,  
- navbar ımızı oluşturduk, 
- footer ekleyebilirsiniz, 
- hangi sayfaya koymak istiyorsanız oradan include edebilirsiniz.
- Veya pageination codunuz varsa pagination.html diye ayrıca yazıp, onu include edebilirsiniz daha sonra, 
- birçok şey yapabilirsiniz. 


#### list template bootstrap, fontawesome style verilmesi;

- Şimdi list.html imizi düzeltelim, yine bootstrap components cards (https://getbootstrap.com/docs/4.5/components/card/) ı biraz modifiye edip kullandık, 

- Nasıl modifiye ettik? şimdi bizim bir tane post umuz yok, birçok post umuz var onun için bir for döngüsü kullanıyoruz,
- bir liste döneceğiz listemiz: object_list nereden alıyoruz bu object_list'i? views.py da context in içine object_list olarak koymuşuz tüm published post larımızı, ve object_list imizi context içerisinde post_list template imize göndermişiz, işte o listenin elemanlarını card componentinin içerisinde göstereceğiz, 
- card componenetimiz, card class ı olan div ile başlıyor, 
  - yan yana görünmesi için row koyduk, 
  - o row u da column lara böldük, 
  - img source'unu obj'nin image ının url ini koyduk, 
  - card body de card title kısmına anchor tag ı ile detail page e link verdik, 
  - postun contentini koyuk, 
  - sonra asıl yapacağımız şeyler; 
    - mesaj sayısı, 
    - görüntüleme sayısı, 
    - like sayısını koyacağız, 
    - ayrı bir p tag ı içerisinde font awesome dan class ları alıp span tagı içerisinde bunları yerleştirdik 
    - sonra {{ obj.comment_count }} bunları modelde bir method belirleyeceğiz, bu methodlarla count sayılarını alacağız.
    - Şimdilik onları yoruma aldık ki hata vermesin.
    - Sonraki p tag ının içerisinde de ne kadar zaman önce post edildiğinin gösterimi için bir tane template tag ı var. Modelde publish date imiz vardı ya ne  yapıyordu? post objemiz oluştuğu zaman bir tarih zaman veriyor, timesince ise şu anki zaman ile post un oluşturulduğu zaman arasındaki farkı alıyor, şukadar gün şu kadar saaat önce diye aradaki farkı alabiliyoruz.
    - font awesome nereden bulduk; 
      - fontawesome artık register olmanızı istiyor, 
      - register olduktan sonra bir javascript kodu veriyor, start for free diyorsunuz, mail inizi girmenizi istiyor,   (https://fontawesome.com/start) sonra mailinize gelen link ile bize özel oluşturulmuş script codunun bulunduğu sayfaya yönlendiriyor, 
      - script codunu base.html de body nin en alt kısmına ekliyoruz. Önceden link veriyordu, şimdi script veriyor.
        <script src="https://kit.fontawesome.com/f3876d5d9f.js" crossorigin="anonymous"></script>

      - Daha sonra; 
        - yorum için comment, 
        - görüntüleme için göz, 
        - beğeni için kalp icon larını seçip span tag ının içinde yazıyoruz; 
            <i class="far fa-comment-alt ml-2"></i> şeklinde 


blog/post_list.html - Önceki;
```html
{% extends 'base.html' %}
{% block content %}

{% for object in object_list %}
<a href="{% url 'blog:detail' object.slug %}">
    <h1>{{object.title}}</h1>
</a>
<img src="{{ object.image.url }}" alt="">
<p>{{object.content|truncatechars:20}}</p>
{% endfor %}

{% endblock content %}
```


blog/post_list.html - bootsrap4.5 ile upgrade edilmişi;
```html
{% extends 'base.html' %}
{% block content %}
<h1 style="text-align: center;">Umit Blog</h1>
<div class="row mt-5">
    {% for obj in object_list %}
    <div class="col-4">

        <div class="card shadow p-3 mb-5 bg-white rounded" style="width: 18rem; height: 25rem;">
            <img src="{{ obj.image.url }}" class="card-img-top" alt="post_image">
            <hr>
            <div class="card-body">
                <h5 class="card-title"><a href="{% url 'blog:detail' obj.slug %}">{{obj.title}}</a></h5>
                <p class="card-text">{{obj.content|truncatechars:20}}</p>
                <p> 
                    {% comment %} {{ obj.comment_count }} {% endcomment %}     
                    <span><i class="far fa-comment-alt ml-2"></i></span>
                    {% comment %} {{ obj.view_count }} {% endcomment %}     
                    <span><i class="fas fa-eye ml-2"></i></span>
                    {% comment %} {{ obj.like_count }} {% endcomment %}     
                    <span><i class="far fa-heart ml-2"></i></span>
                </p>
                <p class="card-text"><small>
                        Posted {{ obj.publish_date|timesince }} ago.
                    </small>
                </p>

                </p>
            </div>
        </div>
    </div>

    {% endfor %}
</div>
{% endblock content %}

```

- çalıştırdık, bootstrap ve yorum için comment, görüntüleme için göz, beğeni için kalp fontawesome icon larının görünür hale geldiğini gördük.


#### postlar için yorum, görüntülenme, beğeni algoritmaları..

- views.py'da comment, görüntülenme, beğeni algoritmalarının kurulması;
- home/list page de post card ların içerisindeki postların, 
  - yorum için comment, 
  - görüntüleme için göz, 
  - beğeni için kalp icon larının yanında counter/sayılarını koyacağız,

- Peki bunları nerede hesaplayabiliriz?
  
- Bir post'un comment, görüntülenme, like sayılarına Post modeli üzerinden alabiliriz, 

- çünkü bu sayıları göstereceğimiz list template'ini, post_view'imizde Post modelinden çektiğimiz ve context içinde gönderdiğimiz objeler oluşturuyor. 

- post_list.html template inde biz for döngüsü ile, post_view'den gelen Post modelinin objeleri üzerinde dönüyoruz.

- Bu yüzden Post modelinde bu hesaplamaları yapabiliriz. Çünkü diğer modeller (Comment, Like, PostView(post görüntülenmesi)) Post modelinin child modelleri.

- Biz bu Post modelinde, parent modelden child modeldeki object'lere erişeceğiz, child modeldeki object'leri saydırıp, post_list.html template'ine göndereceğiz. 

- Django, parent modelinden child modeline otomatik bir ilişki oluşturur. Bu ilişki; 
  - 1. varsayılan olarak "related_name" veya,
  - 2. model adının küçük harflerle çoğul haliyle (comment_set) erişilir. Burada 2. yolu kullanacağız.  

- parrent modelden child modeldeki object'lere şu şeklide erişebiliyoruz;
    "child_model_name"_set

- post_list view'imizde de Post modelinden object'leri filter edip post_list template'ine gönderdiğimiz için de bu saydırma methodlarını Post modelinde yazdık.


##### comment count;

- models.py'a gidip oluşturduğumuz Post modelinin altına, str metodunun da altına, comment_count() methodumuzu yazıyoruz, içerisine self alacak çünkü bu bizim Post class ımızın methodunu yazıyoruz,
    def comment_count(self):
  
- bir post un birden çok comment'i olabilir ama bir comment in bir post'u olabilir. Post model -> parrent, Comment model -> child.

- Yani burada parent model olan Post modelinin bir object'inin ilişkili olduğu, child model olan Comment modeldeki tüm object'lerine erişmemiz ve onları count() methoduyla saydırmak istiyoruz. 

- post object'ine ait tüm commentlere erişmek için; child model'in ismini küçük harfle yazıp, _set eklememiz yeterli;
    comment_set

- parrent modeldeki objenin, child modelde ilişkili olduğu tüm objectler için ise; (.all() yazmaya gerek de yok aslında.)
    <!-- comment_set -->
    comment_set.all()

- parrent modeldeki objenin, child modelde ilişkili olduğu tüm objectlerin sayısı için ise;
    <!-- comment_set.count() -->
    comment_set.all().count()

- Nihayet, parrent modeldeki objenin, child modelde ilişkili olduğu tüm objectlerin sayısını döndüren methodumuz için ise;

    def comment_count(self):
        <!-- return comment_set.count() -->
        return comment_set.all().count()

- djangonun ORM yapısından dolayı biraz karışıkmış gibi görünüyor.


##### like count;

- like count için de;
    def like_count(self):    
        return self.like_set.all().count()

##### view count;

- view count için de;    
    def view_count(self):     
        return self.postview_set.all().count()

- child dan parenta ulaşmak ise çok kolay;
- child modelin parrent model ile ilişkili olduğu field ile child modelinden parrent modeldeki objeye ulaşılabilir. Örneğin comment modeldeki bir objenin post category'si için;
    comment = Comment.objects.get(id=1)  # İlgili Comment objesini al
    category = comment.post.category    # Comment objesinin bağlı olduğu Post'un kategorisine ulaş


blog/models.py
```py
...
class Post(models.Model):
    ...
        
    def __str__(self):
        return self.title
    
    def comment_count(self):
        return self.comment_set.all().count()
    
    def view_count(self):
        return self.postview_set.all().count()
    
    def like_count(self):
        return self.like_set.all().count() 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ...

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ...

class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ...
...
```


##### list template içinde modeldeki method'u yakalama ;

- post_list.html'e gidip oluşturduğumuz count method lara ulaşacağız, 
- yoruma aldığımız yerleri yorumdan kurtarıyoruz, buradan methodlara ulaşabiliyoruz, 
- object oriented da cross oluşturduğumuzda method'a ".method()" yazıp ulaşabiliyorduk ya, ama method da sonuna parantez koyuyorduk method un. Burada template'teyken method a ulaşırken sonuna parantez koymuyoruz. 
- methodları span tag leri arasına icondan hemen sonra koyuyoruz.
    obj.comment_count
    obj.view_count
    obj.like_count

- algoritmayı view de değil de model de yazdık, modelde de class lardan yararlandık, class lara method yazabiliyoruz, methodlarla bu sayılara ulaşabiliyoruz, 
- bunu view'de yazıp, context'in içerisine koyup da yapabilirdik ama bu method daha kolay. Yani bütün logic inizi view e koymanıza gerek yok, modele de koyabilirsiniz, - template e de koyabilirsiniz, üçüne de koyabilirsiniz, ama ana logic view de olur.

blog/templates/blog/post_list.html> ->
```html
...
    <p> 
        {% comment %} {{ obj.comment_count }} {% endcomment %}     
        <span><i class="far fa-comment-alt ml-2"></i>{{ obj.comment_count }}</span>
        {% comment %} {{ obj.view_count }} {% endcomment %}     
        <span><i class="fas fa-eye ml-2"></i>{{ obj.view_count }}</span>
        {% comment %} {{ obj.like_count }} {% endcomment %}     
        <span><i class="far fa-heart ml-2"></i>{{ obj.like_count }}</span>
    </p>
...
```

- çalıştırdık (runserver) sayıları(0) gördük. 
- admin panelden publish postlardan bir tanesine like, post_view, comment ekledik ve home/list page de count ettiğini, logic in çalıştığını gördük.


- blog application ı bitireceğiz, 
- user application ını kuracağız , orada authenticon kısmını kuracağız, profile page ini oluşturacağız, 
- genel çatıyı kurduk, biraz daha süsleyeceğiz, birkaç tane daha form (comment form) ekleyeceğiz,


#### detail view-urls-template eksik kalan kısım; 

- şimdi detail view imizi şekillendireceğiz, 
- blog/views.py' a gidiyoruz, 
- list view de olduğu gibi; 
  - like 
  - message ve 
  - gösterme sayısını yerleştireceğiz, 
  - alta bir de comment formu koyacağız, kullanıcıdan comment almak için bir form oluşturmamız gerekiyor, zaten comment modelimiz var, bu modelden modelForm ile bir tane form oluşturacağız (zaten oluşturmuştuk), bu formu da detail template imize göndereceğiz, zaten CommentForm umuzu modelForm dan oluşturmuştuk forms.py'da. 
  - ModelForm dan inherit ediyoruz, model olarak Comment modelini kullanıyoruz, içerisine sadece content koyuyoruz, neden sadece content koyuyoruz?, zaten kullandığımız Comment modelinde user forignKey, post da forignKey, time_stamp i kendisi veriyordu, kullanıcıdan tek istediğimiz form'a comment ini yazması, 
  - daha sonra bunu view de göstereceğiz, view de nerde? post detail e gidince kullanıcı, post_detail'in içerisinde, sayfasında render edeceğiz bu formu,

- formu nasıl render ediyorduk? CommentForm u forms.py dan import ediyoruz, bir değişkene(form) tanımlıyoruz, get isteği olursa boş form'u context'in içinde obj ile birlikte render ededceğiz.
```py
    from .forms import (
    PostForm,
    CommentForm,
    )

    def post_detail(request, slug):
        form = CommentForm()

        context= {
        'object': obj,
        'form': form
        }
```

- zaten object imizi almışız, 
- arkasından user bir post işlemi yapacak, comment i POST edecek  ve;
    if request.method == 'POST':     

- eğer request method post ise, formu user'dan post ile gelen veri ile dolduruyoruz, formu POST methoduyla request edilen verilerle doldur,
    form = CommentForm(request.POST)   

- sonra formun valid olup olmadığının kontrolü,    
    if form.is_valid(): 

- ardından Post ta yaptığımız gibi; 
  - önce bir obje oluşturacağız, formu save edeceğiz ama db ye kaydetmeyeceğiz neden? bizim form un içerisine (bakın modelde db'ye kaydetmemiz gereken ne var post ve user)  post ve user'ı formun içerisine koymamız gerekiyor, time_stamp i zaten create ettiği zaman db kendisi koyuyor, contenti zaten kullanıcıdan alıp gönderiyoruz, bizim user ve post u form ile birlikte db ye göndermemiz gerekiyor, yani post create'te yaptığımızı burada tekrar edeceğiz, 
  - comment diye bir değişken oluşturuyoruz, sonra formu save et comment'e tanımla, commit false diyerek de commit etmedik yani db'ye göndermedik, bunun default u True dur,  (db ye göndermedik henüz)
    comment = form.save(commit=False)    

  - şimdi artık biz bu comment objesine user ı koymamız lazım db ye göndermeden önce. request objesinin içerisindeki user ı al yani login olmuş user ı al comment objesine koy,
    comment.user = request.user     
  
  - sonra bu comment objesinin bir de post unu göndermemiz lazım, zaten yukarıda obj değişkeniyle slug=slug olan Post u almıştık, obj değişkenimiz yani post umuzu da comment e koyuyoruz  ve formumuzu doldurmuş oluyoruz,
    comment.post = obj         

  - ondan sonra comment.save() ile  db ye bunu kaydetmiş olacağız,  
    comment.save()
  
  - tabi her post işleminden sonra return redirect() yapıcaz ama tabi şöyle olacak, comment form'um  detail page in altında olacağı için post ettiğimiz zaman bizim yine bu sayfada kalmamız gerekecek, aynı sayfayı render etmemiz gerekecek, onun için return redirect('blog:detail', slug=slug)    yani aynı sayfada render etmesi için unique değer olan slug'ı da eklememiz gerekiyor ki hangi detail sayfası olduğunu bu unique değer ile belirtiyoruz,  
    return redirect('blog:detail', slug=slug)

  - Bunu farklı şekillerde de yapabilirsiniz mesela;   
    return redirect(request.path)     
  - bu da aynı bulunduğu sayfaya redirect eder, ancak ilk kullanım daha iyi bir kullanım.

- daha sonra da formu muzu context içerisinde template imize göndereceğiz, 
context= {
    'object': obj,
    'form': form
}

blog/views.py
```py
...
from .forms import (
    PostForm, 
    CommentForm
)

...

def post_detail(request, slug):
    # print(request)
    # print(request.user)
    # print(request.POST)
    # print(request.GET)
    # print(request.path)
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug)  # slug=learn-drf-3c78be2186
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
        'object': obj,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)

...
```

- view imizi yazdık ve formumuzu context içerisinde detail template imize gönderdik, 
- şimdi bu view'i detail.html template imizde, page imizde render edeceğiz, 
- post_detail.html'e gidiyoruz, 
  - formumuzu yerleştiriyoruz, 
  - yine aynı sayfaya gönderdiğimiz için action ımızı yine boş bırakıyoruz , 
  - methodumuz post olacak, 
  - method post olduğu için csrf imizi koyuyoruz, 
  - sonra formumuzu render ediyoruz, 
  - form'un içine bir de submit button u koyuyoruz,
  - save edip page imize gidiyoruz, 
  - tabi şuan sadece comment'i oluşturacak, 


blog/post_detail.html
```html
{% extends 'base.html' %}
{% block content %}

<h1>{{ object.title }}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{ object.content }}</p>
<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Comment</button>
</form>

{% endblock content %}
```

- çalıştığını kontrol edelim, 
- post'umuza comment yazıyoruz,
- admin panelinden Comments tablomuzdan da commentimizi görüyoruz. 
- çalışıyor. Ancak yapılan bu comment'in contentini sadece admin panelden görebiliyoruz.

- Bu detail page'inde, yapılan bu commentleri;  
  - kim yapmış, 
  - ne zaman yapmış, 
  - içeriği ne, 
- post'un detail'inin altında, comment form'un altında, gösterelim.

-  tıpkı post_list template'inde, Post modelinin child modellerindeki postların ilişkili olduğu comment, like,view'lerin count'larını hesaplayıp da post'un hemen altında gösterdiğimiz gibi, 
-  aynı şekilde post_detail page'inde post'un comment'lerini aynı yöntemle çekip, post'un detail'inin altında göstereceğiz; 

- Post modelimizden çektiğimiz, post_detail view imizden template imize context te gönderdiğimiz object in içerisinde neler var bir bakalım? 
- models.py'daki modelimizi açalım,
  - Post modelimizin child modeli olan Comment modelinde, her Post objesine ait commentler var.
  - Biz post_detail view'inde, Post modelinden çektiğimiz her Post objesinin ilişkili olduğu, child modeli olan Comment modelindeki objelerine erişip, onları listeleyeceğiz.
  - Bunun için yine bir method oluşturacağız. Bu method ile, Her Post objesinin ilişkili olduğu child modeldeki (Comment) tüm objelere ulaşıyoruz.
  - Post modelinin içinde yazdığımız method ile, bu modelin herbir objesi ile ilişkili olan, child modeldeki (Comment) tüm objelerini (comment_set) al!
    def comments(self):
        return self.comment_set.all()  
    
    (Normalde Comment ama burada comments küçük harfle kullanıyoruz.)  bu Post classından oluşmuş bir objenin, yani benim post'umun altına yapılmış bütün comments lere bu method la ulaşabileceğiz.


blog/models.py
```py
...

class Post(models.Model):
    ...
    
    def comments(self):
        return self.comment_set.all()
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
    def __str__(self):
        return self.user.username
...
```

- daha sonra, post_detail.html'e gidip; 
  - detail view'inde, Post modelinden çekip de detail template'ine gönderdiğimiz her bir post objesinin, 
  - Post modelde yazdığımız comments() metoduyla eriştiğimiz child modeli olan Comment modelindeki tüm olbjelerine ait olan commentleri,
  - bir for döngüsüyle detail template'imizde göstereceğiz.
 
    for comment in object.comments
        (post_detail view imizde context içerisinde gönderdiğimiz objemizin ismi neydi object ti, modelimizde methodumuza ne isim vermiştik comments), yukarıdaki method larla sayılarına ulaşmıştık, buradaki method ile de sadece commentleri alacağız sayısını değil, 
    {{ comment.content }}
    {% endfor %}

- çalıştığını gördük,  kim tarafından yazıldığını p tagı içerisinde 
    <p>comment by {{ user }}</p>

blog/post_detail.html
```html
{% extends 'base.html' %}
{% block content %}

<h1>{{ object.title }}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{ object.content }}</p>
<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Comment</button>
</form>
<hr>
{% for comment in object.comments %}
<p>comment by {{ user }}</p>
{{ comment.content }}
<hr>
{% endfor %}

{% endblock content %}
```


##### like;
- şimdi like yapmanın mantığını/logic'ini oluşturacağız.
- like için bir view yazacağız.
- Bir kullanıcı, bir post'un like .. tıklayınca db'deki Like modelindeki ilgili like object'inin sayısını artıracak,   icon'ına like objesi oluşturacağız.oluşturacağız, onun için blog/views.py'da bir fonksiyon yazacağız, 
- user like'a tıklayınca db deki like sayısını arttıracak, aynı kullanıcı tekrar tıklarsa like lamışsa geri alacak,
- bunun algoritmasını kuruyoruz, en alt satıra gelip;  
  - biz burada yine db de bir işlem yapacağımız için yani db de bizim like modelimiz var like modelimize bir tane veri ekleyeceğiz, tekrar tıklanırsa silinmesi gerekiyor, bizim bu işlemi post ile yapmamız gerekiyor,
    def like(request, slug):
        if request.method == 'POST':
     
   - şimdi burada bir algoritama kurmamız gerekiyor, ilk önce bizim hangi post u like layacağımızı almamız gerekiyor, bizim yine like ın içerisine request ile birlikte bir slug göndermemiz gerekiyor, slug la bizim hangi post a işlem yapacağımızı bilmemiz gerekiyor, neden bilmemiz gerekiyor?, model de like a gelirsek içinde bir post değişkenimizin olduğunu görüyoruz, hangi post a like yapacağımızı bilmemiz gerekiyor, bunun için request le birlikte slug da gönderiyoruz,
    def like(request, slug):
        if request.method == 'POST': 

   - sonra, burada yine obj diyoruz, ve herzaman yaptığımız gibi Post un içerisinden slug ile hangi post a like yapacağımızı biliyoruz artık;
     obj = get_object_or_404(Post, slug=slug)    

   - artık bununla hangi post a like yapacağımızı biliyoruz,
   - şimdi db de bizim bu post a like vermişmiyiz vermemişmiyiz bunun kontrolünü yapıp, eğer like verilmişse sayıyı bir düşürecek, verilmemişse sayıyı bir artıracağız. Yine şimdi burada like_qs (query set) diye bir değişken oluşturup;
    like_qs = Like.objects.filter(user=request.user, post=obj)  
    
   - like queryset diye bir değişken oluşturuyoruz, (modelden Like modelimizi import ediyoruz, ve filtreliyoruz) bunda da db de yaptığımız bir like var mı onu filtre edeceğiz, kontrol edeceğiz, 
     - filter içinde; user ımız şuandaki request.user ımıza eşit olacak, post ise hangi post olması gerekir? şuanki işlem yaptığımız post a eşit olması lazım yani obj ye eşit olması lazım. 
     - Şimde eğer bundan bir değer dönüyorsa demekki biz bu postu like lamışız o zaman tıkladığımız zaman sayıyı bir düşürecek, eğer like ımız yoksa sayıyı bir arttıracak ; 
        if like_qs.exists():     
        
     - exists() diye bir method var, genelde query set lerde exists() kullanılıyor, yani bu like_qs ten elde ettiğimiz birşey varsa;
       - exists() olmadan da oluyor.
       - exists() kullanılarak yapılmış hali:
        
        if like_qs.exists():
           like_qs[0].delete()  -> o var olanı sil,

        else:       -> yok eğer dolu değilse de 
            Like.objects.create(user=request.user, post=obj)    -> şuanki user ımızı ve şuanki post umuzu al oluştur.
     
     - bunları yaptıktan sonra redirect ile yine detail page de kalmasını söylüyoruz,  
        return redirect('blog:detail', slug=slug)

blog/views.py
```py
from .models import Like
...


def like(request, slug):
    if request.method == 'POST':
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect('blog:detail', slug=slug)
```

- views.py da view imizi yazdık, şimdi buna bir url tanımlayalım, blog app imizin urls.py'ına gidip;

blog/urls.py
```py
from .views import like

app_name='blog'
urlpatterns = [
    ...,
    path('<str:slug>/like/', like, name='like'),
]
```

- oluşturduğumuz bu like viewi çalıştırmak için detail page template'imizde bir form (action olarak view'in endpointini yazacağız, method POST olacak) kullanacağız.
- tabi şuan sadece html yazarak koyuyoruz daha sonra stillendireceğiz, 
- detail template'imizin en altına gelip;
  - kullanıcıdan like bilgisi almak için form kullanıyoruz,
  - bunun için forms.py da form oluşturmadık, kendimiz de html de form oluşturabiliriz, 
  - burası önemli bu formdaki action ımıza nereye gitmesini/hangi endpoint'e istek atıp da hangi view'i çalıştırmasını istiyorsak orasının url ini dinamik olarak tanımlıyoruz, burada blog app imizin 'like' url ine gitmesini ve de giderken objectin slug ını almasını istiyoruz,
  - action kısmında blog app'in 'like' url ine object in slug ıyla gönderme sebebimiz; 
    - bu formdaki verilerle views.py daki like view inde işlem yapmamızı sağlamak için ve de like view ine de urls.py da tanımladığımız like url i vasıtasıyla ulaşabildiğimiz için form un action kısmına blog app inin like url ini vermemiz gerekiyor, arkasından da objenin slug verisiyle hangi post olduğunu belirtmemiz gerekiyor.
    - methodumuz da post olacak.
    - method post olduğu için csrf token ımızı koyuyoruz,
    - form için iki tane input oluşturacağız ama inputlarımızı göstermeyeceğiz, neden; 
      - input oluşturuyoruz? model.py a bakarsak Like modelimizde bir user bir de post bilgisinin girilmesi gerekiyor ama biz bunları otomatik olarak zaten view imizde def like içerisinde Like_objects.create içerisine (user=request.user, post=obj)  ile create ederken koyuyoruz. Dolayısıyla input type text değil de hidden yapıyoruz ki kullanıcı bunu görmesin, name i bu sefer manuel vermek zorundayız çünkü bunu kendimiz hazırlıyoruz, django name i default olarak şu şekilde veriyor; field ın adı ne ise post diyeceğiz.
      - diğer input u da aynı şekilde bu sefer name i ne olacak db de ismi ne ise onu vereceğiz yani user diyeceğiz.
      - bir tane de submit button oluşturuyoruz, şimdilik Like diyoruz daha sonra fontawesome dan alacağımız icon ile değiştireceğiz.
```html
<form action="{% url 'blog:like' object.slug %}" method="POST">
    {% csrf_token %}
    <input type="hidden" name="post">
    <input type="hidden" name="user">
    <button type="submit">Like</button> {{ object.like_count }}
</form>
```


- hemen ardına da post_list.html de olduğu gibi like sayısını  {{ object.like_count }}  ile göstersin istiyoruz. 

blog/post_detail.html
```html
{% extends 'base.html' %}

{% block content %}

<h1>{{ object.title }}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{ object.content }}</p>

<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Comment</button>
</form>
<hr>

{% for comment in object.comment %}
    <p>comment by {{ user }}</p>
    {{ comment.content }}
    <hr>
{% endfor %}

<form action="{% url 'blog:like' object.slug %}" method="POST">
    {% csrf_token %}
    <input type="hidden" name="post">
    <input type="hidden" name="user">
    <button type="submit">Like</button> {{ object.like_count }}
</form>

{% endblock content %}
```

- çalıştırıyoruz, new post oluşturuyoruz, title'ına tıklayıp detail page ine gidiyoruz, like buttonuna tıklıyoruz bir artıyor, bir daha tıklıyoruz bir azalıyor, yani çalışıyor, exists() demeye gerek yokmuş, 
- başka bir kullanıcıyla deneyelim, admin panelden başka bir kullanıcı oluşturuyoruz, staff ve superuser yetkisi de veriyoruz (çünkü sadece admin panalden login olunabiliyor şuanda onun için yeni kullanıcı da ancak admin panelden login olabileceği için superuser yetkisini veriyoruz ki login olsun ve post detail paginden like yapabilsin)  login oluyor, deniyoruz, çalışıyor.  


- EKSTRA    /// Ekstra Başladı ///
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


##### post'un görüntülenme sayısının gösterilmesi (view_count) ;

- Bir post'un user'lar tarafından kaç defa görüntülendiğinin gösterilmesi işlemi.
- Bu işlemde bir user bir postun detail'ini gördüğünde/açtığında, bu iş için oluşturduğumuz PostView modelinde bir obje create edilecek.
- Daha önce Post modelinde oluşturduğumuz view_count() methodu ile de PostView modeli/tablosundaki kayıtlı obje/görüntülenme sayısı hesaplanıp tepmlate'te bu sayı gösterilecek.
- Bu projede, bir user bir postu birden fazla da görüntülese, postun görüntülenme sayısını sadece 1 artırması kurgulanmıştır.
- Bu işlemin logic'ini post_detail view'inde yapıyoruz.
- Yani post_detail view'ini tetikleyen url'e istek atıldığında;
  - post_detail view çalışacak,
  - bu view'de de bir if condition ile eğer user authenticate ise,
  - get_or_create() methodu ile PostView modelinde/tablosunda obje create etmişse/post'u görüntülemişse bir şey yapmayıp sadece getiriyor, veya obje create ediyor.
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)
        # user'ın eğer PostView modelinde objesi varsa getiriyor, yoksa PostView modelinde obje create ediyor.

blog/views.py
```py
from .models import (
    ...,
    PostView
)

def post_detail(request, slug):
    form = CommentForm()
    obj = get_object_or_404(Post, slug=slug) # slug=learn-drf-3c78be2186
    
    #! postun görüntülenme istatistiği için;
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=obj)
        # user'ın eğer PostView modelinde objesi varsa getiriyor, yoksa PostView modelinde obje create ediyor.
     
    ...

    context = {
        'object':obj,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context) 
```

- Test ediyoruz, Çalışıyor.
- Login olmuş authenticate bir user ile bir post'un detail'ine eriştiğimizde PostView modeli/tablosunda bir obje/görüntülenme create ediliyor,
- Bu create edilen obje/görüntülenmeler de Post modelindeki view_count() methodu ile sayılıp, post_detail view'inden template'e gönderiliyor ve detail template'i ile birlikte list template'inde bu istatistikler görüntüleniyor.
- Bir user bir post'u birden fazla dahi görüntülese istatistiklerde sadece 1 artırabiliyor.


- şuanda url imizi korumuyoruz daha, yani herhangi bir user, detail page imizin url kısmına '/update/' veya '/delete/' yazıp istek attığında bu sayfalara ulaşamaması lazım, onlara geleceğiz.


###### user'ın sahiplik durumuna göre, post'un delete/update button'larının gösterilmesi;
- eğer user authenticate ise update ve delete buttonları görünecek, değilse user a update ve delete buttonlarını göstermeyeceğiz, 

- şimdi o işlemi de halledelim, detail.html'e gidiyoruz, 
- bizim, kullanıcının kendi post larını update ve delete yapabilmesi için sadece kendi post larının detail page template'inde update ve delete'i linklerini gösterecek, ancak kendine ait olmayan post ların detail page'inde bunları göstermeyecek şekilde bir logic kurmamız gerekiyor,
- yani bu post bu user a mı ait? ;
- detail template'inde bir tane if statement kuruyoruz, 
    {% if user.id == object.author.id %}   

- user olmuş kişi ile post un author unun id si eşit ise, yani login olmuş kişi ile postun sahibi aynı kişi ise;
    <a href="{% url 'blog:update' object.slug %}">Update</a>   
    Update'e slug sayesinde spesific obje ile  git   

    <a href="{% url 'blog:delete' object.slug %}">Delete</a>   
    Delete e slug sayesinde spesific obje ile git

blog/post_detail.html
```html
{% extends 'base.html' %}

{% block content %}

<h1>{{ object.title }}</h1>
<img src="{{ object.image.url }}" alt="">
<p>{{ object.content }}</p>

<form action="" method="POST">
    {% csrf_token %}
    {{ form }}
    <button type="submit">Comment</button>
</form>
<hr>

{% for comment in object.comments %}
    <p>comment by {{ user }}</p>
    {{ comment.content }}
    <hr>
{% endfor %}
  
<form action="{% url 'blog:like' object.slug %}" method="POST">
    {% csrf_token %}
    <input type="hidden" name="post">
    <input type="hidden" name="user">
    <button type="submit">Like</button> {{ object.like_count }}
</form>
<br>

{% if user.id == object.author.id %}
    <a href="{% url 'blog:update' object.slug %}">Update</a>
    <a href="{% url 'blog:delete' object.slug %}">Delete</a>
{% endif %}

{% endblock content %}
```

- test ediyoruz; user'ın create ettiği post'ların detal'inde update ve delete buttonları görünüyor ve tıklayan user update/delete page'lerine yönlendiriliyor. Fakat başka bir user'ın create ettiği post'un detail'i görüntülenirken update/delete buttonları görünmüyor.

- Ama bizim bir güvenlik açığımız var burada, ne o? user ın sahibi olmadığı postlar ile ilgili update, delete buttonları görünmüyor ama detail page inde iken url e "/update/" veya "/delete/" yazarsa o sayfalara girebiliyor, yani kendine ait olmayan postları update/delete edebiliyor, bu bir güvenlik açığı.

- url imizi view imizde koruyabiliriz. views.py'a gidiyoruz;
- post_delete view imizde obj tanımladıktan sonra hemen altına 
    if request.user.id != obj.author.id:  
    (burda id leri yazmasanız da olur ama garanti olsun diye yazıyoruz.)
    return HttpResponse('You are not authorized!' )      
    (tabi HttpResponse u da import etmeliyiz.)

    return redirect('blog:list')    
    (list sayfasına da redirect edebiliriz.)

- çalıştırıyoruz, artık user, sahibi olmadığı post ların detail page inde iken url'e delete yazıp delete page ine gitmeye çalışırsa list page ine redirect ediliyor.
- veya message vereceğiz, message a daha gelmedik.

- post_update view imiz de de aynı kodu yazıyoruz..
çalıştırıyoruz, artık user, sahibi olmadığı post ların detail page inde iken url e "update" yazıp update page ine gitmeye çalışırsa list page ine redirect ediliyor.

blog/views.py
```py
...

def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)

    #! url'i yetkisiz userdan koruma
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        return redirect('blog:list')

    if form.is_valid():
        form.save()
        return redirect('blog:list')
    context={
        'object':obj,
        'form':form
    }
    return render(request, 'blog/post_update.html', context)
    
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    
    #! url'i yetkisiz userdan koruma
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        return redirect('blog:list')

    if request.method == 'POST':
        obj.delete()
        return redirect('blog:list')
    context = {
        'object':obj
    }
    return render(request, 'blog/post_delete.html', context)
```

- Şuan url imizi de güvenlikli hale getirdik. 
- Daha sonra authentication modülüyle birlikte login require koyacağız, yani login olmayan userlar bazı işlemleri (comment,like gibi) yapamayacak. Bu işlemler içinuser'ın login olması gerekecek.



- Formlarımız çirkin görünüyor, djangonun form düzenleme paketi olan crispy form kullanacağız.
    https://django-crispy-forms.readthedocs.io/en/stable/install.html

- Önce install edeceğiz, arkasından settings.py da INSTALLED_APPS e ekleyeceğiz. 
- default olarak uni-form ile gelen bootstrap i bootstrap4 e çevireceğiz.
- bootstrap4'ü de install ediyoruz.

```bash
- pip install django-crispy-forms
- pip install crispy-bootstrap4
- pip freeze > requirements.txt
```


settings.py
```py
INSTALLED_APPS = [
    ...
    # third_party_package,
    'crispy_forms',
    "crispy_bootstrap4",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

```


```html
{% load crispy_forms_tags %}

<form method="post" class="uniForm">
    {{ my_formset|crispy }}
</form>
```
şeklinde kullanılıyor..


- Şimdi post_detail.html template inin html-css kısmını değiştiriyoruz; üzerinden bir daha geçiyoruz. 
- djangonun crispy forms paketi ile formlarımızı güzelleştirdik, (aşağıda kurulumunu izah ediyoruz.)
card objesi içerisine image ı koyduk, sonra title ı koyduk, 

post_detail.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<!-- <div class="card mb-3"> -->
<div class="container card mb-3" style="width: 40rem;">    
    <img src="{{ object.image.url }}" class="card-img-top" alt="post_image">
    <div class="card-body">
        <h2 class="card-title">{{ object.title }}</h2>
        <hr>
        <div>
            <span><i class="far fa-comment-alt ml-2"></i>{{ object.comment_count }}</span>
            <span><i class="fas fa-eye ml-2"></i>{{ object.view_count }}</span>
            <span><i class="far fa-heart ml-2"></i>{{ object.like_count }}</span>
            <span class="float-right"><small>Posted {{ object.publish_date|timesince }} ago.</small></span>
        </div>
        <hr>
        <p class="card-text">{{ object.content }}</p>
        <hr>
        <div>
            <h4>Enjoy this post? Give it a LIKE!</h4>
        </div>
        <div>
            <form action="{% url 'blog:like' object.slug %}" method="POST">
                {% csrf_token %}
                <input type="hidden" name="post">
                <input type="hidden" name="user">
                <button type="submit"><i class="far fa-heart fa-lg"></i></button>
                {{ object.like_count }}
            </form>
            <hr>
            <!-- {% if user.is_authenticated %} -->
                <h4>Leave a comment below</h4>
                <form action="" method="POST">
                    {% csrf_token %}
                    {{ form | crispy}}
                    <button class="btn btn-secondary btn-sm mt-1 mb-1" type="submit">SEND</button>
                </form>
                <hr>
                <h4>Comments</h4>
                {% for comment in object.comments %}
                <div>
                    <p>
                        <small><b>Comment by {{ user.username}}</b></small> - <small>{{ comment.time_stamp|timesince }} ago.</small>
                    </p>
                    <p>
                        {{ comment.content }}
                    </p>
                </div>
                {% endfor %}
                <hr>
                <!-- {% else %} -->
                        {% comment %} {% url 'login' %} {% endcomment %}
                <!-- <a href="#" class="btn btn-primary btn-block">Login to comment</a> -->
            <!-- {% endif %}        -->
        </div>
    </div>
    <div class="m-3">
        
        {% if user.id == object.author.id %}
        <a href="{% url 'blog:update' object.slug %}" class="btn btn-info">Edit</a>
        <a href="{% url 'blog:delete' object.slug %}" class="btn btn-danger">Delete</a>
        {% endif %}
    </div>
</div>

{% endblock content %}
```


- Tamam artık tüm template lerdeki (post_create.html, post_update.html) formlarımızı crispy ile güzelleştiriyoruz. 
- {% load crispy_forms_tags %}  ve {{form|crispy}}    ile

önceki post_create.html
```html
{% extends 'base.html' %}
{% block content %}

<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form.as_p}}
    <button type="submit">POST</button>
</form>

{% endblock content %}    
```

sonraki post_create.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form|crispy}}
    <button type="submit">POST</button>
</form>

{% endblock content %}    
```

önceki post_update.html
```html
{% extends 'base.html' %}
{% block content %}

<h2>Update {{ object.title }}</h2>
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Update</button>
</form>

{% endblock content %}  
```

sonraki post_update.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<h2>Update {{ object.title }}</h2>
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Update</button>
</form>

{% endblock content %}    
```

- çalıştırdık, login olduğum user ile yapılmış bir post u update etmeye çalıştığımda karşımıza gelen sayfa crispy ile düzeltilmiş sayfa olduğunu gördük, çalışıyor..


- SORU: 
  - crispy e nasıl ayar yapılır? sayfayı tam olarak kaplamasın. bunu div'e vereceğimiz class ile mi yapabiliriz?
  - div e class vererek de olur, 
  - forms da vidget ile oluşturduğunuz field lara class verebiliyorsunuz, 
  - classda bootstrap class ını seçip daha küçük form olarak o class ı değiştirebilirsiniz, 
  - inputlara class vermek istiyorsanız vidget attribute ü ile class verebilirsiniz. 
  - veya bir div içeririsine alıp divin boyutunu değiştirebilirsiniz.


- Birkaç şey eksik kaldı, view count u koyacağız, 

- Şimdi post_create.html template inin html-css kısmını değiştiriyoruz, birkaç tane class verdik bootstrap ile ; djangonun crispy forms paketi ile de formumuzu güzelleştirdik,

önceki post_create.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form|crispy}}
    <button type="submit">POST</button>
</form>

{% endblock content %}    
```

sonraki post_create.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="row">
    <div class="col-md-6 offset-md-3">
        <h3>Blog Post</h3>
        <hr>
        <form action="" method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            {{form|crispy}}
            <button type="submit" class="btn btn-outline-info">POST</button>
        </form>
    </div>
</div>
{% endblock content %}
```


Şimdi post_delete.html template inin html-css kısmını değiştiriyoruz, birkaç tane class verdik bootstrap ile ; djangonun crispy forms paketi ile de formumuzu güzelleştirdik, Burada load static de denmiş ama yazılmasa da olur.

önceki post_delete.html
```html
{% extends 'base.html' %}
{% block content %}

<p>Are you sure delete {{ object.title }}</p>
<form action="" method="POST">
    {% csrf_token %}
    <a href="{% url 'blog:list' %}">Cancel</a>
    <button type="submit">Yes</button>
</form>

{% endblock content %}
```

sonraki post_delete.html
```html
{% extends 'base.html' %}
<!-- {% load static %} -->
{% block content %}

<div class="row mt-5">
    <div class="col-md-6">
        <div class="card card-body">
            <p>Are you sure delete "{{ object }}"?</p>
            <form action="" method="POST">
                {% csrf_token %}
                <a href="{% url 'blog:list' %}" class="btn btn-warning">Cancel</a>
                <input type="submit" class="btn btn-danger" name="Confirm" />
                <!-- <button type="submit" class="btn btn-danger">Yes</button> -->
            </form>
        </div>
    </div>
</div>

{% endblock content %}
```


Şimdi post_update.html template inin html-css kısmını değiştiriyoruz, birkaç tane class verdik bootstrap ile ; djangonun crispy forms paketi ile de formumuzu güzelleştirdik.

önceki post_update.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<h2>Update {{ object.title }}</h2>
<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Update</button>
</form>

{% endblock content %}
    
```

sonraki post_update.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<div class="container card mb-3 pb-3">
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <h3>Update Post</h3>
            <hr>
            <form action="" method="POST" enctype="multipart/form-data">
                {% csrf_token %}
                {{ form|crispy }}
                <button type="submit" class="btn btn-outline-info">Update</button>
            </form>
        </div>
    </div>
</div>

{% endblock content %}
```

- test ediyoruz; 
  - çalıştırdık, 
  - fonksiyonlarımızı kontrol ediyoruz, 
  - detail e gidiyoruz, 
  - comment ekliyoruz, 
  - comment sayısının arttığını, 
  - like ladığımız zaman like sayısının artıp azaldığını gördük, 

- Login fonksiyonu ekleyeceğiz, login olmazsa comment kısmını göstermeyecek, login to comment diyeceğiz, tıklayınca login e gidecek.

- Blog application tarafı tamam gibi; 
  - user application a geçeceğiz, 
  - bir tane Profile page oluşturacağız, 
  - profile a gideceğiz, 
  - edit yapabilecğiz, 
  - login logout ekleyeceğiz, 
  - register ekleyeceğiz, 
  - tamamen normal bir siteye gittiğinizde nasıl görünüyorsa, login logout nasıl oluyorsa aynı şekilde yapacağız.


## Users App (Authentication)

- register/login/logout işlemeleri için yeni bir application (users) oluşturuyoruz. 
- blog app imizle aynı seviyede (manage.py file ile aynı seviyede) terminalde users appizi oluşturup, settings.py'da INSTALLED_APPS'ekliyoruz.

```bash
- py manage.py startapp users
```

settings.py
```py
INSTALLED_APPS = [
    ...,
    'users',
]
```

- settings.py da app imizin ismi ile INSTALLED_APPS'e kaydettik
- Ancak bizim application'ımızın ismi "users" olduğu için, djangoda default olarak bu ismi kullandığı için, farklı yerlerde veya signals kullanırken sıkıntı çıkartıyor, farklı bir yere yazmanız gerekiyor. 
- O yüzden app imizi settings.py a kaydederken uzun haliyle kaydediyoruz ki bize signals kullanırken sıkıntı çıkarmasın. 
- Ayrıca alışkanlık edinin app inizi uzun haliyle kaydedin INSTALLED_APP e kaydedebilirsiniz.

settings.py
```py
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    # my_apps
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    # or
    # 'blog'
    # 3rd party packages
    'crispy_forms',
]
```

- urls configurasyonunu yapalım;

main/urls.py
```py
...

urlpatterns = [
    ...,
    path('users/', include('users.urls')),
]
```

- users app'inin içinde bir urls.py dosyası oluşturup, authenticate işlemleri için buradaki urls pathern'lerini kullanacağız.

users/urls.py
```py
from django.urls import path

urlpatterns = [
]
```


##### user'lar için Profile oluşturma;

- Bu projede user için djangonun default User modelini kullanacağız. Ancak bu modele ilave olarak userlar için ekstra fieldlar (profile_pic, bio) istiyoruz.

- Bunun için default User modeli ile OneToOne ilişkili user fieldına sahip bir Profile modeli oluşturuyoruz.

- Şimdi users da profile sayfamız için model oluşturacağız, 
  - kendimize göre field lar belirledik (kullanıcı ile ilgili bilgi almak için), user ımız profile ile ilişkili olması lazım, bir user ın bir profile ı olması lazım, bir user ın birden fazla profile ı olamaz, yani OneToOne relation olması lazım,  User modelimiz vardı ya onunla bire bir ilişki kuruyoruz, 
  - tabi User modelimizi de import ediyoruz (blog app imizde User modelini djangonun default User modelinden almıştık, burada da yine aynı yerden import ediyoruz, django.contrib.auth.models den djangonun default User modelini import ediyoruz), 
  - on_delete için CASCADE diyoruz ki, user silindiğinde profile da silinsin 
    from django.contrib.auth.models import User
        user = model.OneToOneField(User, on_delete=models.CASCADE)  

  - Bir tane profile image'ı olsun, iki parametre veriyorduk, 
    - biri upload yani nereye yüklesin? ,  
    - diğeri kullanıcı register ile user oluşturduğu zaman otomatik olarak bir profile page'i oluşacak bu profile page'inin de default bir resmi olacak bu kullanıcının,
        image = models.ImageField(upload_to=  , default=  )

  - şimdi daha önce Post modeldeki image field'ında, bu upload değişkenine dinamik birşey yazmıştık media_root klasörünün  içerisinde dinamik olarak bir klasör oluşturmuştuk o klasörün içerisine otomatik olarak kendisi kaydediyordu. Nasıl yapmıştık? 
    - bir tane fonksiyon/method yazmıştık (path/klasör oluşturmak için) modelimizin üzerinde; Burada da aynısını yapıyoruz;
    def user_profile_path(instance, filename) 
    
    - iki parametre alıyordu, 
      - biri instance (instance dan kasıt profile dan üreteceğimiz obje), 
      - diğeri filename
    def user_profile_path(instance, filename)
        return 'user/{0}/{1}'.format(instance.user.id, filename) 
  
  - settings.py da belirttiğimiz media_root klasörünün altına user klasörü, onun da altına, {0} olan kısma instance ın user id sini isim olarak alan bir klasör koyacak, {1} olan kısma da filename i isimli dosyayı koyacak ve user kalsörünün altına tıpkı media_root kalsörünün altına olduğu gibi dinamik olarak iç içe klasör oluşturacak.
    def user_profile_path(instance, filename):
        return 'users/{0}/{1}'.format(instance.user.id, filename)

  - image field ının upload_to parametresine de user_profile_path i yazacağız, 
    image = models.ImageField(upload_to=user_profile_path, default=  )


- Kullanıcıdan aldığımız tüm video ve resimler bu settings.py da tanımlamış olduğumuz media_root un altına otomatik olarak gidecek, 
- ama bu media_root un altında toplanan resimler karman çorman olmasın, hangi app e ait olduğu anlaşılsın diye bir dizin yapısında olması için blog app den gelenleri blog klasörünün altına , users app den gelenleri user kalsörünün altına kaydet.
- default olarak da daha önceden media_root klasörüne yüklediğimiz avatar.png resmini koy diyoruz.
    image = models.ImageField(upload_to=user_profile_path, default='avatar.png')

- bir de bio ekliyoruz, (daha farklı fieldlar da eklenebilir.) 
    bio = models.TextField(blank=True) 

- str methodu tanımlıyoruz (db de bize user olarak göstersin.)

- users app in models.py dosyasına gidip;

users/models.py
```py
from django.db import models
from django.contrib.auth.models import User

def user_profile_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_profile_path, default='avatar.png')
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user
```


- terminale gidip, yeni bir model oluşturduğumuz için migrations ve migrate yapıyoruz, (tabi manage.py dosyası ile aynı sevide olduğumuza dikkat ederek, burada src klasörünün içerisinde bulunuyor manage.py)

```bash
- py manage.py makemigrations
- py manage.py migrate
```

- users app in admin.py'ına gidip, users app inin models.py ından Profile modelimizi import edip, admin site a register ediyoruz.

users/admin.py
```py
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
```

- admin page imize gidip bakıyoruz, evet users application ımız ve içerisinde profile modelimizi görüyoruz.

- Mesela profiles modelimize first name last name de ekleyebilirsiniz, str methodunu şekillendirebilirsiniz, 

- Yeni bir profil oluşturduk, umit Profile diye gösteriyor bize, default olarak da avatar resmini otomatik koydu.

users/models.py
```py
from django.db import models
from django.contrib.auth.models import User

def user_profile_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_profile_path, default='avatar.png')
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return "{}'s {}".format(self.user, 'Profile')
```

- Şuanda profile'ı admin panelden manuel olarak oluşturabiliyoruz.
- Ancak bu işi, yeni bir user oluşturulduğunda yada bir user register olduğunda , o user ın profile ının da otomatik olarak oluşmasını istiyoruz.


##### user için Profile'ı signals kullanarak otomatik oluşturma;

- Her user oluşturulduğunda, otomatik olarak bunun bir de profile ı oluşturulsun!
- Bunun için 'users' app'imizde signals.py oluşturuyoruz.

- Bunda mantık şu;
  - Bir model olacak, bu model signal gönderecek, 
  - bir receiver olacak, o receiver ın altına fonksiyon yazıp, o fonksiyonla ne işlem yapacağımızı yazacağız, 

- Burada bizim sender ımız User, User modelimizden bir User oluşturulduğu zaman, ama ne zaman bu User oluşturulduktan sonra yani save ettikten sonra, bu işlemi gerçekleştir yani post_save, 
- Sonra create_profile diye bir fonksiyon yazıyoruz, bu sender ı alacak, instance ı alacak, created ı alacak neden? post_save de create edildikten sonra olduğu için if created codition ını kullanabilmek için,  **kwargs alacak, 
- Sonra eğer bu User dan bir tane instance oluşturulmuşsa, git Profile dan Profile instance ı oluştur.
- Bunu yapmak için apps.py'a gidip ready methodunu yazmamız gerekiyor. (Eğer bu işlemi signal.py gibi bir dosyada değil de modelde yapmış olsaydık, ki yapabiliriz, apps.py'a ready methodunu yazmak zorunda olmazdık.)

- Geçtiğimiz bölümde signals lardan bahsedilmişti,
  - postsave, presave, postdelete, predelete...
- Yani bir save işlemi yaptıktan sonra, yapmadan önce bir sinyal gönder, o sinyale istinaden farklı bir işlem yapılsın..
- Burada da diyoruz ki bir user oluşturulduğunda, Profile objesi/instance ını otomatik olarak oluştur diyeceğiz.
- blog app imizde ne yapmıştık signals.py diye bir dosya oluşturmuştuk, burada da (users app imizin içinde) bir tane oluşturuyoruz,
- Şuna karar vermemiz gerekiyor, postsave olduktan sonra veya presave (kaydettikten sonra mı? kaydetmeden önce mi?) burada kaydettikten sonra, yani user ı oluşturduktan sonra bana bir tane profile create etmesini istiyoruz.

- signals'larımızı import ediyoruz, (bunları ezberlemek zorunda değilsiniz, document den bakarsınız)
    from django.db.models.signals import post_save

- Burada ne kullanacağız? default olarak gelen bir tane user modelimiz vardı ya hani biz user ı orada oluşturuyoruz, onun için, signals bana user gönderecek, user ı burada import etmemiz gerekiyor, (signal i gönderecek olan şey bu. yani user oluşturulduğunda bir sinyal gönderecek 'yeni bir user oluşturuldu, sen de şunu yap!')
    from django.contrib.auth.models import User

- Sonra bir tane de reciver yani bu signal i alan receiver import etmemiz gerekiyor,
    from django.dispatch import receiver

- Bir de, biz user create edildiğinde profile oluşmasını istiyoruz ya işte o Profile modelini import etmemiz gerekiyor,
    from .models import Profile

- Bu receiver bir decorator dü @receiver, içerisine iki tane parametre alıyor; 
  - biri ne kullanacak; (burada post_save), 
  - diğeri de sender kim olacak? (burada User modelimiz olacak sender=User)
    @receiver(post_save, sender=User):

- create profile oluştur, birkaç tane parametre alıyor;
  - sender (kim gönderdi bunu bana), 
  - instance (User dan oluşan obje) , 
  - post_save ekstaradan created diye birşey alıyor (neden? eğer user modeli created edildiyse şartını koyacağız onun için), 
  - **kwargs bunu yazmak zorunluluğu (django bazı kw arguments ları kendisi koyuyor, onları karşılamak için bu **kwargs kullanıyoruz.)
    def create_profile(sender, instance, created, **kwargs):

- eğer instance dan gelen User modeli create edildiyse:
    if created:

- Profile objesi create et, (image ve bio otomatik oluşturulduğu için signals a sadece user ı gönderiyoruz), user da burada instance dan gelen class (Biz mesela yeni bir user oluşturuyoruz ya manuel olarak, aslında bu bizim user clasından oluşturduğumuz bir instance oluyor. python mantığında bir class dan üretilen herşey o class ın bir instance ı oluyor.)
- Eğer bir user create edilmişse onun instance'ını user a tanımla!
    if created:
        Pofile.objects.create(user=instance)

- save_profile;
  - fonksiyonu, bir User nesnesi kaydedildiğinde otomatik olarak tetiklenen bir sinyal alıcısıdır. Bu fonksiyon, User nesnesine bağlı olan Profile nesnesinin de kaydedilmesini sağlar. Bu, User nesnesinde yapılan değişikliklerin Profile nesnesine de yansıtılmasını garanti eder.
  - Özetle, save_profile fonksiyonu, User nesnesi kaydedildiğinde ilgili Profile nesnesinin de güncellenmesini sağlar.

users/signals.py
```py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

- oluşturduğumuz bu signals.py'ı, users app inin apps.py'ında UsersConfig class'ında ready methoduna import etmemiz gerekiyor. 
    def ready(self):
        import users.signals

users/apps.py
```py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
```

- Ayrıca, buradaki signals ile sadece yeni oluşturulan userlar için otomatik olarak profile objesi create ediliyor. Fakat daha önceden create edilmiş bir user'ın (mesela admin) profile objsei yok ise, bunun için de save_profile() methoduna bir if condition'ı ekleyerek; profile objesi olmayan bir user'ın fieldlarında bir update işlem yapılırsa, hemen o user içinde bir profile objesi create edilmesini sağlayabiliriz.

users/signals.py
```py
...

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
```


- test ediyoruz, admin panelden bir user create edince, signals vasıtasıyla otomatik olarak, create edilen user için bir Profile objesi de create edildiğini gördük.


- ARAŞTIR !
- Bizim yazdığımız like çok düzgün değil, like yaptığımız zaman sayfa komple render oluyor, bulunduğu kısım yani sadece like yenilenmiyor, 
- bunlar genelde AJAX (Asyncron Javascript Xml) ile yazılıyor. 
- AJAX backende sayfayı refresh etmeden veri göndermek için kullanılıyor. 
- Html sayfasında AJAX kodu yazıyoruz Javascript ile,  
- bu sefer Http response gönderiyoruz databse e Javascript koduyla , GET POST methodu yapabiliyoruz. O zaman like yapınca tüm sayfanın yenilenmesinden kurtuluyoruz.

- Flusk daha basit ama djangonun built-in sağladığı security özellikleri yok, ORM yapısı yok, flusk node js ile muadil bir framework


#### login / logout

- şuan autentication login logout larına nereden ulaşacağız? onları göreceğiz, 

- login logout nasıl olacağız? 
- login için form oluşturup kendimiz yapabiliriz, logout için gerek yok.

- login için djangonun otomatik olarak oluşturduğu bir view ve form var, 

- password change/reset için şöyle bir built-in yapısı da var; 
  - login button'ının yanında forgot Password? diye bir link var, 
  - buna tıklayınca sisteme kayıtlı olan email adresinizi istiyor, 
  - mail inizi girip request reset yani reset talebine basınca emailinize otomatik bir mail gönderiyor, 
  - email e gelen mail de istenen linke tıklayınca da yeni bir reset password oluşturma ekranı geliyor.

- register için otomatik olarak oluşturulmuş bir view ve form yok, bunu kendimiz yazdık,


##### login ( default built-in yapısıyla );

- Bu login işlemi için djangonun default built-in yapısını kullanacağız. Yani users app'inin içindeki views.py'da bir login view'i yazmayacağız.
   
- Bu yüzden direkt olarak users app'inin urls.py'ında, yani bu default LoginView'i tetikleyecek urls/endpoint'i yazdığımız yer olan users/urls.py'da, default django.contrib.auth'dan views'i import edip;
  - (LoginView'i import ediyoruz ama genelde best practice djangonun authentication view lerini import ettiğimiz zaman yeniden isimlendiriliyor. burada as auth_views şeklinde yeniden isimlendirdik.) 

- bu views de neler var? Bu normal her app de yazdığımız gibi view ler bunlar. Class base view ler. Burada bize ne vermişler? 
  - LoginView vermiş, 
  - LogoutView vermiş, 
  - PasswordChangeView,
  - PasswordResetView, 
  - PasswordResetDoneView, 

- yani biz burada kendimiz view yazmak yerine buradaki viewleri import edip, 
  - (normalde kendimiz ne yapıyorduk? from .views import viewimiz yazdığımız view i import ediyorduk.) 
  - ama burada komple views i import edip bunun içerisinde işimize yarayacak view leri kullanacağız.

- path imizi yazıyoruz, 
- bunları daha sonra düzenleyeceğiz,
- burada diyoruz ki url de users dan sonra login gelirse, yani users/login/ şu view e git diyoruz ama view i biz yazmadık, auth_views deki default viewlerden aldık.
    path("login/", auth_views.LoginView.as_view(), name='login')     
    (auth_views in içindeki LoginView i al, as_view() ekliyoruz içine parametreler de alabiliyor, bahsedecek, name='login' yazmak zorundayız,neden? document'dan baktık, hangi view e hangi isim vermemiz gerektiği yazıyor orada.)

- django.contrib.auth un içindeki view.py ın içine girerek LoginView i inceliyoruz;
  - mesela template name i değiştireceğiz, bizim yazacağımızdan daha güzel bir view yazmış, siz yazmaya kalksanız bu kadar iyi yazamazsınız. default değerler üzerinde değişiklik yapmak istiyorsanız burayı inceleyip, bununla uğraşmanız gerekiyor djnagonun handikapı da bu.

users/urls.py
```py
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login' ),
]
```

- urls.py'da LoginView'imizi import ettik ve urls/endpoint'i de yazdık. LoginView çalıştırıldığında; 
  - default olarak bir form veriyor. 
  - Bu formu çalıştıracak template'in klasör yapısını users/templates/register/login.html şeklinde oluşturulmasını istiyor.
  - oluşturulan login.html içerisinde KoginView'in default olarak verdiği formu render ediyor.
  - Son olarak da bu form doldurulup da user girişi yapılması için, user login olduktan sonra redirect edilecek url'i istiyor. Bu login redirect url'ini de settings.py'da tanımlıyoruz. 
    LOGIN_REDIRECT_URL = '/' 

- template'imizi oluşturalım;

users/templates/registration/login.html
```html
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <button type="submit">Login</button>
</form>
```

- settings.py'da login redirect tanımlayalım; (Ana sayfa olarak tanımladığımız page'e yönlendiriyoruz.)

main/settings.py
```py
...
# LOGIN_REDIRECT_URL = 'blog:list'
LOGIN_REDIRECT_URL = '/'
```

- bunun aynısını logout için de yapacağız.
 
##### logout ( default built-in yapısıyla );

- users/urls.py'da LogoutView'imizi import edip, path'ini yazalım;

users/urls.py
```py
...

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout' ),
]
```

- Template'imizi yazalım; (Bunu yazmasak da olur. )

users/templates/registration/logout.html
```html
<h2>You have been logged out</h2>
```

- Şimdi bu urls path'imizi/endpointimizi POST methoduyla tetikleyecek bir logout button'ı oluşturacağız.
- Bu button'ı post methodu ile istek atabilmesi için bir form içinde ve {{csrf}} ile birlikte kullanmamız gerekiyor.
- Navbar'da bir logout button'ı yerleştiriyor ve test ediyoruz. 

navbar.html
```html
...
<form action="{% url 'logout' %}" method="POST">
    {% csrf_token %}
    <button type="submit">Logout</button>
</form>
...
```

- Test ediyoruz, evet çalıştı, user'ı logout etti, logout.html template'i render edildi. 


##### registration 

- Yukarıda login, logout yaptık ama, önce registration'ı halledelim, sonra daha detaylı login,logout ile uğraşacağız.

- django login, logout için default viewler sağlamasına rağmen  registration için böyle bir imkan sağlamıyor.

- registration için view-form-urls-template oluşturacağız
- Bir form oluşturup, view ile frontend e göndereceğiz, default olarak verdiği birşey yok, view ini de biz yazacağız,


###### registration form

- şimdi registration formunu yazıp, registration view ini yazalım, 
- users app imizin içinde forms.py dosyası oluşturuyoruz, 
  - içine django nun default olarak sunduğu UserCreationForm'undan inherit ederek RegistrationForm isminde formumuzu oluşturacağız.
  - UserCreationForm u inceliyoruz; 
    - bu form bize ne sunuyor; 
      - 1. password1 ve password2 yi veriyor,
      - 2. class meta ile de User modelinden de ekstra olarak username i çekip veriyor, 
    - password1 ve password2 yi kendisi ekliyor, 
    - class meta ile de ekstra olarak User modelinden de username i ekliyor, bize default olarak bir UserCreationForm vermiş 
    - Ancak biz buna ekstradan bir de email field ı eklemek istiyoruz, ekstradan email field ı koyacağız. Bunu da class Meta' da belirterek yapabiliriz.

- djangodan forms ları import ediyoruz,
- django.contrib.auth.models den default olarak bulunan User modelimizi import ediyoruz (username için),
- django.contrib.auth.forms dan UserCreationForm u import ediyoruz.

- UserCreationForm'dan inherit ederek, RegisterationForm class'ımızı yazıyoruz.
    class RegisterationForm(UserCreationForm):

- (UserCreationForm da forms.ModelForm dan tüm özellikleri inherit ettiği için bizim tekrardan forms.ModelForm dan import etmemize gerek yok. Yani biz UserCreationForm dan import ettiğimiz zaman artık RegistrationForm da  forms.ModelForm dan inherit etmiş olacağız, bundan dolayı şunu yapabiliriz; 
  - Class Meta: Normalde bunu modelForm da kullanabiliyorduk ya yukarıda modelForm belirtmedik ama zaten UserCreationForm form.ModelForm dan inherit etmişti. Bu özelliğe artık RegistrationForm umuz da sahip.)
    class Meta:
        model = User
        fields = ('username', 'email') 

- burada User modelimizden username ve email field larını da ekliyoruz. User modelindeki tüm fieldları ekleyebiliriz. 


users/forms.py
```py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email') # password1 ve password2'yi belirtmeye gerek yok
```

- şuan user create ederken sadece username istiyor, çünkü username zorunlu alanımız, email zorunlu alan değil, 
- Ama biz kullanıcıdan zorunlu olarak email adresi almak istiyoruz, eğer password ünü unutmuşsa email ine mesaj gitsin, oradan reset yapsın. Eğer email ini unique olarak istemezsek sıkıntı olur. 

- Email default olarak (blank=True) zorunlu alan olarak gelmiyor, ama override edebiliyoruz, 
- forms.py'da oluşturduğumuz RegistrationForm'un bir field'ı olan email field'ını yine orada override edebiliriz (yani bazı özelliklerini geçersiz kılabiliriz),
- içerisinde fieldlarımızı belirlediğimiz class Meta nın hemen üzerinde yapıyoruz bu override işlemini, şöyle yapıyoruz;
    email = forms.EmailField()   

- Bu şekilde içerisine hiçbirşey yazmazsak, boş bırakırsak zorunlu alan haline gelir. required=True haline gelir, default hali blank=True dur. (buradaki blank, formdaki required'a denk geliyor yani)

- email field'ına da custom validation yazacağız. bunun için bir method tanımlıyoruz.

- Eğer djangoda bir field için validation yazılacaksa; "clean_fieldname" ismini vermemiz gerekiyor, burada email için validation yazacağımız için "clean_email" diye isimlendiriyoruz.
    def clean_email(self):

- formun içerisindeki kullanıcının doldurduğu email'i al (formun içerisinden bir veri alınırken best practice cleaned_data ile alınır)
    email = self.cleaned_data['email']

- "email" field'ı User modelimizde kayıtlı olduğundan bir kontrol yapılır; yukarıda tanımladığımız email'i olan Userları filter et! eğer bu email exists ise yani kullanıcının girdiği emailin aynısından db'deki User tablosu/modelinde varsa;
    if User.objects.filter(email=email).exists()    

- ValidationError forms un içinde,  ValidationError yükselt!
    raise forms.ValidationError('Please use another Email, that one already taken')

- eğer yoksa hiçbir işlem yapmayıp, kullanıcının girdiği email'i return et diyoruz.
    return email

- ve email custom validation kısmı da tamam, validation methodumuzu yazdık.

users/forms.py

```py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):

    # email = forms.EmailField(required=True)
    email = forms.EmailField() # doldurulması zorunlu olsun istiyorsak (default-> blank=True 'dur. Bu şekilde required=True olmuş oluyor.)


    class Meta:
        model = User
        fields = ('username', 'email') # password1 ve password2'yi belirtmeye gerek yok
    
    def clean_email(self):
        """
        # Burasını AI tavsiye etti!
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanımda.')
        return email
        """
        email = self.cleaned_data['email'] # user@gmail.com
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi zaten kullanımda.')
        return email
```


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


###### registration view

- Registration formumuz tamam, artık view-url vasıtasıyla template'imize koyacağız.
- users/views.py'a gidip view imizi yazalım, 
- önce users/forms.py' dan RegistrationForm umuzu import ediyoruz, ardından;
    def register(request):     
        form = RegisterationForm(request.POST or None) (request post ise post ile doldur değilse None Boş render et!)
        if form.is_valid():  eğer form valid ise 
            form.save()    formu kaydet

users/views.py
```py
from django.shortcuts import render
from .forms import RegisterationForm

def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
```

- şimdi bir html üretip orada render edelim, onun için ne yapmamız gerekiyor?

- context oluşturup formu içerisine koyup return render ile template e göndereceğiz, nereye?

- users app'inin içerisinde templates klasörü oluşturup içine app'imizin ismi (users) ile bir klasör daha oluşturup onun da içine register.html template imizi oluşturuyoruz, 
- işte buraya;
    users/templates/users/register.html

- Ayrıca bir eğer bir user daha önceden register olmuş ve de login olmuş ise tekrardan register olmasının önüne geçmek için bir de koşul yazıyoruz.
  - Eğer istekte bulunan user authenticate ise, list template'ine redirect ediyoruz ki mükerrer register yapamasın.
        if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('blog:list')  #! Kullanıcı zaten giriş yapmışsa yönlendirilecek sayfa. Bir kullanıcının mükerrer kaydını engellemek için bu kontrolü yapabiliriz.

users/views.py
```py
from django.shortcuts import render, redirect
from .forms import RegisterationForm
from django.contrib import messages


def register(request):

    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('blog:list')  #! Kullanıcı zaten giriş yapmışsa yönlendirilecek sayfa. Bir kullanıcının mükerrer kaydını engellemek için bu kontrolü yapabiliriz.

    form = RegisterationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # return redirect('login')  # login page imiz henüz yok.

    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context )
```


###### registration urls

- users/urls.py'a gidip path tanımlayalım; (login, logout path'lerini şimdilik yoruma alalım. Daha sonra onlarla ilgili işlem yapacağız.)

users/urls.py
```py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register,
)

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(), name='login' ),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout' ),
    path('register/', register, name='register'),
]
```

###### registration template (register.html)

users/templates/users/register.html
```html
{% extends 'base.html' %}
<!-- {% block title %}Register{% endblock %} -->
{% load crispy_forms_tags %}   
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Join Today</legend>
            {{ form|crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Sign Up</button>
        </div>
    </form>
    <div class="border-top pt-3">
        <small class="text-muted">
            {% comment %}{% url 'login' %}{% endcomment %}
            Already have an account?<a class="ml-2" href="#">Sign In</a>
        </small>
    </div>
</div>
{% endblock content %}  
```


- normalde register'ımıza nereden ulaşıyorduk? 
- eğer login değilsek navbarda sağ üst köşede login ve register linkleri var oradan ulaşıyorduk. 
- Eğer register linkini göremiyorsak demekki login olmuşuz, 
- Adminden logout ile çıkış yapıyoruz ve tekrar navbar ımıza bakıyoruz evet register geldi. 
- Şimdi navbar template ine gidip bu register url ini aktivate edelim/ekleyelim, 

templates/navbar.html
```html
...
    <!-- Navbar Right Side -->
    <div class="navbar-nav">
        {% if user.is_authenticated %}
        ...
        {% else %}
        ...
        {% comment %} {% url 'register' %} {% endcomment %}
        <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
        {% endif %}
    </div>
...
```


- evet registration page imiz çalıştı, 
- register da oluyoruz, register olduğumuzda, login page imiz henüz hazır olmadığı için redirect etmedik. Bu yüzden aynı sayfada kalıyoruz. 
- Ancak register olabiliyor, admin panelden gördük register olunduğunu.  
- email field ımız da geldi, ve de email field ımız doldurulması zorunlu alan olarak override etmiştik.
- Ayrıca bir user register olup da login olduğunda tekrar register olup da mükerrer register/kayıt'ların önüne geçtik. Gerçi henüz login view'ini yazmadık. Ancak mesela admin ile login olduğunda tekrardan register olamıyor, list template'ine redireck ediliyor. 


- Test ediyoruz, çalıştırdık; 
- register a gittiğimizde email in yanında yıldızı gördük, yani zorunlu alan olmuş (tabi bu yıldızı crispy yapıyor.), 
- kullanıcı oluşturduk, oluştuğunu da admin page de gördük, 
- aynı zamanda signals ile de otomatik olarak user create edildiğinde, o user'a ait profile'ınıda oluşturdu, 
- user create ederken email'i zorunlu alan olduğu için istedi, 
- sign up yaptık yine bizi aynı sayfada tuttu çünkü redirect etmemiştik.

- NOT: Eğer burada RegistrationForm'un class Meta'ının fields kısmında sadece ('email',)  diye yazarsak sadece email ve passwordleri isteyecek, ancak dikkat tupple olduğu için ve tek item olduğu için email item ının sonuna da virgül istiyor.
    class RegistrationForm(UserCreationForm):
        email = forms.EmailField()
        class Meta:
            fields = ('email',) # password1 ve password2'yi belirtmeye gerek yok


##### profile

- her register/kayıt olan user için bir de profile modeli/tablosu oluşturmuş, ve signal vasıtasıyla otomatik olarak bir profile create ediyoruz.
- Kayıt/register olan her user için oluşturulan bu profile'ı, user'a gösterip, update edebilme imkanını sunacağız.
- register olan user'ın profile tablosunda, "image", "bio" fieldları ve "user" field'ı ile de User tablosuyla OneToOne ilişkili olduğu bir field'ı var.
- Şimdi bunları update edebilmesi için user'a bir form vereceğiz.
- Fakat; 
  - User tablosundaki "username" ve "email" field'ını değiştirebilmesi için bir UserUpdateForm, 
  - Profile tablosundaki "bio" ve "image" field'ını değiştirebilmesi için bir ProfileUpdateForm vereceğiz.
- Yani iki form oluşturacağız, bunları bir profile view'inde birleştirip profile template'ine göndereceğiz.
- Çünkü profile tablosundaki "user" field'ı, User modeli ile OneToOne ilişkili. Yani Profile tablosundan oluşturduğumuz form ile, Profile tablosunun "user" field'ıyla bağlantı kurduğumuz User tablosundaki object'in "username" ve "email" fieldlarını değiştiremiyoruz. Ancak bu işi view'de (formdan gelen veri içinden "user" verisini ayırıp onun için ayrı bir logic kurup template'e gönderip, daha sonra template'ten gelen veriyi ayrı bir şekilde User tablosuna create edebiliriz ama çok zahmetli olur.) yapabiliriz.

###### profile form

- Bunun için yani user'ın kendine ait oluşturulmuş bu profile'ı görebilmesi ve de update edebilmesi için forms.py'da bir ProfileUpdateForm oluşturacağız,
    class ProfileUpdateForm(forms.ModelForm):

- Şuan için aslında halihazırda bizim profile modelimiz var ve dolu. Nasıl dolu? user create ederken signals ile bir de Profile modeli create ettiğimiz için, o user'a ait profile tablosunda "user", "image", "bio" field ları olan bir profile objesi mevcut.

- aslında şu anda bir update form gibi olacak, yani profile page'i update form gibi render edeceğiz db den, getirirken içerisini dolu getireceğiz, formları da buna göre isimlendireceğiz update_form diye isimlendireceğiz.

- Bunun için iki form yapacağız; 
  - "username" ve "email"'i User modelinden aldığımız fieldlar için bir formda, 
  - "image" ve "bio" fieldlarını da diğer formda render edip, 
- iki formu tek bir sayfada birleştireceğiz. 
- Bunu da özellikle iki form tek sayfada nasıl birleştirilir görmek için,
    class PorfileUpdateForm(forms.ModelForm):   
        class Meta:
            model = Profile            
            fields = ("image","bio")

    class UserUpdateForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ("username","email")

users/forms.py
```py
...
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image","bio")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","email")
```

- iki formumuz da hazır şuan, 


###### profile view

- user/views.py'a geliyoruz, profile page imiz için bir view yazacağız, 
    def profile(request):

- iki formumuz vardı onları alacağız birine u_form (UserUpdateForm), diğerine de p_form (ProfileUpdateForm) diyoruz,
- Ayrıca form bize db deki bilgilerle dolu gelsin istiyoruz, bunun için specific bir instance belirtiyoruz, instance için hangi user olduğunu belirtmemiz lazım, django da zaten request.user ile bize hangi user ile login olunduğunu verdiği için bu şekilde yazıyoruz.
    u_form = UserUpdateForm(request.POST or None, instance=request.user) 

- Aynısını diğeri için de yapıyoruz. Burada bir de image file olduğu için şunu ekliyoruz; requst.FILES or None, yine formu dolu istiyoruz (yani şuanda login olmuş user ın profile ına ulaşıp onu instance ile p_form a yüklüyoruz) bunun için bir specific bir instance belirtiyoruz, instance=request.user.profile
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user)

- Bunlara ulaştıktan sonra formu validation etmemiz gerekiyor, ama burada iki tane formumuz var bunun için;
- Bu iki form da valid ise koşulunu "and" ile sağladık.  "or" olsa birisi valid olsa geçer.
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()

- formları kaydettikten sonra aynı sayfaya kalınmasını istiyoruz. 
- Bunun için rediret(requets.path) yapısını kullanıyoruz.
    return redirect(request.path)

- formlarımızı kaydettik, şimdi bunları template imize göndereceğiz,
    context={
        "u_form":u_form
        "p_form":p_form
    }
    return render(request, "users/profile.html", context )


user/views.py
```py
from django.shortcuts import render, redirect
from .forms import (
    RegistrationForm,
    ProfileUpdateForm,
    UserUpdateForm,
)

...

def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        return redirect(request.path)
    
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    
    return render(request, "users/profile.html", context)
```


###### profile templates (profile.html)

- users app imizin içerisindeki templates klasörünün içerisindeki app imizin ismini (users) taşıyan klasörümüzün içerisinde profile.html template imizi oluşturuyoruz,
    users/templates/users/profile.html

users/templates/users/profile.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <div class="media">
        <img class="rounded-circle account-img" src="{{ user.profile.image.url }}">
        <div class="media-body">
            <h2 class="account-heading">{{ user.username }}</h2>
            <p class="text-secondary">{{ user.email }}</p>
        </div>
    </div>
    <form action="" method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Profile</legend>
            {{ u_form| crispy }}
            {{ p_form| crispy }}
        </fieldset>
        <div>
            <button class="btn btn-outline-info" type="submit">Update</button>
        </div>
    </form>
</div>
{% endblock content %}
    
```

- url/path'ini oluşturup navbar daki linklerini aktif edeceğiz.


###### profile urls/path

- views.py dan profile view ini import edip, path ini yazıyoruz,

users/urls.py
```py
...
from .views import (
    register,
    profile,
)

urlpatterns = [
    ...,
    path('profile/', profile , name='profile' ),
]
```


- daha sonra templates/navbar.html' deki profile linkinin href kısmını doldurarak linki aktif hale getiriyoruz.

templates/navbar.html
```py
...
    <!-- Navbar Right Side -->
    <div class="navbar-nav">
        {% if user.is_authenticated %}
        ...
        <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
        <a class="nav-item nav-link" href="{% url 'blog:create' %}">New Post</a>
        {% else %}
        ...
        {% endif %}
...
```

- test ediyoruz, evet çalıştı. 
- login olduğumuz durumda navbar a koyduğumuz profile linki ile profile sayfamıza gidebiliyoruz, 
- resmimizi update/değiştiriyoruz, evet update/değişti.

- register, profile için form-view-url-template oluşturduk. Çalışyorlar.

- artık djangonun bize default olarak verdiği özelliklere (login, logout, password_change, password_reset) geçeceğiz.


##### 1. login ( email-password ile login )

- Bu 1. login ile email ve password ile login/authenticate olunacak.

- user'ın username ile değil de email ve password ile login edilmesi için;

###### login ( email-password ile login ) form;

- forms.py' da AuthenticationForm'dan inherit ederek EmailLoginForm'u hazırlıyoruz ve bu formdaki username alanını email olarak değiştiriyoruz.

users/forms.py
```py
...

#! email-password ile login yapmak için form; 
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth import authenticate

class EmailLoginForm(AuthenticationForm):

    username = forms.EmailField(label="Email")  # E-posta alanı kullan

    def clean(self):
        email = self.cleaned_data.get('username')  # Form'daki "username" alanını email olarak kabul ediyoruz
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                # E-posta ile kullanıcıyı bul
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("Bu e-posta ile bir kullanıcı bulunamadı.")
            
            # Bulunan kullanıcının kullanıcı adını (username) authenticate'e gönderiyoruz
            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Geçersiz e-posta veya şifre.")
        
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

```


###### login ( email-password ile login ) view;

- Hazırladığımız bu EmailLoginForm'u ile user_login view'inde kullanıyoruz.

user/views.py
```py
...
#! email-password ile login yapmak için views;
from .forms import EmailLoginForm
from django.contrib.auth import login
from django.contrib import messages

def user_login(request):
    
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('blog:list')  #! Kullanıcı zaten giriş yapmışsa yönlendirilecek sayfa

    form = EmailLoginForm()
    if request.method == 'POST':
        form = EmailLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('blog:list')
    context = {
        'form': form,
    }
    return render(request, 'users/user_login.html', context)

```


###### login ( email-password ile login ) urls;

- user_login view'ini tetikleyecek/çalıştıracak endpoint/url'i yazıyoruz.

users/urls.py
```py
...
from .views import (
    ...,
    user_login,
)

urlpatterns = [
    ...,
    #! email-password ile login yapmak için path; 
    path('user_login/', user_login, name='user_login'),
]
```


###### login ( email-password ile login ) templates;

- user_login view'inin render ettiği user_login.html template'ini aşağıdaki klasör ve dosya yapısında oluşturup yazıyoruz;

users/templates/users/user_login.html
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}
{% block content %}

<form action="" method="POST">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit">Login</button>
</form>

{% endblock content %}

```

- Test ediyoruz;
- url'den ->    /users/user_login/    şeklinde istek attığımızda, eğer isteği atan user login olmuş authenticate bir user ise "list" template'ine yönlendiriliyor.
- Ancak isteği atan user authenticate bir user değilse email ve password ile giriş yapabileceği "user_login" template'i sunuluyor. email ve password ile giriş yapabiliyor.     

- Bu 1. login ile email ve password ile login/authenticate olunabiliyor.


##### 2. login ( default built-in yapısıyla - template name'ini override ederek );

- Daha önce djangonun default olarak built-in olarak bulunan views'lerinden LoginView'ini çalıştıran bir "login/" path'i oluşturmuştuk. 
- Bu path'in çalıştırdığı default LoginView'i, yine djangonun defaut olarak belirlediği klasör yapısında (users/templates/register/login.html) "login.html" template'ini render ediyor.
- Fakat biz bu klasör yapısını kullanmak istemiyoruz.
- O zaman yine djangonun default LoginView'ini kullanacağız, ancak template_name'ini override edeceğiz.
- Böylece login.html template'imizi istediğimiz şekilde konumlandırabileceğiz.


###### login ( default built-in yapısıyla - template name'ini override ederek ) urls;

- users urls.py'a gidiyoruz, 
- hatırlıyorsak djangonun views'lerini as auth_views olacak şekilde import etmiştik, 
- best practice auth_views (authentications views) veriliyor,
- pathi imiz yazıyoruz,
  - url'den "login/" geldiği zaman; 
    - auth_views den LoginView'i al, 
    - .as_view()'i al, 
    - name'i login olsun.
        path("login/", auth_views.LoginView.as_view(), name='login')

- LoginViewi, default olarak template_name'i, registration/login.html e bakıyor. 
- Ancak biz users/templates/users/login.html'e baksın istiyoruz, login.html'i oraya koyacağız, 
- bu yüzden LoginView'in template_name'ini override etmemiz gerekiyor. 
- İşte .as_view() parantez içerisine bunu yazıyoruz.
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name='login')

- Artık "login" page imizin path'ini yazdık.

users/urls.py

```py
...
from django.contrib.auth import views as auth_views
...

urlpatterns = [
    ...,
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
]
```

###### login ( default built-in yapısıyla - template name'ini override ederek ) templates;

- Şimdi urls.py'da belirttiğimiz yerde yani users/templates/users içerisine login.html template imizi yazıyoruz.

users/templates/userslogin.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}  
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset>
            <legend class="border-bottom mb-4">Login</legend>
            {{ form | crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info" type="submit">Login</button>
            <small>
                {% comment %}{% url 'password_reset' %}henüz oluşturulmadı{% endcomment %}
                <a href="#">Forgot Password?</a> 
            </small>
        </div>
    </form>
    <div class="border-top pt-3">
        <small class="text-muted">Need an account?  <a href="{% url 'register' %}">Sign Up Now</a>
        </small>
    </div>
</div>
{% endblock content %}
```


- users/view.py'a gidip register view imizdeki return redirect('login') 'i yorumdan kurtaralım.
- Böylece register olan user direkt olarak "login" template'ine redirect edilsin.
- Aslında burada user'ı login() methoduyla login edip "list" template'ine de redirect edebiliriz. Bu projede böyle yapılmış.

users/view.py
```py
...

def register(request):
    form = RegisterationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')  
        # login page imizi oluşturduk
    
    ...
    return render(request, 'users/register.html', context )

...
```


- navbar.html'e gidip login linkinin href'ini active edelim;  

templates/navbar.html
```html
<header class="site-header">
    <!-- Navbar Right Side -->
    <div class="navbar-nav">
        {% if user.is_authenticated %}
        ...
        {% else %}
        {% comment %} {% url 'login' %} {% endcomment %}
        <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
        {% comment %} {% url 'register' %} {% endcomment %}
        <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
        {% endif %}
    </div>
</header>
```


- Test ettik, çalıştırdık,
- Önce register ile kayıt olduğumuzda, redirect ile login page'ine yönlendirildik. Çalışıyor. 
- "login" page geliyor, ama login button una basınca home page yani blog app imizin list page'i gelmiyor? 
- Login view'ini biz kendimiz yazmayıp djangodan aldığımız için djangonun default LoginView'inin de default olarak redirect ettiği path şu; 
    accounts/profile 

- Çünkü django default olarak login'i redirect ettiği path -> accounts/profile  
- Ama bizim profile diye bir sayfamız var, ancak accounts diye bir klasörümüz yok. 
- Eğer login view ini kendimiz yazmış olsaydık redirect i biz kendimiz verebilirdik.
- Bizim bu redirect url ini değiştirmemiz gerekiyor. 
- Bunu da settings.py'da değiştiriyoruz.
- settings.py' a gidiyoruz ve alt kısmına login olduğumuzda redirect edilecek template'i belirtiyoruz; 
    LOGIN_REDIRECT_URL = "blog:list"    

- yani; login olduğumda beni buraya (blog app'imin "list" page/template'ine (yani home page imize)) redirect et diyoruz.

settings.py
```py
...

LOGIN_REDIRECT_URL = "blog:list"

```

- Tekrar çalıştırdık, username ve password girdikten sonra login button'ına tıklayınca blog:list page ine yani home page imize yönlendirildik. Çalışıyor.


##### 2. logout ( default built-in yapısıyla - template name'ini override ederek );

- şimdi bir de logout olmamız gerekiyor;  

###### logout ( default built-in yapısıyla - template name'ini override ederek ) urls;

- users/urls.py'a gidip logout path imizi yazıyoruz (tıpkı login de olduğu gibi)

users/ urls.py
```py
...
from django.contrib.auth import views as auth_views
...

urlpatterns = [
    ...,
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
```

###### logout ( default built-in yapısıyla - template name'ini override ederek ) templates;

- logout template imizi oluşturuyoruz (tıpkı login de olduğu gibi) users/templates/users içerisine

users/logout.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% block content %}
<h2>You have been logged out</h2>
<div class="border-top pt-3">
    <small class="text-muted">
        <a href="{% url 'login' %}">Log in Again</a>
    </small>
</div>
{% endblock content %}
```

- navbar.html'de de logout linkimizi active edelim;
- logout için "post" methodu ile istek atılması gerektiğinden, 
  - logout isteğini methodu post ve action'ı "logout" endpoint/url'i olan bir form içinde, 
  - csrf token ile 
  - submit button ile yapıyoruz. 

templates/navbar.html
```html
<header class="site-header">
    <!-- Navbar Right Side -->
    <div class="navbar-nav">
        {% if user.is_authenticated %}

            {% comment %} {% url 'logout' %} {% endcomment %}                      
            <form action="{% url 'logout' %}" method="post" style="display: inline;">
                {% csrf_token %}
                <button type="submit" class="nav-item nav-link btn btn-link logout-btn">Logout</button>
            </form>
        
        {% comment %} {% url 'profile' %} {% endcomment %}
            <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
            <a class="nav-item nav-link" href="{% url 'blog:create' %}">New Post</a>
        {% else %}
            ...
        {% endif %}
    </div>
</header>
```


- password reset, password reset done, email işleri var ya onları yapıcaz ama oraya girmeden önce;


###### login required;

- login required yapacaktık, 
- örneğin logout olduğum durumda, bir post'un detail'inden like yapmaya çalışırsam hata veriyor. Çünkü AnonymousUser ile like yapmaya çalışıyorum. Ancak like için bir user gerekiyor. user'ın id'ini alıp Like toblosuna create ettiği için anonymous user (login olmamış) tarafından like yapılmaya çalışılırsa hata verecektir.

- 1. yani bir user'ın like yapabilmesi için login olmasını istememiz lazım;

- 2. ayrıca mesela login olmadan da url kısmına "create/" yazdığımız zaman da create.html template imi görebiliyor, bizim bunu engellememiz lazım, yani bizim buradaki create view imize; login required diye bir decorator ı var djangonun bu decorator ı eklememiz gerekiyor, login olmamışsan sen buraya gidemezsin!

- blog app imizin views.py'ına gidiyoruz, 


###### login required "create/";

- önce django.contrib.auth.decorators dan login_required ı import ediyoruz.
    from django.contrib.auth.decorators import login_required

- post _create view imizin hemen üzerine login_required decorator'ımızı yazıyoruz.
    @login_required()

- ve artık bizim create.html template imle gösterdiğim create sayfasına girebilmem için login olmam gerekiyor. 

blog/views.py
```py
...
from django.contrib.auth.decorators import login_required

...

@login_required()
def post_create(request):
    # form = PostForm(request.POST or None, request.FILES or None)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:list')
    context = {
        'form':form
    }
    return render(request, 'blog/post_create.html', context)

...
```

- Test ediyoruz, anonymous user ile url'den "create/" ile istek attığımız da bize bir hata verdi. 
- "/accounts/login/?next=/create/  hatası verdi. accounts/login yok dedi.
- accounts/login e gitmeye çalışıyor, bizim login imiz accounts un altında olmadığı için bizim usesr/urls.py ımızdaki login e gideceksin dememiz lazım.
- yani login url'ini belirtmemiz gerekiyor, onu da şöyle yapıyoruz, yine settings.py'e geliyoruz, yine en alt kısma    LOGIN_URL = "login"    yazıyoruz, 

- Bu hatayı yukarıda default LoginView'i kullanırken karşılaştığımız sorunu çözdüğümüz gibi çözüyoruz. 
  - orada django default olarak accounts/profile page'ine yönlendirmişti.
    - Bunun önüne geçmek için settings.py'da LOGIN_REDIRECT_URL = 'blog:list' belirtmiştik.
  - burada da django default olarak accounts/login page'ine yönlendiriyor. Ancak bizim böyle bi page'imiz olmadığı için;   
    - Bunun önüne geçmek için settings.py'da LOGIN_URL = 'login' belirtiyoruz.


settings.py
```py
......
LOGIN_REDIRECT_URL = "blog:list"

LOGIN_URL = "login"
```

- ve tekrar test edip, çalıştırıyoruz, 
- artık login olmadan url kısmına create yazarsak login decorator bizi login page e yönlendiriyor.

- login_required decorator'ı çok güzel, login ile korumak istenen sayfalar için import edilip, @login_required() kodu views'lerin üzerine yazılır.

- detail view'ine login_required decorator'ı koymuyoruz çünkü herkesin görmesini istiyoruz. 


###### login required "update/";

- update view imizi de login olmayanlardan korumak istiyoruz, 
- ancak onu zaten if request.user.id != obj.author.id   condition ıyla farklı user lar diğer userların post larını update edemesin diye yazmıştık. (eğer öyle olursa bizi list/home page e yönlendiriyor.) 
- Ama biz yine de garanti olsun diye onu koyalım. 
- Çünkü biz login olmamış birisi detail den update url iyle update etmeye çalışırsa biz onu da login'e yönlendirmek istiyoruz.

blog/views.py
```py
...
@login_required()
def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.user.id != obj.author.id:
        # return HttpResponse('You are not authorized!')
        return redirect('blog:list')
    if form.is_valid():
        form.save()
        return redirect('blog:list')
    context={
        'object':obj,
        'form':form
    }
    return render(request, 'blog/post_update.html', context)
...
```

- test ediyoruz, evet çalıştı.
- artık login olmayan birisi detail den url'e apdate yazarak gitmek isterse logine yönlendiriliyor.


###### login required "like/";

- Yine aynı şekilde like view'inin üzerine de @login_required() ekliyoruz ve like etmeye çalışırsa login olmamış birisi onu da login page'e yönlendiriyoruz.

blog/views.py
```py
...
@login_required()
def like(request, slug):
    if request.method == 'POST':
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect('blog:detail', slug=slug)
...
```

- test ediyoruz, evet çalıştı.
- artık login olmamış birisi like etmeye çalışırsa login page'e yönlendiriliyor.
- Ancak bu şekilde login olmaya çalışınca da, bu sefer hata veriyor. 
- Bu hatayı da şöyle çözdük, like edilince yani POST'ta redirect edilecek sayfayı söylemişiz ama GET de söylemeyi unutmuşuz.
- like view'inde; 
  - if request POST ise şöyle yap, sonra redirect et demişiz ama, 
  - İf request POST değil ise return render dememiz lazım. Şöyle yapıyoruz;
        return redirect('blog:detail', slug=slug)

blog/views.py
```py
...
@login_required()
def like(request, slug):
    if request.method == 'POST':
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs:
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect('blog:detail', slug=slug) # POST için redirect
    return redirect('blog:detail', slug=slug) # GET için redirect
...
```

- tets ediyoruz, ve evet çalıştı. 
- Sıkıntıyı şöyle çözdük; 
  - normalde view imizde POST için bir redirect sayfası vermişiz ama POST olmayan mesela isteği için bir redirect edilecek page vermemişiz, 
  - GET için bir sayfa render etmesi yerine zaten bulunduğu sayfaya redirect ettik, 
  - detail page'indeydi, detaile redirect etmesini söyledik.


###### login required "delete/";

- delete view'imizi de login olmayanlardan korumak istiyoruz, 
- yine biz onu zaten if request.user.id != obj.author.id   condition'ıyla farklı user'lar diğer userların post larını url kısmına /delete yazarak delete page ine gidemesin diye yazmıştık. (eğer öyle olursa bizi list/home page e yönlendiriyor.) 
- Ama biz yine de garanti olsun diye onu koyalım. 
- Çünkü biz login olmamış birisi detail den delete url iyle delete etmeye çalışırsa biz onu login e yönlendirmek istiyoruz.

blog/views.py
```py
...
@login_required() 
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.user.id != obj.author.id:
        # return HttpResponse('You are not authorized!')
        return redirect('blog:list')
    if request.method == 'POST':
        obj.delete()
        return redirect('blog:list')
    context = {
        'object':obj
    }
    return render(request, 'blog/post_delete.html', context)
...
```

- test ediyoruz, evet çalıştı.
- artık login olmamış birisi detail den delete url iyle delete etmeye çalışırsa login page e yönlendiriliyor.


#### messages

##### messages (for create);

- messages kısmına geldik, 
- django.contrib den messages ı import ediyoruz,
    from django.contrib import messages

- post_create view inde;
    - kullanıcı mesela post_create de create ettiği zaman, kullanıcıya bildirim yapalım,
    - post u save ettikten sonra, messages.success(request, "Post created successfully!")    
    (message_tags incelenebilir document'den, request ile alsın response ile dönsün (Burada dönecek yazıyı yazıyoruz.))
        messages.success(request, "Post created successfully!")

blog/views.py
```py
...
from django.contrib import messages

@login_required()
def post_create(request):
    # form = PostForm(request.POST or None, request.FILES or None)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('blog:list')
    context = {
        'form':form
    }
    return render(request, 'blog/post_create.html', context)
...
```

- Ama bu mesajı frontend e göndermemiz gerekiyor, bunu her sayfada ayrı ayrı messages diye tanımlamak yerine şöyle bir yöntem var;
- base.html'e gidiyoruz, navbar ın altında, div container ın dışında, bir container div içerisinde messages ı burada döneceğiz.

<div class="container">
    {% if messages %}        eğer response la dönen bir mesaj varsa
    {% for message in messages %}
    <div class="alert alert-{{message.tags}}">
    {{ message }}
    </div>  
    {% endfor %}
    {% endif %}
</div>


templates/base.html
```html
...
  <body>
    {% include 'navbar.html' %}
    
    <div class="container">
      {% if messages %}
      {% for message in messages %}
      <div class="alert alert-{{message.tags}}">
        {{ message }}
      </div>  
      {% endfor %}
      {% endif %}
    </div>

...
```


##### messages (for update);

- post_update view inde;

blog/views.py
```py
...
@login_required()
def post_update(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        messages.warning(request, "You're not a writer of this post ")
        return redirect('blog:list')
    if form.is_valid():
        form.save()
        messages.success(request, "Post updated!!")
        return redirect('blog:list')
    context={
        'object':obj,
        'form':form
    }
    return render(request, 'blog/post_update.html', context)
...
```


##### messages (for delete);

- post_delete view inde;

blog/views.py
```py
...
@login_required() 
def post_delete(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.user.id != obj.author.id:
        # from django.http import HttpResponse
        # return HttpResponse('You are not authorized!' )
        messages.warning(request, "You're not a writer of this post ")
        return redirect('blog:list')
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Post deleted!!")
        return redirect('blog:list')
    context = {
        'object':obj
    }
    return render(request, 'blog/post_delete.html', context)
...
```

- Test ettik, create, update, delete, messages'ları çalışıyor.

- Bir de bu message ibaresi ekranda sürekli durmasın. Belli bir müddet sonra kaybolsun diye javascript kodu yazalım.

#### javascript kodu ekleme setTimeout()

- css'lerin bulunduğu yere bir tane de timeout.js dosyası create edip JS kodumuzu yazıyoruz.

blog/static/blog/timeout.js
```js
let element = document.querySelector('.alert')

setTimeout(function() {
    element.style.display = 'none';
}, 3000);
```

- messages'larımızın da çalıştığı yer olan base.htm'de JS dosyamızı ekliyoruz.

templates/base.html
```html
...
  <!-- timeout.js Script -->
    <script src="{% static 'blog/timeout.js' %}"></script>
</body>
...
```

- Test ediyoruz. Çalıştı. Message'ların hepsi 3 sn sonra kayboluyor.
 

- blog app'deki yapacaklarımızın hepsini, eklemeleri, çıkarmaları, süslemeleri filan yaptık.
- view_count eksik. Tamamlanması gerekiyor! 

- Şimdi user view ine geri dönelim, 


###### register url'ini korumaya almak;

- blog umuzda şöyle bir açık var, bir kullanıcı logout iken navbar da Login ve Register görüyor, 
- tıklayınca Login, Register a gidiyor. 
- Ama zaten register olmuş bir kullanıcı da url'de manuel olarak users/register veya users/login yazınca o da bu sayfalara ulaşabiliyor. 
- Yani register veya login olduktan sonra bu sayfalara manuel de olsa ulaşmasını istemiyoruz. 
- Bunu istemiyoruz, bunun önüne geçmek için ;

- users/view.py'a gidip; 
  - register view ine, böyle bir durum için bir hata mesajı yazdıracağız. 
  - tabi django.contrib den messages paketini import ediyoruz.
  - sonra view de ilgili yere şunu yazıyoruz; eğer kullanıcı authenticated (kimliği doğrulanmış) ise, bu hata mesajını ver!
        if request.user.is_authenticated():  
            message.warning(request, "You already have an account!") 
  - sonra blog app'in list/home page'ine redirect et!
        return redirect("blog:list")

users/views.py
```py
...
from django.contrib import messages

def register(request):
    form = RegisterationForm(request.POST or None)
    if request.user.is_authenticated:
        messages.warning(request, "You already have an account!")
        return redirect("blog:list")
    if form.is_valid():
        form.save()
        return redirect('login')  
        # login page imizi oluşturduk
    
    context = {
        'form': form,
    }
    
    return render(request, 'users/register.html', context )
...
```

- Tamamdır, artık hali hazırda login olmuş birisinin url de manuel olarak users/register ile register page ine gitmesini önledik.


- Ayrıca register olmaya çalışan bir kullanıcıya register olduğuna dair bir message verelim, doldurduğu form daki username i alıp,
    name = form.cleaned_data.get('username')
        veya
    name = form.cleaned_data["username"]

- ... ismindeki hesabın başarıyla oluşturuldu mesajını da yazdır!
    messages.success(request, f"Account created for {name} successfully")


users/views.py
```py
...
def register(request):
    form = RegisterationForm(request.POST or None)
    if request.user.is_authenticated:
        messages.warning(request, "You already have an account!")
        return redirect("blog:list")
    if form.is_valid():
        form.save()
        # name = form.cleaned_data.get('username')
        name = form.cleaned_data["username"]
        messages.success(request, f"Account created for {name} successfully.")
        return redirect('login')  
        # login page imizi oluşturduk
    
    context = {
        'form': form,
    }
    
    return render(request, 'users/register.html', context )
...
```

- Test ediyoruz. Çalıştı. Bir user create edildiğinde message'ı gördük.
  

- Profile'a gelelim ve eğer profile page update edilirse redirect etmeden önce şöyle bir mesaj gönderelim;
messages.success(request, "Your profile has been updated!")
profiliniz update edildi.
    messages.success(request, "Your profile has been updated!")


users/views.py
```py
...
def profile(request):
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=request.user.profile)
    
    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, "Your profile has been updated!")
        return redirect(request.path)
    
    context = {
        "u_form": u_form,
        "p_form": p_form,
    }
    
    return render(request, "users/profile.html", context)
...
```

- Test ettik. Çalıştı. Profile page'inde user, profile'ını update edince message'ımızı gördük.


- login page'deki en altta bulunan Sign Up Now'a tıklayınca register page'e gidiyoruz.
- register page'deki en alttaki Sign In'e tıklayınca login page'e gidemiyoruz.
- register.html'deki Sign In anchor tag'ine gidip href'ine {% url 'login' %} yazarak login page ine link veriyoruz.

users/register.html
```html
...
    <div class="border-top pt-3">
        <small class="text-muted">
            {% comment %}{% url 'login' %}{% endcomment %}
            Already have an account?<a class="ml-2" href="{% url 'login' %}">Sign In</a>
        </small>
    </div>
...
```

- Test ettik. Çalışıyor. Artık register page deki en alttaki Sign In e tıklayınca login page e gidebiliyoruz.



#### password change, change_done, reset, reset_confirm, reset_done

- user'ın password işlemlerini djangonun built-in view'lerini kullarak yapacağız.
- default view'lerini kullanarak, onlara urls.py da path belirleyip,
- bu viewler için birer de template yazıp, tüm bu işlemleri yapacağız.

- Mesela;
- password'ü unuttum,
  - email imize mail göndersin, 
  - oradan bize link versin, 
  - o linke tıklayıp tekrardan password ümüzü güncelleyelim/oluşturalım.

- Bunun için users/urls.py'ına geliyoruz, 

- burada djangonun bize default olarak verdiği 
  - password_change/, 
  - password_change/done, 
  - password_reset/, 
  - password_reset/done 
- path/endpointlerini kullanacağız.

https://docs.djangoproject.com/en/5.1/topics/auth/default/

accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']


##### password_reset;

- Önce password_reset ile başlayacağız,
- djangonun built-in olarak default verdiği PasswordResetView'ini kullanacağız.
- PasswordResetView'inin default olarak render ettiği template'i (regiseter/password_reset.html) değiştirip kendi template'imizi render etmesini sağlayacağız.
- Eğer kullanıcı passwor'ünü unuttuysa,
- kullanıcıya bir password_reset.html ini göndereceğiz daha sonra diğer işlemleri yapacağız.
- login.html'imizde bulunan Login button un hemen yanındaki Forgot Password linki ile password_reset view ine yönlendireceğiz,


###### password_reset urls;

- Şimdi users/urls.py'a geliyoruz, 
- path ini yazıyoruz,
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),    
    
- Burada önemli olan husus, path name inin djangonun bize verdiği default name olarak kalması, 
- yani default olarak bize name'i "password_reset" olarak veriyor, bizim de öyle kullanmamız gerekiyor, 
- ancak url'ine istediğimiz ismi verebiliriz, mesela 'password-reset/' ayarlayıp, user'ın /password-reset/ endpoint'ine istek atmasıyla reset view'inin çalışmasını sağlayabiliriz.
- bir de template_name'i biz override ettiğimiz için; 
- normalde template'in barındırılması gereken yer default olarak "registration/password_reset.html"
- Ancak biz template'i "users/password_reset_email.html" klasör yapısında barındırmak istiyoruz.
- Bunun için PasswordResetView'ine, as_view() fonksiyonunun içinde parametre olarak template'imizin konumunu ve ismini gönderiyoruz.
- Bu template barındırma hususunda da sorun yok.
- Fakat path_name'i djangonun verdiği default_name olmalı. Yani path name -> name='password_reset'  olmalı.
- Böylelikle password_reset view'ini kendimiz yazmadık.
- login ve logout da olduğu gibi djangodan aldık.

users/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...,
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),
]
```

###### password_reset templates;

- Şimdi gelelim template ini oluşturmaya, users/templates/users/password_reset_email.html oluşturmaya, 
- Bu template içerisinde; PasswordResetView view'i sayesinde;
  - methodu post olan bir form render ediyoruz.
  - doldurulmuş form, submit button'ı ile form'u post olarak gönderiliyor. 
- form'u crispy ile dizayn ediyoruz.

users/password_reset_email.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Reset Password</legend>
            {{ form | crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info"type="submit">Request Reset</button>
        </div>
    </form>
</div>
{% endblock content %}
```

- password_reset_email.html'e erişim için;
  - login page'de Login button'ın yanındaki "Forgot Password?" linkini aktif hale getiriyoruz.

users/login.html
```html
...
    <div class="form-group">
        <button class="btn btn-outline-info" type="submit">Login</button>
        <small>
            {% comment %}{% url 'password_reset' %}henüz oluşturulmadı{% endcomment %}
            <a href="{% url 'password_reset' %}">Forgot Password?</a> 
        </small>
    </div>
...
```

- Test ediyoruz. Çalıştırdık. Evet çalışıyor. 
- linke tıklayınca password_reset.html'e gidiyor. 
- Ancak login olmuş bir kullanıcı da url e manuel olarak /users/password-reset/ yazarsa o da password_reset.html e gidebiliyor. 
- Bunu nasıl önleyeceğiz?
- Aslında önlemeye gerek var mı? Çünkü zaten user login olmuş. Eğer password'ünü resetlemek isterse buna gerek yok, çünkü password_change var. Ama login olduktan sonra unuttuysa o zaman normal bir şekilde de password_reset'e gideblir. Bu şekilde gitmesinde de bir sakınca olmamalı. Ama tabi bunun da önüne geçilebilir diye düşünüyorum.


##### password_reset_done ve password_reset_confirm;

- Password_reset çalıştı, bir form render edildi, user form'u (email ile) doldurdu, formu gönderdi.
- Bu aşamadan sonra yine default olarak verilmiş olan PasswordResetDoneView diye bir view kullanacağız 
- Bu view sayesinde, user'a "- size bir email gönderdik, emailinize gidin ve şeyinizi alın"
- hemen arkasından da password_reset_confirm için viewler'in urls/endpoint'lerini ve template yazacağız.

###### password_reset/done urls;

- users/urls.py'a gidip;,
- djangonun contrib auth'dan aldığımız default oluşturulmuş viewini import edip path ini yazıyoruz,
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),

- Yine dikkat etmimiz gereken path name olarak default name'in verimesi yani: name='password_reset_done'

- Bu isimlere nereden bakıyoruz? Bu linkten.
    https://docs.djangoproject.com/en/5.1/topics/auth/default/

users/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...,
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
]
```

###### password_reset/done templates;

- Şimdi gelelim template ini oluşturmaya, 
- users/templates/users/password_reset_done.html

users/password_reset_done.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% block content %}
<div class="alert alert-info">
    <p>We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.</p>
    <p>If you don't receive an email, please make sure you've entered the address you restered with, and check your spam folder.</p>
</div>
{% endblock content %} 
```


###### password_reset_confirm urls;

- Adım adım ilerliyoruz; 
  - önce password_reset, 
  - password_reset_done, 
  - şimdi password_reset_confirm  i yapacağız,  

- users/urls.py'a gidip, yine djangonun default viewlerinden PasswordResetConfirmView'ini kullanacağız,
- burada url'imiz biraz değişiyor, 
- "password-reset-confirm/<uuid64>/<token>"  password-reset-confirm olarak verdiğimiz ismi değiştirebiliriz, ancak arkasından gelen <uuid64> ve <token> parametrelerini kullamanız gerekiyor.
- bunlar password reset'i kullanan kullanıcının mail'ine link gönderirken bir token üretiyor, o token ile kullanıcı gelen mail'deki linke tıklıyor ve tarayıcısındaki password reset page'inde yeniden şifre üretebiliyor. 
    path('password-reset-confirm/<uuid64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),

users/urls.py
```py
... 
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...,
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
]
```

###### password_reset_confirm template;

- Şimdi PasswordResetConfirmView'inin render edeceği template'i oluşturalım. 
- users/templates/users/password_reset_confirm.html

users/password_reset_confirm.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset>
            <legend class="border-bottom mb-4">Reset Password</legend>
            {{ form | crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info"type="submit">Reset Password</button>
        </div>
    </form>
</div>
{% endblock content %}
```


##### password_reset_complete;

- Sıradaki password_reset_complete

##### password_reset_complete urls;

- users/urls.py'a geliyoruz, yine djangonun default PasswordResetCompleteView'ini kullanacağız,
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

users /urls.py
```py
..
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
```

##### password_reset_complete templates;

- Şimdi gelelim template ini oluşturmaya, users/templates/users/password_reset_complete.html oluşturmaya, 

users/password_reset_complete.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% block content %}
<div class="alert alert-info">
    Your password has been set successfully!
</div>
<a href="{% url 'login' %}">Sign In Here</a>
{% endblock content %}
```


- Test ettik. Çalıştı.
  - Login olmaya çalışırken, password_reset (Forgot Password?) dedik.
  - email'i yazıp gönderdik, (password_reset template)
  - "e-posta'ıza link gönderdik, gidip oradaki linkten password oluşturabilirisiniz."  (password_reset_confirm template) şeklindeki uyarıyı gördük.

- Fakat henüz password'ünü resetleyen user'ın email'ine, password'ünü yenileyebilmesi için gerekli olan mail'i göndermedi.
- Henüz email backendini kurmadık. 


#### password işlemleri için email ayarları; 

- djangoda email göndermek için settings.py da bazı ayarlar yapmamız gerekiyor. 
    https://docs.djangoproject.com/en/5.1/topics/email/

- gizlilik gerektiren değişkenleri .env file'ına taşıyoruz.

settings.py
```py
# Sending email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
```

.env
```py
# Sending email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = developerumit@gmail.com
EMAIL_HOST_PASSWORD = "google_app_password"
EMAIL_USE_TLS = True
```


email için gmail deki ayarlar:   (Deneme için )
https://myaccount.google.com/security

- google account
  - Güvenlik
    - 2 adımlı doğrulama 
      - "Uygulama şifreleri ile oturum açma" linkinden "uygulama şifrenizi oluşturun ve yönetin" ile 16 haneli bir şifre oluştur.
        - bu oluşturulan uygulama şifresini .env'deki email_host_password'e tanımla. 


- Test ediyoruz. Çalıştı.
- Forgot Password? linkinden email adresimizi yazınca, user'ın email adresine bir link gönderdi. 
- user email'ine gelen linke tıklayınca, password oluşturma page'ine yönlendirdi. 
- user buradan kendine yeni bir password oluşturdu. 


- Fakat şöyle bir açık yakaladık;
- Forgot Password? linki ile user'ı yönlendirdiğimiz password_reset_email.html template'indeki email input'una, db'de kayıtlı olmayan bir email adresi bile girsek, o girdiğimiz ve db'de kayıtlı olmayan email adresine de password oluşturmak için bir link gönderiyor.
- Bu açığı kapatmak için, password_reset_email.html template'ini render eden default PasswordResetView'inin kullandığı form olan PasswordResetForm' u override edeceğiz.
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name='password_reset'),


###### db de kayıtlı olmayan email adresine password-reset linki gönderilmesin;

- Bunun için forms.py'da, PasswordResetForm'dan inherit ederek bir form class'ı oluşturacağız. Böylelikle;
  - Bu şekilde oluşturduğumuz class, PasswordResetForm'un tüm özelliklerini alacak,
  - ilave olarak da, kullandığı "email" değişkeni üzerinde bir condition oluşturup, 
    - eğer email olarak girilen değer db'de kayıtlı değilse hata raise et! 
    - db'de kayıtlı ise de email'i döndür'
    - diyeceğiz.

- Öncelikle forms.py'a gidip, UserCreationForm'u da inherit ettiğimiz django.contrib.auth.forms'dan PasswordResetForm'u import ediyoruz.
    from django.contrib.auth.forms import PasswordResetForm

- PasswordResetEmailCheckForm isminde, class yapısında, ve de PasswordResetForm'dan inherit ederek bir form oluşturuyoruz. 
    class PasswordResetEmailCheckForm(PasswordResetForm):

- Bu form ile PasswordResetForm'un tüm özelliklerini almış olduk. Bu özelliklerine ilave olarak formun içindeki email field'ı için bir condition yazacağımız için, clean_"field_name" ismi ile fonksiyonumuzu/methodumuzu yazıyoruz;
    def claen_email(self):

- formun içinden email datasını çekiyoruz;
    email = self.cleaned_data["email"]

- Bu işlemin aynısını RegistrationForm'da da yapmıştık. eğer girilen email adresiyle aynı olan bir user var ise ValidationError döndürüyordu. Burada tam tersini yapacağız. Yani db'de böyle bir email yoksa ValidationError döndüreceğiz. 

- condition'ımızı yazıyoruz; eğer bu email db'de kayıtlı değil ise (User tablosunda kayıtlı olan email'ler arasında değil ise), hata ValidationError döndür. else, yani db'de kayıtlı ise, o zaman girilen email'i döndür.
    if not User.objects.filte(email=email).exists():
        raise forms.ValidationError("There is no email")
    return email

users/forms.py
```py
...
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

#! email-reset için email'in db'de olup olmadığının kontrolü; 
class PasswordResetEmailCheckForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-posta adresi ile kayıtlı bir hesap bulunamadı.')
        return email
```

- Formumuzu yazdık. Nasıl kullanacağız?
- Şimdi artık password reset için kullandığımız default PasswordResetView'inin form olarak kendi default formu olan PasswordResetForm'u değil de bizim bu form'dan inherit ederek oluşturduğumuz ve "email" field'ı için bir condition yazdığımız PasswordResetEmailCheckForm'unu kullanmasını bildirmemiz gerekiyor.

- Bunu da şu şekilde bildiriyoruz;
- PasswordResetView'ini direkt olarak users/urls.py'da path'e yazarak belirttiğimiz için, as_view() methodunun içine parametre olarak gönderiyoruz. Yani aynı template_name parametresi gibi form_class parametresi olarak gönderiyoruz. form_class olarak users/forms.py'da yazdığımız PasswordResetEmailCheckForm'u kullan!  
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html', form_class=PasswordResetEmailCheck), name='password_reset'),

- Tabi users/urls.py'da PasswordResetEmailCheckForm'unu import ediyoruz.
    from .forms import PasswordResetEmailCheckForm

users/urls.py
```py
...
from .forms import PasswordResetEmailCheckForm

urlpatterns = [
    ...,
        path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html', form_class=PasswordResetEmailCheckForm), name='password_reset'),
]
```

- Test ettik, çalışıyor. db'kayıtlı olmayan bir email adresi için password-reset isteği için  ValidationError döndürüyor.



##### password_change;

- password_change,
- djangonun built-in olarak default verdiği PasswordChangeView'ini kullanacağız.
- PasswordChangeView'inin default olarak render ettiği template'i (regiseter/password_cgange.html) değiştirip kendi template'imizi render etmesini sağlayacağız.
- Eğer kullanıcı passwor'ünü değiştirmek isterse,
- kullanıcıya bir password_change.html ini göndereceğiz daha sonra diğer işlemleri yapacağız.
- profile.html'imizde bulunan Update button'un hemen yanındaki Password Change linki ile password_change view ine yönlendireceğiz,


###### password_change urls;

- Şimdi users/urls.py'a geliyoruz, 
- path ini yazıyoruz,
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_reset_email.html'), name='password_change'),
    
- Burada önemli olan husus, path name inin djangonun bize verdiği default name olarak kalması, 
- yani default olarak bize name'i "password_change" olarak veriyor, bizim de öyle kullanmamız gerekiyor, 
- ancak url'ine istediğimiz ismi verebiliriz, mesela 'password-change/' ayarlayıp, user'ın /password-change/ endpoint'ine istek atmasıyla change view'inin çalışmasını sağlayabiliriz.
- bir de template_name'i biz override ettiğimiz için; 
- normalde template'in barındırılması gereken yer default olarak "registration/password_change_form.html"
- Ancak biz template'i "users/password_change_form.html" klasör yapısında barındırmak istiyoruz.
- Bunun için PasswordResetView'ine, as_view() fonksiyonunun içinde parametre olarak template'imizin konumunu ve ismini gönderiyoruz.
- Bu template barındırma hususunda da sorun yok.
- Fakat path_name'i djangonun verdiği default_name olmalı. Yani path name -> name='password_change'  olmalı.
- Böylelikle password_change view'ini kendimiz yazmadık.
- login ve logout da olduğu gibi djangodan aldık.

users/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...,
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
]
```

###### password_change templates;

- Şimdi gelelim template ini oluşturmaya, users/templates/users/password_change_form.html oluşturmaya, 
- Bu template içerisinde; PasswordChangeView view'i sayesinde;
  - methodu post olan bir form render ediyoruz.
  - doldurulmuş form, submit button'ı ile form'u post olarak gönderiliyor. 
- form'u crispy ile dizayn ediyoruz.

users/password_change_form.html
```html
{% extends 'base.html' %}
{% block title %}login{% endblock %}
{% load crispy_forms_tags %}
{% block content %}
<div class="content-section">
    <form action="" method="post">
        {% csrf_token %}
        <fieldset class="form-group">
            <legend class="border-bottom mb-4">Change Password</legend>
            {{ form | crispy }}
        </fieldset>
        <div class="form-group">
            <button class="btn btn-outline-info"type="submit">Change Password</button>
        </div>
    </form>
</div>
{% endblock content %}
```

- password_change_form.html'e erişim için;
  - profile page'de Update button'ın yanındaki "Password Change" linkini aktif hale getiriyoruz.

users/profile.html
```html
...  
    <div>
         <button class="btn btn-outline-info" type="submit">Update</button>
         <a href="{% url 'password_change' %}"><button class="btn btn-outline-info" type="button">Password Change</button></a>
    </div>
...
```

- Test ediyoruz. Çalıştırdık. Evet çalışıyor. 
- linke tıklayınca password_change.html'e gidiyor.
- Karşımıza gelen formda eski password'ümüz, ve yeni password'ümüzü iki defa yazmamızı istiyor.
- Formu doldurup Password Reset button'una bastığımızda, bizden password_resete_done template'i beklediğine dair hata mesajı alıyoruz.
- Fakat aslında password'ümüzü değiştirmiş oluyoruz. Sadece bu değişiklikten sonra user'a password'ünün değiştiğine dair bir bilgilendirme sunmak için password_resete_done template'ine ihtiyacımız var.

##### password_change_done;

- Password_change çalıştı, bir form render edildi, password change form'u doldurdu, formu gönderdi.
- Bu aşamadan sonra yine default olarak verilmiş olan PasswordChangeDoneView diye bir view kullanacağız 
- Bu view sayesinde, user'a "password'ünüz değişti" şeklinde bir template render edeceğiz.

###### password_change/done urls;

- users/urls.py'a gidip;,
- djangonun contrib auth'dan aldığımız default oluşturulmuş viewini import edip path ini yazıyoruz,
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

- Yine dikkat etmimiz gereken path name olarak default name'in verimesi yani: name='password_change_done'

- Bu isimlere nereden bakıyoruz? Bu linkten.
    https://docs.djangoproject.com/en/5.1/topics/auth/default/

users/urls.py
```py
...
from django.contrib.auth import views as auth_views

urlpatterns = [
    ...,
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
]
```

###### password_change/done templates;

- Şimdi gelelim template ini oluşturmaya, 
- users/templates/users/password_change_done.html

users/password_change_done.html
```html
{% extends 'base.html' %}
{% block title %}Password Change Successful{% endblock %}
{% block content %}
<div class="alert alert-success" role="alert">
    <h4 class="alert-heading">Password Changed Successfully!</h4>
    <p>Your password has been changed successfully. You can now use your new password to log in.</p>
    <hr>
    <p class="mb-0">If you did not request this change, please contact support immediately.</p>
</div>
<a href="{% url 'blog:list' %}" class="btn btn-primary">Return to home page</a>
{% endblock content %}
```





/// PROJE BİTTİ ///

- Django_Proj_Temp_Blog_App_V.02_AJAX -> sayfa render etmeden like yapılması;

- Copilot'a soru: 
  - Merhaba Copilot, çalıştığım projede like view ile bir post'u her like edişimde tüm sayfa tekrar render ediliyor. ben daha önce javascript'in react kütüphanesi ile çalışırken öğrenmiştim ki; bu tarz işlemlerde tüm sayfayı tekrardan render etmeden sayfadaki belli bir bölümde değişiklik yapılabiliyor. Aynı bu şekilde djangoda oluşturmaya çalıştığım bu projede de bir user, bir post'u like ederken tüm sayfatı değil de sadece like kısmı render olsun istiyorum. Bunu nasıl başarabilirim?


- Django'da bu tür işlemleri gerçekleştirmek için AJAX kullanabilirsiniz. AJAX, sayfanın tamamını yeniden yüklemeden sunucudan veri almanıza ve sayfanın belirli bölümlerini güncellemenize olanak tanır. Bu, kullanıcı deneyimini iyileştirir ve performansı artırır.

- MySQL Workbench (optional)