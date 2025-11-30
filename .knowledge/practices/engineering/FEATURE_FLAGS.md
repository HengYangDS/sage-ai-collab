# Feature Flag Patterns

> Feature flag design principles and best practices

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Flag Types](#2-flag-types)
- [3. Naming Conventions](#3-naming-conventions)
- [4. Configuration Structure](#4-configuration-structure)
- [5. Code Implementation](#5-code-implementation)
- [6. Gradual Rollout](#6-gradual-rollout)
- [7. Lifecycle Management](#7-lifecycle-management)
- [8. Monitoring & Alerting](#8-monitoring--alerting)
- [9. Best Practices](#9-best-practices)
- [10. Quick Checklist](#10-quick-checklist)

---

## 1. Overview

Feature flags are a technique to control feature enable/disable at runtime without redeploying code.

### Core Value

| Value                   | Description                                  |
|-------------------------|----------------------------------------------|
| **Progressive Release** | Gradually roll out new features to users     |
| **Quick Rollback**      | Disable features instantly when issues arise |
| **A/B Testing**         | Compare different implementation effects     |
| **Ops Control**         | Degrade non-critical features in emergencies |

---

## 2. Flag Types

| Type                | Lifecycle             | Purpose                       | Example             |
|---------------------|-----------------------|-------------------------------|---------------------|
| **Release Flag**    | Short (days~weeks)    | Control new feature release   | `new_checkout_flow` |
| **Experiment Flag** | Medium (weeks~months) | A/B testing                   | `recommendation_v2` |
| **Ops Flag**        | Long-term             | System degradation protection | `enable_cache`      |
| **Permission Flag** | Permanent             | Control feature access        | `premium_features`  |

---

## 3. Naming Conventions

### Naming Rules

```text
[type]_[feature]_[optional:version]
```
### Examples

| Flag Name                 | Meaning                         |
|---------------------------|---------------------------------|
| `release_new_dashboard`   | Release: New dashboard          |
| `exp_search_algorithm_v2` | Experiment: Search algorithm V2 |
| `ops_rate_limiting`       | Ops: Rate limiting feature      |
| `perm_advanced_analytics` | Permission: Advanced analytics  |

---

## 4. Configuration Structure

### Simple Boolean Flag

```yaml
features:
  new_dashboard: true
  dark_mode: false
```
### Conditional Flag

```yaml
features:
  new_checkout:
    enabled: true
    rollout_percentage: 20    # 20% of users
    allowed_users: # Whitelist
      - user_123
      - user_456
    excluded_regions: # Excluded regions
      - EU
```
---

## 5. Code Implementation

### Basic Check

```python
def get_feature(name: str, default: bool = False) -> bool:
    return features_config.get(name, default)

# Usage
if get_feature("new_dashboard"):
    show_new_dashboard()
else:
    show_old_dashboard()
```
### Context-Aware Check

```python
def is_feature_enabled(name: str, context: dict) -> bool:
    feature = features_config.get(name)
    if not feature:
        return False

    if not feature.get("enabled"):
        return False

    # Check whitelist
    if context.get("user_id") in feature.get("allowed_users", []):
        return True

    # Check rollout percentage
    rollout = feature.get("rollout_percentage", 100)
    return hash(context.get("user_id")) % 100 < rollout
```
### Decorator Pattern

```python
def feature_flag(name: str, default: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_feature(name, default):
                return func(*args, **kwargs)
            return None

        return wrapper

    return decorator

@feature_flag("new_recommendation")
def get_recommendations(user_id: str):
    return new_recommendation_engine(user_id)
```
---

## 6. Gradual Rollout

### Rollout Strategy

| Stage    | Percentage | Audience              | Duration |
|----------|------------|-----------------------|----------|
| Internal | 0%         | Internal testers only | 1-2 days |
| Canary   | 1-5%       | Early adopters        | 2-3 days |
| Beta     | 10-30%     | Broader group         | 1 week   |
| GA       | 50-100%    | All users             | Gradual  |

### Rollout Configuration

```yaml
features:
  new_payment:
    enabled: true
    stages:
      - name: internal
        percentage: 0
        whitelist: [ team_member_ids ]
      - name: canary
        percentage: 5
      - name: beta
        percentage: 30
      - name: ga
        percentage: 100
    current_stage: canary
```
---

## 7. Lifecycle Management

### Flag Lifecycle

```
Created → Active → Deprecated → Removed
   │         │          │
   │         │          └─ Cleanup code
   │         └─ Monitor & decide
   └─ Start testing
```
### Cleanup Checklist

| Step | Action                            |
|------|-----------------------------------|
| 1    | Confirm flag at 100% for 2+ weeks |
| 2    | Remove flag checks from code      |
| 3    | Remove flag from configuration    |
| 4    | Update documentation              |
| 5    | Archive experiment results        |

---

## 8. Monitoring & Alerting

### Key Metrics

| Metric                    | Purpose            |
|---------------------------|--------------------|
| Flag evaluation count     | Usage tracking     |
| Error rate by flag state  | Impact comparison  |
| Performance by flag state | Performance impact |
| User feedback by cohort   | User experience    |

### Alert Conditions

```yaml
alerts:
  - name: feature_error_spike
    condition: error_rate > baseline * 1.5
    action: auto_disable_flag

  - name: performance_degradation
    condition: latency_p99 > threshold
    action: notify_oncall
```
---

## 9. Best Practices

### Do

| Practice              | Reason                    |
|-----------------------|---------------------------|
| Use descriptive names | Easy to understand intent |
| Set expiration dates  | Prevent flag accumulation |
| Document flag purpose | Maintain context          |
| Test both states      | Ensure both paths work    |
| Clean up promptly     | Reduce technical debt     |

### Don't

| Anti-Pattern             | Problem              |
|--------------------------|----------------------|
| Nested flags             | Complexity explosion |
| Flags in tight loops     | Performance impact   |
| Long-lived release flags | Technical debt       |
| Flags without owners     | Orphaned flags       |

---

## 10. Quick Checklist

### Before Creating

- [ ] Flag type identified (release/experiment/ops/permission)
- [ ] Naming follows convention
- [ ] Owner assigned
- [ ] Expiration date set (if applicable)
- [ ] Rollout plan defined

### Before Removal

- [ ] Flag at 100% for 2+ weeks
- [ ] No incidents related to feature
- [ ] Code cleanup planned
- [ ] Team notified

---

## Related

- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing with flags
- `.knowledge/practices/engineering/ERROR_HANDLING.md` — Degradation patterns
- `config/capabilities/features.yaml` — Project feature configuration

---

*AI Collaboration Knowledge Base*
