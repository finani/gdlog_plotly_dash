import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("gdLog_210323_172626.csv")
df.columns = df.columns.str.strip()

data_range = range(0, 200)
#data_range = range(len(df))

df_rpy = df.loc[data_range,['rosTime','rpy_0','rpy_1','rpy_2']]
df_rpy.plot(x='rosTime')
plt.grid(b=True)
plt.title('[rpy]   '+ str(data_range))
plt.show()

df_velNed = df.loc[data_range,['rosTime','velNed_0','velNed_1','velNed_2']]
df_velNed.plot(x='rosTime')
plt.grid(b=True)
plt.title('[velNed]   '+ str(data_range))
plt.show()

df_posNed = df.loc[data_range,['rosTime','posNed_0','posNed_1','posNed_2']]
df_posNed.plot(x='rosTime')
plt.grid(b=True)
plt.title('[posNed]   '+ str(data_range))
plt.show()

df_accBody = df.loc[data_range,['rosTime','accBody_0','accBody_1','accBody_2']]
df_accBody.plot(x='rosTime')
plt.grid(b=True)
plt.title('[accBody]   '+ str(data_range))
plt.show()

df_pqr = df.loc[data_range,['rosTime','pqr_0','pqr_1','pqr_2']]
df_pqr.plot(x='rosTime')
plt.grid(b=True)
plt.title('[pqr]   '+ str(data_range))
plt.show()
