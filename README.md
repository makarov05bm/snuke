# SNUKE Bucket Hunter
a CLI tool that accepts a target domain, enumerates its subdomains, crawls them to identify cloud storage buckets (AWS, Azure, GCP), and checks if these buckets are publicly accessible or writable.

>[IMPORTANT] The tool attempts to upload a file to discovered buckets to test writability. While this is a standard method for vulnerability verification, the user should be aware of this active interaction with external logical assets. The file name will be bug_bounty_poc.txt containing a harmless timestamp string.

📦 Supported Cloud Storage Patterns

This tool uses regular expressions to identify and extract bucket URLs for the three major cloud providers. Below are the supported URL formats:
🟠 AWS S3 (Amazon Web Services)

Detects standard S3 buckets and static website hosting endpoints.

    Path-style: s3.amazonaws.com/bucket-name

    Virtual-hosted style: bucket-name.s3.amazonaws.com

    Regional endpoints: bucket-name.s3.us-west-2.amazonaws.com

    S3 Websites: bucket-name.s3-website.us-east-1.amazonaws.com

🔵 Azure Blob Storage

Detects various Azure Storage services (Blob, Data Lake Gen2, File, Queue, and Table).

    Blob Storage: accountname.blob.core.windows.net

    Data Lake (DFS): accountname.dfs.core.windows.net

    File/Queue/Table: Supports .file, .queue, and .table endpoints.

🟢 GCP (Google Cloud Platform)

Detects Google Cloud Storage (GCS) buckets using both the standard API and authenticated browser URLs.

    Standard API: storage.googleapis.com/bucket-name

    Subdomain style: bucket-name.storage.googleapis.com

    Console/Browser: storage.cloud.google.com/bucket-name
