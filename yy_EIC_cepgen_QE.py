
#
# export PYTHONPATH=/afs/cern.ch/user/h/hakhanpo/CEPGEN/cepgen/build:$PYTHONPATH
# export CEPGEN_PATH=/afs/cern.ch/user/h/hakhanpo/CEPGEN/cepgen
# ./build/bin/cepgen lpair_lhec_cfg.py

#  Laurent -- 30 September 2024


import Config.Core as cepgen
from Config.PDG_cfi import PDG
from Config.timer_cfi import timer # enable timing framework
from Config.generator_cfi import generator as _gen
from FormFactors.standardDipole_cfi import standardDipole
from FormFactors.pointLikeFermion_cfi import pointLikeFermion

from OutputModules.rootTree_cfi import rootTree # dump everything into a flat tree


#from Config.PDG_cfi import registerParticle
#registerParticle(6, 'top', mass=174., charge=2./3., fermion=True)


#from Config.PDG_cfi import registerParticle
#registerParticle(15, 'tau', mass=100.0, charge=1.0, fermion=True)


process = cepgen.Module('lpair',
    processParameters = cepgen.Parameters(
#        mode = cepgen.ProcessMode.ElasticElastic,
        mode = cepgen.ProcessMode.InelasticElastic,
#        mode = cepgen.ProcessMode.InelasticInelastic,
#        pair = PDG.tau,   # pair = 13,
         pair = PDG.tau,
    ),
    inKinematics = cepgen.Parameters(
        pdgIds = (2212, 11),
        formFactors = [standardDipole, pointLikeFermion],
        pz = (275.0, 18.0),
#        structureFunctions = cepgen.StructureFunctions.luxLike,
        structureFunctions = cepgen.StructureFunctions.suriYennie,
#        structureFunctions = cepgen.StructureFunctions.fioreBrasse,
#        structureFunctions = cepgen.StructureFunctions.allm97,
    ),
    outKinematics = cepgen.Parameters(
        invmass = (5.0, 0.0),
#        pt = (2.5, 0.0),
        q2 = [(0.0, 10.0), (0.0, 10.0)],
        mx = (1.073248881, 3.0),
#        energy = (5.0,0.0),
#        eta = (-2.50, 2.50),
    )
)

# events generation parameters
generator = _gen.clone(
    numEvents = 100000,
    printEvery = 2500,
)

text = cepgen.Module('text', # histogramming/ASCII output capability
    histVariables={
        'm(4)': cepgen.Parameters(xrange=(0.0, 25.0), nbins=20, log=False),
        'pt(7):pt(8)': cepgen.Parameters(xrange=(0.0, 50.0), yrange=(0.0, 50.0), log=True)
    }
)
#lhef = cepgen.Module('lhef', filename='EIC.lhe')
hepmc = cepgen.Module('hepmc', filename='EIC_100K_QE.hepmc')
dump = cepgen.Module('dump', printEvery = generator.printEvery)
#rootTree.filename = 'my_output_file.root'
output = cepgen.Sequence(
#    rootTree,
    text,
#    lhef,
    hepmc,
    dump,
)
