#!/usr/bin/env python
'''
lnhat

PURPOSES:
+ Khoi lenh nay dung de chuyen doi docx/doc va hop lai trong 1 file txt de tien hanh phan lop
+ khoi lenh su dung cac tachtu4,5,6 de tach nhung phan khong can thiet

pip install underthesea
# step 1: can xac dinh folder: path_folder_input chua cac file de doc
# step 2: dat ten cho txt dau ra, lay file nay dua vao topic classification
chu dau tien la ky hieu cua chu de
tu cac chu thu 2 tro di la text cua bai bao

e.g., lenh de chay
conda activate text
python3 docx_to_txt.py -i data/EN-2018-2022-full -o en-2018-2022
'''
# luu lai thoi gian
from datetime import datetime
from time import gmtime, strftime
import time
## luu lai thoi gian bat dau chay module (s)
start_time = time.time()

today = datetime.today()
time_text = str(strftime("%Y-%m-%d_%H%M%S", gmtime()))

import argparse

parser = argparse.ArgumentParser(description="run",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i", "--path_folder_input", default='data', help="folder input to merge")
parser.add_argument("-o", "--output_merged", default='result',  help="output file of merged txt")
parser.add_argument("-l", "--language", default='en',  help="select language: vn/en")
parser.add_argument("-s", "--section", default='content',  help="select section to extract: abs/title/content")
#parser.add_argument("-d", "--debug", default='n',  help="bat che do debug: CHU Y: NEU BAT CHE DO NAY TAP TIN TAO RA KHONG DUNG CHO VIEC PHAN LOP!!")

parser.add_argument("-fout", "--output_folder_log", default='output',  help="folder luu kq")
args = parser.parse_args()

# merge pdf nhung khong add blank page khi pdf le
import os
import docx2txt
import re
import tachtufull
# import tachtu5
# import tachtu6


# dung bieu thuc chinh quy de do tim ky tu dang *-%%-*, co 2 dau - bao phu ma chu de
# topic_regex = r"\b([A-Za-z]{2})-\b"
topic_regex = r"\b([A-Za-z]{2,4})-\b"
i = 0
er = 0
succeed = 0
topic_not_valid = 0


if not ( os.path.exists(args.output_folder_log)):
    os.makedirs(args.output_folder_log)

# file text
file_out = open(args.output_folder_log + '/'+ args.output_merged + ".txt", "w", encoding="utf-8")
# luu vao log
logfile = open(args.output_folder_log + '/'+ args.output_merged + str(args.section)+ str(args.language) + str(time_text) + "log.txt", "w", encoding="utf-8")

# # file text
# file_out = open(args.output_merged +str(args.section)+ str(args.language) + str(time_text) + ".txt", "w", encoding="utf-8")
# # luu vao log
# logfile = open(args.output_merged + str(args.section)+ str(args.language) + str(time_text) + "log.txt", "w", encoding="utf-8")
# in tieu de
print("No.\tidtxt\tTopic\tfullpath\tname\tlen",file=logfile) 

#logfile.write("\nNo.\tTopic\tfullpath\tname\n") 

for root, dirs, files in os.walk(args.path_folder_input, topdown=True):
    for name in files:
        print(i+1)
        path_file = os.path.join(root, name)
        #print('fullpath:',path_file,', file:',name)
        try:
           
            match = re.search(topic_regex, name)
            if match:
                topic_result = match.group(1)
                #print('topic='+str(topic_result))    
                text1 = docx2txt.process(path_file)
                
                try:
                    #text1 = tachtu4.fileWordTokenize1(text1)
                    if args.section == 'content':
                        f = tachtufull.fileWordTokenize3(text1)
                    elif args.section in ['abs', 'abstract']:
                        # BO SUNG HAM tach_abstract, tach_title trong tachtufull
                        f = tachtufull.tach_abstract(text1)
                    elif args.section in ['title', 'ttl']:
                        f = tachtufull.tach_title(text1)
                    else:
                        print('phan noi dung tach khong ho tro')
                        exit()
                    a = f
                except Exception as e: 
                    print('fileWordTokenize tachtu4 bi loi' + str(e) , file = logfile)
                    # print(e)
                    # try:
                    #     f = tachtu5.fileWordTokenize(text1)
                    #     a = f
                    # except Exception as e: 
                    #     print('fileWordTokenize tachtu5 bi loi' , file = logfile)
                    #     print(e)
                    #     try:
                    #         f = tachtu6.fileWordTokenize2(text1)
                    #         a = f
                    #     except Exception as e: 
                    #         print('fileWordTokenize tachtu6 bi loi' , file = logfile)
                    #         print(e)
                
                #if i > 0:
                    #print("in ngat dong dau,in ngat dong dau,in ngat dong dau")
                #    file_out.write("\n")
                #file_out.write(topic_result + " " + a)
                print(topic_result + " " + a , file = file_out) 
                
                #logfile.write("\nNo." + str(i) + ", Topic: " + str(topic_result) + ", filename: " + str(name))   
                #print("\nNo." + str(i) + "\tTopic: " + str(topic_result) + '\tfullpath:' + path_file + '\t:'+ name , file = logfile)
                #print(str(i+1) + "\t" + str(topic_result) + "\t" + path_file + "\t:"+ name , file = logfile)  
                # print(str(i+1), "\t" , str(topic_result), "\t", path_file, "\t:", name , file = logfile) 
                print(str(i+1), "\t" , str(succeed+1), "\t" , str(topic_result), "\t", path_file + "\t:"+ name+'\t'+str(len(text1)) , file = logfile) 
                #logfile.write(str(i+1) + "\t" + str(topic_result) + "\t" + path_file + "\t:"+ name)                    
                succeed = succeed + 1
            else:
                #print("\nNo." + str(i) + "\tTopic: NOT FOUND\tfullpath:" + path_file + '\tfile:'+ name , file = logfile)    
                print(str(i+1) + "\tNA\tNOT FOUND, skipped\t" + path_file + "\t:"+ name+'\tNA' , file = logfile)               
                topic_not_valid = topic_not_valid + 1

        except Exception as e: 
            #print('file: "'+str(path_file) + '" bi loi, bo qua file nay' , file = logfile)
            print(str(i+1) + "\tNA\tError in reading,",e,", skipped\t" + path_file + "\t:"+ name+'\tNA' , file = logfile)           
            print(e)
            er = er + 1
        i = i + 1
file_out.close()
print('Da doc thanh cong:' + str(i-er-topic_not_valid) +' file, bi loi:' + str(er) + ', khong do tim duoc chu de:' + str(topic_not_valid) , file = logfile)
## luu lai thoi gian ket thuc chay module (s)
end_time = time.time()
thoigianchay = end_time - start_time
print('Thoi gian thuc thi: ' + str(thoigianchay) + ' giay, trung binh:'+str(thoigianchay/i)+' second/file' , file = logfile)
logfile.close()
# find ./EN-2015-2022/ -type f | wc -l