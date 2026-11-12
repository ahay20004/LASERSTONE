# LASERSTONE: An Evidence-Aware and Provenance-Constrained Framework for the Scientific Evaluation of Natural Photonic Materials

**Authoritative manuscript policy:** ONE RESEARCH → ONE MASTER → ONE EVIDENCE TRAIL  
**Research ID:** LASERSTONE-PAPER-001  
**Article type:** Original Research Article  
**Master status:** ACTIVE — update this file in place; do not fork into parallel manuscript versions.

## Abstract

Natural photonic materials are increasingly investigated for fluorescence, optical sensing, light harvesting, imaging, and prospective laser-related applications. Their scientific evaluation, however, is frequently hindered by incomplete photophysical datasets, heterogeneous literature sources, inconsistent parameter definitions, undocumented units, and the conflation of literature-reported, derived, predicted, and missing quantities. When such data are passed directly into computational screening models, apparently quantitative rankings may exceed the strength of the underlying physical evidence.

This work introduces **LASERSTONE**, a computational research framework developed to organize, validate, and evaluate heterogeneous photophysical evidence for natural photonic materials while preserving source provenance, unit consistency, and the distinction between reported, derived, predicted, and missing quantities. The implementation examined here corresponds to the G23 evidence-safety development stage of the platform. The framework enforces explicit semantic and unit contracts, prevents missing quantities from being represented as numerical zero, and applies compatibility and claim-level decision gates before external evidence can enter downstream analytical engines.

PhotochemCAD was used as the initial external spectral-evidence source. Reported molar extinction coefficients were converted, where applicable, into molecular absorption cross sections using a Beer–Lambert-based relation while preserving the derived status and physical units of the calculated quantity. Three representative records—Asn-Bx, quercetin, and lutein—were selected to test different levels of evidence completeness. Their independent core spectral-evidence completeness was 75%, 50%, and 25%, respectively. The framework allowed only operations supported by the available evidence, including absorption analysis, unit-bearing cross-section derivation, and Stokes-shift calculation when both absorption and emission information were explicitly available. Operations requiring unresolved quantities, including legacy absorption parameters, fluorescence lifetime, non-radiative decay terms, or incompletely defined efficiency quantities, were blocked rather than completed using default values.

A provenance audit of the existing LASERSTONE plant dataset additionally identified unresolved field-level source and unit requirements that must be addressed before legacy numerical values can be promoted as physical evidence. Compound-level literature evidence was also kept distinct from plant-extract evidence so that isolated-compound spectra could support interpretation without replacing extract measurements. The evidence-safety architecture, together with the first research-composition entry gates, was validated through **86 automated acceptance tests under Python 3.12**. LASERSTONE therefore provides an evidence-bounded computational framework for the scientific evaluation of natural photonic materials while explicitly preventing unsupported claims of optical gain, laser efficiency, resonator quality, output power, or prototype readiness.

**Keywords:** natural photonic materials; scientific provenance; PhotochemCAD; evidence-aware computation; data harmonization; natural chromophores; reproducible scientific software; laser-material screening

---

## 1. Introduction

Natural chromophores and plant-derived colorants span chemically diverse classes including flavonoids, carotenoids, betalains, tetrapyrroles, and related compounds. Their optical properties have motivated applications in fluorescence imaging, sensing, light harvesting, photomedicine, and other photonic technologies [1]. The scientific value of these materials, however, depends not only on the existence of absorption or fluorescence signals, but on the quality, context, units, and provenance of the underlying measurements.

PhotochemCAD represents one of the most substantial efforts to organize absorption and fluorescence spectra together with photophysical parameters and references to the originating literature. Its third-generation architecture provides multiple spectral databases and calculation modules for quantities such as oscillator strength, transition dipole moment, natural radiative lifetime, and energy-transfer parameters [2]. The accompanying common-compounds database includes absorption and fluorescence spectra together with molar absorption coefficients and fluorescence quantum yields where available, explicitly linked to the primary literature [3]. This literature-connected design is particularly important because photophysical values are condition-dependent and cannot be treated as context-free numerical descriptors.

The broader scientific-data community has independently emphasized that reusable scientific data require rich metadata, interoperability, and detailed provenance. The FAIR principles formalized findability, accessibility, interoperability, and reusability, including the requirement that data be associated with detailed provenance and that algorithms and workflows be treated as research objects rather than detached software utilities [4]. More recent work has extended FAIR concepts to computational workflows, emphasizing machine-actionable provenance for workflow definitions, executions, inputs, and outputs [5]. In materials science, lineage-aware data management has likewise been identified as critical for linking raw measurements, analysis steps, derived properties, and final conclusions [6].

These developments establish a strong foundation for scientific traceability, yet a domain-specific problem remains when heterogeneous photophysical evidence is fed into material-screening or decision-support software. A value can be numerically present while still being scientifically incompatible with a downstream equation because its unit, physical definition, environmental condition, or evidence status differs from what the engine expects. Conversely, a missing value may be silently replaced with zero or a default value, creating an appearance of completeness that is not supported by experiment. In laser-related screening, this problem is particularly consequential because quantities such as fluorescence lifetime, absorption cross section, non-radiative decay rate, refractive index, optical efficiency, cavity quality, and gain do not become interchangeable simply because they appear in the same scoring pipeline.

The present work addresses this gap through LASERSTONE, an evidence-aware computational framework for natural photonic materials. The novelty claimed here is deliberately bounded. Provenance, FAIR data, workflow traceability, and photophysical databases are not presented as new concepts. Instead, LASERSTONE operationalizes these principles as **scientific execution gates**: each quantity must carry an evidence state and unit/semantic contract; each engine must declare whether the available evidence is compatible with its requirements; and each downstream claim must be authorized or blocked according to the evidence actually available.

The study therefore asks:

> **Can heterogeneous photophysical evidence for natural photonic materials be integrated and evaluated without converting missing, semantically incompatible, or unit-ambiguous data into artificial numerical confidence or unsupported laser-performance claims?**

To answer this question, the present G23 implementation was evaluated using three PhotochemCAD benchmark records spanning different evidence-completeness levels, a legacy LASERSTONE provenance audit, explicit compound-versus-extract separation, and automated software verification. The objective is not to establish laser action experimentally. Rather, it is to establish whether the computational framework can distinguish what is scientifically supported from what remains unknown, and whether this distinction can be preserved through analysis, interpretation, and research composition.

---

## 2. Materials and Methods

### 2.1. LASERSTONE framework and study scope

LASERSTONE was developed as a computational research framework for the structured evaluation of heterogeneous photophysical evidence associated with natural photonic materials. The framework distinguishes between the existence of a numerical value and the scientific strength of the evidence supporting that value. Accordingly, numerical completeness is not treated as equivalent to physical validation.

The implementation examined in this work corresponds to the **G23 evidence-safety development stage**. G23 is an internal development designation and is not the scientific name of the platform. Its principal objective was to establish an evidence-aware layer capable of receiving external photophysical data, preserving provenance and units, deriving only physically justified secondary quantities, and preventing incomplete evidence from entering downstream models as if it represented complete experimental information.

The core scientific workflow was organized as

[
	ext{Source}
ightarrow
	ext{Evidence State}
ightarrow
	ext{Unit Contract}
ightarrow
	ext{Physical Derivation}
ightarrow
	ext{Compatibility Gate}
ightarrow
	ext{Claim Boundary}.
]

This pathway was maintained separately from the pre-existing heuristic ranking pipeline so that external evidence could be evaluated without altering previously stored LASERSTONE results.

### 2.2. Evidence-state model

Each scientific quantity was assigned an explicit evidence state. Three principal states were used in the current implementation:

[
E in
{
	ext{LITERATURE_REPORTED},
	ext{DERIVED},
	ext{MISSING}
}.
]

A quantity was classified as **LITERATURE_REPORTED** only when it was explicitly supplied by the source record. A quantity was classified as **DERIVED** when it was calculated from one or more reported quantities using a stated physical relation. A quantity absent from the source and not physically derivable from the available evidence was assigned **MISSING**.

Missing quantities were represented as null values rather than numerical zero:

[
	ext{MISSING} 
eq 0.
]

This distinction is necessary because a physical zero represents an observed or defined numerical state, whereas a missing value represents the absence of evidence. Predicted quantities generated by future or independent LASERSTONE models remain conceptually distinct from both reported and derived evidence.

### 2.3. External spectral-evidence source

PhotochemCAD was selected as the first external spectral-evidence source because it provides structured photophysical information for a broad range of organic chromophores and links spectra and parameters to the scientific literature [2,3].

External records were not inserted directly into the legacy LASERSTONE plant database. Instead, each verified record was passed through a read-only normalization adapter. The normalized schema supports, where available,

[
lambda_{mathrm{abs}},
quad
lambda_{mathrm{em}},
quad
arepsilon,
quad
Phi_f,
quad
sigma_a,
]

together with solvent, temperature, instrument, reference, DOI, spectrum source, source-database identifier, and source URL.

No missing photophysical quantity was generated merely to satisfy an existing engine input.

### 2.4. Semantic and unit contracts

A semantic and unit contract was associated with each physical quantity before compatibility with downstream engines was assessed.

The externally supported contracts used in the present study were

[
lambda_{mathrm{abs}},lambda_{mathrm{em}}
quad [mathrm{nm}],
]

[
arepsilon
quad [mathrm{M^{-1},cm^{-1}}],
]

[
Phi_f quad [1],
]

and

[
sigma_a
quad [mathrm{cm^2,molecule^{-1}}].
]

A direct mapping was allowed only when the physical meaning and unit convention of source and destination quantities were compatible.

The fluorescence quantum yield supplied by PhotochemCAD could therefore be mapped to the LASERSTONE quantum-yield field because both represent a dimensionless quantum yield. Likewise, reported absorption and emission wavelengths could be mapped when expressed in nanometres.

In contrast, the physically derived molecular absorption cross section was not mapped to the historical LASERSTONE parameter labelled `sigma_a`, because the legacy parameter does not yet possess an adequately documented unit or normalization contract. Direct substitution was therefore blocked.

The legacy fields `tau`, `sigma_a`, `eta`, and `knr` were retained as unresolved until authoritative physical definitions and units can be documented.

### 2.5. Derivation of molecular absorption cross section

When the molar extinction coefficient (arepsilon) was explicitly reported, the molecular absorption cross section was derived from the Beer–Lambert relation as

[
sigma_a =
rac{1000ln(10)}{N_A}arepsilon,
]

where

[
N_A = 6.02214076	imes10^{23} mathrm{mol^{-1}}
]

is the Avogadro constant, (arepsilon) is expressed in (mathrm{M^{-1},cm^{-1}}), and (sigma_a) is obtained in (mathrm{cm^2,molecule^{-1}}).

The calculated cross section was stored as **DERIVED**, whereas the original extinction coefficient retained **LITERATURE_REPORTED** status. The two values were therefore not counted as independent experimental observations.

### 2.6. Independent spectral-evidence completeness

A core spectral-evidence completeness measure was introduced to describe coverage of independent reported information without converting evidence completeness into a material-performance score.

Four independent quantities were considered:

[
lambda_{mathrm{abs}},
quad
lambda_{mathrm{em}},
quad
arepsilon,
quad
Phi_f.
]

The evidence-completeness metric was defined as

[
C_E =
100
rac{N_{mathrm{reported}}}
{N_{mathrm{core}}},
]

with

[
N_{mathrm{core}} = 4.
]

Derived quantities such as (sigma_a), when calculated from (arepsilon), were not counted as additional independent evidence.

Thus (C_E) measures **data coverage only** and must not be interpreted as optical gain, laser efficiency, lasing probability, or material quality.

### 2.7. Stokes-shift derivation

When both absorption and emission wavelengths were explicitly available, the wavelength-domain Stokes shift was calculated as

[
Deltalambda =
lambda_{mathrm{em}}
-
lambda_{mathrm{abs}}.
]

The corresponding wavenumber shift was calculated as

[
Delta	ilde{
u}
=
10^7
left(
rac{1}{lambda_{mathrm{abs}}}
-
rac{1}{lambda_{mathrm{em}}}
ight),
]

where wavelengths are expressed in nanometres and (Delta	ilde{
u}) is obtained in (mathrm{cm^{-1}}).

No Stokes-shift value was generated when either spectral peak was missing.

### 2.8. Engine-compatibility assessment

Each normalized evidence record was evaluated against the reviewed input requirements of LASERSTONE analytical engines.

An engine was classified as usable only when all inputs required for the intended operation were available with compatible semantics and units. Otherwise, the engine was assigned a blocked state.

The compatibility decision can be expressed schematically as

[
	ext{Engine Status}
=
f(
	ext{Availability},
	ext{Evidence State},
	ext{Semantic Compatibility},
	ext{Unit Compatibility}
).
]

A missing required input could not be replaced by zero, a representative value, or an internally assumed constant merely to permit execution.

Basic operations such as spectral-region classification could therefore proceed when the required emission wavelength was available, whereas engines requiring unresolved lifetime, non-radiative, efficiency, or legacy absorption parameters remained blocked.

### 2.9. Claim-level decision gate

A separate decision gate was applied after physical and compatibility analysis. Its purpose was to distinguish evidence-supported operations from claims requiring additional experimental or validated physical information.

The following claims were not authorized from spectral evidence alone:

[
	ext{optical gain established},
]

[
	ext{lasing feasibility established},
]

[
	ext{laser efficiency established},
]

[
	ext{Q-factor established},
]

and

[
	ext{prototype readiness established}.
]

This restriction remained active even when the available spectral record was internally complete. In this way, the framework separates “sufficient data for a calculation” from “sufficient evidence for a scientific claim.”

### 2.10. Separation of isolated-compound and plant-extract evidence

Spectral data obtained for an isolated molecular compound were treated as distinct evidence from data obtained for a plant extract containing that compound:

[
	ext{compound evidence}

eq
	ext{plant-extract measurement}.
]

An exact compound-name relationship could be recorded as supporting evidence, but an isolated-compound absorption wavelength, fluorescence quantum yield, or other photophysical value was not allowed to overwrite the corresponding plant-extract value.

This distinction is particularly important for natural materials because the optical response of an extract can depend on composition, concentration, solvent, pH, aggregation, and intermolecular interactions rather than on the isolated chromophore alone [1].

### 2.11. Legacy-data provenance audit

The pre-existing LASERSTONE plant dataset was independently audited for provenance completeness.

For each record, the audit examined the availability of source documentation for the critical photophysical variables

[
Phi,
quad
	au,
quad
sigma_a,
quad
eta,
quad
k_{nr},
quad
n,
quad
lambda_{mathrm{abs}},
quad
lambda_{mathrm{em}}.
]

The presence of a general literature reference for a material was not considered equivalent to field-level provenance for each numerical value. Values lacking a traceable field-level source or explicit unit contract were therefore retained as legacy values requiring provenance upgrade rather than automatically promoted to physical evidence.

### 2.12. Evidence registry and unified external-evidence pipeline

Normalized records were stored in an independent evidence registry identified by source database and source-record identifier.

The registry was designed to be immutable from the perspective of downstream analysis: analytical modules received detached copies of evidence records, and conflicting duplicate records sharing the same evidence identity were rejected.

The external-evidence pipeline was implemented as

[
	ext{External Record}
ightarrow
	ext{Normalization}
ightarrow
	ext{Evidence Registry}
ightarrow
	ext{Physical Analysis}
ightarrow
	ext{Engine Compatibility}
ightarrow
	ext{Decision Gate}
ightarrow
	ext{Interpretation/Trace/Output}.
]

The pipeline explicitly records that legacy scoring was not invoked and that the production registry was not mutated.

### 2.13. Research Directive and novelty gate

To prepare LASERSTONE for evidence-bounded research composition, the current development stage also introduced a machine-readable **Research Directive** and a prior-art-based **Novelty Gate**.

The Research Directive specifies the research question, scientific gap, proposed contribution, evidence scope, claim boundary, excluded claims, application relevance, and future research path. For the present paper, the master policy was defined as

[
	ext{ONE RESEARCH}
ightarrow
	ext{ONE MASTER}
ightarrow
	ext{ONE EVIDENCE TRAIL}.
]

The novelty gate does not calculate novelty from material-performance scores. Instead, research composition is authorized only when:

1. the Research Directive is complete;
2. the prior-art review scope is documented;
3. a distinct contribution relative to reviewed prior art is supported; and
4. the evidence is sufficient for the bounded claims in the directive.

If a direct competitor is identified without a defensible distinct contribution, manuscript composition is blocked. If the contribution is promising but the evidence is incomplete, the project remains in an evidence-acquisition state rather than proceeding automatically to manuscript generation.

### 2.14. Software verification

The G23 evidence-safety and research-entry architecture was developed and tested using Python 3.12.

Automated acceptance tests were created to verify source immutability, physical-domain validation, evidence-state separation, epsilon-to-cross-section conversion, strict missing-data behavior, unit contracts, engine compatibility, registry conflict handling, claim gating, strict decision wrappers, evidence-aware interpretation, legacy provenance auditing, compound–extract separation, unified external-evidence orchestration, Research Directive validation, and prior-art-based novelty authorization.

At the present development checkpoint, **86 automated acceptance tests completed successfully** under the dedicated GitHub Actions workflow.

The test result demonstrates software and rule consistency for the evaluated architecture. It does not constitute experimental validation of laser action or material performance.

---

## 3. Results

### 3.1. Benchmark evidence normalization

Three PhotochemCAD records were selected to exercise progressively incomplete evidence states: Asn-Bx (BX003), quercetin (FL109), and lutein [HPLC] (CAR021a-6).

| Record | (lambda_{mathrm{abs}}) (nm) | (lambda_{mathrm{em}}) (nm) | (arepsilon) (M(^{-1})cm(^{-1})) | (Phi_f) | Derived (sigma_a) (cm(^2) molecule(^{-1})) | (C_E) |
|---|---:|---:|---:|---:|---:|---:|
| Asn-Bx | 476 | Missing | 56,200 | 0.0074 | (2.1488	imes10^{-16}) | 75% |
| Quercetin | 256 | Missing | 18,700 | Missing | (7.1500	imes10^{-17}) | 50% |
| Lutein [HPLC] | 444.5 | Missing | Missing | Missing | Missing | 25% |

For Asn-Bx, three of the four independent core fields were reported. The molecular absorption cross section was derived from the reported extinction coefficient and therefore did not increase the independent evidence count. Quercetin contained two independent core fields, whereas lutein contained only a reported absorption peak in the selected record.

These results demonstrate that LASERSTONE can retain partially complete records without filling absent fields.

### 3.2. Separation of reported and derived evidence

For Asn-Bx,

[
arepsilon = 56{,}200 mathrm{M^{-1}cm^{-1}}
]

yielded

[
sigma_a =
2.1488	imes10^{-16} mathrm{cm^2,molecule^{-1}}.
]

For quercetin,

[
arepsilon = 18{,}700 mathrm{M^{-1}cm^{-1}}
]

yielded

[
sigma_a =
7.1500	imes10^{-17} mathrm{cm^2,molecule^{-1}}.
]

In both cases, (arepsilon) remained literature-reported while (sigma_a) remained explicitly derived. Lutein did not contain a reported extinction coefficient in the selected record, and no cross section was generated.

### 3.3. Stokes-shift calculation remained conditional

None of the three selected benchmark records supplied a usable emission wavelength in the normalized benchmark configuration. Consequently, the production benchmark did not generate a Stokes shift for these records.

A separate software-validation fixture supplied an explicit pair of 476 nm and 510 nm to test the calculation path. The framework returned

[
Deltalambda = 34 mathrm{nm}
]

and

[
Delta	ilde{
u}approx 1400.56 mathrm{cm^{-1}}.
]

This fixture was used only to validate the formula and execution rule. The 510 nm value is not presented as a PhotochemCAD measurement for the Asn-Bx benchmark.

### 3.4. Physical-evidence and legacy-scoring paths diverged by design

The evidence-aware physical pathway remained available for all three benchmark compounds because it can operate on incomplete records while preserving missing states.

The legacy spectral-quality pathway remained blocked. For Asn-Bx, only the quantum-yield and absorption-wavelength fields could be mapped safely into compatible legacy fields. Quercetin and lutein provided only a safely mappable absorption wavelength among the relevant legacy fields.

The principal blocker was not a software error. Rather, the historical LASERSTONE `sigma_a` field lacked a documented unit or normalization contract, whereas the PhotochemCAD-derived (sigma_a) was a physical molecular cross section in (mathrm{cm^2,molecule^{-1}}). Direct substitution would therefore have been scientifically unjustified.

The comparison module consequently reported the two outputs as non-equivalent:

[
	ext{Evidence Completeness}

eq
	ext{Legacy Spectral Quality}.
]

This prevented a 75% evidence-completeness value, for example, from being misinterpreted as a 75% laser-performance score.

### 3.5. Legacy provenance audit identified concrete upgrade requirements

Seven pre-existing LASERSTONE plant records were audited.

The audit found that:

- six of seven records had at least one general reference entry;
- one record, Acacia Nilotica, had no stored reference entry;
- Henna resolved to two reference records requiring reconciliation;
- none of the seven records had complete field-level provenance for the critical photophysical quantities;
- none of the stored reference bundles contained a DOI in the current metadata.

These findings do not invalidate the numerical legacy records. They establish that the records should remain classified as legacy research data until their field-level sources, conditions, and unit contracts are upgraded.

### 3.6. Isolated-compound evidence did not overwrite plant-extract data

The legacy Moringa record identifies quercetin as an active compound. PhotochemCAD FL109 is also quercetin, creating an exact compound-level relationship.

LASERSTONE recorded this relationship as

[
	ext{SUPPORTING_COMPOUND_EVIDENCE_ONLY}
]

with

[
	ext{substitution_allowed} = 	ext{False}.
]

Thus, the legacy Moringa extract absorption value of 410 nm remained unchanged, while the PhotochemCAD isolated-quercetin absorption value of 256 nm remained a separate evidence object.

The result demonstrates that semantic linkage between a plant and an active compound does not imply interchangeability of their measured spectra.

### 3.7. Claim gating prevented unsupported laser conclusions

For all PhotochemCAD-only benchmark records, the framework permitted traceable evidence storage and the physical operations supported by the available fields.

At the same time, it explicitly withheld authorization for claims that optical gain, lasing feasibility, laser efficiency, resonator Q-factor, output power, or prototype readiness had been established.

This behavior remained unchanged even when synthetic test inputs were added to exercise additional spectral calculations. In other words, greater spectral completeness did not automatically promote a record to a laser-performance claim.

### 3.8. Research-composition gate

The authoritative Research Directive for this paper passed structural validation under the policy

[
	ext{ONE RESEARCH}
ightarrow
	ext{ONE MASTER}
ightarrow
	ext{ONE EVIDENCE TRAIL}.
]

A bounded prior-art review covered PhotochemCAD, FAIR data principles, computational-workflow provenance, materials-data lineage, natural photonic materials, and materials-informatics approaches to incomplete data.

No reviewed source was identified that combined all of the following in one natural-photonic-material framework: explicit evidence states, unit contracts, per-engine compatibility gating, claim-level authorization boundaries, compound-versus-extract separation, and manuscript-ready evidence tracing. This finding is intentionally presented as a **bounded review result**, not as an unrestricted claim of being the first framework in all published literature.

The implemented novelty gate therefore authorized composition of the present paper because the contribution was distinct relative to the reviewed prior art and because the evidence was sufficient for the restricted computational claims.

### 3.9. Automated verification

Following integration of the evidence-safety and research-entry components, the dedicated GitHub Actions workflow executed **86 acceptance tests** under Python 3.12. All 86 tests completed successfully.

The tests covered the data path from normalization through evidence storage, physical derivation, compatibility, claim gating, provenance, reporting, compound linkage, strict decision wrappers, unified external-evidence orchestration, Research Directive validation, and novelty authorization.

---

## 4. Discussion

### 4.1. Scientific contribution of the framework

The principal contribution of LASERSTONE is not the introduction of provenance as a concept. PhotochemCAD already emphasizes connection of spectral data to the original scientific literature [2,3], FAIR principles explicitly require detailed provenance [4], and workflow systems increasingly capture machine-actionable processing histories [5]. Materials-science data infrastructures likewise recognize that conclusions must remain linked to the acquisition and processing history of the underlying measurements [6].

The contribution of the present framework is the conversion of these principles into **domain-specific scientific execution rules**.

A quantity is not admitted into an equation solely because it is numeric. It must also satisfy a semantic and unit contract. Likewise, the successful execution of an equation does not automatically authorize a scientific claim. Claim authorization is treated as a separate operation.

This distinction is important because scientific software can be internally consistent while remaining externally invalid if its inputs do not possess the physical meaning assumed by the model.

### 4.2. Why “missing is not zero” matters

Many computational pipelines are designed to remain operational in the presence of incomplete data. In exploratory informatics, imputation can be scientifically useful when the missingness mechanism and predictive uncertainty are explicitly modeled. However, imputation and evidence authorization answer different questions.

The objective of the current LASERSTONE layer is not to predict the most likely missing value. It is to determine whether the source evidence is sufficient to support a specific physical analysis or claim.

For this purpose,

[
	ext{unknown} ightarrow 0
]

is not a neutral transformation. It changes the epistemic state of the record from “not reported” to “known numerical zero.” A zero non-radiative rate, for example, would imply a physical condition radically different from an unreported non-radiative rate.

The fail-closed policy therefore preserves missingness until a traceable source or justified predictive model is introduced.

### 4.3. Evidence completeness is not performance

The 75%, 50%, and 25% values obtained for Asn-Bx, quercetin, and lutein are intentionally limited in meaning. They quantify how many independent core spectral fields were reported in the selected evidence record.

A compound can therefore have high evidence completeness and poor photonic performance, or low evidence completeness and excellent but insufficiently documented performance.

This separation prevents an important category error in materials screening: the substitution of “how much do we know?” for “how well does the material perform?”

Future LASERSTONE versions can evaluate both dimensions, but they should remain separate axes.

### 4.4. Unit contracts as scientific boundaries

The legacy `sigma_a` field illustrates why explicit unit contracts are essential.

A molecular absorption cross section of order (10^{-16} mathrm{cm^2,molecule^{-1}}) cannot be inserted directly into a legacy field containing values of order unity without first demonstrating that both quantities represent the same physical observable under the same normalization.

The decision to block this mapping reduces immediate compatibility but increases scientific defensibility.

The same principle currently applies to the legacy `tau`, `eta`, and `knr` fields. Their stored values are retained, but they are not promoted to externally interoperable physical evidence until authoritative definitions, units, and field-level references are documented.

### 4.5. Compound evidence and extract evidence answer different questions

The Moringa–quercetin example demonstrates another common risk in natural-material research.

An extract may contain a known chromophore, but its measured spectrum is a property of the complete sample under defined preparation and measurement conditions. The isolated compound is valuable for interpretation, molecular assignment, and hypothesis generation, but its spectrum cannot be assumed to reproduce the spectrum of the extract.

LASERSTONE therefore treats compound evidence as a supporting link rather than a replacement.

This distinction also creates a useful experimental pathway: disagreement between an isolated compound and an extract becomes a research question rather than a database inconsistency.

### 4.6. Relationship to FAIR and workflow provenance

LASERSTONE is compatible in philosophy with FAIR and workflow-provenance approaches but focuses on a narrower scientific problem.

FAIR asks whether research objects are findable, accessible, interoperable, and reusable [4]. Workflow provenance asks how processing steps, inputs, outputs, and execution histories can be captured and reproduced [5]. Materials-data lineage systems connect experiments and derived knowledge through traceable analysis histories [6].

LASERSTONE adds a photophysical decision layer:

[
	ext{provenance}
ightarrow
	ext{compatibility}
ightarrow
	ext{claim authorization}.
]

The framework therefore uses provenance not only to answer “where did this value come from?” but also “is this value physically admissible for this calculation?” and “does the resulting evidence support this statement?”

### 4.7. Research composition as a downstream scientific operation

The Research Directive and Novelty Gate introduced in the present development stage establish the first part of a future LASERSTONE Research Composer.

The intended design is not automatic text generation from arbitrary input. Manuscript construction is treated as a downstream operation that becomes available only after the scientific gap, prior-art scope, evidence boundary, contribution, and excluded claims have been defined.

The current paper served as the first benchmark for this architecture.

This approach may ultimately enable a researcher to specify a constrained research objective and have the platform assemble a single authoritative manuscript whose claims are linked to evidence, equations, assumptions, and sources. However, the present work validates only the entry gates and evidence architecture, not a fully autonomous publication system.

### 4.8. Limitations

Several limitations should be stated explicitly.

First, only three PhotochemCAD records were used as the initial external benchmark. They were selected to test different evidence states, not to support population-level conclusions about natural photonic materials.

Second, the study does not experimentally validate laser action, optical gain, Q-factor, laser efficiency, or prototype performance.

Third, the current PhotochemCAD adapter operates on verified source records supplied to the pipeline; large-scale automated ingestion and cross-database reconciliation remain future work.

Fourth, several legacy LASERSTONE fields require authoritative unit and provenance upgrades before they can participate in the external evidence pathway.

Fifth, the current evidence-completeness metric is intentionally simple. It measures the presence of four independent spectral quantities and does not yet weight measurement quality, uncertainty, solvent comparability, temperature, instrument calibration, or source confidence.

Sixth, the bounded prior-art review supports the current novelty statement but does not justify an unrestricted “first ever” claim.

### 4.9. Future research

The immediate next stage is large-scale integration of additional PhotochemCAD families, beginning with natural-dye-relevant classes such as betaxanthins, flavonoids, chlorophylls, and carotenoids.

A second stage will upgrade field-level provenance in the legacy LASERSTONE dataset and formalize physically documented definitions for unresolved fields.

A third stage will introduce experimental validation. Candidate materials selected through the evidence-aware framework should be characterized for absorption, fluorescence, quantum yield, lifetime, photostability, and pump compatibility under controlled conditions.

Only after such validation should LASERSTONE progress from evidence readiness toward experimentally supported laser-system design.

---

## 5. Conclusions

LASERSTONE was developed to address a specific problem in computational evaluation of natural photonic materials: a numerical value should not be treated as scientifically usable until its origin, evidence state, semantic meaning, and unit compatibility are known.

The G23 evidence-safety implementation demonstrated that heterogeneous spectral records can be normalized and analyzed without filling missing fields, conflating reported and derived quantities, or forcing physically incompatible data into legacy models.

Three benchmark PhotochemCAD records produced evidence-completeness values of 75%, 50%, and 25% while retaining their missing fields. Reported molar extinction coefficients were converted into unit-bearing molecular absorption cross sections without being confused with the unresolved historical LASERSTONE absorption parameter. A seven-record legacy provenance audit identified specific source and unit upgrades required before older numerical values can be promoted to physical evidence. The Moringa–quercetin case further demonstrated that isolated-compound evidence can support plant interpretation without replacing plant-extract measurements.

The framework also separated analysis from claim authorization. Spectral evidence alone was not permitted to establish optical gain, laser efficiency, resonator quality, output power, or prototype readiness.

The complete evidence-safety and research-entry architecture passed **86 automated acceptance tests under Python 3.12**.

The present work therefore establishes LASERSTONE as an evidence-aware research framework rather than a conventional scoring system. Its next development stage will expand the evidence base, strengthen field-level provenance, and test whether evidence-aware computational selection predicts experimentally measured photophysical behavior.

---

## Data Availability

The present study uses openly accessible PhotochemCAD records and LASERSTONE development artifacts described in the manuscript. The benchmark source URLs and provenance metadata are retained in the evidence records used by the framework. A journal-specific data-availability statement will be finalized at submission.

## Code Availability

The implementation described in this manuscript is maintained in the LASERSTONE development repository. The exact archival release and persistent software identifier will be assigned before submission so that the version corresponding to the manuscript can be cited reproducibly.

## Conflict of Interest

To be completed by the authors at submission.

## Funding

To be completed by the authors at submission.

## Author Contributions

To be completed after the final author list is frozen.

---

## References

1. Yuan, H.; Jiang, A.; Fang, H.; Chen, Y.; Guo, Z. Optical properties of natural small molecules and their applications in imaging and nanomedicine. *Advanced Drug Delivery Reviews* **2021**, 179, 113917. https://doi.org/10.1016/j.addr.2021.113917

2. Taniguchi, M.; Du, H.; Lindsey, J. S. PhotochemCAD 3: Diverse Modules for Photophysical Calculations with Multiple Spectral Databases. *Photochemistry and Photobiology* **2018**, 94, 277–289. https://doi.org/10.1111/php.12862

3. Taniguchi, M.; Lindsey, J. S. Database of Absorption and Fluorescence Spectra of >300 Common Compounds for Use in PhotochemCAD. *Photochemistry and Photobiology* **2018**, 94, 290–327. https://doi.org/10.1111/php.12860

4. Wilkinson, M. D.; et al. The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data* **2016**, 3, 160018. https://doi.org/10.1038/sdata.2016.18

5. Wilkinson, S. R.; et al. Applying the FAIR Principles to computational workflows. *Scientific Data* **2025**. https://doi.org/10.1038/s41597-025-04451-9

6. Soedarmadji, E.; Stein, H. S.; Suram, S. K.; Guevarra, D.; Gregoire, J. M. Tracking materials science data lineage to manage millions of materials experiments and analyses. *npj Computational Materials* **2019**, 5. https://doi.org/10.1038/s41524-019-0216-x

---

## Master Manuscript Control

This file is the single authoritative manuscript for LASERSTONE-PAPER-001.

Any future scientific revision must update this file in place and must preserve:

- one research question;
- one master manuscript;
- one evidence trail;
- explicit distinction between literature-reported, derived, predicted, and missing quantities;
- bounded novelty language;
- no unsupported experimental laser claims;
- traceable references and unit contracts.
