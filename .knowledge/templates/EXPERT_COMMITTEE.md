# Expert Committee Decision Templates

> Ready-to-use decision prompts for multi-perspective analysis

---

## Table of Contents

- [1. Decision Level Selection](#1-decision-level-selection)
- [2. L1 Quick Check](#2-l1-quick-check-2-3-experts)
- [3. L2 Standard Review](#3-l2-standard-review-4-5-experts)
- [4. L3 Deep Analysis](#4-l3-deep-analysis-6-8-experts)
- [5. L4 Comprehensive Review](#5-l4-comprehensive-review-10-12-experts)
- [6. L5 Full Committee](#6-l5-full-committee-24-experts)
- [7. Usage Tips](#7-usage-tips)

---

## 1. Decision Level Selection

| Level                 | Risk      | Reversibility | Impact     | Time     | Experts |
|-----------------------|-----------|---------------|------------|----------|---------|
| **L1** Quick Check    | Low       | Easy          | 1 team     | <30min   | 2-3     |
| **L2** Standard       | Medium    | Moderate      | 2-3 teams  | 1-2h     | 4-5     |
| **L3** Deep Analysis  | High      | Hard          | Department | 1 day    | 6-8     |
| **L4** Comprehensive  | Critical  | Very Hard     | Cross-dept | 2-3 days | 10-12   |
| **L5** Full Committee | Strategic | Irreversible  | Org-wide   | 1 week   | 24      |

---

## 2. L1: Quick Check (2-3 Experts)

**Use for**: Routine decisions, low-risk changes, quick validations

**Panel**: Engineer · QA

**Template**:

```
Decision: [what]
| Aspect | Status | Notes |
| Implementation | ✅/⚠️/❌ | |
| Test Coverage | ✅/⚠️/❌ | |
| Risk Level | Low/Med/High | |
Recommendation: [Go/No-Go + rationale]
```
---

## 3. L2: Standard Review (4-5 Experts)

**Use for**: Feature decisions, moderate complexity, cross-team impact

**Panel**: Architect · Engineer · QA · PM

**Template**:

```
Decision: [what] | Context: [background]
| Expert | Assessment | Concerns | Recommendations |
Risk: Technical [L/M/H] · Business [L/M/H] · Timeline [L/M/H]
Recommendation: [Approve/Revise/Reject] | Conditions: [if any] | Next Steps: [actions]
```
---

## 4. L3: Deep Analysis (6-8 Experts)

**Use for**: Architecture decisions, significant refactoring, new technology

**Panel**: Architect · Engineer · QA · DevOps · Security · PM · TPM · Knowledge Engineer

**Template**:

```
Decision: [what] | Context: [background] | Stakeholders: [who]

Technical Dimension (1-5): Correctness · Maintainability · Performance · Security · Scalability
Business Dimension (1-5): Value · User Impact · Cost · Time to Market

Risk Matrix: | Risk | Probability | Impact | Mitigation |
Expert Votes: | Expert | Vote | Confidence | Key Concern |

Consensus: [Approve/Conditional/Reject] | Score: [X/100]
Conditions: [required] | Action Items: [with owners]
```
---

## 5. L4: Comprehensive Review (10-12 Experts)

**Use for**: Major architecture changes, critical system decisions

**Groups**: Technical (Architect, Engineer, QA, DevOps, Security) · AI/Data (if applicable) · Business (PM, TPM, UX) ·
Governance (KE, Compliance)

**Template**:

```
Decision: [detailed] | Impact Scope: [systems, teams, users] | Timeline: [deadline]

10×10 Matrix: Roles × Angles (Correct, Maintain, Perform, Secure, Scale, Value, Usable, Efficient, Timely, Document)

Weighted Scoring: Technical [X/100, 40%] · Business [X/100, 35%] · Process [X/100, 25%] = Final [X/100]

Recommendation: [Approve/Conditional/Major Revision/Reject] | Confidence: [H/M/L]
Dissenting Opinions: [if any]
Implementation: Phase 1 [timeline] → Phase 2 [timeline] → Validation checkpoints
```
---

## 6. L5: Full Committee (24 Experts)

**Use for**: Critical decisions, major pivots, organization-wide impact

**Groups** (6 each):

- **Architecture**: Chief Architect, Info Architect, Systems Engineer, API Designer, Perf Architect, Reliability
  Engineer
- **Knowledge**: Knowledge Manager, Doc Engineer, Metadata Specialist, Search Expert, Content Strategist, Ontology
  Designer
- **AI Collaboration**: AI Expert, Prompt Engineer, Autonomy Specialist, Cognitive Scientist, Ethics Expert, Safety
  Expert
- **Engineering**: DevOps, Python Engineer, Test Architect, UX Expert, PM, Security Engineer

**Template**:

```
Decision: [strategic] | Impact: [org-wide implications] | Urgency: [Critical/High/Medium]

Group Assessments: | Group | Approval | Score | Key Concerns | Conditions |

Consensus: Unanimous (4/4) · Strong (3/4) · Conditional (2/4) · Rejected (<2/4)

Final: [Approved/Conditional/Rejected] | Score: [X/100] | Confidence: [X%]
Binding Conditions: [must-meet items]
Post-Decision: Document rationale · Communicate · Set checkpoints · Plan rollback
```
---

## 7. Usage Tips

**Start Low** (escalate if needed) · **Time-Box** (set limits) · **Document** (capture rationale) · **Revisit** (
schedule reviews) · **Adapt** (customize for domain)

---

## Related

- `.knowledge/frameworks/cognitive/EXPERT_COMMITTEE.md` — Full theory
- `.knowledge/frameworks/patterns/DECISION.md` — Quality dimensions
- `.knowledge/frameworks/autonomy/LEVELS.md` — Decision authority

---

*AI Collaboration Knowledge Base*
