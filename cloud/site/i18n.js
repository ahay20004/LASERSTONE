/* LASERSTONE public-preview UI translations. Scientific data is never auto-translated. */
const translations = {
  "en": {
    "skip": "Skip to content",
    "brandSub": "Research platform",
    "navResearch": "Research",
    "navIntegrity": "Integrity",
    "navAccess": "Access",
    "languageLabel": "Language",
    "preview": "PUBLIC PREVIEW · UNDER DEVELOPMENT",
    "hero1": "Scientific modelling with",
    "hero2": "traceable evidence.",
    "lead": "LASERSTONE connects laser physics, photonics, materials and photovoltaic research through transparent computational workflows. This preview contains no private research data or live simulation service.",
    "explore": "Explore research areas",
    "researchAccess": "Research access",
    "note": "Scientific status: platform development. No experimental or numerical validation is implied by this preview.",
    "domains": "RESEARCH DOMAINS",
    "researchTitle": "Designed for scientific workflows",
    "laserTitle": "Laser & photonics",
    "laserDesc": "Modelling, spectral analysis, efficiency and evidence-aware interpretation.",
    "solarTitle": "Photovoltaic modelling",
    "solarDesc": "Solar-cell simulation result inspection with explicit model and source provenance.",
    "analyticsTitle": "Research analytics",
    "analyticsDesc": "Transparent plots and reports separating measurements, simulations and predictions.",
    "previewOnly": "Preview only",
    "integrity": "SCIENTIFIC INTEGRITY",
    "integrityTitle": "Evidence before claims",
    "integrityDesc": "Results must identify their source and status: MEASURED, DERIVED, SIMULATED or PREDICTED. Parsing a SCAPS I–V export does not establish solver convergence or physical validation.",
    "collaboration": "CONTROLLED COLLABORATION",
    "accessTitle": "Research spaces are invitation-only",
    "accessDesc": "Private projects, datasets and compute services are not available on this public preview. Researcher registration and owner approval will be introduced only after authentication, authorization and audit checks are implemented.",
    "notice": "Private login is not enabled yet. No account details are collected on this page.",
    "footer1": "© LASERSTONE™ · Research platform preview",
    "footer2": "Public information only · No live simulations"
  },
  "ar": {
    "skip": "انتقل إلى المحتوى",
    "brandSub": "منصة بحثية",
    "navResearch": "البحوث",
    "navIntegrity": "النزاهة العلمية",
    "navAccess": "الوصول",
    "languageLabel": "اللغة",
    "preview": "معاينة عامة · قيد التطوير",
    "hero1": "نمذجة علمية تستند إلى",
    "hero2": "أدلة قابلة للتتبع.",
    "lead": "تجمع LASERSTONE بين فيزياء الليزر والفوتونيات والمواد وأبحاث الخلايا الشمسية عبر مسارات حوسبة شفافة. لا تتضمن هذه المعاينة بيانات بحثية خاصة أو خدمة محاكاة مباشرة.",
    "explore": "استكشف المجالات البحثية",
    "researchAccess": "الوصول البحثي",
    "note": "الحالة العلمية: المنصة قيد التطوير. لا تعني هذه المعاينة تحققًا تجريبيًا أو عدديًا.",
    "domains": "المجالات البحثية",
    "researchTitle": "مصممة لمسارات العمل العلمي",
    "laserTitle": "الليزر والفوتونيات",
    "laserDesc": "النمذجة والتحليل الطيفي والكفاءة والتفسير المستند إلى الأدلة.",
    "solarTitle": "نمذجة الخلايا الشمسية",
    "solarDesc": "فحص نتائج محاكاة الخلايا الشمسية مع توثيق النموذج ومصدر البيانات.",
    "analyticsTitle": "التحليلات البحثية",
    "analyticsDesc": "رسوم وتقارير شفافة تميز بين القياسات والمحاكاة والتنبؤات.",
    "previewOnly": "معاينة فقط",
    "integrity": "النزاهة العلمية",
    "integrityTitle": "الأدلة تسبق الاستنتاجات",
    "integrityDesc": "يجب تحديد مصدر النتائج وحالتها: مقاسة (MEASURED)، أو مشتقة (DERIVED)، أو محاكاة (SIMULATED)، أو متنبأ بها (PREDICTED). ولا تعني قراءة ملف SCAPS I–V إثبات تقارب الحل العددي أو صحة النموذج فيزيائيًا.",
    "collaboration": "تعاون بحثي مضبوط",
    "accessTitle": "المساحات البحثية بالدعوة فقط",
    "accessDesc": "المشروعات الخاصة ومجموعات البيانات وخدمات الحوسبة غير متاحة في هذه المعاينة العامة. لن يُفعّل تسجيل الباحثين وموافقة المالك إلا بعد تنفيذ المصادقة والتحقق من الصلاحيات وسجلات التدقيق.",
    "notice": "تسجيل الدخول الخاص غير مفعّل بعد. لا تُجمع بيانات الحسابات عبر هذه الصفحة.",
    "footer1": "© LASERSTONE™ · معاينة المنصة البحثية",
    "footer2": "معلومات عامة فقط · لا توجد محاكاة مباشرة"
  }
};
const supported = Object.keys(translations);
const select = document.getElementById('language-select');
const params = new URLSearchParams(location.search);
let stored = null;
try { stored = localStorage.getItem('laserstone-language'); } catch (_) { /* storage unavailable */ }
const requested = params.get('lang') || stored || (navigator.language || 'en').split('-')[0];
function applyLanguage(lang) {
  const chosen = supported.includes(lang) ? lang : 'en';
  const messages = translations[chosen];
  document.documentElement.lang = chosen;
  document.documentElement.dir = chosen === 'ar' ? 'rtl' : 'ltr';
  document.querySelectorAll('[data-i18n]').forEach(element => {
    const key = element.getAttribute('data-i18n');
    element.textContent = messages[key] || translations.en[key] || '';
  });
  select.value = chosen;
  document.title = 'LASERSTONE | ' + messages.brandSub;
  try { localStorage.setItem('laserstone-language', chosen); } catch (_) { /* storage unavailable */ }
}
select.addEventListener('change', () => applyLanguage(select.value));
applyLanguage(requested);
