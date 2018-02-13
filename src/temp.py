#python

import numpy as np
import pandas as pd
import sys, os, datetime

#Only needs to be run once at beginning
def file_struct(input1, input2, outputfile):
   #To check if input files present and returns error if not present
   if os.path.isfile(input1)==False:
      warning = "No Input File Detected in :" + input1 + ". Exiting."
      print(warning)
      exit()


   if os.path.isfile(input2) == False:
      warning = "No Input File Deteccted in :" + input2 + ". Exiting."
      print(warning)
      exit()



   if os.path.isfile(outputfile)==False:
      file = open(outputfile,'w')
      file.close()

def val_date(idate):
   idate_str=str(idate)
   try:
      dt=datetime.datetime.strptime(idate_str,  '%m%d%Y')
      return(dt.year)
   except ValueError:
      return(-1)

def val_zip(inzip):
   zip_str=str(inzip)
   if (len(zip_str) == 9): #9 digit format
      return(zip_str[:5])
   elif (len(zip_str) == 5):
      return(zip_str)
   else:
      return(-1) #Returns -1 if zip is not valid

def donate_analysis(in1, in2, output2):
   #file pathways
   mdir = os.path.dirname(os.path.realpath("file"))
   input1 = os.path.abspath(os.path.realpath(os.path.join(mdir,in1)))
   in2file = os.path.abspath(os.path.realpath(os.path.join(mdir, in2)))
   outputfile = os.path.abspath(os.path.realpath(os.path.join(mdir, output2)))
   
   #file structure
   file_struct(input1,in2file,outputfile)
   #Check for Databank variable
   file_header = ['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT','TRANSACTION_AMT']
   if ('DataBank' in vars()) == False:
      DataBank = pd.DataFrame(columns=file_header)
      DataBank.TRANSACTION_AMT=DataBank.TRANSACTION_AMT.astype(float)
   
   header_1 = ["CMTE_ID","AMNDT_IND","RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP","ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER","OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID","TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID"]
   orgdata = pd.read_csv(input1, sep="|", header = None, names = header_1,converters={'TRANSACTION_DT': lambda x: str(x),'ZIP_CODE': lambda x: str(x)})
   
   header_2 = ["percentile"]
   perc = pd.read_csv(in2file, names=header_2,converters={'percentile': lambda x: int(x)})
   
   #ignore values based on condition
   if (any(pd.isnull(orgdata.OTHER_ID)==False)):
      orgdata=orgdata[pd.isnull(orgdata.OTHER_ID)].reset_index(drop=True)
   
   if (any(pd.isnull(orgdata.CMTE_ID))):
      orgdata=orgdata[pd.isnull(orgdata.CMTE_ID)==False].reset_index(drop=True)
   
   if (any(pd.isnull(orgdata.TRANSACTION_AMT))):
      orgdata=orgdata[pd.isnull(orgdata.TRANSACTION_AMT)==False].reset_index(drop=True)
   
   if (any(pd.isnull(orgdata.NAME))):
      orgdata = orgdata[pd.isnull(orgdata.NAME) == False].reset_index(drop=True)
   print (DataBank)
   
   
   #Loop for required output
   for x in range(len(orgdata)):
      
      new_zip = val_zip(orgdata.ZIP_CODE[x])
      new_name = orgdata.NAME[x]
      new_CMTE_ID = orgdata.CMTE_ID[x]
      new_year = val_date(orgdata.TRANSACTION_DT[x])
      new_per =perc.iloc[0]['percentile']
      
      #Append databank
      
      DataBank = DataBank.append(pd.DataFrame([[new_CMTE_ID,new_name,new_zip,new_year,orgdata.TRANSACTION_AMT[x]]],columns=file_header),ignore_index=True)
      print(DataBank)
      if int(new_zip)>0: #Check for valid zip code
         
         zipvalue = DataBank.TRANSACTION_AMT[(DataBank.CMTE_ID==new_CMTE_ID) & (DataBank.ZIP_CODE==new_zip) & (DataBank.TRANSACTION_DT==2018)]
         
         if new_year==2018:
            zipvalue_sort = zipvalue.sort_values()
            percent = zipvalue_sort.quantile(new_per/100,interpolation='nearest')
            index_zip = len(zipvalue_sort)
            total_zip = np.sum(zipvalue_sort)
         
        #append data
         if new_year==2018:
            out1 = open(outputfile,"a")
            out1.write(new_CMTE_ID + '|' + str(new_zip) + '|' + str(new_year) + '|' + str(int(percent) ) + '|' + str(int(total_zip)) + '|' + str(index_zip) + '\n')
            out1.close()


if __name__== "__main__":
   donate_analysis(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))