# Data Pipeline Checklist

> Task checklist for ETL and data processing workflows

---

## Design

- [ ] Data sources identified
- [ ] Data schema documented
- [ ] Pipeline architecture defined
- [ ] Scheduling strategy decided
- [ ] Recovery strategy planned

## Data Extraction

- [ ] Source connections configured
- [ ] Incremental extraction supported
- [ ] Change data capture (if needed)
- [ ] Rate limiting respected
- [ ] Connection pooling used

## Data Transformation

- [ ] Business rules documented
- [ ] Data validation rules defined
- [ ] Null handling specified
- [ ] Type conversions correct
- [ ] Deduplication logic implemented

## Data Loading

- [ ] Target schema created
- [ ] Upsert logic implemented
- [ ] Batch sizes optimized
- [ ] Transaction handling correct
- [ ] Indexes managed

## Quality & Validation

- [ ] Data quality checks defined
- [ ] Row count validation
- [ ] Schema validation
- [ ] Null/empty checks
- [ ] Business rule validation
- [ ] Anomaly detection

## Error Handling

- [ ] Retry logic implemented
- [ ] Dead letter queue configured
- [ ] Alerting setup
- [ ] Error logging comprehensive
- [ ] Manual intervention procedures

## Performance

- [ ] Parallel processing enabled
- [ ] Memory usage optimized
- [ ] Partitioning strategy defined
- [ ] Bottlenecks identified
- [ ] SLA targets defined

## Monitoring

- [ ] Pipeline status dashboard
- [ ] Data freshness tracking
- [ ] Row count monitoring
- [ ] Latency metrics
- [ ] Cost monitoring

## Security

- [ ] Credentials in secrets manager
- [ ] Data encryption (at rest/transit)
- [ ] PII handling compliant
- [ ] Access controls configured
- [ ] Audit logging enabled

## Documentation

- [ ] Pipeline diagram created
- [ ] Data lineage documented
- [ ] Runbook written
- [ ] On-call procedures defined

---

*SAGE Knowledge Base - Data Pipeline Checklist*
