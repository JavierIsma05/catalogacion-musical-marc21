from bs4 import BeautifulSoup
import re

with open('debug_form_response.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

print("CAMPOS CON ERRORES (aria-invalid=true):\n")
campos_invalidos = soup.find_all(attrs={'aria-invalid': 'true'})
for campo in campos_invalidos[:10]:
    name = campo.get('name', 'SIN NOMBRE')
    field_type = campo.name
    print(f"  • <{field_type} name='{name}'>")

print(f"\n\nTOTAL: {len(campos_invalidos)} campos con errores")
