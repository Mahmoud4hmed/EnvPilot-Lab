# Independent three-hour mock

ابدأ بس لما تكون جاهز: `python lab.py exam start`.
الـCLI بينسخ template مستقلة من instructor folder إلى sibling `EnvPilot-Mock` مرة واحدة، ويشغّل Compose project `envpilot-mock` وDB منفصلين على http://localhost:8091.
مش بيعتمد على أي إصلاح عملته في تمارين التدريب. exact issue cards بتظهر في `EnvPilot-Mock/TASKS.md` وقت البدء.

`python lab.py exam status` يعرض UTC start time والوقت المتبقي. الوقت مستمر بعد قفل terminal/browser.
`exam start` مرة تانية resume لنفس الوقت ونفس الشغل؛ لا reset صامت. الوقت advisory؛ عند انتهاء 180 دقيقة مفيش حذف أو قفل ملفات.
`python lab.py exam submit` بيحفظ snapshot آمن من شغلك، يشغّل checks ويطلع report مستقل. بيحافظ على الأصل وبيدعم إعادة عرض آخر تسليم.
الساعة بتبدأ عند أول start قبل تجهيز الـstack؛ لو setup اتعطل، سجّل الوقت وخده في المراجعة اليدوية، الـtimer مش security boundary.
الـfeedback بيشمل functional checks، ومراجعة يدوية للـtests/diagnosis/engineering explanation، وأهم 3 أولويات للتحسين. الدرجة النهائية من 100 بعد المراجعة اليدوية، مش percentage آلي يوهمك إنه تقييم كامل.
المهام 3 فقط: API behavior، React async state، service configuration. اقرأ criteria وقت البدء، واكتب notes من قالب الامتحان.
