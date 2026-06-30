state bucket作成は手元のgcloudでやった。

1. storage bucket作成
```bash
PROJECT_ID=waseda-syllabus-project
REGION=asia-northeast1
BUCKET_NAME="${PROJECT_ID}-terraform-state"

gcloud storage buckets create "gs://${BUCKET_NAME}" \
  --project="${PROJECT_ID}" \
  --location="${REGION}" \
  --uniform-bucket-level-access
```

2. versioning

```bash
gcloud storage buckets update "gs://${BUCKET_NAME}" \
  --versioning
```

3. bucketへのアクセス付与
objectAdminつけるのはビミョイかもだが後から調整する。全部gitOpsで管理できるようになったら適切に権限分離したSAからだけ触れるようにする
```bash
USER_EMAIL="$(gcloud config get-value account)"

gcloud storage buckets add-iam-policy-binding "gs://${BUCKET_NAME}" \
  --member="user:${USER_EMAIL}" \
  --role="roles/storage.objectAdmin"
```

4. versions.tfを書く

5. terraform init -migrate-state