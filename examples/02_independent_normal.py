from contactimpactbench import compare_normal
from contactimpactbench.normal import PSI_PA
x=compare_normal(pressure_pa=8*PSI_PA,law='A',dt=2e-6)
print(x['difference'])
