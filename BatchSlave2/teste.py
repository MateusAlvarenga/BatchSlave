print("CHECAGENS")

repetir = True

while(repetir):
    try:   
        svdoi70_total = float(input("Svdoi70 Total:").replace(' ','').replace(',','.'))
        svdoi70_devolucoes = float(input("Svdoi70 Devolucoes:").replace(' ','').replace(',','.'))
        sasoi60 = sas24 = sas08 = float(input("Sasoi60:").replace(' ','').replace(',','.'))
        subtotal = svdoi70_total - svdoi70_devolucoes
        srtbi01 = subtotal + sasoi60
        repetir = False
    except ValueError:
        print('Valor inserido invalido tente algo assim: 12345.67 ')

print('\n')
print('svdoi70_total:',svdoi70_total)
print('svdoi70_devolucoes:',svdoi70_devolucoes)
print('sasoi60:',sasoi60)
print('sas24 esperado:',sas24)
print('sas08 esperado:',sas08)
print('subtotal:',subtotal)
print('srtbi01 esperado:',srtbi01)