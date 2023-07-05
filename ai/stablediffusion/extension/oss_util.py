import oss2, logging

from config import ACCESS_ID as ACCESS_KEY_ID, ACCESS_KEY as ACCESS_KEY_SECRET, OSS_ENDPOINT, OSS_BUCKET

logger = logging.getLogger(__name__)

auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)

bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET, is_cname=False)

def upload_bytes_to_oss(bytes, oss_file_name):
    index = oss_file_name.rfind("/")
    file_name = oss_file_name[index+1:]
    content_disposition = 'attachment;filename="%s"' % file_name
    
    bucket.put_object(oss_file_name, bytes, headers={'Content-Disposition': content_disposition})

def upload_to_oss(local_file_path, oss_file_name):
    """
      upload to oss
    """
    # 上传文件到 OSS
    index = oss_file_name.rfind("/")
    file_name = oss_file_name[index+1:]
    content_disposition = 'attachment;filename="%s"' % file_name
    
    with open(local_file_path, 'rb') as f:
        bucket.put_object(oss_file_name, f, headers={'Content-Disposition': content_disposition})

def sign_url(oss_file_name):
    # sign an oss url with expiration time
    expiration_seconds = 60 * 60
    url = bucket.sign_url('GET', oss_file_name, expiration_seconds)
    url = url.replace("http:", "https:")

    logger.info(f'Getting url for {oss_file_name}')
    return url

# entry point
if __name__ == '__main__':
    local_file_path, oss_file_name = "/data/Downloads/test.ppt", "Downloads/test.ppt"
    upload_to_oss(local_file_path, oss_file_name)
