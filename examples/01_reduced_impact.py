from contactimpactbench import ReducedCase,run_impact,result_summary
r=run_impact(ReducedCase(spin_rad_s=20.0))
summary=result_summary(r)
print('N3.3: contact time (ms)',summary['contact_time_ms'])
print('N3.3: lateral rebound (m/s)',summary['vy'])
print('N3.3: energy residual (J)',summary['residual_max'])
print('These are reduced-model outputs, not experimentally validated values.')
