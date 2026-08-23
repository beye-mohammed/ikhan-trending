# TMDB Weekly Trending → JSON

Workflow خدام على GitHub Actions كيجيب Trending Movies / TV Series / Anime ديال هاد الأسبوع من TMDB،
وكيصيفط النتيجة فـ `data/trending.json` (عنوان + بوستر غير).

## خطوات الإعداد

### 1. حصل على TMDB API Key
- سجل فـ https://www.themoviedb.org
- سالي بالإيميل بحال verified، بعدها روح لـ Settings → API
- خد "API Key (v3 auth)"

### 2. زيد الـ Secret فـ GitHub
فالريبو ديالك:
`Settings → Secrets and variables → Actions → New repository secret`

- Name: `TMDB_API_KEY`
- Value: المفتاح لي جبتي

### 3. حط الملفات
```
.github/workflows/trending.yml
scripts/fetch_trending.py
```
دوز الاثنين للريبو ديالك بحال ما هوما (git add / commit / push).

### 4. شغل الـ workflow
- روح لتبويب **Actions** فالريبو
- اختار "Update TMDB Trending"
- دوس "Run workflow" باش تجربها مباشرة (workflow_dispatch)
- أو خليها تخدم وحدها كل الاثنين على 06:00 UTC (تقدر تبدل التوقيت فـ cron)

### 5. النتيجة
بعد ما تخدم، غادي تلقى/يتحدث ملف:
```
data/trending.json
```

## شكل الـ JSON

```json
{
  "movies": [
    { "title": "Movie Name", "poster": "https://image.tmdb.org/t/p/w500/xxxx.jpg" }
  ],
  "tv_series": [
    { "title": "Series Name", "poster": "https://image.tmdb.org/t/p/w500/xxxx.jpg" }
  ],
  "anime": [
    { "title": "Anime Name", "poster": "https://image.tmdb.org/t/p/w500/xxxx.jpg" }
  ]
}
```

## ملاحظات مهمة

- **الفلترة ديال Anime**: TMDB ما عندهاش category اسمها "anime" مباشرة.
  السكريبت كيدير فلترة heuristic: أي عنصر من TV/Movies اللي عندو `genre = Animation`
  و `original_language = ja` (ياباني) → كيتحسب anime. هاد الطريقة مقبولة بزاف
  ديال الحالات، ولكن ماشي 100% دقيقة (مثلاً بعض الأفلام اليابانية غير-anime
  ممكن يدخلو، أو anime بلغة ثانية ما يدخلوش).

- **تغيير عدد النتائج**: TMDB كيرجع صفحة وحدة (~20 نتيجة) فكل endpoint.
  إلا بغيتي أكثر، خاصك تزيد صفحات إضافية (`page=2`, `page=3`...) بنفس الطريقة.

- **cron schedule**: `0 6 * * 1` تعني كل يوم اثنين 06:00 UTC.
  إلا بغيتي كل يوم بدلها لـ `0 6 * * *`.

- الـ workflow كيعمل commit تلقائي للتغييرات فـ `data/trending.json`
  إلا كانت النتيجة تبدلات، وإلا ما بدلاتش ما غاديش يدير commit فارغ.
