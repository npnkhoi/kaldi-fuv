../../src/latbin/lattice-best-path ark:'gunzip -c exp/mono/decode/lat.1.gz |' 'ark,t:| utils/int2sym.pl -f 2- exp/mono/graph/words.txt > outputs/out_mono.txt'
../../src/latbin/lattice-best-path ark:'gunzip -c exp/tri1/decode/lat.1.gz |' 'ark,t:| utils/int2sym.pl -f 2- exp/tri1/graph/words.txt > outputs/out_tri1.txt'