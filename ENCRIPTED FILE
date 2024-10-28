import base64
with open("guibotdc.py", "r") as f:
    codigo = f.read()
codigo_base64 = base64.b64encode(codigo.encode("utf-8")).decode("utf-8")
with open("guibotdc_codificado.py", "w") as f:
    f.write(f'import base64, exec\nexec(base64.b64decode("{codigo_base64}").decode("utf-8"))')

