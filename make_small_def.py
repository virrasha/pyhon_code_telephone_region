import csv

def small_one_def(file_in,file_out):
    #тут склеиваем идущие подряд диапазоны с одим DEF и одним регионом
    with open(file_in,encoding='utf-8-sig') as f_def:
        with open(file_out,"w",encoding='utf-8-sig') as f_out:
            r_def = csv.DictReader(f_def,delimiter=";")
            fieldnames = ["def","from","to","region"]
            out_writer = csv.DictWriter(f_out,delimiter=";",fieldnames=fieldnames)
            out_writer.writeheader()
            first=r_def.__next__()
            old_def=first["АВС/ DEF"]
            old_from_n=first["От"]
            start_from_n=old_from_n
            old_to_n=first["До"]
            start_region_full=first["Территория ГАР"].split('|')
            old_region=start_region_full[len(start_region_full)-1]
            new_row={"def":"","from":"","to":"","region":""}
            for row in r_def: 
                def_next=row["АВС/ DEF"]
                from_n=row["От"]
                to_n=row["До"]
                region_full=row["Территория ГАР"].split('|')
                region=region_full[len(region_full)-1]
                if (def_next==old_def and region==old_region): #совпадает DEF и регион
                    if ((int(old_to_n)+1)==int(from_n)): #диапазон продолжается 
                        old_from_n=from_n
                        old_to_n=to_n
                        continue
                # else write new line
                new_row["def"]=old_def
                new_row["from"]=start_from_n
                new_row["to"]=old_to_n
                new_row["region"]=old_region
                out_writer.writerow(new_row)
                
                start_from_n=from_n #new start number
                old_from_n=from_n #new old number, like a start
                old_to_n=to_n
                old_def=def_next
                old_region=region            
            else:
                new_row["def"]=old_def
                new_row["from"]=start_from_n
                new_row["to"]=old_to_n
                new_row["region"]=old_region
                out_writer.writerow(new_row)

def small_two_def(file_in,file_out):
    with open(file_in,encoding='utf-8-sig') as f_def:
        with open(file_out,"w",encoding='utf-8-sig') as f_out:          
            #тут склеиваем регионы по def - так как если в дырках ничего нет, то чего его сравнивать
            r_def = csv.DictReader(f_def,delimiter=";")
            fieldnames = ["def","from","to","region"]
            out_writer = csv.DictWriter(f_out,delimiter=";",fieldnames=fieldnames)
            out_writer.writeheader()
            first=r_def.__next__()
            old_def=first["def"]
            old_region=first["region"]
            old_from=first["from"]
            start_from=old_from
            old_to=first["to"]
            new_row={"def":"","from":"","to":"","region":""}
            for row in r_def:
                def_next=row["def"]
                region=row["region"]
                from_n=row["from"]
                to_n=row["to"]
                if (def_next==old_def and region==old_region): #совпадает DEF и регион все склеиваем уже вместе с дырками в диапазонах
                    old_from=from_n
                    old_to=to_n
                    continue
                new_row["def"]=old_def
                new_row["from"]=start_from
                new_row["to"]=old_to
                new_row["region"]=old_region
                out_writer.writerow(new_row)
                
                start_from=from_n
                old_from=from_n
                old_to=to_n
                old_def=def_next
                old_region=region            
            else:
                new_row["def"]=old_def
                new_row["from"]=start_from       
                new_row["to"]=old_to
                new_row["region"]=old_region
                out_writer.writerow(new_row)
                    
def small_msk_spb_def(file_in,file_out):
    with open(file_in,encoding='utf-8-sig') as f_def:
        with open(file_out,"w",encoding='utf-8-sig') as f_out:  
            id=0        
            r_def = csv.DictReader(f_def,delimiter=";")
            fieldnames = ["ID","def","from","to","region"]
            out_writer = csv.DictWriter(f_out,delimiter=";",fieldnames=fieldnames)
            out_writer.writeheader()
            for row in r_def:
                row.update({"ID":id})
                id+=1
                if ("800" <= row["def"] <= "809"):#800-809 это общероссийские номера, не региональные.
                    continue
                elif(("Москва" in row["region"]) or ("Московская" in row["region"])):
                    row.update({"region":"Москва"})
                elif (("Санкт-Петербург" in row["region"]) or ("Ленинградская" in row["region"])):
                    row.update({"region":"Город Санкт-Петербург"})
                out_writer.writerow(row)       

def clay_them(file1,file2,file3,file_out):
    with open(file_out,"w",encoding='utf-8-sig') as f_out: 
        fieldnames = ["ID","def","from","to","region"]
        out_writer = csv.DictWriter(f_out,delimiter=";",fieldnames=fieldnames)
        out_writer.writeheader()
        id=0
        with open(file1,encoding='utf-8-sig') as f_read:
            r_def = csv.DictReader(f_read,delimiter=";")
            for row in r_def:
                row.update({"ID":id})
                id+=1
                out_writer.writerow(row)
        with open(file2,encoding='utf-8-sig') as f_read:
            r_def = csv.DictReader(f_read,delimiter=";")
            for row in r_def:
                row.update({"ID":id})
                id+=1
                out_writer.writerow(row)      
        with open(file3,encoding='utf-8-sig') as f_read:
            r_def = csv.DictReader(f_read,delimiter=";")
            for row in r_def:
                row.update({"ID":id})
                id+=1
                out_writer.writerow(row)
#START HERE            
#я их просто по два запускала.

#Оптимизируем номера на 3, тут без сюрпризов.                    
small_one_def("ABC-3xx.csv","smaller-ABC-3xx.csv")
small_two_def("smaller-ABC-3xx.csv","smallest-ABC-3xx.csv")
#Оптимизируем номера на 4, тут есть Москва и мособласть, их нужно будет свести.
small_one_def("ABC-4xx.csv","smaller-ABC-4xx.csv")
small_two_def("smaller-ABC-4xx.csv","smallest-ABC-4xx.csv")
#причесываем Москву и снова оптимизируем.
small_msk_spb_def("smallest-ABC-4xx.csv","smaller-ABC-4xx-msk.csv")
small_two_def("smaller-ABC-4xx-msk.csv","smallest-ABC-4xx-msk.csv")
#Оптимизируем номера на 8. Тут будет Питер и также номера 800-809 общероссийские.
small_one_def("ABC-8xx.csv","smaller-ABC-8xx.csv")
small_two_def("smaller-ABC-8xx.csv","smallest-ABC-8xx.csv")
#причесываем Питер и снова оптимизируем.
small_msk_spb_def("smallest-ABC-8xx.csv","smaller-ABC-8xx-spb.csv")
small_two_def("smaller-ABC-8xx-spb.csv","smallest-ABC-8xx-spb.csv")
#склеиваем три итога
clay_them("smallest-ABC-3xx.csv","smallest-ABC-4xx-msk.csv","smallest-ABC-8xx-spb.csv","def_final_cities.csv")
#А на девятку только одно миниманизирование делаем, не склеиваем диапазоны через дырки
small_one_def("DEF-9xx.csv","smaller-DEF-9xx.csv")
small_msk_spb_def("smaller-DEF-9xx.csv","smallest-DEF-9xx.csv")
#итоговые файлы:
#для города "def_final_cities.csv"
#для мобильников "smallest-DEF-9xx.csv"
