import datetime
import calendar

# Obtendo o mês atual
mes_atual_numero = datetime.datetime.now().month
mes_atual_nome = calendar.month_name[mes_atual_numero]

print(mes_atual_numero)
print("O mês atual é:", mes_atual_nome)
