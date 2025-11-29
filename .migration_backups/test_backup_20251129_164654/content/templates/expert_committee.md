# Expert Committee Decision Templates

> **Load Time**: On-demand (~150 tokens)  
> **Purpose**: Ready-to-use decision prompts for multi-perspective analysis  
> **Reference**: See [Expert Committee Framework](../frameworks/cognitive/expert_committee.md) for theory

---

## Quick Decision Templates

### Level 1: Quick Check (2-3 Experts)

**Use for**: Routine decisions, low-risk changes, quick validations.

```markdown
## Quick Decision Review

**Decision**: [Describe what needs to be decided]

### Expert Panel (2-3 roles)
- **Engineer**: Code quality, implementation feasibility
- **QA**: Test coverage, edge cases

### Quick Assessment
| Aspect | Status | Notes |
|--------|--------|-------|
| Implementation | ✅/⚠️/❌ | |
| Test Coverage | ✅/⚠️/❌ | |
| Risk Level | Low/Med/High | |

### Recommendation
[Go/No-Go with brief rationale]
```

---

### Level 2: Standard Review (4-5 Experts)

**Use for**: Feature decisions, moderate complexity, cross-team impact.

```markdown
## Standard Decision Review

**Decision**: [Describe what needs to be decided]
**Context**: [Background and constraints]

### Expert Panel (4-5 roles)
- **Architect**: System impact, design patterns
- **Engineer**: Implementation approach
- **QA**: Quality assurance strategy
- **Product Manager**: Business value alignment

### Analysis Matrix
| Expert | Assessment | Concerns | Recommendations |
|--------|------------|----------|-----------------|
| Architect | | | |
| Engineer | | | |
| QA | | | |
| PM | | | |

### Risk Assessment
- **Technical Risk**: [Low/Medium/High]
- **Business Risk**: [Low/Medium/High]
- **Timeline Risk**: [Low/Medium/High]

### Consensus Decision
**Recommendation**: [Approve/Revise/Reject]
**Conditions**: [Any conditions for approval]
**Next Steps**: [Action items]
```

---

### Level 3: Deep Analysis (6-8 Experts)

**Use for**: Architecture decisions, significant refactoring, new technology adoption.

```markdown
## Deep Analysis Review

**Decision**: [Describe what needs to be decided]
**Context**: [Background, constraints, timeline]
**Stakeholders**: [Who is affected]

### Expert Panel (6-8 roles)
- **Architect**: System architecture implications
- **Engineer**: Implementation complexity
- **QA**: Testing strategy and coverage
- **DevOps**: Deployment and operations impact
- **Security**: Security implications
- **Product Manager**: Business alignment
- **TPM**: Timeline and resource assessment
- **Knowledge Engineer**: Documentation needs

### Multi-Angle Analysis

#### Technical Dimension
| Angle | Score (1-5) | Analysis |
|-------|-------------|----------|
| Correctness | | |
| Maintainability | | |
| Performance | | |
| Security | | |
| Scalability | | |

#### Business Dimension
| Angle | Score (1-5) | Analysis |
|-------|-------------|----------|
| Business Value | | |
| User Impact | | |
| Cost Efficiency | | |
| Time to Market | | |

### Risk Matrix
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| | | | |

### Expert Votes
| Expert | Vote | Confidence | Key Concern |
|--------|------|------------|-------------|
| | Approve/Reject | High/Med/Low | |

### Final Decision
**Consensus**: [Approve/Conditional/Reject]
**Score**: [X/100]
**Conditions**: [Required conditions]
**Action Items**: [Specific next steps with owners]
```

---

### Level 4: Comprehensive Review (10-12 Experts)

**Use for**: Major architecture changes, critical system decisions, cross-domain impact.

```markdown
## Comprehensive Decision Review

**Decision**: [Detailed description]
**Context**: [Full background and constraints]
**Impact Scope**: [Systems, teams, users affected]
**Timeline**: [Decision deadline and implementation timeline]

### Expert Committee (10-12 roles)

#### Technical Group
- Architect, Engineer, QA, DevOps, Security

#### AI/Data Group (if applicable)
- AI Engineer, Data Architect

#### Business Group
- Product Manager, TPM, UX Designer

#### Governance Group
- Knowledge Engineer, Compliance Expert

### 10×10 Core Matrix Analysis

[Use the Core 10×10 Matrix from the framework]

| Role/Angle | Correct | Maintain | Perform | Secure | Scale | Value | Usable | Efficient | Timely | Document |
|------------|---------|----------|---------|--------|-------|-------|--------|-----------|--------|----------|
| Architect | | | | | | | | | | |
| Engineer | | | | | | | | | | |
| QA | | | | | | | | | | |
| DevOps | | | | | | | | | | |
| Security | | | | | | | | | | |
| PM | | | | | | | | | | |
| TPM | | | | | | | | | | |
| AI Eng | | | | | | | | | | |
| UX | | | | | | | | | | |
| KE | | | | | | | | | | |

### Weighted Scoring
- **Technical Score**: [X/100] (weight: 40%)
- **Business Score**: [X/100] (weight: 35%)
- **Process Score**: [X/100] (weight: 25%)
- **Final Score**: [X/100]

### Decision Summary
**Recommendation**: [Approve/Conditional/Major Revision/Reject]
**Confidence Level**: [High/Medium/Low]
**Dissenting Opinions**: [Note any significant disagreements]

### Implementation Plan
1. [Phase 1 with timeline]
2. [Phase 2 with timeline]
3. [Validation checkpoints]
```

---

### Level 5: Full Committee (24 Experts)

**Use for**: Critical decisions, major pivots, organization-wide impact.

```markdown
## Level 5 Expert Committee Review

**Decision**: [Strategic decision description]
**Impact**: [Organization-wide implications]
**Urgency**: [Critical/High/Medium]

### Full Committee Structure (24 Experts)

#### Architecture & Systems Group (6)
Chief Architect, Information Architect, Systems Engineer,
API Designer, Performance Architect, Reliability Engineer

#### Knowledge Engineering Group (6)
Knowledge Manager, Documentation Engineer, Metadata Specialist,
Search Expert, Content Strategist, Ontology Designer

#### AI Collaboration Group (6)
AI Collaboration Expert, Prompt Engineer, Autonomy Specialist,
Cognitive Scientist, Ethics Expert, Timeout & Safety Expert

#### Engineering Practice Group (6)
DevOps Expert, Python Engineer, Test Architect,
UX Expert, Product Manager, Security Engineer

### Group Assessments

| Group | Approval | Score | Key Concerns | Conditions |
|-------|----------|-------|--------------|------------|
| Architecture | Yes/No | /100 | | |
| Knowledge | Yes/No | /100 | | |
| AI Collaboration | Yes/No | /100 | | |
| Engineering | Yes/No | /100 | | |

### Consensus Building
- **Unanimous**: All groups approve
- **Strong Consensus**: 3/4 groups approve, conditions addressed
- **Conditional**: 2/4 groups approve, major conditions required
- **Rejected**: <2 groups approve

### Final Verdict
**Decision**: [Approved/Conditional/Rejected]
**Overall Score**: [X/100]
**Committee Confidence**: [X%]

### Binding Conditions
1. [Must-meet condition]
2. [Must-meet condition]

### Post-Decision Actions
- [ ] Document decision rationale
- [ ] Communicate to stakeholders
- [ ] Set up review checkpoints
- [ ] Plan rollback strategy
```

---

## Quick Reference: Decision Level Selection

| Criteria | L1 | L2 | L3 | L4 | L5 |
|----------|----|----|----|----|-----|
| Risk Level | Low | Medium | High | Critical | Strategic |
| Reversibility | Easy | Moderate | Hard | Very Hard | Irreversible |
| Team Impact | 1 team | 2-3 teams | Dept | Cross-dept | Org-wide |
| Time Needed | <30min | 1-2 hours | 1 day | 2-3 days | 1 week |
| Expert Count | 2-3 | 4-5 | 6-8 | 10-12 | 24 |

---

## Usage Tips

1. **Start Low**: Begin with a lower level and escalate if needed
2. **Time-Box**: Set time limits for each level of review
3. **Document**: Always capture the decision rationale
4. **Revisit**: Schedule review for major decisions
5. **Adapt**: Customize templates for your domain

---

**See Also**:
- [Expert Committee Framework](../frameworks/cognitive/expert_committee.md) - Full theory
- [Quality Angles](../frameworks/decision/quality_angles.md) - Detailed quality dimensions
- [Autonomy Levels](../frameworks/autonomy/levels.md) - Decision authority guidelines
