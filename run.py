import shutil,os,zipfile,time,logging,logging.config,re
   
def main():
    logging.basicConfig(filename='log.txt',
                            filemode='a',
                            format='[%(asctime)s] %(name)s: %(levelname)s -- %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
    
    logging.root = logging.getLogger('File Transfer')

    datlist = []
    with open('config.dat') as file:
        array = []
        for line in file:
            array.append(line) #return ['car\n','bike\n','plane\n'] if newline found.

    source = array[0].rstrip('\n') #remove newline '\n' in array
    path = source[7:]

    destination = array[1].rstrip('\n')
    moveto = destination[12:]

    sleep = array[2].rstrip('\n')
    sleep = sleep[6:] 

    if os.path.exists(path) and os.path.exists(moveto) and not re.search('[a-zA-Z\-]+',sleep): 
        sleep=float(sleep)
        logging.info('Path exist, sleep -- %s',sleep)
        while(True):        
            try:

                files = os.listdir(path)     #returns a list in the directory given by path
                #files.sort() #sort
                for f in files:
        
                    src = path+f
                    dst = moveto+f

                    statinfo=os.stat(src)
                    logging.info('File: %s, Size: %s',f,statinfo.st_size)

                    if os.path.exists(src):
                        if zipfile.is_zipfile(src):
                            
                            with zipfile.ZipFile(src,"r") as zip_ref:
                                zip_ref.extractall(dst) #extract at path
                                
                                for fileinfo in zip_ref.infolist(): #fileinfo = <ZipInfo filename='file3.xlsx' compress_type=deflate external_attr=0x20 file_size=8351 compress_size=5889>
                                    logging.info('Extracted file: %s, size : %s',fileinfo.filename,fileinfo.file_size) 
                            
                                size = sum([zinfo.file_size for zinfo in  zip_ref.filelist])
                                logging.info('Total extracted size : %s',size)
                                    
                        else:
                            shutil.move(src,dst)    #moving files
            
                    os.remove(src)
                    print(".zip file removed!")
                again()
            except:
                pass
            time.sleep(sleep) 
    
    elif not os.path.exists(path):
        logging.error('Source path does not exist -- %s',path)
    elif not os.path.exists(moveto):
        logging.error('Destination path does not exist -- %s',moveto)
    else:
        logging.error('Sleep value must be positive number -- ')

if __name__ == "__main__":
    main()