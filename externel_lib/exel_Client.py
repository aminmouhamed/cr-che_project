import xlsxwriter
import pandas as pd
def Import(file_name) :
    data_list = []
    data = pd.read_excel(f'{file_name}.xlsx')
    client_parent_name = data["client parent name"].values.tolist()
    client_Child_name = data["client parent name"].values.tolist()
    client_phone = data["client phone"].values.tolist()
    client_national_id = data["client national id"].values.tolist()
    pay_prise_of_subscription = data["pay prise of subscription"].values.tolist()
    for i in range(len(client_parent_name)) :
        data_list.append([client_parent_name[i] , client_Child_name[i] ,client_phone[i] ,client_national_id[i] ,pay_prise_of_subscription[i]])
    return data_list
DECT = {
    1 : 'A',
    2 : 'B',
    3 : 'C',
    4 : 'D',
    5 : 'E'
}
class  Export :
    def __init__(self , file_name):
        self.workbook = xlsxwriter.Workbook(f'{file_name}.xlsx')
        self.worksheet = self.workbook.add_worksheet()
    def add_data(self,x,y , data):
        self.worksheet.write(f'{DECT[x]}{y}', data)
    def close_file(self):
        self.workbook.close()

def main():
    file = Export('test')
    file.add_data(1,1,"test")
    file.close_file()
if __name__ == '__main__':
    Import()