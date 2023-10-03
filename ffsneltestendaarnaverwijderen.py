import pandas as pd

data = {'a':['ja1', 'nee', 'wellicht'],
        'b':['ja2', 'nee', 'wellicht'],
        'c':['ja3', 'nee', 'wellicht']}

df = pd.DataFrame(data)
print(df['a'][0][:1],df['a'][0])