program  greb_shell

! initialisation of the greb model

USE mo_numerics
USE mo_physics

print*,'% start climate shell'

! open input files
open(10,file='namelist')

! read namelist
read(10,numerics)
read(10,physics)

if ( log_clim .eq. 0 ) then ! ERA-Interim
  open(11,file='base_dir/input/erainterim.tsurf.1979-2015.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(12,file='base_dir/input/erainterim.zonal_wind.850hpa.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(13,file='base_dir/input/erainterim.meridional_wind.850hpa.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(14,file='base_dir/input/erainterim.atmospheric_humidity.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(15,file='base_dir/input/isccp.cloud_cover.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(16,file='base_dir/input/ncep.soil_moisture.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(17,file='base_dir/input/Tocean.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(18,file='base_dir/input/woce.ocean_mixed_layer_depth.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(19,file='base_dir/input/global.topography.bin',& 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(20,file='base_dir/input/greb.glaciers.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(21,file='base_dir/input/solar_radiation.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*ydim*nstep_yr)
  open(22,file='base_dir/input/erainterim.windspeed.850hpa.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(23,file='base_dir/input/erainterim.omega.vertmean.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(24,file='base_dir/input/erainterim.omega_std.vertmean.clim.bin', &
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
else if ( log_clim .eq. 1 ) then ! NCEP
  open(11,file='base_dir/input/ncep.tsurf.1948-2007.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(12,file='base_dir/input/ncep.zonal_wind.850hpa.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(13,file='base_dir/input/ncep.meridional_wind.850hpa.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(14,file='base_dir/input/ncep.atmospheric_humidity.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(15,file='base_dir/input/isccp.cloud_cover.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(16,file='base_dir/input/ncep.soil_moisture.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(17,file='base_dir/input/Tocean.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(18,file='base_dir/input/woce.ocean_mixed_layer_depth.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(19,file='base_dir/input/global.topography.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(20,file='base_dir/input/greb.glaciers.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(21,file='base_dir/input/solar_radiation.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*ydim*nstep_yr)
  open(22,file='base_dir/input/erainterim.windspeed.850hpa.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(23,file='base_dir/input/ncep.omega.vertmean.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(24,file='base_dir/input/ncep.omega_std.vertmean.clim.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
end if

! read climatologies
do n=1,nstep_yr
   read(11,rec=n) tclim(:,:,n)
   read(12,rec=n) uclim(:,:,n)
   read(13,rec=n) vclim(:,:,n)
   read(14,rec=n) qclim(:,:,n)
   read(15,rec=n) cldclim(:,:,n)
   read(16,rec=n) swetclim(:,:,n)
   read(17,rec=n) Toclim(:,:,n)
   read(18,rec=n) mldclim(:,:,n)
   read(22,rec=n) wsclim(:,:,n)
   read(23,rec=n) omegaclim(:,:,n)
   read(24,rec=n) omegastdclim(:,:,n)
end do

! read fix data
read(19,rec=1)  z_topo
read(20,rec=1)  glacier
read(21,rec=1)  sw_solar_ctrl

! read scenario solar forcing for paleo scenarios or oribital forcings
if ( log_exp .eq. 30 .or. log_exp .eq. 31 .or. log_exp .eq. 35 .or. log_exp .eq. 36 ) then
    open(25,file='solar_scenario', ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*ydim*nstep_yr)
    read(25,rec=1)  sw_solar_scnr
end if

! open CO2 forcing file for IPCC RCP scenarios (CO2 is read in forcing subroutine)
if ( log_exp .ge. 96 .and. log_exp .le. 100 ) then
    open(26,file='co2forcing')
end if

! open external forcing for climate change (ensemble mean) (it is read in forcing subroutine)
if ( log_exp .eq. 230 ) then
  open(31,file='base_dir/input/cmip5.tsurf.rcp85.ensmean.forcing.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(32,file='base_dir/input/cmip5.zonal.wind.rcp85.ensmean.forcing.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(33,file='base_dir/input/cmip5.meridional.wind.rcp85.ensmean.forcing.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(34,file='base_dir/input/cmip5.omega.rcp85.ensmean.forcing.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  open(35,file='base_dir/input/cmip5.windspeed.rcp85.ensmean.forcing.bin', & 
  & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  do i=1,nstep_yr ! Read in the anomalies
    if (log_tsurf_ext .eq. 1) read(31,rec=i) Tclim_anom_cc(:,:,i)
    if (log_hwind_ext .eq. 1) read(32,rec=i) uclim_anom_cc(:,:,i)
    if (log_hwind_ext .eq. 1) read(33,rec=i) vclim_anom_cc(:,:,i)
    if (log_omega_ext .eq. 1) read(34,rec=i) omegaclim_anom_cc(:,:,i)
    if (log_hwind_ext .eq. 1) read(35,rec=i) wsclim_anom_cc(:,:,i)
  end do
end if

! ENSO forcing
if ( log_exp .eq. 240 .or. log_exp .eq. 241 ) then
  ! open external forcing for El Nino (era-interim composite mean) (it is read in forcing subroutine)
  if ( log_exp .eq. 240 ) then
    open(41,file='base_dir/input/erainterim.tsurf.elnino.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(42,file='base_dir/input/erainterim.zonal.wind.elnino.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(43,file='base_dir/input/erainterim.meridional.wind.elnino.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(44,file='base_dir/input/erainterim.omega.elnino.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(45,file='base_dir/input/erainterim.windspeed.elnino.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  ! open external forcing for La Nina (era-interim composite mean) (it is read in forcing subroutine)
  else if ( log_exp .eq. 241 ) then
    open(41,file='base_dir/input/erainterim.tsurf.lanina.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(42,file='base_dir/input/erainterim.zonal.wind.lanina.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(43,file='base_dir/input/erainterim.meridional.wind.lanina.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(44,file='base_dir/input/erainterim.omega.lanina.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    open(45,file='base_dir/input/erainterim.windspeed.lanina.forcing.bin', & 
    & ACCESS='DIRECT',FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
  end if
  do i=1,nstep_yr ! Read in the anomalies
    if (log_tsurf_ext .eq. 1) read(41,rec=i) Tclim_anom_enso(:,:,i)
    if (log_hwind_ext .eq. 1) read(42,rec=i) uclim_anom_enso(:,:,i)
    if (log_hwind_ext .eq. 1) read(43,rec=i) vclim_anom_enso(:,:,i)
    if (log_omega_ext .eq. 1) read(44,rec=i) omegaclim_anom_enso(:,:,i)
    if (log_hwind_ext .eq. 1) read(45,rec=i) wsclim_anom_enso(:,:,i)
  end do
end if ! ENSO forcing

! Geo-engineering forcing with artificial clouds
if ( log_exp .eq. 930 ) then
    open(27, file='cldart', ACCESS='DIRECT', FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    do n=1,nstep_yr
        read(27,rec=n) cldclim_artificial(:,:,n)
    end do
end if

! Geo-engineering forcing with artificial solar radiation
if ( log_exp .ge. 931 .and. log_exp .le. 933 ) then
    open(28, file='swart', ACCESS='DIRECT', FORM='UNFORMATTED', RECL=ireal*xdim*ydim)
    do n=1,nstep_yr
        read(28,rec=n) sw_solar_artificial(:,:,n)
    end do
end if

! start greb_model run
print*,'% time flux/control/scenario: ', time_flux, time_ctrl, time_scnr
call greb_model

end program greb_shell
