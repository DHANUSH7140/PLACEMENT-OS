# Integration Contract for Member 4 (Cloud Run + BigQuery + Looker Studio)
**Owner:** Member 3 (Data Architecture & Question Intelligence)  
**Target:** Member 4 (DevOps, BigQuery Analytics, Looker Studio & Deployment)

---

## 1. Cloud Scheduler Ingestion Trigger

Deploy a Google Cloud Scheduler job targeting Member 2's FastAPI service running on Cloud Run:

- **Schedule:** Every 6 hours (`0 */6 * * *`)
- **HTTP Target:** `https://<YOUR-CLOUD-RUN-URL>/api/v1/ingest/trigger`
- **HTTP Method:** `POST`
- **Headers:**
  - `X-Scheduler-Secret: <MATCHING_SCHEDULER_SECRET_TOKEN>`
  - `Content-Type: application/json`

---

## 2. BigQuery Streaming Export (Firebase Extension)

Install the **Stream Collections to BigQuery** Firebase Extension (`firestore-bigquery-export`) for the following key collections:
- `questions` -> `placement_os_analytics.questions_raw_changelog`
- `question_attempts` -> `placement_os_analytics.question_attempts_raw_changelog`
- `student_profiles` -> `placement_os_analytics.student_profiles_raw_changelog`
- `mistakes` -> `placement_os_analytics.mistakes_raw_changelog`
- `assessments` -> `placement_os_analytics.assessments_raw_changelog`

---

## 3. Recommended BigQuery Flattened Views for Looker Studio

Because Firestore stores nested arrays (`skills`, `companies`, `roles`), create BigQuery SQL views that unnest these arrays for easy charting in Looker Studio:

### 3.1. Questions Dimensional View
```sql
CREATE OR REPLACE VIEW `placement_os_analytics.v_questions_flattened` AS
SELECT
  JSON_VALUE(data, '$.id') AS question_id,
  JSON_VALUE(data, '$.category') AS category,
  JSON_VALUE(data, '$.subcategory') AS subcategory,
  JSON_VALUE(data, '$.topic') AS topic,
  JSON_VALUE(data, '$.difficulty') AS difficulty,
  CAST(JSON_VALUE(data, '$.observed_frequency') AS INT64) AS observed_frequency,
  CAST(JSON_VALUE(data, '$.source_count') AS INT64) AS source_count,
  CAST(JSON_VALUE(data, '$.student_relevance') AS FLOAT64) AS student_relevance,
  company,
  role
FROM
  `placement_os_analytics.questions_raw_latest`,
  UNNEST(JSON_EXTRACT_ARRAY(data, '$.companies')) AS company_json,
  UNNEST([JSON_VALUE(company_json)]) AS company,
  UNNEST(JSON_EXTRACT_ARRAY(data, '$.roles')) AS role_json,
  UNNEST([JSON_VALUE(role_json)]) AS role;
```

### 3.2. Student Performance & Mistake Heatmap View
```sql
CREATE OR REPLACE VIEW `placement_os_analytics.v_student_mistakes_summary` AS
SELECT
  JSON_VALUE(data, '$.student_id') AS student_id,
  JSON_VALUE(data, '$.category') AS category,
  JSON_VALUE(data, '$.subcategory') AS subcategory,
  JSON_VALUE(data, '$.mistake_type') AS mistake_type,
  COUNT(1) AS mistake_count
FROM
  `placement_os_analytics.mistakes_raw_latest`
GROUP BY
  student_id, category, subcategory, mistake_type;
```

---

## 4. Looker Studio Dashboard Specs

The demo Looker Studio dashboard should feature:
1. **Company Hiring Focus Scorecard:** Heatmap of most frequent questions per target company (Amazon, Google, Microsoft, Deloitte, TCS).
2. **Category Preparedness Gauge:** Average student readiness score across college cohorts.
3. **Mistake Recurrence Matrix:** Bar chart of top conceptual mistakes (e.g., Dynamic Programming edge cases vs SQL window syntax).
4. **Ingestion Volume Time Series:** Daily count of ingested, verified, and deduplicated questions over time.
