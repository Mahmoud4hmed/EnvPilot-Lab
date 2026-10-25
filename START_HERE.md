# EnvPilot Lab — ابدأ هنا

يا محمود، ده معمل عملي مستقل لمنتج خيالي بيدير development environments مؤقتة.
المستهدف 14 ساعة تركيز في يومين، والـmock آخر 3 ساعات منهم. الـbreaks زيادة.
دي target timeboxes مش وعد إن كل حاجة هتخلص في نفس الوقت.
التمارين فيها defects مقصودة؛ دورك تقرأ الكود وتعيد إنتاج المشكلة وتصلحها وتشرح قراراتك.
دي مش نسخة من تقييم EasyEnv، ومفيش ادعاء إننا عارفين أسئلة المقابلة.

## التشغيل

محتاج Docker Engine وCompose v2، وPython 3.10+ للـCLI فقط. أول build محتاج Internet.
على Windows: شغّل Docker Desktop بوضع Linux containers، فعّل WSL2 integration لتوزيعة Ubuntu من Settings → Resources → WSL Integration.
التنفيذ الموصى بيه من WSL2. ممكن تنسخ المجلدين المتجاورين تحت `~/envpilot` لأداء ملفات أحسن.
متغيّرش host services. مفيش Docker socket mount أو privileged containers.
خصص تقريبًا 4 CPUs و6 GB RAM لـDocker. الـstack معمول للابتوب، والخدمات الداخلية مش exposed للـhost.

من WSL2:

```bash
cd '/mnt/d/Code/Job Application System/EnvPilot-Lab'
python3 lab.py doctor
python3 lab.py up
python3 lab.py check smoke
```

من PowerShell:

```powershell
cd 'D:\Code\Job Application System\EnvPilot-Lab'
python lab.py doctor
python lab.py up
python lab.py check smoke
```

افتح http://localhost:8090. الحسابات fictional وكلها password: `LabPass123!`.

| Username | Membership |
|---|---|
| mahmoud | Nile Labs owner |
| developer | Nile Labs developer |
| viewer | Nile Labs viewer |
| nora | Delta Works owner |
| dual | developer in both organizations |
| outsider | no memberships |

أول `up` بيعمل migrations وadditive seed. التكرار مبيمسحش شغلك أو notes أو يغير password اتعدّل.
فيه 480 environment و1440 history events في أول seed. هات IDs من `/api/me/` و`/api/projects/` بدل ما تفترض أرقام ثابتة.
`up` مش بيصلح التمارين، وبيحافظ على incident نشط. طفّيه بالـstop قبل baseline smoke.

## أول خطوة فعلية — 30 دقيقة

افتح [DAY_1.md](DAY_1.md)، انسخ [قالب الملاحظات](notes/TEMPLATE.md) إلى `notes/day-1.md`.
سجّل نتيجة smoke، ارسم request path من Nginx لحد DB، جرّب login واعرض environment واحد.
اقرأ contract قبل التعديل. بعد كده افتح [Exercise 1](issues/01-api.md).
متفتحش المجلد المجاور `EnvPilot-Instructor` أثناء التدريب؛ فيه grader وreference repairs للتأكد من عدالة التمرين.
الـchecks بتستدعيه تلقائيًا. الفصل لتنظيم self-study، مش security boundary.

## قواعد مهمة

`python lab.py check smoke` لازم ينجح لما البنية التحتية شغالة.
`python lab.py check 1` إلى `7` متوقع يفشل في assertions مرتبطة بالتمرين لحد ما تصلحه.
Build/connection/import/collection failures أعطال infrastructure، مش جزء من المطلوب منك.
اقرأ [VERIFICATION.md](VERIFICATION.md) لمعرفة اللي اتنفذ فعلًا وقت البناء.
متستخدمش SQLite كدليل على PostgreSQL concurrency، ومتعتبرش eager task اختبار worker.

## أوامر يومية

```bash
python3 lab.py down                 # stop, keep data
python3 lab.py up                   # restart, keep code/data/notes
python3 lab.py seed                 # additive, preserve existing objects
python3 lab.py check 3              # PostgreSQL parallel API + actual worker/provider
python3 lab.py hint 3 1             # only the explicitly requested hint
python3 lab.py incident start proxy
python3 lab.py incident stop proxy
python3 lab.py incident start queue
python3 lab.py incident stop queue
python3 lab.py reset 2              # print exact scope, change nothing
python3 lab.py reset 2 --yes        # mandatory backup, then selected code only
python3 lab.py e2e                  # browser happy path; downloads browser image
```

تعديلات الـbackend موجودة في bind mount، بس Gunicorn/Celery مش autoreload:
`docker compose restart api worker`. الواجهة بتعمل hot reload؛ تغييرات dependencies محتاجة rebuild.
لو incident نشط استخدم أوامر `lab.py` لإعادة إنشاء الخدمة بالـoverlay الصحيح.
Reset بيرجع ملفات الكود المختارة، مش DB أو migrations اللي انت أضفتها. ملفات مشتركة بين تمارين ممكن تتأثر؛ اقرأ scope الأول.
النسخة الاحتياطية في `.lab/backups/`، والـreports في `.lab/reports/`. متحذفش volumes عشان تعيد تجربة سيناريو؛ استخدم pending environment جديد وidempotency key جديد.

## بعدين: mock مستقل

لما تكون جاهز فقط: `python3 lab.py exam start`. هيجهز workspace وCompose project وDB مستقلين على port 8091.
اقرأ [MOCK.md](MOCK.md) لقواعد الوقت والتسليم؛ تفاصيل المهام بتظهر جوه workspace الامتحان وقت البدء.
