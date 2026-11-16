/* LASERSTONE public-preview UI translations. Scientific data is never auto-translated. */
const translations = {
  "en": {
    "navCockpit": "Cockpit",
    "cockpitEyebrow": "SCIENTIFIC COCKPIT · PREVIEW",
    "cockpitTitle": "A transparent research control center",
    "cockpitIntro": "A conceptual view of the platform's research workflow. The indicators below describe interface readiness, not live engine health, experimental results, or simulation output.",
    "cockpitEvidenceTitle": "Evidence registry",
    "cockpitEvidenceDesc": "Planned traceability from source and parameters to interpretation.",
    "statusPlanned": "Concept preview",
    "cockpitPhysicsTitle": "Physics engines",
    "cockpitPhysicsDesc": "Private scientific calculations are not connected to this site.",
    "statusDisconnected": "Not connected",
    "cockpitSolarTitle": "Solar simulation",
    "cockpitSolarDesc": "SCAPS result import and validation remain outside the public preview.",
    "cockpitAccessTitle": "Owner workspace",
    "cockpitAccessDesc": "Restricted access awaits verified authentication and authorization.",
    "statusRestricted": "Not enabled",
    "cockpitFootnote": "Illustrative interface only · No live telemetry, private data, or authenticated sessions.",
    "selectPanel": "Illuminate panel",
    "readoutIdle": "No panel selected",
    "readoutIdleDesc": "Choose a panel to inspect its preview status. No scientific engine will start.",
    "readoutEvidence": "Evidence registry · concept preview only. No datasets are loaded.",
    "readoutPhysics": "Physics engines · disconnected. No calculations are running.",
    "readoutSolar": "Solar simulation · disconnected. No SCAPS execution or validation is performed.",
    "readoutOwner": "Owner workspace · not enabled. No login or private access is available.",
    "gatesEyebrow": "SCIENTIFIC ENTRANCES · ORIGINAL MAXIMS",
    "gatesTitle": "A guiding principle at every entrance",
    "gatesIntro": "Original LASERSTONE editorial maxims: teaching prompts, not quotations attributed to historical scientists or evidence of scientific validation.",
    "gatePhysicsTitle": "Physics & laser science",
    "gatePhysicsQuote": "Let imagination open the question, and measurement determine the answer.",
    "gatePhysicsMeaning": "Distinguish hypothesis, measurement and model assumptions.",
    "gateEngineeringTitle": "Engineering & simulation",
    "gateEngineeringQuote": "A simulation guides design; validation earns trust.",
    "gateEngineeringMeaning": "Report parameters, numerical stability and independent checks.",
    "gateIntegrityTitle": "Scientific integrity",
    "gateIntegrityQuote": "We refine our language without weakening our evidence.",
    "gateIntegrityMeaning": "Clear explanation never replaces the limits of what data establish.",
    "gatesAttribution": "LASERSTONE™ original editorial wording · Concept preview",
    "learningEyebrow": "SCIENTIFIC LEARNING PATH · INTERACTIVE PREVIEW",
    "learningTitle": "From curiosity to evidence",
    "learningIntro": "Explore five steps of scientific reasoning. This is an educational navigation demonstration, not a running experiment or simulation.",
    "learningStep0": "Observe",
    "learningStep1": "Understand",
    "learningStep2": "Formulate",
    "learningStep3": "Test",
    "learningStep4": "Validate",
    "learningDesc0": "What phenomenon do we want to understand? Describe the observation before explaining it.",
    "learningDesc1": "What concepts help explain the phenomenon? Separate established knowledge from hypotheses.",
    "learningDesc2": "Which equation or model represents it? State variables, units and assumptions.",
    "learningDesc3": "How would we compare model predictions with observations? Specify controls and uncertainty.",
    "learningDesc4": "What evidence supports the conclusion? Check reproducibility, limitations and independent tests.",
    "learningPrev": "Previous",
    "learningNext": "Next",
    "learningDisclaimer": "Educational concept only · No data collection, engine execution, or claim of scientific validation.",
    "exampleEyebrow": "WORKED PHYSICS EXAMPLE · SYMBOLIC",
    "exampleTitle": "Light attenuation in a uniform absorbing medium",
    "exampleObservation": "Observation: transmitted intensity can decrease with propagation distance in an absorbing medium.",
    "exampleVariables": "I₀: incident intensity at z = 0; I(z): intensity at depth z; α: attenuation coefficient (inverse length).",
    "exampleAssumptions": "Model conditions: a homogeneous medium, constant α, and a single exponential attenuation law; reflection, scattering and complex geometry require additional treatment.",
    "exampleValidation": "Validation path: measure transmitted intensity at known depths, fit the attenuation law, report uncertainty, and check systematic deviations. No measured data are supplied here.",
    "exampleWarning": "Teaching example only · A symbolic equation is not evidence of experimental agreement or numerical validation.",
    "missionMotto": "We dream with the imagination of scientists, build with the precision of engineers, and declare success only when supported by evidence.",
    "missionMenu": "MISSION CONTROL",
    "missionDashboard": "◈ Dashboard",
    "missionProjects": "◇ Research projects",
    "missionAgents": "◎ Scientific agents",
    "missionEvidence": "▤ Evidence & integrity",
    "missionSecurity": "⬡ Security & access",
    "missionMenuNote": "Navigation preview · no private workspaces connected",
    "missionMonitorEyebrow": "MONITORING PANELS · DESIGN PREVIEW",
    "missionMonitorTitle": "Research mission overview",
    "missionProjectsTitle": "Research projects",
    "missionProjectsDesc": "Project metrics await a verified data source.",
    "missionAgentsTitle": "Scientific agents",
    "missionAgentsDesc": "Agent status requires authenticated telemetry.",
    "missionAlertsTitle": "Alerts and reviews",
    "missionAlertsDesc": "No private alerts or researcher messages are displayed.",
    "missionProgressTitle": "Validation progress",
    "missionProgressDesc": "No percentage is shown without an audited measurement.",
    "missionNoData": "No live data",
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
    "navCockpit": "قمرة القيادة",
    "cockpitEyebrow": "القمرة العلمية · معاينة",
    "cockpitTitle": "مركز تحكم بحثي شفاف",
    "cockpitIntro": "تصور مبدئي لمسار العمل البحثي في المنصة. المؤشرات أدناه تصف حالة الواجهة فقط، وليست قياسات مباشرة لصحة المحركات أو نتائج تجريبية أو محاكاة.",
    "cockpitEvidenceTitle": "سجل الأدلة",
    "cockpitEvidenceDesc": "تتبع مخطط له من المصدر والمعلمات حتى التفسير العلمي.",
    "statusPlanned": "معاينة تصورية",
    "cockpitPhysicsTitle": "المحركات الفيزيائية",
    "cockpitPhysicsDesc": "الحسابات العلمية الخاصة غير متصلة بهذا الموقع.",
    "statusDisconnected": "غير متصل",
    "cockpitSolarTitle": "محاكاة الخلايا الشمسية",
    "cockpitSolarDesc": "استيراد نتائج SCAPS والتحقق منها خارج المعاينة العامة.",
    "cockpitAccessTitle": "مساحة المالك",
    "cockpitAccessDesc": "الوصول المقيد ينتظر تنفيذ المصادقة والتحقق من الصلاحيات.",
    "statusRestricted": "غير مفعّل",
    "cockpitFootnote": "واجهة توضيحية فقط · لا قياسات حية أو بيانات خاصة أو جلسات دخول موثقة.",
    "selectPanel": "إضاءة القسم",
    "readoutIdle": "لم يُحدَّد قسم",
    "readoutIdleDesc": "اختر قسمًا لعرض حالته التجريبية. لن يعمل أي محرك علمي.",
    "readoutEvidence": "سجل الأدلة · معاينة تصورية فقط. لم تُحمَّل أي بيانات.",
    "readoutPhysics": "المحركات الفيزيائية · غير متصلة. لا توجد حسابات جارية.",
    "readoutSolar": "محاكاة الخلايا الشمسية · غير متصلة. لا يُشغَّل SCAPS ولا يُتحقق من نتائجه.",
    "readoutOwner": "مساحة المالك · غير مفعّلة. لا يوجد تسجيل دخول أو وصول خاص.",
    "gatesEyebrow": "مداخل الساحات العلمية · عبارات أصلية",
    "gatesTitle": "لكل ساحة مفتاح من البيان والبرهان",
    "gatesIntro": "عبارات تحريرية أصلية لمنصة LASERSTONE للتعليم والإلهام؛ ليست اقتباسات منسوبة إلى علماء تاريخيين، ولا دليلًا على تحقق علمي.",
    "gatePhysicsTitle": "ساحة الفيزياء والليزر",
    "gatePhysicsQuote": "ليفتح الخيال باب السؤال، وليحسم القياس صدق الجواب.",
    "gatePhysicsMeaning": "نميّز بين الفرضية والقياس وافتراضات النموذج.",
    "gateEngineeringTitle": "ساحة الهندسة والمحاكاة",
    "gateEngineeringQuote": "المحاكاة تهدي إلى التصميم، والتحقق يمنح النتائج الثقة.",
    "gateEngineeringMeaning": "نوثّق المعلمات واستقرار الحل العددي والاختبارات المستقلة.",
    "gateIntegrityTitle": "ساحة النزاهة العلمية",
    "gateIntegrityQuote": "نُحسن صياغة البيان، دون أن نُضعف سلطان البرهان؛ ونقرّب العلم إلى الأذهان، دون أن نُفرّط في دقة الميزان.",
    "gateIntegrityMeaning": "وضوح الشرح لا يتجاوز حدود ما تثبته البيانات.",
    "gatesAttribution": "صياغات تحريرية أصلية لمنصة LASERSTONE™ · معاينة تصميمية",
    "learningEyebrow": "المسار العلمي للفهم والتحقق · معاينة تفاعلية",
    "learningTitle": "من فضول السؤال إلى قوة الدليل",
    "learningIntro": "استكشف خمس مراحل للتفكير العلمي. هذا عرض تعليمي للتنقل، وليس تجربة أو محاكاة قيد التشغيل.",
    "learningStep0": "تأمّل",
    "learningStep1": "افهم",
    "learningStep2": "صُغ",
    "learningStep3": "اختبر",
    "learningStep4": "تحقّق",
    "learningDesc0": "ما الظاهرة التي نريد فهمها؟ صِف المشاهدة قبل تفسيرها.",
    "learningDesc1": "ما المفاهيم التي تفسّر الظاهرة؟ ميّز المعرفة الراسخة من الفرضيات.",
    "learningDesc2": "أي معادلة أو نموذج يصف الظاهرة؟ حدّد المتغيرات والوحدات والافتراضات.",
    "learningDesc3": "كيف نقارن تنبؤ النموذج بالمشاهدات؟ حدّد الضوابط وعدم اليقين.",
    "learningDesc4": "ما الدليل الذي يسند الاستنتاج؟ افحص قابلية إعادة الإنتاج والحدود والاختبارات المستقلة.",
    "learningPrev": "السابق",
    "learningNext": "التالي",
    "learningDisclaimer": "تصور تعليمي فقط · لا جمع بيانات أو تشغيل محركات أو ادعاء بتحقق علمي.",
    "exampleEyebrow": "مثال فيزيائي تطبيقي · صياغة رمزية",
    "exampleTitle": "توهين الضوء في وسط ماص متجانس",
    "exampleObservation": "المشاهدة: قد تنخفض شدة الضوء النافذ مع مسافة الانتشار داخل وسط ماص.",
    "exampleVariables": "I₀: الشدة الابتدائية عند z = 0؛ I(z): الشدة عند العمق z؛ α: معامل التوهين (مقلوب الطول).",
    "exampleAssumptions": "شروط النموذج: وسط متجانس، ومعامل α ثابت، وقانون توهين أسي واحد؛ أما الانعكاس والتشتت والهندسة المعقدة فتحتاج معالجة إضافية.",
    "exampleValidation": "مسار التحقق: قياس شدة الضوء النافذ عند أعماق معلومة، وملاءمة قانون التوهين، والإبلاغ عن عدم اليقين، وفحص الانحرافات المنتظمة. لا تُعرض هنا بيانات مقاسة.",
    "exampleWarning": "مثال تعليمي فقط · المعادلة الرمزية لا تثبت توافقًا تجريبيًا أو تحققًا عدديًا.",
    "missionMotto": "نحلم بخيال العلماء، ونبني بدقة المهندسين، ولا نعلن نجاحًا إلا بشهادة الدليل.",
    "missionMenu": "غرفة القيادة",
    "missionDashboard": "◈ لوحة القيادة",
    "missionProjects": "◇ المشروعات البحثية",
    "missionAgents": "◎ الوكلاء العلميون",
    "missionEvidence": "▤ الأدلة والنزاهة العلمية",
    "missionSecurity": "⬡ الأمان والصلاحيات",
    "missionMenuNote": "معاينة تنقل فقط · لا اتصال بمساحات بحثية خاصة",
    "missionMonitorEyebrow": "لوحات المراقبة · معاينة تصميمية",
    "missionMonitorTitle": "نظرة عامة على المهمة البحثية",
    "missionProjectsTitle": "المشروعات البحثية",
    "missionProjectsDesc": "مؤشرات المشروعات تنتظر مصدر بيانات موثقًا.",
    "missionAgentsTitle": "الوكلاء العلميون",
    "missionAgentsDesc": "تتطلب حالة الوكلاء قياسات تشغيل موثقة.",
    "missionAlertsTitle": "التنبيهات والمراجعات",
    "missionAlertsDesc": "لا تُعرض تنبيهات خاصة أو رسائل باحثين.",
    "missionProgressTitle": "تقدم التحقق",
    "missionProgressDesc": "لا تُعرض نسب مئوية دون قياس مدقق.",
    "missionNoData": "لا توجد بيانات حية",
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
  updateReadout(chosen);
  updateLearning(chosen);
  try { localStorage.setItem('laserstone-language', chosen); } catch (_) { /* storage unavailable */ }
}
select.addEventListener('change', () => applyLanguage(select.value));
/* Visual selection only: no network calls, authentication or engine execution. */
const cockpitButtons = Array.from(document.querySelectorAll('.cockpit-switch'));
const cockpitReadout = document.getElementById('cockpit-readout');
const readoutKeys = { evidence: 'readoutEvidence', physics: 'readoutPhysics', solar: 'readoutSolar', owner: 'readoutOwner' };
let selectedPanel = null;
function updateReadout(lang) {
  if (!cockpitReadout) return;
  const messages = translations[lang] || translations.en;
  const title = cockpitReadout.querySelector('strong');
  const description = cockpitReadout.querySelector('p');
  title.textContent = selectedPanel ? messages[selectedPanel === 'evidence' ? 'cockpitEvidenceTitle' : selectedPanel === 'physics' ? 'cockpitPhysicsTitle' : selectedPanel === 'solar' ? 'cockpitSolarTitle' : 'cockpitAccessTitle'] : messages.readoutIdle;
  description.textContent = selectedPanel ? messages[readoutKeys[selectedPanel]] : messages.readoutIdleDesc;
}
cockpitButtons.forEach(button => {
  button.addEventListener('click', () => {
    selectedPanel = button.dataset.panel === selectedPanel ? null : button.dataset.panel;
    cockpitButtons.forEach(item => {
      const active = item.dataset.panel === selectedPanel;
      item.setAttribute('aria-pressed', String(active));
      item.closest('.cockpit-panel').classList.toggle('is-selected', active);
    });
    updateReadout(document.documentElement.lang);
  });
});
/* Educational interaction only; no network, personal data or physics engines. */
const learningButtons = Array.from(document.querySelectorAll('.learning-step'));
const learningReadout = document.getElementById('learning-readout');
const learningCount = document.getElementById('learning-count');
const learningPrev = document.getElementById('learning-prev');
const learningNext = document.getElementById('learning-next');
let learningIndex = 0;
function updateLearning(lang) {
  if (!learningReadout) return;
  const messages = translations[lang] || translations.en;
  learningReadout.querySelector('strong').textContent = messages['learningStep' + learningIndex];
  learningReadout.querySelector('p').textContent = messages['learningDesc' + learningIndex];
  learningButtons.forEach((button, index) => {
    const active = index === learningIndex;
    button.setAttribute('aria-pressed', String(active));
    button.classList.toggle('is-current', active);
  });
  learningCount.textContent = (learningIndex + 1) + ' / ' + learningButtons.length;
  learningPrev.disabled = learningIndex === 0;
  learningNext.disabled = learningIndex === learningButtons.length - 1;
}
learningButtons.forEach((button, index) => button.addEventListener('click', () => {
  learningIndex = index;
  updateLearning(document.documentElement.lang);
}));
learningPrev.addEventListener('click', () => {
  learningIndex = Math.max(0, learningIndex - 1);
  updateLearning(document.documentElement.lang);
});
learningNext.addEventListener('click', () => {
  learningIndex = Math.min(learningButtons.length - 1, learningIndex + 1);
  updateLearning(document.documentElement.lang);
});
applyLanguage(requested);
