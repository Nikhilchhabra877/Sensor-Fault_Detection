import os
class S3Sync:


    def sync_dir_to_s3(self,dir,s3_bucket_url):
        command = f"aws s3 sync {dir} {s3_bucket_url}"
        os.system(command)
    

    def sync_s3_to_dir(self,dir,s3_bucket_url):
        command = f"aws s3 sync {s3_bucket_url} {dir} "
        os.system(command)

    