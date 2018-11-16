import sys



print ('HEO=LLO')
output=sys.stdout

outputfile=open("printlog.txt","a")
sys.stdout=outputfile
print ('HEO=LLO2')

print ('HEO=LLO3')