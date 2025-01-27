"""
End-to-end test 1

The most basic test.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from os import chdir
from astropy import units as u

import VSPEC

chdir(Path(__file__).parent)

CFG_PATH = Path(__file__).parent / 'test4.yaml'
FIG_PATH = Path(__file__).parent / 'out.png'
u_flux = u.Unit('W m-2 um-1')
u_time = u.day
u_wl = u.um

def make_fig(data:VSPEC.PhaseAnalyzer):
    fig = plt.figure()
    gs = fig.add_gridspec(2,2)

    therm = fig.add_subplot(gs[0,0])
    im = therm.pcolormesh(
        data.time.to_value(u_time),
        data.wavelength.to_value(u_wl),
        data.thermal.to_value(u_flux)
    )
    fig.colorbar(im,ax=therm,label=f'Flux {data.thermal.unit}')
    therm.set_xlabel(f'Time ({u_time})')
    therm.set_ylabel(f'Wavelength ({u_wl})')

    spec = fig.add_subplot(gs[0,1])
    images = 0
    spec.plot(data.wavelength,1e6*data.spectrum('thermal',images,False)/data.spectrum('total',images,False),c='xkcd:azure',label='True')
    spec.errorbar(data.wavelength,1e6*data.spectrum('thermal',images,True)/data.spectrum('total',images,False),c='xkcd:rose pink',label='Observed',
                    yerr = 1e6*data.spectrum('noise',images,False)/data.spectrum('total',images,False),fmt='o',markersize=6)
    spec.set_ylabel('Flux (ppm)')
    spec.set_xlabel(f'Wavelength ({data.wavelength.unit})')
    spec.legend()

    lc = fig.add_subplot(gs[1,:])
    for i in [0,20,40,80,145]:
        lc.plot(data.time,data.lightcurve('star',i,normalize=0),label=f'{data.wavelength[i]:.1f}')
    lc.set_ylabel('Flux (normalized)')
    lc.set_xlabel(f'Time ({data.time.unit})')
    fig.subplots_adjust(hspace=0.4,wspace=0.4)
    fig.savefig(FIG_PATH,facecolor='w')

def test_run():
    model = VSPEC.ObservationModel.from_yaml(CFG_PATH)
    model.build_planet()
    model.build_spectra()

    data = VSPEC.PhaseAnalyzer(model.directories['all_model'])
    make_fig(data)

if __name__ in '__main__':
    test_run()