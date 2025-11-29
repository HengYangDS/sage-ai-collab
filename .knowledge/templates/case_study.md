# Case Study Template

> Template for documenting problem-solving cases and lessons learned

---

## Usage Instructions

1. Copy this template to `.context/intelligence/cases.md` or create a new file
2. Fill in each section with details from your case
3. Update the summary table at the top
4. Add to the cases index for future reference

---

## Case Summary

| Field          | Value                                                       |
|----------------|-------------------------------------------------------------|
| **Case ID**    | CASE-YYYY-MM-DD-NNN                                         |
| **Title**      | [Brief descriptive title]                                   |
| **Date**       | YYYY-MM-DD                                                  |
| **Category**   | [Bug Fix / Performance / Architecture / Integration / etc.] |
| **Difficulty** | [Simple / Medium / Complex]                                 |
| **Time Spent** | [X hours/minutes]                                           |
| **Status**     | [Resolved / Ongoing / Documented]                           |

---

## 1. Problem Description

### 1.1 Context

[Describe the context and background of the problem]

- **Project/Module**: [Affected area]
- **Environment**: [Development/Staging/Production]
- **Impact**: [What was affected?]

### 1.2 Symptoms

[What were the observable symptoms?]

- Symptom 1: [Description]
- Symptom 2: [Description]
- Error messages (if any):

```
[Error message or log output]
```

### 1.3 Expected Behavior

[What should have happened?]

### 1.4 Actual Behavior

[What actually happened?]

---

## 2. Investigation

### 2.1 Initial Hypothesis

[What did you initially think was wrong?]

1. Hypothesis 1: [Description]
2. Hypothesis 2: [Description]

### 2.2 Investigation Steps

| Step | Action         | Result           |
|------|----------------|------------------|
| 1    | [What you did] | [What you found] |
| 2    | [What you did] | [What you found] |
| 3    | [What you did] | [What you found] |

### 2.3 Root Cause

[What was the actual root cause?]

**Category**: [Code Bug / Configuration / Environment / Design Flaw / External Dependency]

**Details**:
[Detailed explanation of the root cause]

---

## 3. Solution

### 3.1 Approach

[Describe the approach taken to solve the problem]

### 3.2 Implementation

**Files Changed**:

- `path/to/file1.py` - [Brief description of change]
- `path/to/file2.yaml` - [Brief description of change]

**Key Code Changes**:

```python
# Before
[original code]

# After
[fixed code]
```

### 3.3 Verification

[How did you verify the fix worked?]

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual verification
- [ ] Performance verified

---

## 4. Lessons Learned

### 4.1 What Went Well

- [Positive aspect 1]
- [Positive aspect 2]

### 4.2 What Could Be Improved

- [Improvement area 1]
- [Improvement area 2]

### 4.3 Key Takeaways

| Takeaway     | Action Item       |
|--------------|-------------------|
| [Learning 1] | [How to apply it] |
| [Learning 2] | [How to apply it] |

### 4.4 Prevention

[How can similar issues be prevented in the future?]

- Prevention measure 1
- Prevention measure 2

---

## 5. Related Information

### 5.1 Related Cases

- [CASE-YYYY-MM-DD-NNN] - [Brief description]

### 5.2 References

- [Link or reference 1]
- [Link or reference 2]

### 5.3 Tags

`tag1` `tag2` `tag3`

---

## Quick Reference: Case Categories

| Category      | Description               | Examples                     |
|---------------|---------------------------|------------------------------|
| Bug Fix       | Fixing incorrect behavior | Logic errors, edge cases     |
| Performance   | Optimization issues       | Slow queries, memory leaks   |
| Architecture  | Design-level issues       | Coupling, scalability        |
| Integration   | External system issues    | API changes, connectivity    |
| Configuration | Config-related issues     | Wrong settings, env vars     |
| Security      | Security vulnerabilities  | Auth, data exposure          |
| Documentation | Doc-related fixes         | Incorrect docs, missing info |

---

## Example Case

### Case Summary

| Field          | Value                                   |
|----------------|-----------------------------------------|
| **Case ID**    | CASE-2025-11-29-001                     |
| **Title**      | Output files created in wrong directory |
| **Date**       | 2025-11-29                              |
| **Category**   | Bug Fix                                 |
| **Difficulty** | Simple                                  |
| **Time Spent** | 15 minutes                              |
| **Status**     | Resolved                                |

### Problem

The `build_knowledge_graph` function was creating output files in the current working directory instead of the
designated `.outputs/` directory.

### Root Cause

The function directly used the provided `output_file` path without ensuring it was placed in the `.outputs/` directory.

### Solution

Modified `mcp_server.py` to:

1. Create `.outputs/` directory if it doesn't exist
2. Extract only the filename from user-provided path
3. Construct output path as `.outputs/{filename}`

```python
# Before
builder.export_to_json(Path(output_file))

# After
outputs_dir = project_root / ".outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)
output_path = outputs_dir / Path(output_file).name
builder.export_to_json(output_path)
```

### Lessons Learned

- Always normalize output paths to designated directories
- Create output directories programmatically
- Document output file locations in function docstrings

---

*Template version: 1.0 — Part of SAGE Knowledge Base*
