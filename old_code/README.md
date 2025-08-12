
```python
# Como os parâmetros devem ser inseridos
mobile = PCA(
    "PCA-MOBILE-2D",    
    "mobile_devices.csv", 
    1.0,
    ['price_range'],
    2,
    'png',
    ""
)

# Para rodar o algoritmo, você deve rodar a função "run()" do mesmo.
mobile.run() 

# Isso é para caso você queira ver o tempo de processamento e a variância total do processo de redução 
print(f"Tempo de processamento: {mobile.tempo}")
print(f"Variância total: {mobile.variancia}")
```