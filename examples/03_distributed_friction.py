from contactimpactbench import distributed_friction,friction_ellipsoid,drilling_arm
alpha=0.0;q=1.0
print('N3.6 prescribed pressure, chi/a:',drilling_arm(alpha))
print('Distributed:',distributed_friction(q,alpha))
print('Ellipsoid:  ',friction_ellipsoid(q,alpha))
