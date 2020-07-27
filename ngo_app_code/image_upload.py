import connection

def upload_contact_image(filename, key):
    bucket = "aaksathe-app"
    connection.cos.upload_file(Filename=filename,Bucket=bucket,Key=key)

def download_contact_image(filename):
    bucket = "aaksathe-app"
    try :
        connection.cos.download_file(Bucket=bucket,Key=filename,Filename='resources/contact/'+filename)
        file_found = True
    except :
        file_found = False
    finally :
        return file_found

def upload_org_logo(filename, key):
    bucket = "aaksathe-app"
    connection.cos.upload_file(Filename=filename,Bucket=bucket,Key=key)

def download_org_image(filename):
    bucket = "aaksathe-app"
    src_file_name = 'org_'+str(filename)+'.png'
    try :
        connection.cos.download_file(Bucket=bucket,Key=src_file_name,Filename='resources/org/'+filename+'.png')
        file_found = True
    except :
        file_found = False
    finally :
        return file_found