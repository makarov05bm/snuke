# SNUKE Bucket Hunter
a CLI tool that accepts a target domain, enumerates its subdomains, crawls them to identify cloud storage buckets (AWS, Azure, GCP), and checks if these buckets are publicly accessible or writable.

>[IMPORTANT] The tool attempts to upload a file to discovered buckets to test writability. While this is a standard method for vulnerability verification, the user should be aware of this active interaction with external logical assets. The file name will be bug_bounty_poc.txt containing a harmless timestamp string.
