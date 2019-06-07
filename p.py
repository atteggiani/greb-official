% plots
my_colormap
clev  =  0:0.05:1.;
clev2 = 0.1*(-1.05:0.1:1.05);
clev3 = 5*(-1.05:0.1:1.05);

% clouds
figure(1); clf
subplot(2,2,1)
contourf(cld_old,clev)
caxis([clev(1) clev(21)]); grid on; colorbar
title('cloud cover original')
subplot(2,2,2)
contourf(cld_new,clev)
caxis([clev(1) clev(21)]); grid on; colorbar
title('cloud cover 1st correction')
subplot(2,2,3)
contourf(cld_new-cld_old,clev2)
caxis([clev2(1) clev2(21)]); grid on; colorbar
title('diff. [1st] - [org]')

%  Tsurf and cloud corrections
figure(2); clf
my_colormap
subplot(2,2,1)
contourf(ts_old-ts_c,clev3)
caxis([clev3(1) clev3(21)]); grid on; colorbar
title('Tsurf response 2xCO2')
subplot(2,2,2)
contourf(ts_new-ts_c,clev3)
caxis([clev3(1) clev3(21)]); grid on; colorbar
title('Tsurf response 2xCO2 & cld-1')
subplot(2,2,3)
contourf(NEW_CLD-cld_new,clev2)
caxis([clev2(1) clev2(21)]); grid on; colorbar
title('diff. [davide]-[1st]')
subplot(2,2,4)
contourf(dcld_new,clev2)
caxis([clev2(1) clev2(21)]); grid on; colorbar
title('diff. [dietmar]-[1st]')



%  cloud sensitivity
figure(3); clf
my_colormap
subplot(2,2,1)
contourf(dCLD,clev2)
caxis([clev2(1) clev2(21)]); grid on; colorbar
title('changes in Ccloud cover')
subplot(2,2,2)
contourf(dT,clev3)
caxis([clev3(1) clev3(21)]); grid on; colorbar
title('changes in Tsurf')
subplot(2,2,3)
contourf(r_cld,clev2)
caxis([clev2(1) clev2(21)]); grid on; colorbar
title('cloud sensitivity (inverse)')
