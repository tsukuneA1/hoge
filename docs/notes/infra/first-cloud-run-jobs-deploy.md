1. projectを作る。project_idはimmutable
2. Artifact Registry Repositoryを作る (syllabus)
3. Docker認証 gcloud auth configure-docker asia-northeast1-docker.pkg.dev
4. crawler imageをビルド
    ```bash
    docker build \
    -f packages/crawler/Dockerfile \
    -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/crawler:dev \
    .
    ```
5. push 
    ```bash
    docker build \
    -f packages/crawler/Dockerfile \
    -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/crawler:dev \
    .
    ```
6. Cloud SQL instance作成
    ```bash
    PROJECT_ID=<your-project-id>
    REGION=asia-northeast1
    INSTANCE=syllabus-postgres

    gcloud sql instances create $INSTANCE \
    --project=$PROJECT_ID \
    --database-version=POSTGRES_16 \
    --region=$REGION \
    --tier=db-f1-micro \
    --storage-type=SSD \
    --storage-size=10 \
    --availability-type=ZONAL \
    --no-backup
    ```
7. database作成
    ```bash
    DB_NAME=hoge_db

    gcloud sql databases create $DB_NAME \
    --instance=$INSTANCE \
    --project=$PROJECT_ID
    ```
8. user passwordを作る
    ```bash
    gcloud sql users set-password postgres \
    --instance=$INSTANCE \
    --password=$DB_PASSWORD \
    --project=$PROJECT_ID
    ```
9. Secret Manager
    ```bash
    SECRET_NAME=crawler-db-password

    printf "%s" "$DB_PASSWORD" | gcloud secrets create $SECRET_NAME \
    --data-file=- \
    --project=$PROJECT_ID
    ```
10. Cloud SQL Connection
    ```bash
    CONNECTION=$(gcloud sql instances describe $INSTANCE \
    --project=$PROJECT_ID \
    --format='value(connectionName)')

    echo $CONNECTION
    ```
11. SA
    ```bash
    SA_NAME=crawler-job-sa

    gcloud iam service-accounts create $SA_NAME \
    --project=$PROJECT_ID \
    --display-name="Crawler Job Service Account"
    ```
12. DDLを打つ
    ```bash
    gcloud sql connect syllabus-postgres --user=$DB_USER --database=$DB_NAME
    ```
    \i sqlc/schema.sql
    ```psql
13. Job作成
    ```bash
    IMAGE_URL=asia-northeast1-docker.pkg.dev/$PROJECT_ID/<REPOSITORY>/crawler:dev

    gcloud run jobs create crawler-discover \
    --image=$IMAGE_URL \
    --region=$REGION \
    --service-account=$SA_EMAIL \
    --add-cloudsql-instances=$CONNECTION_NAME \
    --set-env-vars=PGHOST="/cloudsql/$CONNECTION_NAME",PGPORT=5432,PGDATABASE=$DB_NAME,PGUSER=$DB_USER \
    --set-secrets=PGPASSWORD=$SECRET_NAME:latest \
    --args="discover,--year,2026,--page-size,2000" \
    --max-retries=0 \
    --task-timeout=30m
  ```
14. execute
    ```bash
    gcloud run jobs execute crawler-discover \
    --region=$REGION
    ```
15. logging
    ```bash
    gcloud logging read \
    'resource.type="cloud_run_job" AND resource.labels.job_name="crawler-discover"' \
    --limit=100 \
    --format="value(textPayload)"
    ```
