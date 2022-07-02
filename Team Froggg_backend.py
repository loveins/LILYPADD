

####################################

#Finding the date from the file
import re
# open the text file and read the data
def get_date(file):
    fi = open(file,'r')

    text = fi.read()
    # match a regex pattern for formatted dates
    matches = re.findall(r'(\d+-\d+-\d+)',text)
    fi.close()
    return matches[0]

#################################

#Invoices

##################################
def get_inv_num(filename):
    number = ''
    criteria1 = False
    criteria2 = False
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            for word in columns:
                if word.lower() in ['inv','invoice']:
                    criteria1 = True
                elif word.lower() in ['no','number', 'no.']:
                    criteria2 = True
                if criteria1 and criteria2:
                    if word.isalnum() and not word.isalpha():
                        number = word
                        criteria1 = False
                        criteria2 = False
    return number  
###########################################################
def get_recipient(filename):
    recipient = ''
    criteria = False
    target_words = ['attention:','attention']
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            for word in columns:
                if word.lower() in target_words:
                    criteria = True 
                if criteria and word.lower() not in target_words:
                    recipient += word
                    recipient += " "
            criteria = False
    return recipient[:-1]                
##############################################################
def get_sender(filename):
    sender = ''
    criteria = False
    target_words = ['by']
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            for word in columns:
                if word.lower() in target_words:
                    criteria = True 
                if criteria and word.lower() not in target_words:
                    sender += word
                    sender += " "
            criteria = False
    return sender[:-1] 
#############################################################

#Consolidating the structured document description for invoice

def get_inv_des(filename):
    date = get_date(filename)
    number = get_inv_num(filename)
    recipient = get_recipient(filename)
    sender = get_sender(filename)
    inv_des = f"{date}_Invoice No {number} from {sender}to {recipient}"
    print(inv_des)
############################################################

#Emails

#####################################################
def get_email_des(filename):
    sender = ''
    recipient = ''
    subject = ''
    attachment = ''
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            if 'From' in columns:
                for word in columns:
                    if '@' in word:
                        sender = word
            if 'To' in columns:
                for word in columns:
                    if '@' in word:
                        recipient = word

            if 'Subject' in columns:
                for i in range(2,len(columns)):
                    subject += columns[i]
                    subject += " "
                subject = subject[:-1]

            if 'Attachment' in columns:
                for i in range(2,len(columns)):
                    attachment += columns[i]
                    attachment += " "
                attachment = attachment[:-1]
    date = get_date(filename)
    email_des = f"{date}_Email from {sender} to {recipient} Re {subject} |{attachment}"
    print(email_des)
####################################################

#Bank Statements

########################################
def get_bank_name(filename):
    bank_name = ""
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            if "Bank" in columns or "bank" in columns:
                bank_name = " ".join(columns)
                break
    return bank_name
################################################
def get_customer_name(filename):
    customer_name = ""
    criteria = False
    with open(filename,'r') as fi:
        for line in fi:
            line = line.rstrip("\n")
            columns = line.split(" ")
            for word in columns:
                if word.lower() in ["mr",'ms','mrs','madam']:
                    criteria = True
                if criteria:
                    customer_name += word
                    customer_name += " " 
    return customer_name[:-1]
#############################################

#Consolidating the structured document description for bank statements

def get_bank_acc(filename):
    date = get_date(filename)
    bank_name = get_bank_name(filename)
    customer_name = get_customer_name(filename)
    bank_desc = f"{date}_Bank Statement from {bank_name} to {customer_name}"
    print(bank_desc)

#############################################

#Differentiating between the documents#
def differentiate_file(file1):
    with open(file1, "r") as fi:
    
        for line in fi:
            line = line.rstrip('\n')
            line = line.lower()
            columns = line.split(" ")
            if 'invoice' in columns:
                get_inv_des(file1)
                break 
            elif '@' in columns and '.com' in columns:
                get_email_des(file1)
                break
            elif 'account' in columns:
                get_bank_acc(file1)
                break        
##########################################
#Testing 

#differentiate_file('invoice3.txt')