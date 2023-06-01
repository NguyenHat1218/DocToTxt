from underthesea import word_tokenize
import regex as re
import os
import sys
import time
import docx2txt
from re import sub
from collections import Counter
from underthesea import sent_tokenize

uniChars = "àáảãạâầấẩẫậăằắẳẵặèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÂĂĐÔƠƯ"
unsignChars = "aaaaaaaaaaaaaaaaaeeeeeeeeeeediiiiiooooooooooooooooouuuuuuuuuuuyyyyyAAAAAAAAAAAAAAAAAEEEEEEEEEEEDIIIOOOOOOOOOOOOOOOOOOOUUUUUUUUUUUYYYYYAADOOU"
 
def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic
dicchar = loaddicchar()

# Hàm chuyển Unicode dựng sẵn về Unicde tổ hợp (phổ biến hơn)
def convert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)

bang_nguyen_am = [['a', 'à', 'á', 'ả', 'ã', 'ạ', 'a'],
                  ['ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ', 'aw'],
                  ['â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ', 'aa'],
                  ['e', 'è', 'é', 'ẻ', 'ẽ', 'ẹ', 'e'],
                  ['ê', 'ề', 'ế', 'ể', 'ễ', 'ệ', 'ee'],
                  ['i', 'ì', 'í', 'ỉ', 'ĩ', 'ị', 'i'],
                  ['o', 'ò', 'ó', 'ỏ', 'õ', 'ọ', 'o'],
                  ['ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ', 'oo'],
                  ['ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ', 'ow'],
                  ['u', 'ù', 'ú', 'ủ', 'ũ', 'ụ', 'u'],
                  ['ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự', 'uw'],
                  ['y', 'ỳ', 'ý', 'ỷ', 'ỹ', 'ỵ', 'y']]
bang_ky_tu_dau = ['', 'f', 's', 'r', 'x', 'j']

nguyen_am_to_ids = {}

for i in range(len(bang_nguyen_am)):
    for j in range(len(bang_nguyen_am[i]) - 1):
        nguyen_am_to_ids[bang_nguyen_am[i][j]] = (i, j)

def chuan_hoa_dau_tu_tieng_viet(word):
    if not is_valid_vietnam_word(word):
        return word

    chars = list(word)
    dau_cau = 0
    nguyen_am_index = []
    qu_or_gi = False
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x == -1:
            continue
        elif x == 9:  # check qu
            if index != 0 and chars[index - 1] == 'q':
                chars[index] = 'u'
                qu_or_gi = True
        elif x == 5:  # check gi
            if index != 0 and chars[index - 1] == 'g':
                chars[index] = 'i'
                qu_or_gi = True
        if y != 0:
            dau_cau = y
            chars[index] = bang_nguyen_am[x][0]
        if not qu_or_gi or index != 1:
            nguyen_am_index.append(index)
    if len(nguyen_am_index) < 2:
        if qu_or_gi:
            if len(chars) == 2:
                x, y = nguyen_am_to_ids.get(chars[1])
                chars[1] = bang_nguyen_am[x][dau_cau]
            else:
                x, y = nguyen_am_to_ids.get(chars[2], (-1, -1))
                if x != -1:
                    chars[2] = bang_nguyen_am[x][dau_cau]
                else:
                    chars[1] = bang_nguyen_am[5][dau_cau] if chars[1] == 'i' else bang_nguyen_am[9][dau_cau]
            return ''.join(chars)
        return word

    for index in nguyen_am_index:
        x, y = nguyen_am_to_ids[chars[index]]
        if x == 4 or x == 8:  # ê, ơ
            chars[index] = bang_nguyen_am[x][dau_cau]
            # for index2 in nguyen_am_index:
            #     if index2 != index:
            #         x, y = nguyen_am_to_ids[chars[index]]
            #         chars[index2] = bang_nguyen_am[x][0]
            return ''.join(chars)

    if len(nguyen_am_index) == 2:
        if nguyen_am_index[-1] == len(chars) - 1:
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            chars[nguyen_am_index[0]] = bang_nguyen_am[x][dau_cau]
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            # chars[nguyen_am_index[1]] = bang_nguyen_am[x][0]
        else:
            # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
            # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
            x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
            chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
    else:
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[0]]]
        # chars[nguyen_am_index[0]] = bang_nguyen_am[x][0]
        x, y = nguyen_am_to_ids[chars[nguyen_am_index[1]]]
        chars[nguyen_am_index[1]] = bang_nguyen_am[x][dau_cau]
        # x, y = nguyen_am_to_ids[chars[nguyen_am_index[2]]]
        # chars[nguyen_am_index[2]] = bang_nguyen_am[x][0]
    return ''.join(chars)


def is_valid_vietnam_word(word):
    chars = list(word)
    nguyen_am_index = -1
    for index, char in enumerate(chars):
        x, y = nguyen_am_to_ids.get(char, (-1, -1))
        if x != -1:
            if nguyen_am_index == -1:
                nguyen_am_index = index
            else:
                if index - nguyen_am_index != 1:
                    return False
                nguyen_am_index = index
    return True


def chuan_hoa_dau_cau_tieng_viet(sentence):
    """
        Chuyển câu tiếng việt về chuẩn gõ dấu kiểu cũ.
        :param sentence:
        :return:
        """
    sentence = sentence.lower()
    words = sentence.split()
    for index, word in enumerate(words):
        cw = re.sub(r'(^\p{P}*)([p{L}.]*\p{L}+)(\p{P}*$)', r'\1/\2/\3', word).split('/')
        # print(cw)
        if len(cw) == 3:
            cw[1] = chuan_hoa_dau_tu_tieng_viet(cw[1])
        words[index] = ''.join(cw)
    return ' '.join(words)



def StrList(text):
    words = text.replace("', '", '#').replace("['", '').replace("']", '')
    return words.split("#")


def listToString(s):
    str1 = " "
    return (str1.join(s))

def text_preprocess(document):
   
    # chuẩn hóa unicode
    document = convert_unicode(document)
    # chuẩn hóa cách gõ dấu tiếng Việt
    document = chuan_hoa_dau_cau_tieng_viet(document)
    return document
def fileWordTokenize1(fileName):
    # file_input = open(fileName, "r+", encoding="utf-8")
    # read_file = file_input.read()  # Đọc nội dung của File
    
    # Tách nội dung File theo từng dòng vô list
    list_string = fileName.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa


    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'TÓM TẮT'
            
   
    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT' :
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra và xử lý và lấy ra tiêu đề
    # title_index_listUpper = listUpper.index('TÓM TẮT')
    # if title_index_listUpper == 2:
    #     get_title = listWord[0]
    # elif title_index_listUpper == 4:
    #     title_list = listUpper[0:3]
    #     get_title = ' '.join(title_list)
    # else:
    #     title_list = listUpper[0:2]
    #     get_title = ' '.join(title_list)

    # title = get_title  
    # Begin lấy ra và xử lý và lấy ra tiêu đề
    # get_title = listWord[1]
    # End lấy ra và xử lý tiêu đề
    # # Lấy ra tên tiêu đề bài báo
    # End lấy ra và xử lý tiêu đề

    # Begin Lấy nội dung từ Giới thiệu đến Kết luận
    # tomtat_listUpper = listUpper.index('TÓM TẮT')
    # gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    gioiThieu = listWord.index('TÓM TẮT')

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]
    

 
    
    test=[]
    test =content
    

    testTachBoNgoac=[]
    for sentences1 in test:
        a=re.sub(r'\([^(:)]*\)', "", sentences1)
        if a == '' or a == ' ' or len(a) <= 2:
            pass
        else:
            testTachBoNgoac.append(a)
        

    # tiep tuc loc
    testTachBoNgoac2=[]
    for sentences2 in testTachBoNgoac:
        b=re.sub(r'\([^()]*\)', "", sentences2)
        if b == '' or b == ' ' or len(b) <= 2:
            pass
        else:
            testTachBoNgoac2.append(b)
        
        
    testTachBangHinh3=[]
    for sentences6 in testTachBoNgoac:
        Hinh ="""(^Hình |^Bảng | ^Bước |^\tBước )[0-9][a-zA-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂưăạảấầẩẫậắằẳẵặẹẻẽếềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵýỷỹ,':/{}()!#@$%^&*_+=;?~`| 0123456789\-'"\[\]/]{1,}"""
        text2=re.sub(Hinh, "", sentences6)
        if text2 == '' or text2 == ' ' or len(text2) <= 2:
            pass
        else:
            testTachBangHinh3.append(text2)
       
   
   
   
    
    testTachCongThuc=[]
    for sentences4 in testTachBangHinh3:
        congthuc ="""[■:°τ;()%_^/+Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×]|;|-"""
        d = re.sub(congthuc," ",sentences4)
        if d == '' or d == ' ' or len(d) <= 2:
            pass
        else:
            testTachCongThuc.append(d)
        

    testTachSinCos=[]
    for sentencesfinal in testTachCongThuc:
        m=re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', "", sentencesfinal)
        if m == '' or m == ' ' or len(m) <= 2:
            pass
        else:
            testTachSinCos.append(m)
    
    tachkhoangtrang=[]
    for tach_1 in testTachSinCos:
        m=re.sub("    +","",tach_1)
        if m == '' or m == ' ' or len(m) <= 2:
            pass
        else:
            tachkhoangtrang.append(m)
    
    testTachSo=[]
    for sentencestest in tachkhoangtrang:
        n=re.sub(r'\b\d+\b', " ", sentencestest)
        testTachSo.append(n)
        
    
        
    ketqua = []
    for word in testTachSo:  # tách câu
        if '.' in word:
            cau = []
            caughep = word.split(".")
            for i in range(0, len(caughep)):
                if i == 0:
                    cau.append(caughep[i].strip())
                elif i == 1 and len(caughep[0].split(" ")) <= 5:
                    cau[len(cau)-1] += ". "+caughep[i]
                elif len(caughep[i].split(" ")) > 5:
                    cau.append(caughep[i].strip())
                elif len(caughep[i].split(" ")) <= 5:
                    cau[len(cau)-1] += ". "+caughep[i]
            # ketqua.extend(cau)
            for i in cau:
                if i!=" " and i!="" and i!="\n" and len(re.split(" ",i)) > 4:
                    ketqua.append(i.strip())
        elif word!=" " and word!="" and word!="\n"  and len(re.split(" ",word.strip())) > 4:
            ketqua.append(word.strip())
    if '' in ketqua:
        ketqua.remove('')
    
    # tiep tuc xoa
    xoadau=[]
    for tach_1 in ketqua:
        dau ="""[,|.|*]"""
        m=re.sub(dau,"",tach_1)
        if m == '' or m == ' ' or len(m) <= 2:
            pass
        else:
            xoadau.append(m)
  
        
    words1=[]
    for sentences5 in xoadau:
        f= re.sub(r"((?<=^)|(?<= )).((?=$)|(?= ))", "", sentences5)
        words1.append(f)
        
    word3=[]
    for sentences6 in words1:
        m=re.sub(' +', ' ',sentences6)
        word3.append(m)  
      
    end = []
    for word in word3:  # tách câu
        if '.' in word:
            cau = []
            caughep = word.split(".")
            for i in range(0, len(caughep)):
                if i == 0:
                    cau.append(caughep[i].strip())
                elif i == 1 and len(caughep[0].split(" ")) <= 5:
                    cau[len(cau)-1] += ". "+caughep[i]
                elif len(caughep[i].split(" ")) > 5:
                    cau.append(caughep[i].strip())
                elif len(caughep[i].split(" ")) <= 5:
                    cau[len(cau)-1] += ". "+caughep[i]
            # ketqua.extend(cau)
            for i in cau:
                if i!=" " and i!="" and i!="\n" and len(re.split(" ",i)) > 4:
                    end.append(i.strip())
        elif word!=" " and word!="" and word!="\n"  and len(re.split(" ",word.strip())) > 4:
            end.append(word.strip())
    if '' in end:
        end.remove('')


    testTachBangHinh4 = []
    for sentences6 in end:
        Hinh = """[0-9][a-zA-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂưăạảấầẩẫậắằẳẵặẹẻẽếềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵýỷỹ']"""
        text2 = re.sub(Hinh, "", sentences6)
        testTachBangHinh4.append(text2)
        
    testTachBangHinh5 = []
    for sentences6 in testTachBangHinh4:
        Hinh = """\S*\d\S*"""
        text2 = re.sub(Hinh, "", sentences6)
        testTachBangHinh5.append(text2)
    

    
    content_string_one = ' '.join(testTachBangHinh5)
#     # tách các câu ra 
    listRes = sent_tokenize(content_string_one)
    
#     # đưa về chữ thường
    testlower = list(map(lambda x: x.lower(), listRes))
  

#     # phân đoạn tách các từ
    Segmentation=[]
    for sentences10 in testlower:
        # print(sentences10)
        content_process = word_tokenize(sentences10,format="text")
        phanDoan=content_process
        Segmentation.append(phanDoan)
    

#     # gôm lại thành 1 list
    content_string_two = ' '.join(Segmentation)  
    final = text_preprocess(content_string_two)
    return final


# openfile = r"C:\Users\Admin\Downloads\Share-20220913T071719Z-001\Share\Share\TrinhMinhKiemTraDoTuongDongVanBan\KiemTra\test1\A-CN\01-CN-BUI LE ANH TUAN(1-7)062.txt"
# f = fileWordTokenize(openfile)
# print(f)

# test_file = "file_SoSanh/"
# student = [doc for doc in os.listdir(test_file) if (doc.endswith('.docx') )]
# test =  docx2txt.process(test_file+student[0])
# f=fileWordTokenize1(test)[0]
# abc = text_preprocess(test)
# print(abc)

def fileWordTokenize_tiengviet(fileName):
    list_string = fileName.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa


    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'ABSTRACT'
            
   
    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT' :
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra và xử lý và lấy ra tiêu đề
    # title_index_listUpper = listUpper.index('TÓM TẮT')
    # if title_index_listUpper == 2:
    #     get_title = listWord[0]
    # elif title_index_listUpper == 4:
    #     title_list = listUpper[0:3]
    #     get_title = ' '.join(title_list)
    # else:
    #     title_list = listUpper[0:2]
    #     get_title = ' '.join(title_list)

    # title = get_title  # Lấy ra tên tiêu đề bài báo
    # End lấy ra và xử lý tiêu đề

    # Begin Lấy nội dung từ Giới thiệu đến Kết luận
    # tomtat_listUpper = listUpper.index('TÓM TẮT')
    # gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    gioiThieu = listWord.index('ABSTRACT')

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]

    # Begin Kết hợp từ Giới thiệu đến Kết luận
    contentJoin = ' '.join(content)  # Ghép lại thành 1 text duy nhất từ list
    contentSplit = contentJoin.split(' ')
    # End Kết hợp từ Giới thiệu đến Kết luận

    # Begin Xóa đi số và công thức
    content_math = []
    for w in contentSplit:
        re_w_one = re.sub(
            r'[\d,():=/.^°\-_¬∧∨∃∅&@+%;■*Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ ̂>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×\'‖┬∏ε¯⁻−↔ξ⊂μ⋯δïф∇∙∫ϱ↦∞ωψ∞∆∬σ″²⟦⟧∙∂≠≔⋅ζ ⁄ç•≮∉\⇔∃ º⌉⌈〉〈□]', ' ', w)
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', re_w_one)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            content_math.append(re_w_two)
    # End Xóa đi số và công thức

    # Begin loại bỏ tiếp các phần còn thừa
    content_string_two = ' '.join(content_math)
    word_split = content_string_two.split(' ')
    listWord_split = []
    for word in word_split:
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', word)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            listWord_split.append(word)
    # End loại bỏ tiếp các phần còn thừa

    # Begin Đưa hết về lower
    content_string_three = ' '.join(filter(str.isalpha, listWord_split))
    content_lower = content_string_three.lower()
    # End Đưa hết về lower

    # Begin tách từ
    content_process = word_tokenize(content_lower, format="text")
    content_process_split = content_process.split(' ')
    # End tách từ

    # Begin Xóa Stopword
    # stopwords = open("./data/stopword/stopwords.txt",
    #                  "r+", encoding="utf-8")
    # stopwords_read = stopwords.read()
    # stopwords_split = stopwords_read.split('\n')
    # content_stopword = []
    # for n in content_process_split:
    #     if n in stopwords_split:
    #         pass
    #     else:
    #         content_stopword.append(n)
    # End Xóa Stopword

    # Begin Final content
    contentFinal = ' '.join(content_process_split)
    # End Final content
    return  contentFinal

def fileWordTokenize3(fileName):
    print(fileName)
    list_string = fileName.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa


    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'ABSTRACT'
            
   
    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT' :
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra và xử lý và lấy ra tiêu đề
    # title_index_listUpper = listUpper.index('TÓM TẮT')
    # if title_index_listUpper == 2:
    #     get_title = listWord[0]
    # elif title_index_listUpper == 4:
    #     title_list = listUpper[0:3]
    #     get_title = ' '.join(title_list)
    # else:
    #     title_list = listUpper[0:2]
    #     get_title = ' '.join(title_list)

    # title = get_title  # Lấy ra tên tiêu đề bài báo
    # End lấy ra và xử lý tiêu đề

    # Begin Lấy nội dung từ Giới thiệu đến Kết luận
    # tomtat_listUpper = listUpper.index('TÓM TẮT')
    # gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    gioiThieu = listWord.index('ABSTRACT')

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]

    # Begin Kết hợp từ Giới thiệu đến Kết luận
    contentJoin = ' '.join(content)  # Ghép lại thành 1 text duy nhất từ list
    contentSplit = contentJoin.split(' ')
    # End Kết hợp từ Giới thiệu đến Kết luận

    # Begin Xóa đi số và công thức
    content_math = []
    for w in contentSplit:
        re_w_one = re.sub(
            r'[\d,():=/.^°\-_¬∧∨∃∅&@+%;■*Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ ̂>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×\'‖┬∏ε¯⁻−↔ξ⊂μ⋯δïф∇∙∫ϱ↦∞ωψ∞∆∬σ″²⟦⟧∙∂≠≔⋅ζ ⁄ç•≮∉\⇔∃ º⌉⌈〉〈□]', ' ', w)
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', re_w_one)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            content_math.append(re_w_two)
    # End Xóa đi số và công thức

    # Begin loại bỏ tiếp các phần còn thừa
    content_string_two = ' '.join(content_math)
    word_split = content_string_two.split(' ')
    listWord_split = []
    for word in word_split:
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', word)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            listWord_split.append(word)
    # End loại bỏ tiếp các phần còn thừa

    # Begin Đưa hết về lower
    content_string_three = ' '.join(filter(str.isalpha, listWord_split))
    content_lower = content_string_three.lower()
    # End Đưa hết về lower

    # Begin tách từ
    
    content_process = word_tokenize(content_lower, format="text")
    print('content_process')
    print(content_process)
    content_process_split = content_process.split(' ')
    print('content_process_split')
    print(content_process_split)
    # End tách từ

    # Begin Xóa Stopword
    # stopwords = open("./data/stopword/stopwords.txt",
    #                  "r+", encoding="utf-8")
    # stopwords_read = stopwords.read()
    # stopwords_split = stopwords_read.split('\n')
    # content_stopword = []
    # for n in content_process_split:
    #     if n in stopwords_split:
    #         pass
    #     else:
    #         content_stopword.append(n)
    # End Xóa Stopword

    # Begin Final content
    contentFinal = ' '.join(content_process_split)
    print('contentFinal')
    print(contentFinal)
    # End Final content
    return  contentFinal

def fileWordTokenize0(fileName):
    list_string = fileName.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa


    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'TÓM TẮT'
            
   
    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT' :
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra và xử lý và lấy ra tiêu đề
    # title_index_listUpper = listUpper.index('TÓM TẮT')
    # if title_index_listUpper == 2:
    #     get_title = listWord[0]
    # elif title_index_listUpper == 4:
    #     title_list = listUpper[0:3]
    #     get_title = ' '.join(title_list)
    # else:
    #     title_list = listUpper[0:2]
    #     get_title = ' '.join(title_list)

    # title = get_title  # Lấy ra tên tiêu đề bài báo
    # End lấy ra và xử lý tiêu đề

    # Begin Lấy nội dung từ Giới thiệu đến Kết luận
    # tomtat_listUpper = listUpper.index('TÓM TẮT')
    # gioithieu_listUpper = listUpper[tomtat_listUpper + 1]
    gioiThieu = listWord.index('TÓM TẮT')

    # Lấy ra tài liệu tham khảo nếu ko có LCT
    if flag == 1:
        content = listWord[gioiThieu:]
    else:
        tailieu_listUpper = listUpper[len(listUpper) - 1]
        tailieu = listWord.index(tailieu_listUpper)
        content = listWord[gioiThieu:tailieu]

    # Begin Kết hợp từ Giới thiệu đến Kết luận
    contentJoin = ' '.join(content)  # Ghép lại thành 1 text duy nhất từ list
    contentSplit = contentJoin.split(' ')
    # End Kết hợp từ Giới thiệu đến Kết luận

    # Begin Xóa đi số và công thức
    content_math = []
    for w in contentSplit:
        re_w_one = re.sub(
            r'[\d,():=/.^°\-_¬∧∨∃∅&@+%;■*Ωλπω∈βαηρ〖〗⃗\[\]⁡{}∑▒█φθ ̂>γ&#@<!?~`´⊆<=>±→∅–"┤├│∀≤≥|√ŷ∩∪×\'‖┬∏ε¯⁻−↔ξ⊂μ⋯δïф∇∙∫ϱ↦∞ωψ∞∆∬σ″²⟦⟧∙∂≠≔⋅ζ ⁄ç•≮∉\⇔∃ º⌉⌈〉〈□]', ' ', w)
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', re_w_one)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            content_math.append(re_w_two)
    # End Xóa đi số và công thức

    # Begin loại bỏ tiếp các phần còn thừa
    content_string_two = ' '.join(content_math)
    word_split = content_string_two.split(' ')
    listWord_split = []
    for word in word_split:
        re_w_two = re.sub(r'(m)s|\_\w+|sin|cos|khz|^\s+$', '', word)
        if re_w_two == '' or re_w_two == ' ' or len(re_w_two) <= 2:
            pass
        else:
            listWord_split.append(word)
    # End loại bỏ tiếp các phần còn thừa

    # Begin Đưa hết về lower
    content_string_three = ' '.join(filter(str.isalpha, listWord_split))
    content_lower = content_string_three.lower()
    # End Đưa hết về lower

    # Begin tách từ
    content_process = word_tokenize(content_lower, format="text")
    content_process_split = content_process.split(' ')
    # End tách từ

    # Begin Xóa Stopword
    # stopwords = open("./data/stopword/stopwords.txt",
    #                  "r+", encoding="utf-8")
    # stopwords_read = stopwords.read()
    # stopwords_split = stopwords_read.split('\n')
    # content_stopword = []
    # for n in content_process_split:
    #     if n in stopwords_split:
    #         pass
    #     else:
    #         content_stopword.append(n)
    # End Xóa Stopword

    # Begin Final content
    contentFinal = ' '.join(content_process_split)
    # End Final content
    return  contentFinal

# Tuyet bo sung tach title, tach abstract
# Begin lấy ra và xử lý và lấy ra tiêu đề
def tach_title(filename):
    
    # Tách nội dung File theo từng dòng vô list
    list_string = filename.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa

    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'TÓM TẮT'

    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])
            vietHoa=listUpper

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT':
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra và xử lý và lấy ra tiêu đề
        get_title = listWord[1]
    # End lấy ra và xử lý tiêu đề
    return get_title

# End lấy ra và xử lý tiêu đề

# Begin lấy ra abstract (tieng Anh)
def tach_abstract(filename):
    # Tách nội dung File theo từng dòng vô list
    list_string = filename.split('\n')
    listWord = []  # Đưa vào list mới sau khi xử lý xóa các kí tự không cần thiết và bỏ DOI
    listUpper = []  # Lấy ra những tiêu đề viết hoa

    for sen1 in range(len(list_string)):
        if list_string[sen1] == 'TRỪU TƯỢNG':
            list_string[sen1] = 'TÓM TẮT'

    # Đọc từng câu trong list ban đầu và xóa 1 vài chỗ ko cần thiết, cho vào listW
    for sen in list_string:
        subText = re.sub(r'\t|^\s+|\s+$|\ufeff', '', sen)
        i = subText
        if i == '' or 'DOI:' in i:
            pass
        else:
            listWord.append(i)

    # Begin Lấy ra lời cảm tạ thì xóa từ đó trở xuống
    flag = 0  # Mark nếu = 1 là có LCT và đã xóa rồi, xóa bao gồm TLTK
    for index, value in enumerate(listWord):
        if value == 'LỜI CẢM TẠ' or value == 'LỜI CẢM ƠN':
            indexLCT = index
            del listWord[indexLCT:]
            flag = 1
    # End Lấy ra index tài liệu tham khảo và xóa từ đó trở xuống

   # Begin Kiểm tra đề mục nào viết hóa thì đưa vào listUpper
    for senW in range(len(listWord)):
        if listWord[senW].isupper():
            listUpper.append(listWord[senW])
            vietHoa=listUpper

    for senU in range(len(listUpper)):
        if listUpper[senU] == 'TÓM TẮT':
            listUpper[senU] = 'TÓM TẮT'
    # End Kiểm tra đề mục nào viết hóa thì đưa vào listUpper

    # Begin lấy ra tom tat (tieng Viet)
    # index_tomtat = listWord.index('TÓM TẮT')
    # get_content_tomtat = listWord[index_tomtat + 1]
    # get_tomtat = get_content_tomtat
    # return get_tomtat
    # End lấy ra tom tat (tieng Viet)

    # Begin lấy ra abstract (tieng Anh, file tieng Viet)

    index_abstract = listWord.index('ABSTRACT')
    get_content_abstract = listWord[index_abstract + 1]
    get_abstract = get_content_abstract
    return get_abstract

    # End lấy ra abstract (tieng Anh, file tieng Viet)


    # Begin lấy ra abstract (tieng Anh, file tieng Anh)
    
    # index_abstract_en = listWord.index('ABSTRACT')
    # get_content_abstract_en = listWord[index_abstract_en + 3]
    # if len(get_content_abstract_en) <= 30:
    #     get_content_abstract_en = listWord[index_abstract_en + 4]
    # get_abstract_en = get_content_abstract_en
    # return get_abstract_en

    # # End lấy ra abstract (tieng Anh, file tieng Anh)


    





