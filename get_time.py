import datetime

# Retorna a data e hora atual, formatados de acordo com a documentação
def get_time():
    timestamp = datetime.datetime.now()
    time_formatted = timestamp.strftime("%H:%M:%S %d/%m/%Y")
    return time_formatted