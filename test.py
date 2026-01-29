cash = 508

sto = int (cash/100)
pjtdesat = int (cash % 100 / 50)
desat = int(((cash % 100) - (pjtdesat * 50))/10)
pjat = int((((cash % 100) - (pjtdesat * 50))%10)/5)
odin = (((cash % 100) - (pjtdesat * 50))%10) - (pjat*5)

print(f'сто:{sto},пятьдесят: {pjtdesat}, десять: {desat}, пять: {pjat}, один: {odin}')

