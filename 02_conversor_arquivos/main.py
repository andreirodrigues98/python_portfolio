from json_para_csv import converter_json_csv
from csv_para_txt import converter_csv_txt
from csv_para_json import converter_csv_json
from time import sleep
import os 


def menu():

    sleep(3)
    os.system('cls')
    print('================ MENU ===============')
    print('1 - Converter CSV para TXT')   
    print('2 - Converter CSV para JSON') 
    print('3 - Converter JSON para CSV') 
    print('0 - Sair') 
    
def main():
    while True:

        menu()

        try: 
            opcao = int(input('Digite uma opção do menu: ').strip())

            if opcao < 0 or opcao > 3:
                print('Opção deve ser de 0 a 3.')
                continue
            
        except ValueError:
            print('A opção informada deve ser de 0 a 3.')
            continue
        

        if opcao == 1:
            os.system('cls')
            print('\n========== Converter CSV para TXT ===========') 
            converter_csv_txt()  

        elif opcao == 2:
            os.system('cls')
            print('\n=========== Converter CSV para JSON ============') 
            converter_csv_json()

        elif opcao == 3:
            os.system('cls')
            print('\n=========== Converter JSON para CSV ===========') 
            converter_json_csv()

        elif opcao == 0:
            print('Finalizando o sistema...') 
            break 
        else:
            print('Opção invalida, digite um numero de 0 a 3.')
            continue 


if __name__ == '__main__':
    main()     